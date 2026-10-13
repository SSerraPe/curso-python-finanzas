# Documento 1 · Temario rediseñado

**Curso:** Python aplicado a Finanzas (FP&A) en una aseguradora
**Formato:** 5 sesiones × 2 h (la primera empieza con la preparación del entorno, guiada en clase) + 2 módulos complementarios autónomos
**Público:** equipo de administración y planeación financiera (FP&A). Dominan Excel y no han programado en Python
**Entorno:** VS Code en local. Cada alumno instala Python 3.12 y VS Code, descarga la carpeta del curso desde GitHub (ZIP o `git clone`) y trabaja siempre sobre esa carpeta con un entorno `.venv`. No requiere cuenta de GitHub. Google Colab queda como plan B

---

## 1. Principios de diseño

1. **Un único caso de negocio de principio a fin.** Una aseguradora de autos con unas 678.000 pólizas, cuatro canales comerciales y un año de operación (2025). En cada sesión se responde a una pregunta de negocio sobre esa misma cartera, sin datasets nuevos que haya que entender cada vez.
2. **Lenguaje FP&A, no actuarial.** Hablamos de ingresos (primas), costes (siniestros, comisiones, gastos de estructura), margen, rentabilidad por canal, real frente a presupuesto y forecast. Los conceptos actuariales (frecuencia, coste medio, GLM) aparecen como *drivers* del coste, que es lo que le interesa a finanzas.
3. **De Excel a Python.** Cada técnica nueva se presenta con su equivalente en Excel: BUSCARV → `merge`, tabla dinámica → `pivot_table`, SUMAR.SI.CONJUNTO → `groupby().sum()`.
4. **Notebooks autónomos.** Cada notebook tiene explicación, ejemplo resuelto, ejercicio con huecos y una celda de comprobación automática. Hay una versión con soluciones en `notebooks/soluciones/`. Quien no termine en clase puede acabar en casa sin ayuda.
5. **Un mismo principio recorre todo el curso.** Los ratios de un grupo se calculan como **cociente de sumas**, no como media de ratios. Aparece en el margen por canal (sesión 2), el reparto de gastos (sesión 3), el bootstrap del ratio de siniestralidad (sesión 4), los pesos del GLM (sesión 5) y los factores de desarrollo del chain-ladder (C2).
6. **Priorizar lo que se usa el lunes siguiente.** La automatización del cierre mensual va en la sesión 3, antes de la estadística y los modelos.

## 2. Qué pasa con cada punto del temario original

| Temario original | Dónde se ve | Profundidad |
|---|---|---|
| 1. Fundamentos de Python (sintaxis, tipos, control, funciones, módulos, buenas prácticas) | P0 + **S1** | En clase (núcleo) |
| 2. Pandas y NumPy: limpieza, EDA, KPIs, agrupación por portafolios y líneas de negocio | **S2** (y se refuerza en S3) | En clase (núcleo) |
| 3. Visualización: matplotlib, seaborn, plotly, gráficos interactivos | **S2** (último bloque), S3 (gráficos del informe) | En clase |
| 4. Automatización: scripts que actualizan reportes, envío de correos, Excel y PDF, validación y control | **S3** | En clase (núcleo) |
| 5. Estadística aplicada: ajuste de frecuencia y severidad, IC y bootstrap | **S4**, en clave de incertidumbre de costes y forecast | En clase |
| 6. Modelos actuariales y ML básico: segmentación y GLM | **S5**, en clave de *drivers* de rentabilidad | En clase |
| 7. Grandes volúmenes: lectura eficiente, SQL, Dask y PySpark | **C1** (autónomo) + demo de 5 min en S2 | Autónomo |
| 8. Buenas prácticas y Git | S1 (estilo), **S3** (estructura de proyecto y Git en 15 min) + guía en las notas técnicas | En clase (breve) + guía |
| 9. Automatización de reportes financieros | **S3**, el informe de cierre mensual completo | En clase (núcleo) |
| *(añadido)* Reservas e IBNR (chain-ladder) | **C2** (autónomo) | Autónomo, opcional |

