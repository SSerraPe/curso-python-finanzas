# Python aplicado a Finanzas (FP&A) en Seguros

Curso práctico de **5 sesiones × 2 h** para equipos de administración y planeación financiera que dominan Excel y empiezan con Python. Todo gira alrededor de **un único caso de negocio**: la cuenta de resultados del ramo Autos de una aseguradora, con 678.000 pólizas reales (dataset público freMTPL2) y una capa financiera simulada (canales, presupuesto, gastos y cierres mensuales).

Los notebooks se ejecutan **en local con VS Code**: cada alumno tiene la carpeta del curso en su ordenador. Google Colab queda como plan B.

---

## 📚 Documentos

| # | Documento | Para qué |
|---|---|---|
| 1 | [`docs/01_temario.md`](docs/01_temario.md) | Temario rediseñado: objetivos, agenda minuto a minuto y correspondencia con el temario original |
| 2 | [`docs/02_notas_tecnicas.md`](docs/02_notas_tecnicas.md) | Notas técnicas del instructor: conceptos, fórmulas, errores típicos y mensajes clave por sesión |
| 3 | [`docs/03_caso_de_uso.md`](docs/03_caso_de_uso.md) | El caso: historia, origen de los datos, diccionario, recorrido paso a paso y **cifras de referencia** |
| — | [`docs/investigacion/`](docs/investigacion/) | Informe de investigación previa (datasets, métodos, herramientas, pedagogía) |

## 🧑‍💻 Notebooks (alumnos)

| Sesión | Notebook (en la carpeta del curso) | Plan B |
|---|---|---|
| S1 · inicio (guiado) · tu entorno en VS Code | [`notebooks/00_preparacion_vscode_y_python.ipynb`](notebooks/00_preparacion_vscode_y_python.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/00_preparacion_vscode_y_python.ipynb) |
| S1 · Python para quien viene de Excel | [`notebooks/01_fundamentos_python.ipynb`](notebooks/01_fundamentos_python.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/01_fundamentos_python.ipynb) |
| S2 · pandas, KPIs y visualización | [`notebooks/02_pandas_kpis_visualizacion.ipynb`](notebooks/02_pandas_kpis_visualizacion.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/02_pandas_kpis_visualizacion.ipynb) |
| S3 · Automatización del cierre mensual | [`notebooks/03_automatizacion_cierre_mensual.ipynb`](notebooks/03_automatizacion_cierre_mensual.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/03_automatizacion_cierre_mensual.ipynb) |
| S4 · Estadística aplicada a costes | [`notebooks/04_estadistica_aplicada.ipynb`](notebooks/04_estadistica_aplicada.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/04_estadistica_aplicada.ipynb) |
| S5 · GLM y segmentación | [`notebooks/05_glm_segmentacion.ipynb`](notebooks/05_glm_segmentacion.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/05_glm_segmentacion.ipynb) |
| C1 · Grandes volúmenes y SQL | [`notebooks/C1_grandes_volumenes_sql.ipynb`](notebooks/C1_grandes_volumenes_sql.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/C1_grandes_volumenes_sql.ipynb) |
| C2 · Reservas e IBNR | [`notebooks/C2_reservas_chain_ladder.ipynb`](notebooks/C2_reservas_chain_ladder.ipynb) | [Colab](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/C2_reservas_chain_ladder.ipynb) |

Las soluciones (ya ejecutadas, con gráficos) están en [`notebooks/soluciones/`](notebooks/soluciones/).

### 🛠️ Puesta en marcha del alumno (VS Code, una sola vez, ~20 min)

GitHub es el **original de solo lectura** del profesor. Cada alumno trabaja en **su carpeta del curso en su ordenador**: allí se guardan sus notebooks, sus ejercicios y lo que generan (Excel, PDF…). No hace falta cuenta de GitHub. Conviene hacerlo **antes de la sesión 1**; el notebook `00` lo comprueba en clase.

