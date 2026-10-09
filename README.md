# Python aplicado a Finanzas (FP&A) en Seguros

Curso práctico de **5 sesiones × 2 h** para equipos de administración y planeación financiera que dominan Excel y empiezan con Python. Todo gira alrededor de **un único caso de negocio**: la cuenta de resultados del ramo Autos de una aseguradora, con 678.000 pólizas reales (dataset público freMTPL2) y una capa financiera simulada (canales, presupuesto, gastos y cierres mensuales).

Los notebooks se ejecutan en **Google Colab** sin instalar nada, y también en local.

---

## 📚 Documentos

| # | Documento | Para qué |
|---|---|---|
| 1 | [`docs/01_temario.md`](docs/01_temario.md) | Temario rediseñado: objetivos, agenda minuto a minuto y correspondencia con el temario original |
| 2 | [`docs/02_notas_tecnicas.md`](docs/02_notas_tecnicas.md) | Notas técnicas del instructor: conceptos, fórmulas, errores típicos y mensajes clave por sesión |
| 3 | [`docs/03_caso_de_uso.md`](docs/03_caso_de_uso.md) | El caso: historia, origen de los datos, diccionario, recorrido paso a paso y **cifras de referencia** |
| — | [`docs/investigacion/`](docs/investigacion/) | Informe de investigación previa (datasets, métodos, herramientas, pedagogía) |

## 🧑‍💻 Notebooks (alumnos)

| Sesión | Notebook | Abrir |
|---|---|---|
| S1 · inicio (guiado) · tu copia del curso | `00_preparacion_colab_y_python` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/00_preparacion_colab_y_python.ipynb) |
| S1 · Python para quien viene de Excel | `01_fundamentos_python` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/01_fundamentos_python.ipynb) |
| S2 · pandas, KPIs y visualización | `02_pandas_kpis_visualizacion` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/02_pandas_kpis_visualizacion.ipynb) |
| S3 · Automatización del cierre mensual | `03_automatizacion_cierre_mensual` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/03_automatizacion_cierre_mensual.ipynb) |
| S4 · Estadística aplicada a costes | `04_estadistica_aplicada` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/04_estadistica_aplicada.ipynb) |
| S5 · GLM y segmentación | `05_glm_segmentacion` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/05_glm_segmentacion.ipynb) |
| C1 · Grandes volúmenes y SQL | `C1_grandes_volumenes_sql` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/C1_grandes_volumenes_sql.ipynb) |
| C2 · Reservas e IBNR | `C2_reservas_chain_ladder` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SSerraPe/curso-python-finanzas/blob/main/notebooks/C2_reservas_chain_ladder.ipynb) |

Las soluciones (ya ejecutadas, con gráficos) están en [`notebooks/soluciones/`](notebooks/soluciones/).

### Cómo trabajan los alumnos: su propia copia del curso en Google Drive

GitHub es la **fuente de solo lectura**. Cada alumno trabaja sobre **una copia completa del repositorio en su Google Drive** (`Mi unidad › curso-python-finanzas`), así sus notebooks, sus ejercicios y los ficheros que generan (Excel, PDF…) se conservan de una sesión a otra. No hace falta cuenta de GitHub, solo una cuenta de Google.

**Primer día (al inicio de la sesión 1, todos a la vez, ~25 min):**
1. El profesor comparte **un único enlace**: el botón *Open in Colab* del notebook `00`.
2. El alumno ejecuta la celda **📥 Copia el curso en tu Google Drive** y autoriza el acceso a Drive. La celda clona el repositorio y lo copia en su Drive.
3. Abre **su copia** del notebook 00 (*Archivo → Abrir cuaderno → Google Drive*) y sigue allí.

**Cada sesión:**
1. Abrir el notebook **desde Drive** (*Archivo → Abrir cuaderno → Google Drive*, o *Recientes*).
2. Ejecutar la primera celda ⚙️: conecta Drive, se sitúa en la copia del alumno e instala lo que Colab no trae. Si no encuentra la copia, avisa y trabaja con una copia temporal clonada de GitHub.
3. Leer, ejecutar y completar los ejercicios ✏️ (sustituyendo los `...`). La celda siguiente dice ✅ o ❌ y da una pista.
4. Si un ejercicio se atasca, una celda 🛟 carga la solución para poder seguir.

**Si corriges algo durante el curso:** haz `push` a GitHub y pide a los alumnos que ejecuten la celda **🔄 Actualizar mi copia** (sección 9 del notebook 00). Renueva datos, `src/`, scripts, documentos y soluciones, y añade notebooks nuevos **sin sobrescribir** los notebooks en los que trabaja el alumno.

---

## 🗂️ Estructura

```
curso-python-finanzas/
├── README.md
├── requirements.txt          ← entorno local completo
├── requirements-colab.txt    ← lo que Colab no trae (lo instala la celda ⚙️)
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
El repositorio debe ser **público** (los datos son públicos o simulados): las celdas 📥, 🔄 y ⚙️ lo clonan desde Colab sin autenticación. Si fuera privado, esa copia fallaría.

### 2. Comprobar que todo funciona
```bash
pip install -r requirements.txt nbclient
python herramientas/verificar_notebooks.py        # ejecuta soluciones y versión alumno
python scripts/run_report.py --periodo 2025-09    # genera output/2025-09/
```
Además, **abre cada notebook en Colab la semana anterior** (Colab actualiza librerías sin avisar).

### 3. Modificar el contenido
Los notebooks **se generan** a partir de `herramientas/fuentes_notebooks/*.txt`, que contienen la versión alumno y la de soluciones a la vez. Para cambiar un notebook:
```bash
# editar herramientas/fuentes_notebooks/0X_....txt
python herramientas/construir_notebooks.py
python herramientas/verificar_notebooks.py 0X
```

### 4. Trabajar en local (plan B si Colab no está permitido)
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (source .venv/bin/activate en Mac/Linux)
pip install -r requirements.txt
jupyter lab
```
El notebook C2 necesita `pip install chainladder==0.10.1` (requiere pandas ≥ 2.3.3).

---

## ⚖️ Datos y licencias
- **freMTPL2freq / freMTPL2sev**: paquete R [CASdatasets](https://github.com/dutangc/CASdatasets) (Dutang & Charpentier), GPL ≥ 2; espejo en OpenML (ids 41214 / 41215, CC0).
- **Triángulos**: muestras `raa` y `clrd2025` del paquete [chainladder](https://github.com/casact/chainladder-python) (MPL-2.0); origen: CAS Loss Reserving Database (NAIC Schedule P).
- Canales, fechas, primas, presupuesto, gastos y bordereaux son **simulados** (ver `docs/03_caso_de_uso.md`). Cualquier parecido con una compañía real es casual.
- **En Colab solo deben usarse datos públicos o simulados**, nunca datos de la empresa.
