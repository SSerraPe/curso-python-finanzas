"""Lógica del cierre mensual (versión 'de producción' de lo que se construye
paso a paso en el notebook 03).

Flujo:
    bordereaux (12 Excel)  ──normalizar──▶  siniestros limpios ──┐
    cartera ──devengo──▶ primas devengadas por canal/mes ────────┼──▶ cuenta de resultados
    parámetros (comisiones, claves) + gastos de estructura ──────┘          │
    presupuesto (formato ancho) ──melt──────────────────────────────▶ real vs presupuesto
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from . import controles as ctl
from .datos import DATA

log = logging.getLogger("cierre")

MAPA_COLUMNAS = {
    # sistema antiguo (ene-jun)          # sistema nuevo (jul-dic)
    "Nº Siniestro": "id_siniestro",      "N_SINIESTRO": "id_siniestro",
    "Nº Póliza": "id_poliza",            "N_POLIZA": "id_poliza",
    "Fecha ocurrencia": "fecha_ocurrencia", "F_OCURRENCIA": "fecha_ocurrencia",
    "Fecha declaración": "fecha_declaracion", "F_DECLARACION": "fecha_declaracion",
    "Canal": "canal",                    "CANAL": "canal",
    "Región": "region",                  "REGION": "region",
    "Importe (€)": "importe",            "IMPORTE_EUR": "importe",
    "Estado": "estado",                  "ESTADO": "estado",
}
CANALES = ["Agentes", "Corredores", "Directo", "Bancaseguros"]
CONCEPTOS = ["Primas devengadas", "Coste de siniestros", "Comisiones", "Gastos de estructura"]
MESES_CORTOS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


# --------------------------------------------------------------------------- utilidades
def a_numero(serie: pd.Series) -> pd.Series:
    """Convierte importes con formato español ('1.234,56') a número. Si ya son
    números, los deja igual."""
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)
    texto = serie.astype(str).str.strip().str.replace("€", "", regex=False)
    texto = texto.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(texto, errors="coerce")


def a_fecha(serie: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(serie):
        return serie
    return pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")


def mes_de_fichero(ruta: Path) -> int:
    return int(re.search(r"(\d{4})-(\d{2})", Path(ruta).stem).group(2))


# --------------------------------------------------------------------------- siniestros
def normalizar_bordereau(ruta: Path) -> tuple[pd.DataFrame, dict]:
    """Lee un bordereau mensual (cualquiera de los dos formatos) y lo deja en un
    formato estándar. Devuelve (detalle, resumen_declarado)."""
    df = pd.read_excel(ruta, sheet_name="Detalle", header=3)
    df = df.rename(columns=MAPA_COLUMNAS)
    df = df[df["id_siniestro"].notna() & (df["id_siniestro"].astype(str) != "TOTAL")].copy()
    df["id_poliza"] = pd.to_numeric(df["id_poliza"], errors="coerce").astype("Int64")
    df["importe"] = a_numero(df["importe"])
    df["fecha_ocurrencia"] = a_fecha(df["fecha_ocurrencia"])
    df["fecha_declaracion"] = a_fecha(df["fecha_declaracion"])
    df["canal"] = df["canal"].astype(str).str.strip().str.title()
    df["estado"] = df["estado"].astype(str).str.strip().str.title()
    df["mes"] = mes_de_fichero(ruta)
    res = pd.read_excel(ruta, sheet_name="Resumen").set_index("Concepto")["Valor"]
    resumen = {"n_siniestros": int(res.iloc[0]), "importe_total": float(res.iloc[1])}
    return df.reset_index(drop=True), resumen


def cargar_siniestros(hasta_mes: int, rutas: list[Path], cartera: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga, valida y consolida los bordereaux hasta `hasta_mes` (incluido).
    Devuelve (siniestros_limpios, tabla_de_controles)."""
    partes, filas_ctl = [], []
    for ruta in rutas:
        mes = mes_de_fichero(ruta)
        if mes > hasta_mes:
            continue
        df, resumen = normalizar_bordereau(ruta)
        etiqueta = f"{mes:02d}"
        filas_ctl.append({**ctl.control_sin_duplicados(df, "id_siniestro"), "mes": etiqueta})
        df = df.drop_duplicates(subset="id_siniestro")
        filas_ctl.append({**ctl.control_sin_nulos(df, ["id_siniestro", "id_poliza", "importe", "canal"]),
                          "mes": etiqueta})
        filas_ctl.append({**ctl.control_integridad(df, "id_poliza", cartera["id_poliza"], "cartera"),
                          "mes": etiqueta})
        filas_ctl.append({**ctl.control_rango(df, "importe", minimo=0, aviso=True), "mes": etiqueta})
        filas_ctl.append({**ctl.control_cuadre("Cuadre nº siniestros vs Resumen", len(df),
                                               resumen["n_siniestros"], 0), "mes": etiqueta})
        filas_ctl.append({**ctl.control_cuadre("Cuadre importe vs Resumen", df["importe"].sum(),
                                               resumen["importe_total"]), "mes": etiqueta})
        canales_raros = sorted(set(df["canal"]) - set(CANALES))
        filas_ctl.append({**ctl.resultado("Canales válidos", not canales_raros, ", ".join(canales_raros)
                                          or "todos válidos"), "mes": etiqueta})
        partes.append(df)
        log.info("Bordereau %s: %d siniestros, %.2f €", etiqueta, len(df), df["importe"].sum())
    sin = pd.concat(partes, ignore_index=True)
    controles = pd.DataFrame(filas_ctl)[["mes", "control", "resultado", "detalle"]]
    return sin, controles


