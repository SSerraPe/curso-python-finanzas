"""
Genera los notebooks del curso (versión alumno + versión soluciones) a partir
de las fuentes en herramientas/fuentes_notebooks/*.txt

Formato de las fuentes
----------------------
#== md                 -> empieza una celda markdown
#== code               -> empieza una celda de código
#== setup              -> inserta la celda estándar de preparación del entorno
#== setup:chainladder  -> idem, instalando además chainladder (reinicia Colab)
{{REPO_URL}}          -> se sustituye por REPO_URL (en celdas md y de código)

Dentro de una celda de código:
# >>> ALUMNO           (líneas comentadas con '# ' que verá el alumno)
# <<< ALUMNO
# >>> SOLUCION         (código de la solución)
# <<< SOLUCION

Uso: python herramientas/construir_notebooks.py
"""
from __future__ import annotations

import re
from pathlib import Path

import nbformat as nbf

RAIZ = Path(__file__).resolve().parents[1]
FUENTES = RAIZ / "herramientas" / "fuentes_notebooks"
DESTINO = RAIZ / "notebooks"

REPO_URL = "https://github.com/SSerraPe/curso-python-finanzas.git"

SETUP = '''# @title ⚙️ Ejecuta esta celda primero (prepara el entorno) { display-mode: "form" }
import os, sys, subprocess
from pathlib import Path

REPO_URL = "{repo}"
COPIA_DRIVE = Path("/content/drive/MyDrive/curso-python-finanzas")  # la crea el notebook 00
EN_COLAB = "google.colab" in sys.modules

if EN_COLAB:
    from google.colab import drive
    try:
        drive.mount("/content/drive")
    except Exception as e:
        print("⚠️ No se ha podido conectar Google Drive:", e)
    if COPIA_DRIVE.is_dir():
        os.chdir(COPIA_DRIVE)
    else:
        print("⚠️ No encuentro tu copia del curso en Mi unidad › curso-python-finanzas (ver notebook 00).")
        print("   Uso una copia TEMPORAL: lo que generes se pierde al cerrar Colab.")
        if not Path("/content/curso-python-finanzas").exists():
            subprocess.run(["git", "clone", "-q", "--depth", "1", REPO_URL, "/content/curso-python-finanzas"], check=True)
        os.chdir("/content/curso-python-finanzas")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True){extra}
else:
    # En tu ordenador: nos situamos en la carpeta raíz del curso (la que tiene data/ y src/)
    while not (Path("data").is_dir() and Path("src").is_dir()) and Path.cwd() != Path.cwd().parent:
        os.chdir("..")

sys.path.insert(0, str(Path("src").resolve()))
print("✅ Entorno listo. Carpeta de trabajo:", Path.cwd())'''

EXTRA_CHAINLADDER = '''
    try:
        import chainladder  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "chainladder==0.10.1"], check=True)
        print("🔄 Se ha instalado chainladder y Colab se reiniciará. Cuando reconecte, VUELVE A EJECUTAR ESTA CELDA.")
        os.kill(os.getpid(), 9)'''

RE_ALUMNO = re.compile(r"^[ \t]*# >>> ALUMNO\n(.*?)^[ \t]*# <<< ALUMNO\n?", re.S | re.M)
RE_SOLUCION = re.compile(r"^[ \t]*# >>> SOLUCION\n(.*?)^[ \t]*# <<< SOLUCION\n?", re.S | re.M)


def descomentar(bloque: str) -> str:
    lineas = []
    for l in bloque.splitlines():
        m = re.match(r"^([ \t]*)# ?(.*)$", l)
        lineas.append(m.group(1) + m.group(2) if m else l)
    return "\n".join(lineas) + "\n"


def version(codigo: str, alumno: bool) -> str:
    if alumno:
        codigo = RE_SOLUCION.sub("", codigo)
        codigo = RE_ALUMNO.sub(lambda m: descomentar(m.group(1)), codigo)
    else:
        codigo = RE_ALUMNO.sub("", codigo)
        codigo = RE_SOLUCION.sub(lambda m: m.group(1), codigo)
    return codigo.strip("\n")


def parsear(texto: str) -> list[tuple[str, str]]:
    celdas, tipo, buf = [], None, []
    for linea in texto.splitlines():
        m = re.match(r"^#== (md|code|setup(?::\w+)?)\s*$", linea)
        if m:
            if tipo:
                celdas.append((tipo, "\n".join(buf).strip("\n")))
            tipo, buf = m.group(1), []
        else:
            buf.append(linea)
    if tipo:
        celdas.append((tipo, "\n".join(buf).strip("\n")))
    return celdas


def construir(fuente: Path) -> None:
    celdas = parsear(fuente.read_text(encoding="utf-8"))
    for alumno in (True, False):
        nb = nbf.v4.new_notebook()
        nb.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3"},
                       "language_info": {"name": "python"},
                       "colab": {"provenance": [], "toc_visible": True}}
        for tipo, contenido in celdas:
            if tipo == "md":
                contenido = contenido.replace("{{REPO_URL}}", REPO_URL)
                if not alumno:
                    contenido = contenido.replace("{{SOLUCIONES}}", "> 🔑 **Versión con soluciones.**")
                else:
                    contenido = contenido.replace("{{SOLUCIONES}}", "")
                nb.cells.append(nbf.v4.new_markdown_cell(contenido))
            elif tipo.startswith("setup"):
                extra = EXTRA_CHAINLADDER if tipo == "setup:chainladder" else ""
                nb.cells.append(nbf.v4.new_code_cell(SETUP.replace("{repo}", REPO_URL).replace("{extra}", extra)))
            else:
                es_ejercicio = "# >>> SOLUCION" in contenido
                cel = nbf.v4.new_code_cell(version(contenido.replace("{{REPO_URL}}", REPO_URL), alumno))
                if es_ejercicio:
                    cel.metadata["tags"] = ["ejercicio"]
                nb.cells.append(cel)
        destino = DESTINO / (fuente.stem + ".ipynb") if alumno else DESTINO / "soluciones" / (fuente.stem + ".ipynb")
        destino.parent.mkdir(parents=True, exist_ok=True)
        nbf.write(nb, destino)
    print("✔", fuente.stem)


if __name__ == "__main__":
    for f in sorted(FUENTES.glob("*.txt")):
        construir(f)
