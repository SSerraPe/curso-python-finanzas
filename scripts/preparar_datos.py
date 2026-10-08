"""
Prepara TODOS los datos del curso a partir de fuentes públicas.

Los alumnos NO necesitan ejecutar este script: los ficheros resultantes ya
están en la carpeta data/. Se incluye para que el proceso sea reproducible
y auditable (¡buena práctica!).

Fuentes
-------
* freMTPL2freq / freMTPL2sev  — cartera francesa de RC autos (≈678k pólizas),
  paquete R CASdatasets (Dutang & Charpentier), descargada de
  https://github.com/dutangc/CASdatasets (licencia GPL>=2; espejo CC0 en
  OpenML ids 41214 / 41215).
* Triángulos de reservas — paquete Python `chainladder` 0.10.1
  (muestras 'raa' y 'clrd2025' = CAS Loss Reserving Database, Schedule P
  NAIC, actualización dic-2025). Se exportan en otro entorno porque
  chainladder exige pandas>=2.3.3 (ver herramientas/exportar_triangulos.py).

Qué se genera
-------------
data/raw/freMTPL2freq.parquet          datos originales (tal cual, con sus rarezas)
data/raw/freMTPL2sev.parquet
data/cartera/cartera_2025.parquet      cartera "interna" SIMULADA a partir de freMTPL2:
                                       canal, fechas de efecto 2025 y prima anual
                                       de una "tarifa actual" simplificada
data/entrada/bordereaux/*.xlsx         12 ficheros mensuales de siniestros declarados,
                                       con problemas de calidad INTRODUCIDOS a propósito
data/entrada/parametros/parametros_2025.xlsx     comisiones por canal y claves de reparto
data/entrada/gastos_estructura_2025.xlsx         gastos reales por mes/centro de coste/partida
data/entrada/presupuesto_2025.xlsx               presupuesto mensual por canal (formato ancho)
data/referencia/siniestros_2025_maestro.parquet  versión limpia (solución)
data/referencia/problemas_introducidos.csv       qué se ha "ensuciado" y dónde

Uso:  python scripts/preparar_datos.py  [--descargar]
"""
from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "data"
SEMILLA = 2025
URL_CAS = "https://raw.githubusercontent.com/dutangc/CASdatasets/master/data/{}.rda"

CANALES = ["Agentes", "Corredores", "Directo", "Bancaseguros"]
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