# --------------------------------------------------------------------------- primas
def devengo_mensual(cartera: pd.DataFrame, anio: int = 2025) -> pd.DataFrame:
    """Prima devengada y pólizas en vigor por canal y mes.
    prima devengada del mes = prima anual × días cubiertos en el mes / 365."""
    filas = []
    for mes in range(1, 13):
        ini = pd.Timestamp(anio, mes, 1)
        fin = ini + pd.offsets.MonthBegin(1)
        dias = (cartera["fecha_vencimiento"].clip(upper=fin) - cartera["fecha_efecto"].clip(lower=ini)
                ).dt.days.clip(lower=0)
        g = pd.DataFrame({"canal": cartera["canal"], "prima": cartera["prima_anual"] * dias / 365,
                          "vigor": (dias > 0).astype(int)}).groupby("canal")[["prima", "vigor"]].sum()
        for canal, fila in g.iterrows():
            filas.append({"mes": mes, "canal": canal, "prima_devengada": fila["prima"],
                          "polizas_en_vigor": int(fila["vigor"])})
    return pd.DataFrame(filas)


# --------------------------------------------------------------------------- gastos
def reparto_gastos(gastos: pd.DataFrame, claves: pd.DataFrame, drivers: pd.DataFrame) -> pd.DataFrame:
    """Reparte los gastos de estructura de cada centro de coste entre canales
    según su clave de reparto. `drivers` tiene por mes y canal: n_siniestros,
    n_polizas, prima_devengada."""
    g = gastos.copy()
    g["mes"] = g["mes"].str[-2:].astype(int)
    g = g.groupby(["mes", "centro_coste"], as_index=False)["importe"].sum()
    g = g.merge(claves[["centro_coste", "clave_reparto"]], on="centro_coste", how="left")
    d = drivers.copy()
    d["solo_directo"] = (d["canal"] == "Directo").astype(float)
    largo = d.melt(id_vars=["mes", "canal"], value_vars=["n_siniestros", "n_polizas", "prima_devengada",
                                                           "solo_directo"],
                   var_name="clave_reparto", value_name="driver")
    largo["peso"] = largo["driver"] / largo.groupby(["mes", "clave_reparto"])["driver"].transform("sum")
    rep = g.merge(largo[["mes", "canal", "clave_reparto", "peso"]], on=["mes", "clave_reparto"], how="left")
    rep["gasto_asignado"] = rep["importe"] * rep["peso"]
    return rep


# --------------------------------------------------------------------------- presupuesto
def presupuesto_largo(ruta: Path) -> pd.DataFrame:
    """Pasa el presupuesto de formato ancho (meses en columnas) a largo."""
    ancho = pd.read_excel(ruta, header=2)
    largo = ancho.drop(columns="Total").melt(id_vars=["canal", "concepto"], var_name="mes_txt",
                                              value_name="importe")
    largo["mes"] = largo["mes_txt"].map({m: i + 1 for i, m in enumerate(MESES_CORTOS)})
    return largo.drop(columns="mes_txt")


# --------------------------------------------------------------------------- cuenta de resultados
def cuenta_resultados_mensual(sin: pd.DataFrame, devengo: pd.DataFrame, comisiones: pd.DataFrame,
                              gastos_rep: pd.DataFrame) -> pd.DataFrame:
    """Cuenta técnica REAL en formato largo: mes × canal × concepto."""
    coste = sin.groupby(["mes", "canal"], as_index=False).agg(coste=("importe", "sum"),
                                                              n_siniestros=("id_siniestro", "size"))
    base = devengo.merge(coste, on=["mes", "canal"], how="left").fillna({"coste": 0, "n_siniestros": 0})
    base = base.merge(comisiones[["canal", "tasa_comision"]], on="canal", how="left")
    base["comisiones"] = base["prima_devengada"] * base["tasa_comision"]
    gas = gastos_rep.groupby(["mes", "canal"], as_index=False)["gasto_asignado"].sum()
    base = base.merge(gas, on=["mes", "canal"], how="left").fillna({"gasto_asignado": 0})
    base = base[base["mes"] <= sin["mes"].max()]
    largo = base.rename(columns={"prima_devengada": "Primas devengadas", "coste": "Coste de siniestros",
                                 "comisiones": "Comisiones", "gasto_asignado": "Gastos de estructura"}
                        ).melt(id_vars=["mes", "canal"], value_vars=CONCEPTOS, var_name="concepto",
                               value_name="importe")
    return largo


