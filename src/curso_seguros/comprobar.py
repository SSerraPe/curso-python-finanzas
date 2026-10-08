"""Comprobaciones amables para los ejercicios.

Uso en un notebook:
    from curso_seguros.comprobar import comprobar
    comprobar(mi_resultado, esperado, "Pista: ¿has dividido sumas o has promediado ratios?")
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _iguales(a, b, rtol: float) -> bool:
    if isinstance(a, (pd.DataFrame, pd.Series)) and isinstance(b, (pd.DataFrame, pd.Series)):
        a, b = a.sort_index(), b.sort_index()
    if isinstance(a, (pd.DataFrame, pd.Series)) or isinstance(b, (pd.DataFrame, pd.Series)):
        a_, b_ = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        return a_.shape == b_.shape and np.allclose(a_, b_, rtol=rtol, equal_nan=True)
    if isinstance(a, (np.ndarray, list, tuple)) or isinstance(b, (np.ndarray, list, tuple)):
        try:
            a_, b_ = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
            return a_.shape == b_.shape and np.allclose(a_, b_, rtol=rtol, equal_nan=True)
        except (TypeError, ValueError):
            return list(a) == list(b)
    if isinstance(a, (int, float, np.number)) and isinstance(b, (int, float, np.number)):
        return bool(np.isclose(float(a), float(b), rtol=rtol))
    return a == b


def comprobar(valor, esperado, pista: str = "", rtol: float = 1e-4) -> None:
    """Imprime ✅ si `valor` coincide con `esperado` (con tolerancia) o ❌ + pista.

    `valor` puede ser una función sin argumentos (p. ej. `lambda: df["col"]`): así,
    si el ejercicio aún no está hecho, se avisa en lugar de dar un error.
    """
    if callable(valor) and not isinstance(valor, (pd.DataFrame, pd.Series)):
        try:
            valor = valor()
        except Exception:  # noqa: BLE001
            print("⏳ Aún no has completado el ejercicio (o tu resultado no tiene la forma esperada).")
            if pista:
                print("💡", pista)
            return
    if valor is ... or valor is None:
        print("⏳ Aún no has completado el ejercicio (sustituye los ___ o el ... por tu código).")
        return
    try:
        ok = _iguales(valor, esperado, rtol)
    except Exception as e:  # noqa: BLE001
        print(f"❌ No he podido comparar el resultado ({type(e).__name__}: {e}).")
        if pista:
            print("💡", pista)
        return
    if ok:
        print("✅ ¡Correcto!")
    else:
        print(f"❌ Todavía no. Obtienes {valor!r:.80} y se esperaba otra cosa.")
        if pista:
            print("💡", pista)


def comprobar_condicion(condicion: bool, mensaje_ok: str = "✅ ¡Correcto!", pista: str = "") -> None:
    print(mensaje_ok if condicion else f"❌ Todavía no.{(' 💡 ' + pista) if pista else ''}")
