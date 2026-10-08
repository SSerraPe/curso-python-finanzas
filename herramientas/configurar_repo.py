"""
Sustituye el usuario/organización de GitHub de ejemplo (TU_USUARIO) por el real
en los notebooks, el README y el generador.

Uso:  python herramientas/configurar_repo.py mi-usuario-o-organizacion
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

if len(sys.argv) != 2:
    sys.exit(__doc__)
usuario = sys.argv[1].strip().strip("/")
ficheros = [RAIZ / "README.md", RAIZ / "herramientas" / "construir_notebooks.py",
            *(RAIZ / "notebooks").rglob("*.ipynb")]
n = 0
for f in ficheros:
    texto = f.read_text(encoding="utf-8")
    if "TU_USUARIO" in texto:
        f.write_text(texto.replace("TU_USUARIO", usuario), encoding="utf-8")
        n += 1
print(f"Actualizados {n} ficheros con github.com/{usuario}/curso-python-finanzas")
