# Documento 3 · Caso de uso: FP&A del ramo Autos

> **Para el instructor.** Este documento describe el caso, los datos (con su origen y lo que es real o simulado), el recorrido paso a paso por sesión y las **cifras de referencia** para validar en clase. La sección 4 contiene *spoilers* (los problemas de calidad introducidos a propósito).

---

## 1. La historia

Somos el equipo de **FP&A del ramo de Autos (responsabilidad civil)** de una aseguradora. En 2025 la cartera tuvo **677.991 pólizas**, comercializadas por cuatro canales:

| Canal | Comisión | Perfil |
|---|---|---|
| Agentes | 15 % | Red exclusiva; el mayor volumen (≈ 43 % de las primas) |
| Corredores | 18 % | Corredurías independientes |
| Directo | 2 % | Web y teléfono; atrae a más conductores jóvenes |
| Bancaseguros | 20 % | Acuerdo de distribución con un banco |

Cada mes llega:
- Un **Excel de siniestros declarados** (*bordereau*) desde el sistema de siniestros. En julio se migró a un sistema nuevo y cambió el formato.
- El **presupuesto** anual por canal y mes.
- Los **gastos de estructura** reales por centro de coste, desde contabilidad analítica.
- La **cartera** de pólizas, extraída del sistema de emisión.

Dirección pregunta:
1. ¿Cuánto ganamos y dónde? (S2)
2. ¿Cómo vamos frente al presupuesto este mes? ¿Podemos tenerlo el día 3 sin tres días de copiar y pegar? (S3)
3. ¿Cuánto nos costará 2026 y dónde cerraremos 2025? ¿Son reales las diferencias entre canales? (S4)
4. ¿Qué segmentos destruyen valor y qué hacemos con el precio? (S5)
5. *(Complementarios)* ¿Y si los datos fueran 50 veces más grandes? (C1) ¿Cuánto nos falta por conocer de lo ya ocurrido? (C2)

---

## 2. Origen de los datos (qué es real y qué es simulado)

| Elemento | Origen | Real / simulado |
|---|---|---|
| Pólizas: características (edad, bonus-malus, zona, región, vehículo, densidad), exposición | **freMTPL2freq**: cartera francesa de RC Autos de una aseguradora privada, paquete R `CASdatasets` (Dutang & Charpentier), licencia GPL ≥ 2; espejo en OpenML (id 41214, CC0) | **Real** |
| Siniestros: número e importe por póliza | **freMTPL2sev** (OpenML 41215) | **Real** |
| Canal comercial | Asignado aleatoriamente (los menores de 30 años, con más peso en Directo) | Simulado |
| Fechas de efecto y vencimiento (dentro de 2025), coherentes con la exposición real | Simuladas | Simulado |
| Prima anual ("tarifa actual") | GLM sencillo con **solo 2 factores** (tramo de bonus-malus y zona), recargado para una siniestralidad objetivo del 70 %, con ajuste por canal y ruido del ±3 % | Simulado |
| Fecha de ocurrencia y de declaración de cada siniestro | Ocurrencia uniforme dentro de la cobertura; retraso de declaración con cola (el 3 % tarda entre 60 y 400 días) | Simulado |
| Bordereaux mensuales, presupuesto, gastos de estructura, comisiones | Generados a partir de lo anterior, **con problemas de calidad introducidos a propósito** | Simulado |
| Triángulos de reservas | **RAA** (clásico de la literatura) y **CAS Loss Reserving Database**, Schedule P autos particulares 1998–2007 (actualización de diciembre de 2025), extraídos del paquete `chainladder` 0.10.1 | **Real** |