1. **Instalar Python 3.12** desde [python.org/downloads](https://www.python.org/downloads/).
   - **Windows:** en la primera pantalla del instalador marca **☑ Add python.exe to PATH**.
   - Comprueba en una terminal: `python --version` (Mac: `python3 --version`).
2. **Instalar VS Code** desde [code.visualstudio.com](https://code.visualstudio.com/) y, en *Extensions* (Ctrl+Shift+X), las extensiones **Python** y **Jupyter** de Microsoft. Al abrir la carpeta del curso, VS Code las propone solo.
3. **Descargar la carpeta del curso** (elige una):
   - **ZIP (sin instalar nada más):** en la página de GitHub del curso, botón verde **Code → Download ZIP**. Descomprímelo en *Documentos* y renombra la carpeta `curso-python-finanzas-main` → `curso-python-finanzas`.
   - **Git** (si lo tienes instalado): `git clone https://github.com/SSerraPe/curso-python-finanzas.git`
4. **Abrir la carpeta en VS Code:** *File → Open Folder…* → `curso-python-finanzas` (la que contiene `data/`, `notebooks/` y `src/`, no una carpeta por encima). Si pregunta *¿Confías en los autores?* → **Yes, I trust the authors**.
5. **Crear el entorno `.venv` e instalar las librerías.** Abre *Terminal → New Terminal* y ejecuta:
   ```bash
   python -m venv .venv                 # Mac: python3 -m venv .venv
   .venv\Scripts\activate               # Mac: source .venv/bin/activate
   pip install -r requirements.txt      # 3-5 minutos
   ```
   *Alternativa sin terminal:* paleta de comandos (Ctrl+Shift+P) → **Python: Create Environment** → **Venv** → Python 3.12 → marcar `requirements.txt`.
6. **Abrir `notebooks/00_preparacion_vscode_y_python.ipynb`**, elegir el kernel **`.venv`** (arriba a la derecha → *Select Kernel → Python Environments → .venv*) y ejecutar la celda 🩺: todo debe salir ✅.

**Cada sesión:**
1. Abrir VS Code en la carpeta del curso y, en `notebooks/`, el notebook de la sesión.
2. Comprobar que el kernel es `.venv` y ejecutar la primera celda ⚙️: se sitúa en la carpeta del curso y, si falta alguna librería, la instala.
3. Leer, ejecutar y completar los ejercicios ✏️ (sustituyendo los `...`). La celda siguiente dice ✅ o ❌ y da una pista. **Guardar con Ctrl+S.**
4. Si un ejercicio se atasca, una celda 🛟 carga la solución para poder seguir.

**Si corriges algo durante el curso:** haz `push` a GitHub. Quien usó Git ejecuta `git pull`. Quien usó el ZIP lo descarga de nuevo y ejecuta la celda **🔄 Actualizar mi copia** (sección 9 del notebook 00): renueva datos, `src/`, scripts, documentos y soluciones, y añade notebooks nuevos **sin sobrescribir** los notebooks en los que trabaja el alumno.

**Plan B · Colab:** si un alumno no puede instalar nada, abre el notebook con el enlace *Colab* de la tabla. La celda ⚙️ clona una **copia temporal** del curso (lo generado se pierde al cerrar; hay que descargarlo) e instala `requirements-colab.txt`.

---

## 🗂️ Estructura

```
curso-python-finanzas/
├── README.md
├── .vscode/                  ← extensiones recomendadas y ajustes (kernel .venv, raíz del curso)
├── requirements.txt          ← entorno local completo (VS Code)
├── requirements-colab.txt    ← plan B: lo que Colab no trae (lo instala la celda ⚙️)
├── config/params.yaml        ← parámetros del cierre (periodo, destinatarios…)
├── data/
│   ├── raw/                  ← freMTPL2 original (tal cual, con sus rarezas)
│   ├── cartera/              ← cartera 2025 (pólizas reales + capa financiera simulada)
│   ├── entrada/              ← lo que "llega" cada mes: bordereaux, presupuesto, gastos, parámetros
│   ├── referencia/           ← maestro limpio de siniestros + lista de problemas introducidos
│   └── triangulos/           ← RAA y CAS Schedule P (reservas)
├── docs/                     ← los 3 documentos + investigación
├── notebooks/                ← versión alumno (+ soluciones/)
├── scripts/
│   ├── run_report.py         ← cierre mensual automático (Excel + PDF + correos)
│   └── preparar_datos.py     ← regenera todos los datos desde las fuentes públicas
├── src/curso_seguros/        ← funciones reutilizables (datos, kpis, cierre, controles, informes, correo…)
├── herramientas/             ← generador y verificador de notebooks (para el instructor)
└── output/                   ← salidas generadas (no se versiona)
```

---

## 🧭 Puesta en marcha (instructor)

### 1. Publicar el repositorio en GitHub
```bash
cd curso-python-finanzas
python herramientas/configurar_repo.py <tu-usuario-u-organizacion>   # pone tu usuario en los enlaces de notebooks, README y generador
git init && git add . && git commit -m "Curso Python FP&A Seguros"
git branch -M main
git remote add origin https://github.com/<tu-usuario-u-organizacion>/curso-python-finanzas.git
git push -u origin main
```
El repositorio debe ser **público** (los datos son públicos o simulados): los alumnos lo descargan (ZIP o `git clone`) sin cuenta de GitHub, y la celda ⚙️ del plan B lo clona desde Colab sin autenticación.

### 2. Comprobar que todo funciona
```bash
pip install -r requirements.txt nbclient
python herramientas/verificar_notebooks.py        # ejecuta soluciones y versión alumno
python scripts/run_report.py --periodo 2025-09    # genera output/2025-09/
```
Además, **haz la puesta en marcha del alumno en un ordenador limpio** (idealmente Windows con el usuario corporativo) la semana anterior.

### 3. Modificar el contenido
Los notebooks **se generan** a partir de `herramientas/fuentes_notebooks/*.txt`, que contienen la versión alumno y la de soluciones a la vez. Para cambiar un notebook:
```bash
# editar herramientas/fuentes_notebooks/0X_....txt
python herramientas/construir_notebooks.py
python herramientas/verificar_notebooks.py 0X
```

### 4. Entorno local del instructor
Igual que el alumno (ver *Puesta en marcha del alumno*), más `pip install nbclient` para el verificador. `chainladder==0.10.1` (notebook C2, requiere pandas ≥ 2.3.3) ya viene en `requirements.txt`; la celda ⚙️ del C2 lo instala solo si falta.

---

## ⚖️ Datos y licencias
- **freMTPL2freq / freMTPL2sev**: paquete R [CASdatasets](https://github.com/dutangc/CASdatasets) (Dutang & Charpentier), GPL ≥ 2; espejo en OpenML (ids 41214 / 41215, CC0).
- **Triángulos**: muestras `raa` y `clrd2025` del paquete [chainladder](https://github.com/casact/chainladder-python) (MPL-2.0); origen: CAS Loss Reserving Database (NAIC Schedule P).
- Canales, fechas, primas, presupuesto, gastos y bordereaux son **simulados** (ver `docs/03_caso_de_uso.md`). Cualquier parecido con una compañía real es casual.
- **En Colab (plan B) solo deben usarse datos públicos o simulados**, nunca datos de la empresa.
