"""KPIs actuariales.

REGLA DE ORO: los ratios de un grupo se calculan como COCIENTE DE SUMAS,
nunca como media de ratios individuales.

    frecuencia  = Σ siniestros / Σ exposición           (por año-póliza)
    severidad   = Σ coste       / Σ siniestros          (coste medio)
    prima pura  = Σ coste       / Σ exposición  = frecuencia × severidad
    siniestralidad (loss ratio) = Σ coste / Σ prima devengada
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def tabla_kpis(df: pd.DataFrame, por: str | list[str] | None = None, *,
               exposicion: str = "exposicion", n: str = "n_siniestros",
               coste: str = "coste", prima: str | None = None) -> pd.DataFrame:
    """Tabla de KPIs por segmento (o total si `por` es None).

    >>> tabla_kpis(df, por="zona", prima="prima_devengada")
    """
    cols = {"exposicion": (exposicion, "sum"), "n_siniestros": (n, "sum"), "coste": (coste, "sum")}
    if prima:
        cols["prima"] = (prima, "sum")
    if por is None:
        t = df.assign(_total="Total").groupby("_total").agg(**cols)
        t.index.name = None
    else:
        t = df.groupby(por, observed=True).agg(**cols)
    t["frecuencia"] = t["n_siniestros"] / t["exposicion"]
    t["severidad"] = t["coste"] / t["n_siniestros"].replace(0, np.nan)
    t["prima_pura"] = t["coste"] / t["exposicion"]
    if prima:
        t["siniestralidad"] = t["coste"] / t["prima"]
    t["peso_exposicion"] = t["exposicion"] / t["exposicion"].sum()
    return t


def ic_frecuencia(n: float, exposicion: float, nivel: float = 0.95) -> tuple[float, float]:
    """IC exacto (Garwood) para una frecuencia de Poisson n / exposición."""
    from scipy.stats import chi2

    a = 1 - nivel
    lo = chi2.ppf(a / 2, 2 * n) / 2 if n > 0 else 0.0
    hi = chi2.ppf(1 - a / 2, 2 * (n + 1)) / 2
    return lo / exposicion, hi / exposicion