Con 10 horas, el temario original completo solo se podría cubrir en modo "presentación". La propuesta prioriza que los alumnos **hagan** las cosas. Los puntos 7 y el anexo de reservas pasan a material autónomo con su notebook y su solución.

## 3. El caso de negocio (hilo conductor)

> *"Somos el equipo de FP&A del ramo de Autos. Cada mes recibimos la cartera de pólizas, los ficheros de siniestros declarados (uno por mes, cada uno de su padre y de su madre), el presupuesto y los gastos de estructura. Tenemos que cerrar el mes, explicar las desviaciones contra presupuesto por canal, decirle a Dirección qué segmentos destruyen valor y dar un rango creíble para el cierre del año."*

Datos (todos en `data/`, descritos en el documento 3):

- **Cartera 2025**: 677.991 pólizas reales de autos (dataset público freMTPL2), a las que se añaden el canal, las fechas y la prima anual (simulados).
- **12 ficheros Excel mensuales de siniestros** con problemas de calidad reales: cambio de sistema en julio, duplicados, pólizas mal tecleadas, recobros negativos y un descuadre en septiembre.
- **Presupuesto 2025** por canal y mes, en formato ancho como en Excel.
- **Gastos de estructura** por centro de coste y partida, con sus claves de reparto.
- **Tabla de comisiones** por canal.
- **Triángulos de reservas** (CAS Schedule P) para el anexo C2.

---

## 4. Sesiones

### P0 · Tu entorno en VS Code (al inicio de S1, guiada, 25 min) — `00_preparacion_vscode_y_python.ipynb`

La instalación (Python, VS Code, carpeta del curso y `.venv`) se pide **por correo unos días antes**, con la guía del README. En clase, todos a la vez y con el profesor proyectando su pantalla, se **comprueba** y se rescata a quien no lo tenga.

| Min (dentro de S1) | Paso | Qué hace el alumno |
|---|---|---|
| 5–10 | Abrir la carpeta | VS Code → *File → Open Folder…* → `curso-python-finanzas` → *Trust the authors*. Quien no tenga la carpeta: *Download ZIP* desde el enlace que comparte el profesor |
| 10–20 | **Entorno y kernel** | Si no hay `.venv`: *Python: Create Environment → Venv → requirements.txt*. Abre `notebooks/00_…`, *Select Kernel → .venv* y ejecuta la celda 🩺. **Comprobación en voz alta:** todos con la 🩺 en ✅ |
| 20–30 | Notebooks y errores | Ejecutar, *Restart* y *Run All*; guardar con Ctrl+S; leer un `NameError` (secciones 3 y 7 del 00) |

- Las secciones 4–6 y 8 del 00 (calculadora, variables, f-strings y ejercicio de margen) se hacen como calentamiento si sobra tiempo. Si no, quedan como repaso para casa: el bloque 1 de S1 repite esos conceptos.
- **Por qué la carpeta completa del repositorio:** los notebooks tienen al lado sus datos y funciones, y lo que generan (el Excel y el PDF del cierre en S3) queda en el ordenador del alumno, donde lo abre con su Excel. Además, el alumno practica desde el primer día la idea de *repositorio* que se formaliza en S3 (Git en 15 min).
- **Quien no consiga instalar** (permisos, proxy…): que siga la sesión en Colab (plan B, enlace del README) y se resuelve con IT antes de S2.
- **Resultado:** al acabar, cada alumno tiene la carpeta del curso abierta en VS Code con el kernel `.venv` funcionando.

### S1 · Python para quien viene de Excel — `01_fundamentos_python.ipynb`

**Objetivo:** leer y escribir código Python básico con ejemplos financieros, y dar el primer paso con pandas.