**Por qué este diseño:**
- Los **riesgos e importes son reales**, con sus colas pesadas, picos de convenio, sobredispersión y variables de confusión (edad ↔ bonus-malus). Así, la estadística y los GLM encuentran patrones auténticos.
- La **capa financiera es simulada** para tener canales, calendario, presupuesto y gastos, que es el mundo de FP&A, sin usar datos de ninguna compañía real.
- La "tarifa actual" usa **a propósito solo 2 factores**, para que el GLM de la sesión 5 tenga margen de mejora demostrable.
- Todo se regenera con `python scripts/preparar_datos.py` (semilla fija = 2025, reproducible).

> Versión de los datos: usamos la versión de **CASdatasets** (677.991 pólizas y 26.444 siniestros, con las tablas de frecuencia y severidad consistentes entre sí). La versión de OpenML es ligeramente distinta (678.013 y 26.639).

---

## 3. Diccionario de datos

### `data/cartera/cartera_2025.parquet` (677.991 filas, una por póliza)

| Columna | Tipo | Descripción |
|---|---|---|
| `id_poliza` | int | Identificador de póliza (= IDpol original) |
| `canal` | str | Agentes / Corredores / Directo / Bancaseguros |
| `fecha_efecto`, `fecha_vencimiento` | fecha | Periodo de cobertura dentro de 2025 |
| `prima_anual` | float | Prima anualizada de la tarifa actual (€) |
| `zona` | str | A (rural) … F (centro urbano), según densidad |
| `region` | str | 22 regiones francesas (antiguas) |
| `potencia` | int | Potencia del vehículo (4–15) |
| `antig_vehiculo` | int | Antigüedad del vehículo (años; 100 = posible código de "desconocido") |
| `edad_conductor` | int | Edad del conductor (18–100) |
| `bonus_malus` | int | 50 = bonificación máxima; > 100 = malus |
| `marca` | str | Marca codificada (B1 … B14) |
| `combustible` | str | Diesel / Regular |
| `densidad` | int | Habitantes/km² del municipio |

### `data/referencia/siniestros_2025_maestro.parquet` (26.444 filas, una por siniestro)
`id_siniestro`, `id_poliza`, `fecha_ocurrencia`, `fecha_declaracion`, `canal`, `region`, `importe`, `estado`. Es el maestro **limpio**: lo que se reconstruye en la S3 a partir de los bordereaux (más los 957 siniestros declarados en 2026, que son el IBNR del C2).

### `data/entrada/bordereaux/siniestros_2025-MM.xlsx` (12 ficheros)
- Hoja **Detalle**: 3 filas de título, la cabecera en la fila 4, una fila vacía y una fila `TOTAL` al final.
  - Ene–jun (sistema antiguo): `Nº Siniestro`, `Nº Póliza`, `Fecha ocurrencia`, `Fecha declaración`, `Canal`, `Región`, `Importe (€)`, `Estado`. Fechas e importes numéricos.
  - Jul–dic (sistema nuevo): `N_SINIESTRO`, `N_POLIZA`, `F_OCURRENCIA`, `F_DECLARACION`, `CANAL`, `REGION`, `IMPORTE_EUR`, `ESTADO`. Fechas como texto `dd/mm/aaaa`, importes como texto `1.234,56` y estado en MAYÚSCULAS.
- Hoja **Resumen**: nº de siniestros e importe total según el sistema (para el cuadre).

### `data/entrada/presupuesto_2025.xlsx`
Título en la fila 1 y cabecera en la fila 3 (`header=2`). Formato **ancho**: `canal`, `concepto` (Primas devengadas, Coste de siniestros, Comisiones, Gastos de estructura), `Ene` … `Dic`, `Total`. Es un presupuesto algo optimista: primas un +2 % y siniestralidades objetivo del 60–70 %.

### `data/entrada/gastos_estructura_2025.xlsx`
`mes` (AAAA-MM), `centro_coste`, `partida` (Personal, Servicios externos, Alquileres y suministros, Amortizaciones), `importe`. En total, unos 11,05 M€ en 2025, un ≈ 12 % por encima de los 9,9 M€ presupuestados. Marketing digital tiene campañas en marzo y septiembre.

