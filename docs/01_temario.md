# Documento 1 · Temario rediseñado

**Curso:** Python aplicado a Finanzas (FP&A) en una aseguradora
**Formato:** 5 sesiones × 2 h + preparación previa autónoma + 2 módulos complementarios autónomos
**Público:** equipo de administración y planeación financiera (FP&A). Dominan Excel y no han programado en Python
**Entorno:** Google Colab, con notebooks que se abren desde GitHub y no requieren instalación

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

### P0 · Preparación previa (autónoma, 45–60 min) — `00_preparacion_colab_y_python.ipynb`

- Abrir un notebook desde GitHub en Colab y guardar una copia en el Drive propio.
- Ejecutar celdas, reiniciar y ejecutar todo, y saber qué hacer cuando sale un error.
- Python mínimo: variables, números, texto, `print` y f-strings.
- **Resultado:** el día 1 nadie pierde 20 minutos configurando.

### S1 · Python para quien viene de Excel — `01_fundamentos_python.ipynb`

**Objetivo:** leer y escribir código Python básico con ejemplos financieros, y dar el primer paso con pandas.

| Min | Bloque | Contenido |
|---|---|---|
| 0–10 | Arranque | Presentación del caso; demo de 2 min del informe final para mostrar adónde vamos; normas del notebook |
| 10–35 | Tipos y operaciones | `int`, `float`, `str`, `bool`; cuenta de resultados de una póliza (prima − siniestros − comisión); f-strings con formato de miles y %; por qué `0.1 + 0.2 != 0.3` y `round`/`math.isclose` |
| 35–55 | Colecciones y control de flujo | Listas y diccionarios como "filas" de una cartera mini; `for`, `if/elif/else` para clasificar pólizas rentables y no rentables; acumuladores |
| 55–65 | *Pausa* | |
| 65–90 | Funciones y módulos | `def margen_tecnico(...)`, valores por defecto y docstrings; `import math`, `datetime`; importar nuestras funciones de `src/`; buenas prácticas (nombres claros, no repetir código, una función hace una cosa) |
| 90–115 | Primer contacto con pandas | Leer el presupuesto en Excel (`header=2`); seleccionar, filtrar y sumar; chuleta Excel → pandas |
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

- [ ] Confirmar con IT que `colab.research.google.com`, `github.com` y `pypi.org` son accesibles desde la red corporativa y que hay cuenta de Google utilizable. **Plan B:** Anaconda o VS Code en local con `requirements.txt`.
- [ ] Publicar el repositorio en GitHub (público, o privado con acceso de los alumnos) y sustituir `REPO_URL` en la celda de arranque de cada notebook (ver README).
- [ ] Ejecutar todos los notebooks en Colab la semana anterior (Colab cambia versiones de librerías sin avisar).
- [ ] Enviar P0 una semana antes y pedir que lo completen.
- [ ] Recordar que en Colab **solo se usan datos públicos o simulados**, nunca datos reales de la compañía.
