"""Gráficos reutilizables para el curso (matplotlib)."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AZUL, NARANJA, GRIS = "#1f4e79", "#e07b39", "#9e9e9e"


def barras_con_exposicion(t: pd.DataFrame, metrica: str = "frecuencia", titulo: str = "",
                          ax=None, formato: str = "{:.1%}"):
    """Barras de exposición (eje derecho, gris) + línea de la métrica (eje izq.).

    Es el gráfico 'clásico' de un actuario: muestra a la vez cuánto pesa cada
    segmento y cómo se comporta.
    """
    ax = ax or plt.subplots(figsize=(8, 4))[1]
    x = np.arange(len(t))
    ax2 = ax.twinx()
    ax2.bar(x, t["exposicion"], color=GRIS, alpha=0.35, label="Exposición")
    ax2.set_ylabel("Exposición (años-póliza)")
    ax.plot(x, t[metrica], marker="o", color=AZUL, lw=2, label=metrica.capitalize())
    if {"ic_inf", "ic_sup"} <= set(t.columns):
        ax.fill_between(x, t["ic_inf"], t["ic_sup"], color=AZUL, alpha=0.15, label="IC 95%")
    ax.set_xticks(x, [str(i) for i in t.index], rotation=0)
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: formato.format(v)))
    ax.set_title(titulo or f"{metrica.capitalize()} por {t.index.name}")
    ax.legend(loc="upper left")
    return ax


def curva_lift(y_real, y_pred, exposicion, n_grupos: int = 10, ax=None, titulo="Curva de lift"):
    """Agrupa pólizas en deciles de IGUAL EXPOSICIÓN según la predicción y compara
    la tasa real vs la predicha en cada grupo."""
    d = pd.DataFrame({"real": np.asarray(y_real, float), "pred": np.asarray(y_pred, float),
                      "w": np.asarray(exposicion, float)}).sort_values("pred")
    d["grupo"] = np.minimum((d["w"].cumsum() / d["w"].sum() * n_grupos).astype(int), n_grupos - 1) + 1
    g = d.groupby("grupo").apply(
        lambda x: pd.Series({"real": np.average(x["real"], weights=x["w"]),
                             "pred": np.average(x["pred"], weights=x["w"])}), include_groups=False)
    ax = ax or plt.subplots(figsize=(7, 4))[1]
    ax.plot(g.index, g["real"], "o-", color=NARANJA, label="Observado")
    ax.plot(g.index, g["pred"], "s--", color=AZUL, label="Predicho")
    ax.set_xlabel("Grupo (de menor a mayor riesgo predicho)")
    ax.set_title(titulo)
    ax.legend()
    return g


def gini(y_real, y_pred, exposicion) -> float:
    """Índice de Gini (curva de Lorenz ordenada por la predicción).
    0 = el modelo no ordena nada; cuanto mayor, mejor ordena el riesgo."""
    d = pd.DataFrame({"y": np.asarray(y_real, float) * np.asarray(exposicion, float),
                      "p": np.asarray(y_pred, float), "w": np.asarray(exposicion, float)})
    d = d.sort_values("p", ascending=False)
    x = np.r_[0, d["w"].cumsum() / d["w"].sum()]
    y = np.r_[0, d["y"].cumsum() / d["y"].sum()]
    area = np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]) / 2)
    return 2 * area - 1


def curva_lorenz(y_real, y_pred, exposicion, ax=None, etiqueta="Modelo"):
    d = pd.DataFrame({"y": np.asarray(y_real, float) * np.asarray(exposicion, float),
                      "p": np.asarray(y_pred, float), "w": np.asarray(exposicion, float)})
    d = d.sort_values("p", ascending=False)
    x = np.r_[0, d["w"].cumsum() / d["w"].sum()]
    y = np.r_[0, d["y"].cumsum() / d["y"].sum()]
    ax = ax or plt.subplots(figsize=(5, 5))[1]
    ax.plot(x, y, label=f"{etiqueta} (Gini={gini(y_real, y_pred, exposicion):.3f})")
    ax.plot([0, 1], [0, 1], "k:", label="Azar")
    ax.set_xlabel("% exposición acumulada (de más a menos riesgo predicho)")
    ax.set_ylabel("% siniestros acumulados")
    ax.legend()
    return ax