### `data/entrada/parametros/parametros_2025.xlsx`
- Hoja **Comisiones**: `canal`, `tasa_comision`, `descripcion`.
- Hoja **Claves_reparto**: `centro_coste`, `gasto_anual_presupuestado`, `clave_reparto` (`n_siniestros` / `n_polizas` / `prima_devengada` / `solo_directo`).

### `data/triangulos/`
- `raa.csv`: `anio_ocurrencia`, `desarrollo_meses`, `pagos_acumulados` (1981–1990).
- `cas_ppauto_1998_2007.csv`: `compania` (136), `anio_ocurrencia`, `desarrollo_meses` (12–120), `pagos_acumulados`, `incurrido`, `prima_devengada_neta` (miles de USD). Incluye el triángulo inferior, lo que permite hacer back-testing.

### `data/raw/`
`freMTPL2freq.parquet` y `freMTPL2sev.parquet` **tal cual vienen de la fuente**, con nombres originales en inglés e `IDpol` como texto (con valores tipo `'1e+05'`). Se usan para el ejercicio opcional de limpieza y como trazabilidad.

---

## 4. Problemas de calidad introducidos (⚠️ spoilers)

Listado completo en `data/referencia/problemas_introducidos.csv`.

| Problema | Dónde | Cuántos | Qué debe detectar / hacer el alumno |
|---|---|---|---|
| Cambio de formato de sistema | jul–dic | 6 ficheros | Mapa de columnas + conversión de importes y fechas |
| Filas de título, vacía y TOTAL | todos | 12 | `header=3` y filtrar las filas sin ID o con "TOTAL" |
| Canal con mayúsculas o espacios | todos | ~4 % de las filas | `.str.strip().str.title()` antes de validar |
| Siniestros duplicados | meses pares | 61 filas | `drop_duplicates("id_siniestro")` |
| Póliza inexistente (un "9" delante) | todos | 3 por mes (36) | Control de integridad: se mantienen y se reportan |
| Recobros (importes negativos) | marzo y octubre | 2 + 2 | Aviso (son legítimos) |
| Falta una línea en el detalle | **septiembre** | 1 siniestro (3.204 €) | **Cuadre contra la hoja Resumen → KO** |

---

## 5. Recorrido paso a paso

### Preparación (P0) — `00_preparacion_colab_y_python.ipynb`
Abrir Colab, ejecutar y reiniciar; variables y f-strings; un ejercicio de margen y ratio combinado de una póliza (margen 63,40 €; ratio combinado 89,8 %).

### Sesión 1 — `01_fundamentos_python.ipynb`
1. Cuenta de resultados de una póliza con variables y tipos.
2. Cartera mini de 6 pólizas (lista de diccionarios) → bucles y condicionales para clasificar la rentabilidad → "SUMAR.SI" a mano.
3. Funciones `margen_tecnico()`, `cuenta_resultados()` y `ratio_combinado()`; módulos; buenas prácticas.
4. pandas: leer el **presupuesto** (`header=2`), filtrar, crear columnas y agrupar; ejercicio: siniestralidad presupuestada por canal.

### Sesión 2 — `02_pandas_kpis_visualizacion.ipynb`
1. Cargar la cartera y los siniestros; `info`/`describe`; detectar los valores 100 en antigüedad y edad → `clip`.
2. Exposición y prima devengada vectorizadas (comparativa de tiempos frente a un bucle).
3. Agregar siniestros por póliza → `merge` con la cartera → `merge` con comisiones → reparto simple de gastos → margen por póliza.
4. Cuenta técnica por canal (cociente de sumas) y demostración de por qué la media de ratios es errónea.
5. Segmentos: zona, tramos de edad y bonus-malus, `pivot_table` canal × edad, top 5 regiones con peor margen.
6. Gráficos: exposición + siniestralidad, cascada prima → margen, heatmap, treemap interactivo de plotly (exportado a HTML).
7. Demo: DuckDB sobre Parquet.