| Min | Bloque | Contenido |
|---|---|---|
| 0–5 | Arranque | Presentación del caso; demo de 2 min del informe final para mostrar adónde vamos |
| 5–30 | **P0 guiado** | Comprobar el entorno en VS Code (carpeta, `.venv`, kernel), ejecutar y leer errores (ver P0) |
| 30–50 | Tipos y operaciones | Se abre `01` en VS Code y se ejecuta la ⚙️. `int`, `float`, `str`, `bool`; cuenta de resultados de una póliza (prima − siniestros − comisión); f-strings con formato de miles y %; por qué `0.1 + 0.2 != 0.3` y `round`/`math.isclose` |
| 50–70 | Colecciones y control de flujo | Listas y diccionarios como "filas" de una cartera mini; `for`, `if/elif/else` para clasificar pólizas rentables y no rentables; acumuladores |
| 70–80 | *Pausa* | |
| 80–100 | Funciones y módulos | `def margen_tecnico(...)`, valores por defecto y docstrings; `import math`, `datetime`; importar nuestras funciones de `src/`; buenas prácticas (nombres claros, no repetir código, una función hace una cosa) |
| 100–115 | Primer contacto con pandas | Leer el presupuesto en Excel (`header=2`); seleccionar, filtrar y sumar; chuleta Excel → pandas. El ejercicio de siniestralidad por canal puede terminarse en casa |
| 115–120 | Cierre | Ticket de salida: una cosa aprendida y una duda |

**Entregable:** función `cuenta_resultados(poliza)` probada sobre la cartera mini + total presupuestado por canal.

### S2 · De la cartera al resultado técnico: pandas, NumPy y visualización — `02_pandas_kpis_visualizacion.ipynb`

**Objetivo:** construir la cuenta técnica 2025 por canal y segmento a partir de datos brutos y comunicarla con gráficos.

| Min | Bloque | Contenido |
|---|---|---|
| 0–10 | Repaso | Pregunta diagnóstica de opción múltiple (media de ratios frente a cociente de sumas) |
| 10–35 | Carga, exploración y limpieza | `info`, `describe`, `value_counts`; tipos de dato; fechas; IDs mal formados en el dataset público (`'1e+05'`); valores extremos; NumPy vectorizado: exposición y **prima devengada** = prima anual × días cubiertos / 365 |
| 35–60 | Unir y calcular KPIs | Agregar siniestros por póliza; `merge` (= BUSCARV) con comisiones; **ingresos, costes, margen técnico**; ratios de siniestralidad, comisiones, gastos y ratio combinado; regla del cociente de sumas |
| 60–70 | *Pausa* | |
| 70–90 | Portafolios y segmentos | `groupby` por canal, zona, región; `pd.cut` para tramos de edad y bonus-malus; `pivot_table` canal × tramo; ¿dónde se pierde dinero? (conductores < 25 años con siniestralidad > 150 %) |
| 90–115 | Visualización | matplotlib/seaborn: barras de exposición con línea de siniestralidad, mapa de calor canal × edad, **cascada (waterfall) prima → margen**; plotly: treemap interactivo de margen por canal y región, exportado a HTML |
| 115–120 | Cierre | Demo de 5 min: "¿y si la cartera tuviera 50 M de filas?" → Parquet + DuckDB (se amplía en C1) |

**Entregable:** tabla de resultado técnico por canal y segmento + 3 gráficos exportados.

### S3 · Automatización del cierre mensual — `03_automatizacion_cierre_mensual.ipynb` + `scripts/run_report.py`

**Objetivo:** pasar de "3 días de copiar y pegar" a un proceso que se ejecuta con un comando, se valida solo y genera Excel, PDF y correos.

