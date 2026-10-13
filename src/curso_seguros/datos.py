"""Rutas y carga de datos del curso.

Todas las funciones devuelven DataFrames de pandas. Si los ficheros locales no
existen (p. ej. abriste un notebook suelto sin descargar la carpeta del curso),
`cargar_fremtpl2` intenta descargarlos de OpenML como plan B.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def raiz_proyecto() -> Path:
    """Devuelve la carpeta raíz del curso (la que contiene `data/`)."""
    aqui = Path.cwd().resolve()
    for p in [aqui, *aqui.parents]:
        if (p / "data").is_dir() and (p / "src").is_dir():
            return p
    return Path(__file__).resolve().parents[2]


RAIZ = raiz_proyecto()
DATA = RAIZ / "data"
OUTPUT = RAIZ / "output"


def cargar_fremtpl2(origen: str = "local") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga freMTPL2freq y freMTPL2sev **tal cual** (sin limpiar).

    origen = "local"  -> data/raw/*.parquet (por defecto)
    origen = "openml" -> descarga desde OpenML (ids 41214 y 41215).
             Ojo: la versión de OpenML es ligeramente distinta (678.013 pólizas
             y 26.639 siniestros) a la de CASdatasets que usamos (677.991 / 26.444).
    """
    f_freq, f_sev = DATA / "raw" / "freMTPL2freq.parquet", DATA / "raw" / "freMTPL2sev.parquet"
    if origen == "local" and f_freq.exists():
        return pd.read_parquet(f_freq), pd.read_parquet(f_sev)
    from sklearn.datasets import fetch_openml

    print("Descargando de OpenML (puede tardar 1-2 minutos)...")
    freq = fetch_openml(data_id=41214, as_frame=True).frame
    sev = fetch_openml(data_id=41215, as_frame=True).frame
    return freq, sev


def cargar_cartera() -> pd.DataFrame:
    """Cartera interna 2025 (simulada sobre freMTPL2): una fila por póliza."""
    return pd.read_parquet(DATA / "cartera" / "cartera_2025.parquet")


def cargar_siniestros_referencia() -> pd.DataFrame:
    """Maestro LIMPIO de siniestros 2025 (sirve para comprobar tus resultados)."""
    return pd.read_parquet(DATA / "referencia" / "siniestros_2025_maestro.parquet")


def rutas_bordereaux() -> list[Path]:
    """Lista ordenada de los ficheros mensuales de siniestros."""
    return sorted((DATA / "entrada" / "bordereaux").glob("siniestros_2025-*.xlsx"))


def cargar_base_polizas(gastos_por_prima: bool = True) -> pd.DataFrame:
    """Una fila por póliza con exposición, prima devengada 2025, siniestros
    (número y coste), comisiones, gastos de estructura (reparto simple por prima)
    y margen técnico. Es la tabla que se construye paso a paso en la sesión 2."""
    cartera = cargar_cartera()
    sin = cargar_siniestros_referencia()
    df = cartera.copy()
    df["antig_vehiculo"] = df["antig_vehiculo"].clip(upper=25)
    df["edad_conductor"] = df["edad_conductor"].clip(upper=90)
    df["exposicion"] = (df["fecha_vencimiento"] - df["fecha_efecto"]).dt.days / 365
    df["prima_devengada"] = df["prima_anual"] * df["exposicion"]
    agg = sin.groupby("id_poliza").agg(n_siniestros=("id_siniestro", "count"), coste_siniestros=("importe", "sum"))
    df = df.merge(agg, left_on="id_poliza", right_index=True, how="left")
    df[["n_siniestros", "coste_siniestros"]] = df[["n_siniestros", "coste_siniestros"]].fillna(0)
    df["n_siniestros"] = df["n_siniestros"].astype(int)
    com = pd.read_excel(DATA / "entrada" / "parametros" / "parametros_2025.xlsx", sheet_name="Comisiones")
    df = df.merge(com[["canal", "tasa_comision"]], on="canal", how="left")
    df["comisiones"] = df["prima_devengada"] * df["tasa_comision"]
    if gastos_por_prima:
        total = pd.read_excel(DATA / "entrada" / "gastos_estructura_2025.xlsx")["importe"].sum()
        df["gastos_estructura"] = total * df["prima_devengada"] / df["prima_devengada"].sum()
    else:
        df["gastos_estructura"] = 0.0
    df["margen"] = df["prima_devengada"] - df["coste_siniestros"] - df["comisiones"] - df["gastos_estructura"]
    df["tramo_edad"] = pd.cut(df["edad_conductor"], bins=[17, 25, 35, 50, 65, 90],
                              labels=["18-25", "26-35", "36-50", "51-65", "66+"])
    return df