### Sesión 3 — `03_automatizacion_cierre_mensual.ipynb` + `scripts/run_report.py`
1. Demo del producto final: `python scripts/run_report.py --periodo 2025-09`.
2. Leer los 12 bordereaux: diagnóstico con `header=None`, mapa de columnas, `a_numero()` (ejercicio), `normalizar_bordereau()`, consolidación (ejercicio).
3. Controles: duplicados, integridad, recobros, **cuadre** (ejercicio: detectar septiembre), tabla de controles, `pandera`, `logging`.
4. Presupuesto ancho → largo con `melt` (ejercicio); devengo mensual; reparto de gastos por claves; cuenta real vs presupuesto; discusión sobre la desviación de gastos de Directo.
5. Excel con formato (`xlsxwriter`), PDF (`fpdf2`) y un correo `.eml` por canal.
6. Script, configuración YAML, estructura del proyecto, Git y programación. Ejercicio: cierre de diciembre.

**Salida de `run_report.py --periodo 2025-09`** (`output/2025-09/`): `cierre_2025-09.xlsx` (hojas Resultado YTD, Resultado mes, Real vs Ppto YTD y Controles, con gráfico nativo), `cierre_2025-09.pdf` (una página), `por_canal/*.xlsx` (4), `correos/*.eml` (4) y `ejecucion.log`.

### Sesión 4 — `04_estadistica_aplicada.ipynb`
1. Frecuencia: Poisson frente a lo observado (sobredispersión).
2. Severidad: escala log, picos, peso de la cola; ajuste lognormal, gamma y Weibull; AIC frente a la media; QQ-plots; ejercicio P(X > 1 M€).
3. Monte Carlo del coste anual (lognormal frente a empírico) → P5/P50/P90/P99; forecast de cierre a septiembre; ejercicio P(siniestralidad > 75 %).
4. IC de frecuencia por canal (Garwood), regla ±2/√N, IC t del coste medio; ejercicio: jóvenes frente al resto.
5. Bootstrap de la siniestralidad por canal, diferencia Agentes − Corredores, `scipy.stats.bootstrap`; ejercicio: Agentes 18–25; límites del bootstrap.

### Sesión 5 — `05_glm_segmentacion.ipynb`
1. Univariante de edad frente a la tabla cruzada edad × bonus-malus (confusión).
2. GLM Poisson con *offset*: relatividades con IC; gráfico univariante frente a GLM; ejercicio: factor de la zona E y frecuencia de un perfil.
3. Carga por grandes siniestros; GLM Gamma (enlace log, `var_weights`); prima pura calibrada.
4. Árbol Poisson (reglas y gráfico) → margen por segmento; ejercicio: peor segmento; contraste con k-means.
5. Lift, Lorenz/Gini (GLM frente a la tarifa actual), doble lift, simulación de la tarifa neutral en ingresos con límite de ±25 %; ejercicio: dispersión de la siniestralidad entre segmentos.

### C1 — `C1_grandes_volumenes_sql.ipynb` (autónomo)
Cartera ×5 (3,4 M filas, ~300 MB en CSV): `usecols`/`dtype`, `chunksize`, Parquet, DuckDB, SQLite + SQLAlchemy, inyección SQL frente a consulta parametrizada, Polars lazy y Dask.

### C2 — `C2_reservas_chain_ladder.ipynb` (autónomo)
IBNR de la propia cartera → triángulo RAA → factores (ejercicio) → CDF, última y reserva → `chainladder`: Mack y bootstrap ODP → back-test con State Farm (CAS) (ejercicio).

---

## 6. Cifras de referencia (para validar en clase)

**Año 2025 completo, con todos los siniestros ocurridos** (vista de la S2, gastos repartidos por prima):