| Min | Bloque | Contenido |
|---|---|---|
| 0–10 | Repaso + demo | Ejecutar `run_report.py --periodo 2025-09` y ver lo que produce |
| 10–35 | Ficheros | `pathlib` y `glob`; leer 12 Excel con dos formatos (cambio de sistema en julio); función `normalizar_bordereau()`; números con formato español (`'1.234,56'`); `concat` |
| 35–55 | Validación y control | Duplicados, pólizas inexistentes, rangos, recobros negativos y **cuadre contra la hoja Resumen** (aparece el descuadre de septiembre); hoja "Controles" con OK/KO; `pandera` como versión profesional; `logging` |
| 55–65 | *Pausa* | |
| 65–85 | Real vs presupuesto | `melt` del presupuesto ancho; **reparto de gastos de estructura** por claves (nº de siniestros, pólizas, prima); cuenta de resultados por canal; desviaciones absolutas y %; semáforo |
| 85–105 | Salidas automáticas | Excel con `xlsxwriter` (formatos €, %, condicional, paneles fijos, gráfico nativo); PDF de una página con `fpdf2`; un **correo por responsable de canal** con su Excel adjunto, en modo simulacro (`.eml`) |
| 105–120 | Del notebook al proceso | `run_report.py` + `config/params.yaml`; estructura del proyecto; **Git en 15 min** (clone, commit, push, pull, rama; demo con GitHub Desktop); cómo programarlo (Programador de tareas de Windows) |

**Entregable:** carpeta `output/2025-09/` con Excel, PDF y 4 correos `.eml`.

### S4 · Estadística aplicada a la incertidumbre de costes — `04_estadistica_aplicada.ipynb`

**Objetivo:** dejar de reportar solo números puntuales y empezar a dar rangos defendibles para presupuesto y forecast.

| Min | Bloque | Contenido |
|---|---|---|
| 0–10 | Repaso | "El ratio de Bancaseguros es 56 % y el de Agentes 79 %. ¿Es una diferencia real?" |
| 10–35 | Distribuciones del coste | Número de siniestros: Poisson frente a binomial negativa, sobredispersión. Coste por siniestro: histograma en escala log, ajuste lognormal, gamma y Weibull con `scipy.stats` (`floc=0`), QQ-plot, AIC. Cola pesada: el 1 % de los siniestros más caros pesa un 38 % del coste |
| 35–55 | Simulación Monte Carlo | Coste anual = Σ de N siniestros; 10.000 escenarios → P50/P90/P99 para el presupuesto; **forecast de cierre de año** a partir del real acumulado a septiembre |
| 55–65 | *Pausa* | |
| 65–90 | Intervalos de confianza | Frecuencia (Poisson), coste medio (t), siniestralidad por canal; regla práctica ±2/√N; ¿cuántos siniestros hacen falta para fiarse de un ratio? |
| 90–110 | Bootstrap | `scipy.stats.bootstrap` (remuestreo de pólizas, `paired`); IC del ratio de siniestralidad por canal; diferencia Agentes − Corredores; cuándo falla (colas pesadas) |
| 110–120 | Cierre | Opcional: demo de 5 min del anexo C2 (IBNR) |

**Entregable:** tabla de KPIs con IC por canal + distribución simulada del coste 2026.

### S5 · Drivers de rentabilidad: GLM y segmentación — `05_glm_segmentacion.ipynb`

**Objetivo:** identificar qué características explican el coste, construir segmentos de rentabilidad y cuantificar cuánto margen se recuperaría con una tarifa mejor.

| Min | Bloque | Contenido |
|---|---|---|
| 0–10 | Repaso + intuición | La tarifa es una tabla de factores multiplicativos (como en Excel): prima = base × f₁ × f₂ × … |
| 10–45 | GLM de frecuencia | Poisson con *offset* de exposición (`statsmodels`); **relatividades** exp(β) con IC; nivel base; lectura de negocio |
| 45–60 | GLM de coste medio y prima pura | Gamma con enlace log ponderado por nº de siniestros; prima pura = frecuencia × coste medio; comparación con la tarifa actual |
| 60–70 | *Pausa* | |
| 70–90 | Segmentación | Árbol de decisión (criterio Poisson, peso de exposición mínimo por hoja) → reglas legibles; *tiers* de riesgo; **margen por tier**; k-means como contraste (agrupa parecidos, no rentables) |
| 90–110 | Validación y negocio | Train/test; curva de lift; Gini; **doble lift frente a la tarifa actual**; simulación: margen recuperado si se reprecian los segmentos deficitarios |
| 110–120 | Cierre del curso | Hoja de ruta, recursos y encuesta |

