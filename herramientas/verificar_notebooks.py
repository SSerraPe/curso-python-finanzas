"""
Ejecuta los notebooks y verifica que:
  * versión soluciones: ninguna celda da error y ninguna comprobación sale ❌/⏳
  * versión alumno:     ninguna celda que NO sea ejercicio da error

Uso:  python herramientas/verificar_notebooks.py [patrón]     (p. ej. 03)
Ejecutar desde la raíz del curso. Recomendado antes de cada edición del curso.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = Path(__file__).resolve().parents[1]


def salida_texto(cell) -> str:
    partes = []
    for o in cell.get("outputs", []):
        if o.get("output_type") == "stream":
            partes.append(o.get("text", ""))
        elif o.get("output_type") in ("execute_result", "display_data"):
            partes.append(str(o.get("data", {}).get("text/plain", "")))
    return "".join(partes)


def ejecutar(ruta: Path, permitir_errores: bool) -> tuple[nbformat.NotebookNode, float]:
    nb = nbformat.read(ruta, as_version=4)
    t = time.time()
    NotebookClient(nb, timeout=900, kernel_name="python3", allow_errors=permitir_errores,
                   resources={"metadata": {"path": str(ruta.parent)}}).execute()
    return nb, time.time() - t


def main(patron: str = "") -> int:
    fallos = 0
    for ruta in sorted((RAIZ / "notebooks" / "soluciones").glob(f"*{patron}*.ipynb")):
        try:
            nb, dur = ejecutar(ruta, permitir_errores=False)
        except CellExecutionError as e:
            print(f"❌ {ruta.name}: error de ejecución\n{str(e)[:1500]}")
            fallos += 1
            continue
        malas = [salida_texto(c)[:200] for c in nb.cells if c.cell_type == "code"
                 and any(s in salida_texto(c) for s in ("❌", "⏳"))]
        print(f"{'✅' if not malas else '❌'} soluciones/{ruta.name} ({dur:.0f}s)")
        for m in malas:
            print("     ", m.replace("\n", " | "))
        fallos += bool(malas)
        nbformat.write(nb, ruta)          # guardamos la versión ejecutada (con gráficos) para consulta

        ruta_al = RAIZ / "notebooks" / ruta.name
        nb_al, dur = ejecutar(ruta_al, permitir_errores=True)
        errores = [c.source[:120] for c in nb_al.cells if c.cell_type == "code"
                   and "ejercicio" not in c.metadata.get("tags", [])
                   and any(o.get("output_type") == "error" for o in c.get("outputs", []))]
        print(f"{'✅' if not errores else '⚠️ '} alumno/{ruta_al.name} ({dur:.0f}s)"
              + (f" -> {len(errores)} celdas no-ejercicio con error" if errores else ""))
        for e in errores:
            print("     ", e.replace("\n", " | "))
    return fallos


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