# ---------------------------------------------------------------------------
# 1. Datos originales
# ---------------------------------------------------------------------------
def descargar_rda(destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ["freMTPL2freq", "freMTPL2sev"]:
        f = destino / f"{nombre}.rda"
        if not f.exists():
            print(f"Descargando {nombre} ...")
            urllib.request.urlretrieve(URL_CAS.format(nombre), f)


def rda_a_parquet(origen: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    import rdata  # pip install rdata  (lector puro Python de ficheros .rda)

    freq = rdata.read_rda(origen / "freMTPL2freq.rda")["freMTPL2freq"]
    sev = rdata.read_rda(origen / "freMTPL2sev.rda")["freMTPL2sev"]
    for df in (freq, sev):
        df.reset_index(drop=True, inplace=True)
        # IDpol viene como texto (¡con valores tipo '1e+05'!). Lo dejamos así
        # en raw/ a propósito: es uno de los ejercicios de limpieza.
        df["IDpol"] = df["IDpol"].astype(str)
    for c in ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]:
        freq[c] = freq[c].astype("int64")
    for c in ["VehBrand", "VehGas", "Area", "Region"]:
        freq[c] = freq[c].astype(str)
    (DATA / "raw").mkdir(parents=True, exist_ok=True)
    freq.to_parquet(DATA / "raw" / "freMTPL2freq.parquet", index=False)
    sev.to_parquet(DATA / "raw" / "freMTPL2sev.parquet", index=False)
    print(f"raw: freq {freq.shape}, sev {sev.shape}")
    return freq, sev


# ---------------------------------------------------------------------------
# 2. Cartera interna simulada
# ---------------------------------------------------------------------------
def tramo_bm(bm: pd.Series) -> pd.Series:
    return pd.cut(bm, [0, 50, 70, 100, 1000], labels=["50", "51-70", "71-100", ">100"]).astype(str)


def construir_cartera(freq: pd.DataFrame, sev: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    f = freq.copy()
    f["IDpol"] = f["IDpol"].astype(float).astype("int64")
    s = sev.copy()
    s["IDpol"] = s["IDpol"].astype(float).astype("int64")

    # --- "Tarifa actual": GLM sencillo con solo 2 factores (a propósito: deja
    #     margen de mejora para el GLM de la sesión 5) ----------------------
    f["tramo_bm"] = tramo_bm(f["BonusMalus"])
    f["expo"] = f["Exposure"].clip(upper=1.0)
    f["n"] = f["ClaimNb"].clip(upper=4)
    glm = smf.glm("n ~ C(tramo_bm, Treatment('50')) + C(Area, Treatment('C'))", data=f,
                  family=sm.families.Poisson(), offset=np.log(f["expo"])).fit()
    frec_anual = glm.predict(f, offset=np.zeros(len(f)))
    coste_medio = s["ClaimAmount"].mean()
    ratio_objetivo = 0.70
    prima = frec_anual * coste_medio / ratio_objetivo

    # Canal comercial (sintético). Los jóvenes contratan más en Directo.
    p = np.tile([0.45, 0.27, 0.18, 0.10], (len(f), 1))
    joven = f["DrivAge"].to_numpy() < 30
    p[joven] = [0.30, 0.20, 0.42, 0.08]
    u = rng.random(len(f))[:, None]
    canal_idx = (u > p.cumsum(axis=1)).sum(axis=1)
    canal = np.array(CANALES)[canal_idx]
    ajuste_canal = pd.Series(canal).map({"Agentes": 1.00, "Corredores": 0.97,
                                         "Directo": 0.92, "Bancaseguros": 1.03}).to_numpy()
    ruido = rng.normal(1.0, 0.03, len(f))
    prima = np.maximum(np.round(prima * ajuste_canal * ruido, 2), 120.0)

    # Fechas de cobertura dentro de 2025
    dias_expo = np.maximum(np.round(f["expo"].to_numpy() * 365), 1).astype(int)
    inicio_max = 365 - dias_expo
    desplaz = np.floor(rng.random(len(f)) * (inicio_max + 1)).astype(int)
    efecto = pd.Timestamp("2025-01-01") + pd.to_timedelta(desplaz, unit="D")
    vencimiento = efecto + pd.to_timedelta(dias_expo, unit="D")

    cartera = pd.DataFrame({
        "id_poliza": f["IDpol"],
        "canal": canal,
        "fecha_efecto": efecto,
        "fecha_vencimiento": vencimiento,
        "prima_anual": prima,
        "zona": f["Area"],
        "region": f["Region"],
        "potencia": f["VehPower"],
        "antig_vehiculo": f["VehAge"],
        "edad_conductor": f["DrivAge"],
        "bonus_malus": f["BonusMalus"],
        "marca": f["VehBrand"],
        "combustible": f["VehGas"],
        "densidad": f["Density"],
    })
    cartera["prima_anual"] = cartera["prima_anual"].astype(float)

    # --- Siniestros con fechas ------------------------------------------------
    s = s.merge(cartera[["id_poliza", "canal", "region", "fecha_efecto", "fecha_vencimiento"]],
                left_on="IDpol", right_on="id_poliza", how="left")
    dur = (s["fecha_vencimiento"] - s["fecha_efecto"]).dt.days.to_numpy()
    ocurr = s["fecha_efecto"] + pd.to_timedelta(np.floor(rng.random(len(s)) * dur), unit="D")
    # Retraso de declaración: mayoría rápida, cola larga (=> IBNR a cierre)
    lag = np.where(rng.random(len(s)) < 0.97,
                   rng.exponential(12, len(s)),
                   rng.uniform(60, 400, len(s))).round().astype(int)
    declar = ocurr + pd.to_timedelta(lag, unit="D")
    estado = np.where(rng.random(len(s)) < 0.65, "Cerrado", "Abierto")
    sin = pd.DataFrame({
        "id_siniestro": [f"S25-{i:06d}" for i in range(1, len(s) + 1)],
        "id_poliza": s["id_poliza"].to_numpy(),
        "fecha_ocurrencia": ocurr.to_numpy(),
        "fecha_declaracion": declar.to_numpy(),
        "canal": s["canal"].to_numpy(),
        "region": s["region"].to_numpy(),
        "importe": s["ClaimAmount"].round(2).to_numpy(),
        "estado": estado,
    }).sort_values("fecha_declaracion", kind="stable").reset_index(drop=True)
    sin["id_siniestro"] = [f"S25-{i:06d}" for i in range(1, len(sin) + 1)]
    return cartera, sin


# ---------------------------------------------------------------------------
# 3. Bordereaux mensuales "sucios"
# ---------------------------------------------------------------------------
def fmt_es(x: float) -> str:
    """1234.5 -> '1.234,50'"""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def escribir_bordereaux(sin: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    destino = DATA / "entrada" / "bordereaux"
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("*.xlsx"):
        viejo.unlink()
    problemas = []
    decl = sin[sin["fecha_declaracion"] < "2026-01-01"].copy()
    for mes in range(1, 13):
        m = decl[decl["fecha_declaracion"].dt.month == mes].copy()
        resumen = {"n_siniestros": len(m), "importe_total": round(m["importe"].sum(), 2)}
        det = m.copy()

        # (a) pólizas mal tecleadas: anteponer un 9 al número
        idx_typo = rng.choice(det.index, 3, replace=False)
        det.loc[idx_typo, "id_poliza"] = ("9" + det.loc[idx_typo, "id_poliza"].astype(str)).astype("int64")
        problemas += [("poliza_inexistente", mes, i) for i in det.loc[idx_typo, "id_siniestro"]]
        # (b) canal escrito de formas distintas
        idx_canal = rng.choice(det.index, max(1, len(det) // 25), replace=False)
        det.loc[idx_canal, "canal"] = [rng.choice([c.upper(), c.lower() + " ", " " + c])
                                       for c in det.loc[idx_canal, "canal"]]
        # (c) duplicados en meses pares
        if mes % 2 == 0:
            dup = det.sample(n=max(2, len(det) // 200), random_state=mes)
            det = pd.concat([det, dup]).sort_values("fecha_declaracion", kind="stable")
            problemas += [("duplicado", mes, i) for i in dup["id_siniestro"]]
        # (d) septiembre: falta una línea respecto al resumen
        if mes == 9:
            quitado = det.sample(1, random_state=9)
            det = det.drop(quitado.index)
            problemas += [("falta_en_detalle", mes, quitado["id_siniestro"].iloc[0])]
        # (e) importes negativos (recobros) en marzo y octubre
        if mes in (3, 10):
            rec = det.sample(2, random_state=mes).copy()
            rec["importe"] = -(rec["importe"] * 0.5).round(2)
            rec["id_siniestro"] = rec["id_siniestro"] + "-R"
            rec["estado"] = "Recobro"
            det = pd.concat([det, rec])
            resumen["n_siniestros"] += 2
            resumen["importe_total"] = round(resumen["importe_total"] + rec["importe"].sum(), 2)
            problemas += [("recobro_negativo", mes, i) for i in rec["id_siniestro"]]

        if mes <= 6:   # sistema antiguo
            salida = pd.DataFrame({
                "Nº Siniestro": det["id_siniestro"],
                "Nº Póliza": det["id_poliza"],
                "Fecha ocurrencia": det["fecha_ocurrencia"].dt.date,
                "Fecha declaración": det["fecha_declaracion"].dt.date,
                "Canal": det["canal"],
                "Región": det["region"],
                "Importe (€)": det["importe"],
                "Estado": det["estado"],
            })
        else:          # julio: migración de sistema -> otros nombres y formatos
            salida = pd.DataFrame({
                "N_SINIESTRO": det["id_siniestro"],
                "N_POLIZA": det["id_poliza"].astype(str),
                "F_OCURRENCIA": det["fecha_ocurrencia"].dt.strftime("%d/%m/%Y"),
                "F_DECLARACION": det["fecha_declaracion"].dt.strftime("%d/%m/%Y"),
                "CANAL": det["canal"],
                "REGION": det["region"],
                "IMPORTE_EUR": [fmt_es(x) for x in det["importe"]],
                "ESTADO": det["estado"].str.upper(),
            })
            problemas.append(("cambio_formato_sistema", mes, "todas"))

        f = destino / f"siniestros_2025-{mes:02d}.xlsx"
        with pd.ExcelWriter(f, engine="openpyxl") as xw:
            titulo = pd.DataFrame([[f"Bordereau de siniestros declarados - {MESES_ES[mes-1]} 2025"],
                                   ["Fuente: Sistema de Siniestros (extracción automática)"],
                                   [""]])
            titulo.to_excel(xw, sheet_name="Detalle", header=False, index=False)
            salida.to_excel(xw, sheet_name="Detalle", startrow=3, index=False)
            fila_total = 3 + 1 + len(salida) + 1
            suma = round(det["importe"].sum(), 2)
            total = pd.DataFrame([["TOTAL", None, None, None, None, None,
                                   suma if mes <= 6 else fmt_es(suma), None]])
            total.to_excel(xw, sheet_name="Detalle", startrow=fila_total, header=False, index=False)
            pd.DataFrame([{"Concepto": "Número de siniestros", "Valor": resumen["n_siniestros"]},
                          {"Concepto": "Importe total declarado (€)", "Valor": resumen["importe_total"]}]
                         ).to_excel(xw, sheet_name="Resumen", index=False)
        print(f"  {f.name}: {len(salida)} filas")
    return pd.DataFrame(problemas, columns=["problema", "mes", "id_siniestro"])


# ---------------------------------------------------------------------------
# 4. Datos FP&A: comisiones, gastos de estructura y presupuesto
# ---------------------------------------------------------------------------
COMISIONES = pd.DataFrame({
    "canal": CANALES,
    "tasa_comision": [0.15, 0.18, 0.02, 0.20],
    "descripcion": ["Red de agentes exclusivos", "Corredurías", "Web y teléfono (sin intermediario)",
                    "Acuerdo de distribución bancaria"],
})

CENTROS = {
    # centro de coste: (gasto anual €, clave de reparto)
    "Tramitación de siniestros": (3_600_000, "n_siniestros"),
    "Tecnología": (2_400_000, "n_polizas"),
    "Marketing digital": (1_500_000, "solo_directo"),
    "Administración y finanzas": (1_300_000, "prima_devengada"),
    "Dirección comercial": (1_100_000, "prima_devengada"),
}
PARTIDAS = {"Personal": 0.55, "Servicios externos": 0.25, "Alquileres y suministros": 0.12,
            "Amortizaciones": 0.08}


def prima_devengada_mensual(cartera: pd.DataFrame) -> pd.DataFrame:
    """Prima devengada por mes y canal: prima anual × días cubiertos en el mes / 365."""
    filas = []
    for mes in range(1, 13):
        ini = pd.Timestamp(2025, mes, 1)
        fin = ini + pd.offsets.MonthBegin(1)
        dias = (cartera["fecha_vencimiento"].clip(upper=fin) - cartera["fecha_efecto"].clip(lower=ini)
                ).dt.days.clip(lower=0)
        t = (cartera["prima_anual"] * dias / 365).groupby(cartera["canal"]).sum()
        filas += [{"mes": mes, "canal": c, "prima_devengada": v} for c, v in t.items()]
    return pd.DataFrame(filas)


def escribir_datos_fpa(cartera: pd.DataFrame, sin: pd.DataFrame, rng: np.random.Generator) -> None:
    ent = DATA / "entrada"
    (ent / "parametros").mkdir(parents=True, exist_ok=True)

    # 4.1 Parámetros: comisiones y claves de reparto
    claves = pd.DataFrame([{"centro_coste": k, "gasto_anual_presupuestado": v[0], "clave_reparto": v[1]}
                           for k, v in CENTROS.items()])
    with pd.ExcelWriter(ent / "parametros" / "parametros_2025.xlsx", engine="openpyxl") as xw:
        COMISIONES.to_excel(xw, sheet_name="Comisiones", index=False)
        claves.to_excel(xw, sheet_name="Claves_reparto", index=False)

    # 4.2 Gastos de estructura reales (contabilidad analítica), formato largo
    filas = []
    estacional = 1 + 0.08 * np.sin(np.arange(12) / 12 * 2 * np.pi)   # algo de estacionalidad
    for centro, (anual, _) in CENTROS.items():
        desvio = rng.normal(1.04, 0.03)    # en general se gasta algo más de lo presupuestado
        for mes in range(1, 13):
            for partida, peso in PARTIDAS.items():
                imp = anual / 12 * peso * estacional[mes - 1] * desvio * rng.normal(1, 0.05)
                if centro == "Marketing digital" and mes in (3, 9):   # campañas
                    imp *= 1.8
                filas.append({"mes": f"2025-{mes:02d}", "centro_coste": centro, "partida": partida,
                              "importe": round(imp, 2)})
    gastos = pd.DataFrame(filas)
    gastos.to_excel(ent / "gastos_estructura_2025.xlsx", sheet_name="Gastos", index=False)

    # 4.3 Presupuesto 2025 (formato ANCHO: conceptos en filas, meses en columnas, como en Excel)
    pdm = prima_devengada_mensual(cartera)
    pdm["prima_ppto"] = pdm["prima_devengada"] * rng.normal(1.02, 0.02, len(pdm))   # algo optimista
    lr_ppto = {"Agentes": 0.68, "Corredores": 0.66, "Directo": 0.70, "Bancaseguros": 0.60}
    tasa = COMISIONES.set_index("canal")["tasa_comision"]
    pdm["siniestros_ppto"] = pdm["prima_ppto"] * pdm["canal"].map(lr_ppto)
    pdm["comisiones_ppto"] = pdm["prima_ppto"] * pdm["canal"].map(tasa)
    # gastos de estructura presupuestados repartidos por peso de prima (simplificación del ppto)
    peso = pdm.groupby("canal")["prima_ppto"].sum() / pdm["prima_ppto"].sum()
    total_gastos = sum(v[0] for v in CENTROS.values())
    pdm["gastos_ppto"] = pdm["canal"].map(peso) * total_gastos / 12
    conceptos = {"prima_ppto": "Primas devengadas", "siniestros_ppto": "Coste de siniestros",
                 "comisiones_ppto": "Comisiones", "gastos_ppto": "Gastos de estructura"}
    largo = pdm.melt(id_vars=["mes", "canal"], value_vars=list(conceptos), var_name="concepto",
                     value_name="importe")
    largo["concepto"] = largo["concepto"].map(conceptos)
    ancho = largo.pivot_table(index=["canal", "concepto"], columns="mes", values="importe", aggfunc="sum")
    ancho.columns = [MESES_ES[m - 1][:3].capitalize() for m in ancho.columns]
    ancho = ancho.round(0).reset_index()
    orden = {v: i for i, v in enumerate(conceptos.values())}
    ancho = ancho.sort_values(["canal", "concepto"], key=lambda s: s.map(orden) if s.name == "concepto" else s)
    ancho["Total"] = ancho.iloc[:, 2:].sum(axis=1)
    with pd.ExcelWriter(ent / "presupuesto_2025.xlsx", engine="openpyxl") as xw:
        pd.DataFrame([["PRESUPUESTO 2025 - Ramo Autos RC - Importes en euros"]]).to_excel(
            xw, sheet_name="Presupuesto", header=False, index=False)
        ancho.to_excel(xw, sheet_name="Presupuesto", startrow=2, index=False)
    print(f"FP&A: parametros, gastos ({len(gastos)} filas), presupuesto ({ancho.shape})")


def main(descargar: bool) -> None:
    rng = np.random.default_rng(SEMILLA)
    fuente = RAIZ / "data" / "_fuente_rda"
    if descargar or not (DATA / "raw" / "freMTPL2freq.parquet").exists():
        descargar_rda(fuente)
        freq, sev = rda_a_parquet(fuente)
    else:
        freq = pd.read_parquet(DATA / "raw" / "freMTPL2freq.parquet")
        sev = pd.read_parquet(DATA / "raw" / "freMTPL2sev.parquet")

    cartera, sin = construir_cartera(freq, sev, rng)
    (DATA / "cartera").mkdir(parents=True, exist_ok=True)
    (DATA / "referencia").mkdir(parents=True, exist_ok=True)
    cartera.to_parquet(DATA / "cartera" / "cartera_2025.parquet", index=False)
    sin.to_parquet(DATA / "referencia" / "siniestros_2025_maestro.parquet", index=False)
    print(f"cartera {cartera.shape}, siniestros {sin.shape}")
    print(f"  declarados en 2026 (IBNR a 31/12/2025): {(sin['fecha_declaracion'] >= '2026-01-01').sum()}")

    problemas = escribir_bordereaux(sin, rng)
    problemas.to_csv(DATA / "referencia" / "problemas_introducidos.csv", index=False)
    print("Problemas introducidos:\n", problemas.groupby("problema").size())
    escribir_datos_fpa(cartera, sin, rng)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--descargar", action="store_true", help="Volver a descargar las fuentes .rda")
    main(ap.parse_args().descargar)