**Entregable:** tabla de relatividades + segmentos con su margen + estimación del impacto de repricing.

### C1 · Grandes volúmenes y SQL (autónomo, 60–90 min) — `C1_grandes_volumenes_sql.ipynb`

- `read_csv` eficiente (`usecols`, `dtype`, `chunksize`); CSV frente a **Parquet** (tiempo y tamaño).
- **DuckDB**: SQL directo sobre ficheros, más rápido que pandas y sin servidor.
- Bases de datos SQL: `sqlite3` + SQLAlchemy + `pd.read_sql` con **consultas parametrizadas** (y por qué no se usan f-strings); cadena de conexión típica a SQL Server.
- Polars (modo lazy) y cuándo tiene sentido Dask o PySpark (solo si ya hay Spark/Databricks).

### C2 · Reservas, IBNR e impacto en resultados (autónomo, 45 min) — `C2_reservas_chain_ladder.ipynb`

- Por qué el coste de siniestros del mes no es solo lo declarado: IBNR y provisiones.
- Triángulo de desarrollo en pandas; factores ponderados por volumen (otra vez cociente de sumas); IBNR.
- Paquete `chainladder`: Mack y bootstrap ODP → percentil 99,5 (enlace con Solvencia II).
- Back-test con datos reales del CAS: ¿cuánto acertó la reserva?

---

## 5. Dinámica de cada sesión

- **Live coding**: el instructor teclea y narra, y comete errores a propósito para enseñar a leer las trazas. Los alumnos siguen el mismo notebook.
- **Bloques de 20–25 min**: demo de 8–10 min seguida de ejercicio de 10–15 min con celda de comprobación (`✅ Correcto` / `❌ pista`).
- **Señal de ayuda**: un post-it rojo (o una reacción en Teams) significa "estoy atascado" y uno verde "he terminado". Así se detecta pronto a quien se queda atrás.
- **Ejercicios ⭐ opcionales** al final de cada bloque para quien vaya más rápido. Con esto se gestiona la heterogeneidad del grupo.
- **Soluciones** en `notebooks/soluciones/`, para consultar después de intentarlo.

## 6. Checklist logístico (antes de la sesión 1)

- [ ] Confirmar con IT que los alumnos **pueden instalar** Python 3.12 y VS Code (o que IT los instala) y que `python.org`, `pypi.org`, `files.pythonhosted.org`, `github.com` y el *marketplace* de VS Code (`marketplace.visualstudio.com`) son accesibles desde la red corporativa. Si hay **proxy**, pedir la configuración para `pip`. **Plan B:** Google Colab (requiere `colab.research.google.com` y una cuenta de Google).
- [ ] Publicar el repositorio en GitHub como **público** (ver README).
- [ ] Hacer la puesta en marcha del README en un **portátil corporativo limpio** (como el de un alumno): instalar, descargar el ZIP, crear `.venv`, ejecutar la 🩺 del 00 y la ⚙️ del 01.
- [ ] Ejecutar `python herramientas/verificar_notebooks.py` la semana anterior.
- [ ] Una semana antes, enviar un correo con el enlace a la guía *Puesta en marcha del alumno* del README: *instalad Python y VS Code, descargad la carpeta y cread el entorno; si algo falla, no pasa nada, lo resolvemos el primer día*.
- [ ] El día 1, tener a mano el enlace al repositorio (para el *Download ZIP*) y el enlace de Colab del 00 (plan B) para pegarlos en el chat.
- [ ] Recordar que en Colab (plan B) **solo se usan datos públicos o simulados**, nunca datos reales de la compañía.