| Canal | Prima devengada | Coste siniestros | Siniestralidad | Ratio combinado | Margen técnico |
|---|---|---|---|---|---|
| Agentes | 36,21 M€ | 28,47 M€ | 78,6 % | 106,9 % | **−2,48 M€** |
| Corredores | 21,34 M€ | 14,35 M€ | 67,3 % | 98,5 % | 0,32 M€ |
| Directo | 17,43 M€ | 12,25 M€ | 70,3 % | 85,5 % | 2,53 M€ |
| Bancaseguros | 8,56 M€ | 4,83 M€ | 56,5 % | 89,7 % | 0,88 M€ |
| **Total** | **83,54 M€** | **59,91 M€** | **71,7 %** | **98,5 %** | **1,25 M€** |

Otros datos: exposición de 358.333 años-póliza; 26.444 siniestros; frecuencia de 7,38 %; coste medio de 2.266 €; comisiones de 11,33 M€; gastos de estructura de 11,05 M€.

**Segmentos (S2):** siniestralidad de 18–25 años = 181 % (Agentes 18–25: 365 %, con dos siniestros de 4,1 y 1,4 M€); zona B = 107 % (grandes siniestros).

**Cierre de septiembre, acumulado (S3)** (solo lo declarado, con reparto de gastos por claves): primas de 66,47 M€, margen de 3,51 M€, ratio combinado del 94,7 %, desviación del margen frente al presupuesto de **−2,24 M€**. Agentes queda en −1,30 M€ (RC 104,5 %). Hay 15 controles KO y 1 aviso (el cuadre de septiembre falla por −3.204 €).

**Cierre de diciembre (S3, ejercicio 5.1):** margen técnico de **2.976.102 €**. La diferencia con los 1,25 M€ de la S2 se debe casi entera a los **1,72 M€ de IBNR** (siniestros de 2025 declarados en 2026), que el cierre por declarados no ve (→ C2). Hay que comentarlo.

**S4:** el 1 % de los siniestros más caros suma el 38 % del coste. La lognormal (mejor AIC) da una media de 1.781 € frente a 2.266 € reales. Las simulaciones infravaloran el coste anual en ~13 M€. Frecuencia de 18–25 años: IC [0,142; 0,154] frente a [0,069; 0,071] del resto. Diferencia de siniestralidad Agentes − Corredores: +11 pp, con un IC al 95 % de aproximadamente [−9 %, +39 %] (incluye el 0).

**S5:** relatividades GLM de frecuencia: 18–25 = 0,97 (no significativo), 26–35 = 0,67, BM > 100 = 7,6, zona E = 1,26. Severidad: 18–25 = 1,30 [1,13; 1,50]. Carga por grandes siniestros: 1,215. Árbol: el segmento BM > 90 destruye ~7,8 M€. Gini en test: GLM ≈ 0,27 frente a tarifa ≈ 0,24. Dispersión de la siniestralidad entre segmentos: 32,6 % → 28,4 %.

**C2:** RAA: reserva de 52.135; error estándar de Mack de 26.881; P99,5 bootstrap ≈ 2,1 veces la media. State Farm: error de la reserva total del chain-ladder = −2,5 %.

> Las cifras de la S4 y la S5 que dependen de simulación o de la partición train/test pueden variar ligeramente si se cambian las semillas.

---

## 7. Ideas para ampliar el caso
- **Presupuesto 2026**: usar la S4 (Monte Carlo) y la S5 (nuevas relatividades) para proponer primas y costes por canal, con rango de confianza.
- **Informe trimestral para el Consejo**: reutilizar `informes.py` con un PDF de 3 páginas.
- **Elasticidad**: simular bajas según la subida de precio en la tarifa nueva de la S5.
- **Reaseguro**: un *excess of loss* sobre 500 k€; ¿cuánto cambia la volatilidad del resultado (S4)?
- **Dashboard**: llevar la tabla de real vs presupuesto a Streamlit o Power BI.
