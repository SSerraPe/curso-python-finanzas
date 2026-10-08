"""Rutinas de validación y control (el 'checklist' de cierre, en código).

Cada control devuelve un dict con: control, resultado (OK/KO/AVISO), detalle.
`ejecutar_controles` los junta en un DataFrame listo para volcar a Excel.
"""
from __future__ import annotations

import math
from typing import Callable

import pandas as pd


def resultado(nombre: str, ok: bool, detalle: str = "", aviso: bool = False) -> dict:
    return {"control": nombre, "resultado": "OK" if ok else ("AVISO" if aviso else "KO"),
            "detalle": detalle}


def control_sin_duplicados(df: pd.DataFrame, clave: str) -> dict:
    n = int(df.duplicated(subset=clave).sum())
    return resultado(f"Sin duplicados en '{clave}'", n == 0, f"{n} filas duplicadas")


def control_sin_nulos(df: pd.DataFrame, columnas: list[str]) -> dict:
    nulos = df[columnas].isna().sum()
    malos = nulos[nulos > 0]
    return resultado("Campos obligatorios informados", malos.empty,
                     ", ".join(f"{c}: {v}" for c, v in malos.items()) or "sin nulos")


def control_rango(df: pd.DataFrame, columna: str, minimo=None, maximo=None, aviso=False) -> dict:
    fuera = pd.Series(False, index=df.index)
    if minimo is not None:
        fuera |= df[columna] < minimo
    if maximo is not None:
        fuera |= df[columna] > maximo
    return resultado(f"'{columna}' en rango [{minimo}, {maximo}]", not fuera.any(),
                     f"{int(fuera.sum())} valores fuera de rango", aviso=aviso)


def control_integridad(df: pd.DataFrame, col: str, maestro: pd.Series, nombre_maestro: str) -> dict:
    huerfanos = ~df[col].isin(maestro)
    return resultado(f"'{col}' existe en {nombre_maestro}", not huerfanos.any(),
                     f"{int(huerfanos.sum())} registros sin correspondencia")


def control_cuadre(nombre: str, calculado: float, esperado: float, tolerancia: float = 0.01) -> dict:
    """Cuadre de totales. ¡Nunca uses == con decimales! (0.1 + 0.2 != 0.3)"""
    ok = math.isclose(calculado, esperado, abs_tol=tolerancia)
    return resultado(nombre, ok, f"calculado={calculado:,.2f} | esperado={esperado:,.2f} | "
                                 f"diferencia={calculado - esperado:,.2f}")


def ejecutar_controles(controles: list[Callable[[], dict]] | list[dict]) -> pd.DataFrame:
    filas = [c() if callable(c) else c for c in controles]
    return pd.DataFrame(filas)
