"""
Genera los notebooks del curso (versión alumno + versión soluciones) a partir
de las fuentes en herramientas/fuentes_notebooks/*.txt

Formato de las fuentes
----------------------
#== md                 -> empieza una celda markdown
#== code               -> empieza una celda de código
#== setup              -> inserta la celda estándar de preparación del entorno
#== setup:chainladder  -> idem, instalando además chainladder (pide reiniciar el kernel)
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

SETUP = '''# ⚙️ Ejecuta esta celda primero (prepara el entorno)
import os, sys, subprocess, importlib.util
from pathlib import Path

REPO_URL = "{repo}"
EN_COLAB = "google.colab" in sys.modules

if EN_COLAB:
    # Plan B: Colab con una copia TEMPORAL del curso (lo que generes se pierde al cerrar)
    if not Path("/content/curso-python-finanzas").exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO_URL, "/content/curso-python-finanzas"], check=True)
    os.chdir("/content/curso-python-finanzas")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
    print("ℹ️ Estás en Colab (plan B): trabajas sobre una copia temporal. Descarga lo que quieras conservar.")
else:
    # En tu ordenador (VS Code): nos situamos en la carpeta raíz del curso (la que tiene data/ y src/)
    while not (Path("data").is_dir() and Path("src").is_dir()) and Path.cwd() != Path.cwd().parent:
        os.chdir("..")
    if not (Path("data").is_dir() and Path("src").is_dir()):
        raise RuntimeError("No encuentro la carpeta del curso. En VS Code usa File → Open Folder… → curso-python-finanzas")
    if not Path(sys.prefix).resolve().is_relative_to(Path.cwd().resolve()):
        print("⚠️ El kernel no es el entorno .venv del curso:", sys.executable)
        print("   Arriba a la derecha del notebook → Select Kernel → Python Environments → .venv")
    faltan = [m for m in ("pandas", "openpyxl", "xlsxwriter", "fpdf", "pandera", "statsmodels", "matplotlib", "yaml")
              if importlib.util.find_spec(m) is None]
    if faltan:
        print("⏳ Faltan librerías (" + ", ".join(faltan) + "). Instalando requirements.txt…")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=True)
        print("🔄 Instaladas. Si alguna celda da ModuleNotFoundError, pulsa Restart (barra del notebook) y vuelve a ejecutar esta celda."){extra}

sys.path.insert(0, str(Path("src").resolve()))
print("✅ Entorno listo. Carpeta de trabajo:", Path.cwd())'''

EXTRA_CHAINLADDER = '''
try:
    import chainladder  # noqa: F401
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "chainladder==0.10.1"], check=True)
    if EN_COLAB:
        print("🔄 Se ha instalado chainladder y Colab se reiniciará. Cuando reconecte, VUELVE A EJECUTAR ESTA CELDA.")
        os.kill(os.getpid(), 9)
    raise SystemExit("🔄 Se ha instalado chainladder. Pulsa Restart (barra del notebook) y VUELVE A EJECUTAR ESTA CELDA.")'''

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
                       "language_info": {"name": "python"}}
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