def tabla_resultados(largo: pd.DataFrame, meses: list[int]) -> pd.DataFrame:
    """Pivot canal × concepto para los meses indicados + margen y ratios."""
    t = (largo[largo["mes"].isin(meses)].pivot_table(index="canal", columns="concepto", values="importe",
                                                       aggfunc="sum")[CONCEPTOS])
    t.loc["Total"] = t.sum()
    t["Margen técnico"] = t["Primas devengadas"] - t[CONCEPTOS[1:]].sum(axis=1)
    p = t["Primas devengadas"]
    t["Siniestralidad %"] = t["Coste de siniestros"] / p
    t["Ratio gastos+comisiones %"] = (t["Comisiones"] + t["Gastos de estructura"]) / p
    t["Ratio combinado %"] = t["Siniestralidad %"] + t["Ratio gastos+comisiones %"]
    return t


def real_vs_presupuesto(real: pd.DataFrame, ppto: pd.DataFrame, meses: list[int]) -> pd.DataFrame:
    r = real[real["mes"].isin(meses)].groupby(["canal", "concepto"])["importe"].sum().rename("Real")
    p = ppto[ppto["mes"].isin(meses)].groupby(["canal", "concepto"])["importe"].sum().rename("Presupuesto")
    t = pd.concat([r, p], axis=1).reset_index()
    tot = t.groupby("concepto", as_index=False)[["Real", "Presupuesto"]].sum().assign(canal="Total")
    t = pd.concat([t, tot], ignore_index=True)
    # margen como un concepto más
    signo = t["concepto"].map(lambda c: 1 if c == "Primas devengadas" else -1)
    m = (t.assign(Real=t["Real"] * signo, Presupuesto=t["Presupuesto"] * signo)
         .groupby("canal", as_index=False)[["Real", "Presupuesto"]].sum().assign(concepto="Margen técnico"))
    t = pd.concat([t, m], ignore_index=True)
    t["Desviación"] = t["Real"] - t["Presupuesto"]
    t["Desviación %"] = t["Desviación"] / t["Presupuesto"].abs()
    # Desviación favorable: más ingresos/margen o menos costes
    favorable = np.where(t["concepto"].isin(["Primas devengadas", "Margen técnico"]),
                         t["Desviación"] >= 0, t["Desviación"] <= 0)
    t["Valoración"] = np.where(favorable, "Favorable", "Desfavorable")
    orden_c = {c: i for i, c in enumerate(CONCEPTOS + ["Margen técnico"])}
    orden_k = {c: i for i, c in enumerate(CANALES + ["Total"])}
    return t.sort_values(["canal", "concepto"], key=lambda s: s.map(orden_k if s.name == "canal" else orden_c)
                         ).reset_index(drop=True)


def ejecutar_cierre(mes: int, data: Path = DATA) -> dict:
    """Ejecuta todo el cierre para el mes indicado y devuelve los resultados."""
    from .datos import cargar_cartera, rutas_bordereaux

    cartera = cargar_cartera()
    sin, controles = cargar_siniestros(mes, rutas_bordereaux(), cartera)
    dev = devengo_mensual(cartera)
    par = pd.read_excel(data / "entrada" / "parametros" / "parametros_2025.xlsx", sheet_name=None)
    gastos = pd.read_excel(data / "entrada" / "gastos_estructura_2025.xlsx")
    drivers = dev.rename(columns={"polizas_en_vigor": "n_polizas"}).merge(
        sin.groupby(["mes", "canal"], as_index=False).agg(n_siniestros=("id_siniestro", "size")),
        on=["mes", "canal"], how="left").fillna({"n_siniestros": 0})
    rep = reparto_gastos(gastos, par["Claves_reparto"], drivers)
    real = cuenta_resultados_mensual(sin, dev, par["Comisiones"], rep)
    ppto = presupuesto_largo(data / "entrada" / "presupuesto_2025.xlsx")
    ytd = list(range(1, mes + 1))
    return {
        "mes": mes,
        "siniestros": sin,
        "controles": controles,
        "resultado_mes": tabla_resultados(real, [mes]),
        "resultado_ytd": tabla_resultados(real, ytd),
        "rvp_mes": real_vs_presupuesto(real, ppto, [mes]),
        "rvp_ytd": real_vs_presupuesto(real, ppto, ytd),
        "real_largo": real,
        "ppto_largo": ppto,
    }
