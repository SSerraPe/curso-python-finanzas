# Documento 2 · Notas técnicas para el instructor

Notas de apoyo para impartir cada sesión. Para cada bloque se indica **qué explicar**, **las fórmulas o los conceptos exactos**, **los errores típicos de los alumnos** y **los mensajes clave**. El código de referencia completo está en `notebooks/soluciones/` (ejecutados, con salidas) y en `src/curso_seguros/`.

> **Hilo conductor:** el principio del **cociente de sumas**. Un ratio de un grupo se calcula como Σ numerador / Σ denominador, que equivale a la media de los ratios individuales **ponderada** por el denominador. Aparece en los KPIs (S2), los repartos (S3), el bootstrap del ratio (S4), los pesos del GLM (S5), el procesamiento por trozos (C1) y los factores de desarrollo (C2). Merece la pena nombrarlo cada vez que aparezca.

---

## Índice
- [0. Entorno y compatibilidad](#0-entorno-y-compatibilidad)
- [S1. Fundamentos de Python](#s1-fundamentos-de-python)
- [S2. pandas, NumPy, KPIs y visualización](#s2-pandas-numpy-kpis-y-visualización)
- [S3. Automatización del cierre](#s3-automatización-del-cierre)
- [S4. Estadística aplicada](#s4-estadística-aplicada)
- [S5. GLM y segmentación](#s5-glm-y-segmentación)
- [C1. Grandes volúmenes y SQL](#c1-grandes-volúmenes-y-sql)
- [C2. Reservas y chain-ladder](#c2-reservas-y-chain-ladder)
- [Guía de Git para el equipo](#guía-de-git-para-el-equipo)
- [Glosario financiero-actuarial](#glosario-financiero-actuarial)
- [Preguntas frecuentes de los alumnos](#preguntas-frecuentes-de-los-alumnos)
- [Referencias](#referencias)

---

## 0. Entorno y compatibilidad

**Colab, octubre de 2026** (ver informe de investigación): runtime con Python 3.12–3.13, **pandas 2.2**, numpy 2.x, statsmodels 0.14–0.15, scikit-learn, matplotlib, seaborn, plotly 5.x, duckdb 1.3, polars 1.x, dask y SQLAlchemy 2.x preinstalados. **No** vienen XlsxWriter, fpdf2 ni pandera. Los instala `requirements-colab.txt` desde la celda de arranque.

**pandas 3.0** (enero de 2026) ya es la versión estable en PyPI. Todo el código del curso funciona en **pandas 2.2 y 3.0**. Reglas que seguimos y que conviene explicar cuando surjan:

| Evitar | Usar | Motivo |
|---|---|---|
| `df["a"][mask] = 0` (asignación encadenada) | `df.loc[mask, "a"] = 0` | Con *Copy-on-Write* (por defecto en pandas 3) la asignación encadenada **no modifica** `df` |
| `ser[0]` para "el primero" | `ser.iloc[0]` | En pandas 3, `[]` es siempre por etiqueta |
| `applymap`, `fillna(method="ffill")` | `DataFrame.map`, `.ffill()` | Eliminados en pandas 3 |
| `groupby` por categóricas sin `observed` | `groupby(..., observed=True)` | Cambia el valor por defecto en pandas 3 |
| `dtype == object` para detectar texto | `pd.api.types.is_string_dtype` | En pandas 3 el texto es `str` por defecto |
| `freq="M"` | `freq="ME"` | Alias renombrados |

**`chainladder` 0.10.1** exige pandas ≥ 2.3.3: al instalarlo, Colab actualiza pandas y **hay que reiniciar** el entorno. La celda de arranque de C2 lo hace sola: instala, reinicia, y el alumno vuelve a ejecutar la celda.

**Gobernanza:** en Colab se usan **solo** datos públicos o simulados. Si IT bloquea Colab, el plan B es Anaconda o VS Code en local con `requirements.txt`. Los notebooks detectan si están en Colab o en local y funcionan en ambos.

**Antes del curso:** ejecuta `python herramientas/verificar_notebooks.py` (en local) **y** abre y ejecuta cada notebook en Colab la semana anterior.

### La copia del curso en el Drive de cada alumno

GitHub es la fuente de **solo lectura**. El primer día (P0, al inicio de S1) cada alumno **copia el repositorio entero en su Google Drive** (`Mi unidad › curso-python-finanzas`) y a partir de ahí abre siempre los notebooks desde su Drive. Así se resuelven tres problemas a la vez: el trabajo del alumno no se pierde, los notebooks tienen al lado sus datos y su `src/`, y lo que generan (el Excel y el PDF de S3) queda guardado.

| Celda | Dónde | Qué hace |
|---|---|---|
| 📥 Copia el curso | notebook 00, sección 2 | Monta Drive, clona el repositorio en `/content` (`--depth 1`) y copia **todo menos `.git`** a `MyDrive/curso-python-finanzas`. Si la carpeta ya existe, **no toca nada** |
| ⚙️ Prepara el entorno | primera celda de 01–05, C1 y C2 | Monta Drive y se sitúa en la copia del alumno. Si no la encuentra, avisa y clona una copia **temporal** en `/content` para no bloquear la clase. Instala `requirements-colab.txt` |
| 🔄 Actualizar mi copia | notebook 00, sección 9 | Descarga la última versión y sobrescribe `config/`, `data/`, `docs/`, `herramientas/`, `scripts/`, `src/`, `notebooks/soluciones/` y los requirements. Añade los notebooks que falten. **Nunca sobrescribe un notebook de alumno que ya exista** |

- **Por qué no se usa Git dentro de Drive:** Git sobre el disco montado de Drive es lento y a veces deja el repositorio a medias. Clonar en `/content` y copiar es más robusto, y la actualización no necesita `.git`.
- **Por qué no un *fork* en GitHub:** obliga a que cada alumno tenga cuenta de GitHub y no resuelve dónde se guarda su trabajo en Colab. El *fork* y el *pull request* se explican en S3 (Git en 15 min), cuando ya tiene sentido.
- **Si corriges algo a mitad de curso:** `git push` y pide que ejecuten la celda 🔄. Si el cambio es en un notebook de alumno, la celda 🔄 no lo pisa. Diles que abran la versión nueva desde GitHub (*Open in Colab*) o que borren su notebook antes de pulsar 🔄.
- La ruta `MyDrive` es la misma aunque Drive esté en español (*Mi unidad*).

---

## S1. Fundamentos de Python

### P0 guiado (minutos 5–30) · La copia del curso
- **Proyecta tu pantalla con una cuenta "de alumno"** (no la tuya de profesor), para que lo que ven coincida con lo que tú ves.
- Pega en el chat el enlace *Open in Colab* del 00 y avanzad **paso a paso, esperando a todos**: post-it verde cuando la celda 📥 diga ✅.
- **Ventanas que van a salir** (avísalas antes): *"Este notebook no es de Google"* → *Ejecutar de todos modos*; *"¿Permitir acceso a Google Drive?"* → *Conectar* → elegir cuenta → *Permitir*. Si alguien desmarca permisos en la pantalla de Google, el montaje falla: repetir y aceptarlos todos.
- **Comprobación clave:** cuando todos hayan abierto su copia, pregunta *"¿alguien ve el botón «Copiar en Drive» arriba?"*. Quien lo vea sigue en la versión de GitHub y sus cambios se perderán.
- **Problemas típicos:**
  - *"Abrir con" no muestra Colab* en drive.google.com → usar *Archivo → Abrir cuaderno → Google Drive* desde Colab (siempre funciona).
  - *Cuenta corporativa que bloquea Drive en Colab* → que use una cuenta personal de Google (los datos son públicos o simulados) o el plan B en local.
  - *Ha ejecutado la 📥 dos veces* → no pasa nada, la segunda no toca la copia.
  - *Ha movido o renombrado la carpeta* → devolverla a *Mi unidad* con el nombre `curso-python-finanzas`. Si la ha estropeado: renombrarla (p. ej. `…_viejo`) y volver a ejecutar la 📥.
- **Mensaje:** *"GitHub es el original del profesor; vuestra carpeta de Drive es vuestro cuaderno. En S3 veremos que esto mismo, con control de versiones, es Git."*

### Bloque 1 · Tipos y operaciones
- **Tipado dinámico**: el tipo lo lleva el valor, no la variable. `type()` para inspeccionar.
- `int` / `float` / `str` / `bool`. Conversiones: `float("1250.75")`. `int(3.99)` **trunca** (= 3) y `round(3.99)` redondea (= 4).
- **Redondeo bancario**: `round(2.5) == 2` y `round(3.5) == 4` (redondeo al par, norma IEEE). Excel redondea "hacia arriba" desde .5. Si alguien lo detecta, se explica así; para importes con redondeo comercial existe `decimal.Decimal` con `ROUND_HALF_UP`.
- **Coma flotante**: `0.1 + 0.2 != 0.3` porque 0,1 no tiene representación binaria exacta. A Excel le pasa lo mismo, pero lo disimula mostrando 15 dígitos. **Regla para cuadres:** `math.isclose(a, b, abs_tol=0.01)`.
- **f-strings**: `f"{x:,.2f}"` (miles con coma y 2 decimales), `f"{r:.1%}"` (porcentaje), `f"{s:<13}"` (alinear). El separador de miles es `,` (formato anglosajón). Para formato español en informes se usa `.replace` o se formatea en Excel.

### Bloque 2 · Colecciones y control de flujo
- **Lista** `[]`: ordenada y mutable, indexada desde **0**. Un *slice* `[a:b]` incluye `a` y excluye `b`. `-1` es el último elemento.
- **Diccionario** `{clave: valor}`: búsqueda por clave. `d.get(k, 0)` evita el `KeyError`.
- **Lista de diccionarios** = tabla: es el puente mental hacia el DataFrame.
- **Indentación**: define los bloques; 4 espacios. Es el `IndentationError` más común al copiar y pegar.
- **Acumuladores** (`total += x`) y **agrupación manual** con diccionario: sirve para mostrar qué hace `groupby` por dentro.
- *List comprehension*: solo como ⭐. No hay que insistir.

### Bloque 3 · Funciones, módulos y buenas prácticas
- Anatomía: `def`, argumentos posicionales y con nombre, **valores por defecto**, docstring y `return`. Sin `return`, la función devuelve `None`.
- ⚠️ Nunca usar un valor por defecto **mutable** (`def f(x=[])`): la lista se comparte entre llamadas. Mencionarlo solo si alguien lo pregunta.
- Módulo = fichero `.py`; paquete = carpeta con `__init__.py`; `pip install` instala paquetes de terceros. El curso importa `curso_seguros` porque la celda de arranque añade `src/` a `sys.path`.
- **Buenas prácticas (PEP 8)**: `snake_case`, `CONSTANTES`, funciones cortas que hacen una sola cosa, comentarios sobre el *porqué*, nada de números mágicos ni credenciales en el código. Mensaje: **"si lo copias por tercera vez, conviértelo en función"**.

### Bloque 4 · Primer contacto con pandas
- `DataFrame` (tabla) frente a `Series` (columna con índice). El **índice** es la etiqueta de las filas (no confundir con el número de fila de Excel).
- `read_excel(header=2)`: la cabecera está en la 3.ª fila del fichero porque pandas cuenta desde 0.
- Filtros booleanos: `df[cond]`. Condiciones combinadas con `&`, `|` y `~`, **cada una entre paréntesis**.
  - Error típico: `df[df.a > 1 and df.b < 2]` → `ValueError: The truth value of a Series is ambiguous`. Se arregla con `&` y paréntesis.
- `sum(axis=1)` suma por filas; `axis=0` (por defecto) suma por columnas.

**Mensaje de cierre S1:** Python es más verboso que una fórmula de Excel, pero es **legible, repetible y auditable**.

---

## S2. pandas, NumPy, KPIs y visualización

### Definiciones de KPIs (tabla para proyectar)

| KPI (es) | Inglés | Fórmula (para un grupo) | Comentario |
|---|---|---|---|
| Prima emitida | Written premium | Σ prima anual de las pólizas emitidas en el periodo | Base para comisiones en muchos contratos |
| **Prima devengada** (imputada) | Earned premium | Σ prima anual × fracción del periodo cubierta | **El ingreso contable** del periodo |
| **Exposición** | Exposure | Σ días cubiertos / 365 (años-póliza) | La unidad de riesgo |
| **Frecuencia** | Claim frequency | Σ nº siniestros / Σ exposición | Siniestros por año-póliza |
| **Coste medio / severidad** | Severity | Σ coste / Σ nº siniestros | |
| **Prima pura / burning cost** | Pure premium | Σ coste / Σ exposición = frecuencia × coste medio | Coste esperado por póliza-año |
| **Siniestralidad** | Loss ratio | Σ coste siniestros / Σ prima devengada | |
| Ratio de gastos | Expense ratio | (comisiones + gastos) / prima devengada | Por convención histórica, las comisiones a veces van sobre prima emitida |
| **Ratio combinado** | Combined ratio | siniestralidad + ratio de gastos | > 100 % = pérdida técnica |
| **Margen técnico** | Technical result | prima − siniestros − comisiones − gastos | Sin resultado financiero |

Fuente de las definiciones: Werner & Modlin, *Basic Ratemaking* (CAS), cap. 1. Terminología española: AHERAS/UCM, *Introducción a la tarificación en seguros No Vida*.

### Cociente de sumas: la demostración (1 minuto en la pizarra)
Con $r_i = c_i / p_i$:

$$\frac{\sum_i c_i}{\sum_i p_i} = \sum_i \frac{p_i}{\sum_j p_j}\, r_i \neq \frac{1}{n}\sum_i r_i$$

El ratio del grupo es la media de los ratios **ponderada por el denominador**. El notebook enseña el caso extremo: pólizas con 3 días de exposición y un siniestro dan "siniestralidades" de miles de por cien, y la media simple se dispara. Equivalente en Excel: `SUMAR.SI.CONJUNTO / SUMAR.SI.CONJUNTO`, nunca `PROMEDIO.SI.CONJUNTO` sobre una columna de ratios.

### Exploración y limpieza
- Checklist de exploración: `shape`, `info()` (tipos y nulos), `describe()` (rangos), `value_counts()` (categorías), `duplicated()` (claves), integridad entre tablas (`isin`).
- Rarezas reales del dataset público (merece la pena contarlas, porque son verosímiles):
  - `antig_vehiculo` y `edad_conductor` llegan hasta **100**, un código típico de "desconocido". Se limitan con `clip` y la decisión se **documenta**.
  - Importes con **picos** en 1.204 € y 1.128,12 € (importes fijos del convenio francés IRSA-IDA).
  - **Cola pesada**: el 1 % de los siniestros más caros suma el 38 % del coste; el mayor supera los 4 M€.
  - En el fichero original de CASdatasets (`data/raw/`), `IDpol` es texto con valores como `'1e+05'`. Hay que convertirlo con `astype(float).astype("int64")` antes de cruzar las tablas. Es un ejercicio ⭐ opcional.
- **Vectorización**: las operaciones entre columnas se ejecutan en C sobre arrays de NumPy, del orden de 100 a 1.000 veces más rápido que un bucle Python (el notebook lo mide). `np.where` es el SI vectorizado y `np.select` el SI anidado.
- **Prima devengada** = prima anual × días en vigor en el periodo / 365. En la S3 se calcula mes a mes con `clip` sobre las fechas: `(min(venc, fin_mes) − max(efecto, ini_mes)).days`, con mínimo 0.

### Uniones (`merge`)
- `how="left"` conserva la tabla principal; las filas sin pareja quedan con `NaN`, que se rellenan con 0 solo si **significan** 0 (sin siniestros = coste 0).
- `validate="one_to_one"` o `"many_to_one"`: protege contra claves duplicadas, que **multiplican filas** sin avisar. Es el error más caro de un BUSCARV mal hecho.
- `indicator=True` añade la columna `_merge` (`both` / `left_only` / `right_only`), útil para controles.
- Antes de unir siniestros (una fila por siniestro) con la cartera (una fila por póliza) hay que **agregar** los siniestros por póliza.

### Agrupación por portafolios
- *Named aggregation*: `.agg(nombre=("col", "func"))`, legible y sin `MultiIndex`.
- `pd.cut` para tramos (límites cerrados por la derecha por defecto) y `pd.qcut` para cuantiles.
- `pivot_table(index, columns, values, aggfunc="sum")`. Para ratios, pivota **numerador y denominador** y divide después.
- **Mensaje de negocio S2:** Agentes es el único canal en pérdidas; los 18–25 años y la zona B destacan. Antes de concluir hay que mirar si los explican **unos pocos siniestros grandes**: en Agentes 18–25 lo explican dos siniestros de 4,1 y 1,4 M€. Eso deja planteada la S4.

### Visualización
- **API orientada a objetos** de matplotlib (`fig, ax = plt.subplots()`): mejor que `plt.plot` en cuanto hay más de un gráfico.
- **Principios:** el título cuenta la conclusión; nada de tartas con más de 3 categorías; doble eje solo cuando las dos magnitudes se interpretan juntas (exposición + ratio, el gráfico clásico actuarial); el color, con significado (rojo = pérdidas).
- **Waterfall** (cascada) de prima a margen: el gráfico favorito de FP&A. Se construye con barras apiladas sobre una base acumulada.
- **seaborn** `heatmap(annot=True, fmt=".0%")` para tablas canal × segmento.
- **plotly**: `px.treemap`, `px.sunburst`, `px.bar`. Con `fig.write_html()` se obtiene un HTML autónomo para enviar por correo. Para cuadros de mando "de verdad", el siguiente paso sería Power BI o Streamlit/Dash (fuera de alcance).

---

## S3. Automatización del cierre

### Diseño del proceso (lo que hay que transmitir)
```
Entradas (no se tocan a mano) → Normalizar → Validar → Calcular → Presentar → Distribuir
data/entrada/                    función    controles   src/       Excel/PDF   .eml
```
Principios: **idempotencia** (ejecutarlo dos veces da lo mismo), **trazabilidad** (log y hoja de controles), **parametrización** (el periodo y los destinatarios en `config/params.yaml`) y **una sola fuente de lógica** (`src/`, compartida por notebooks y scripts).

### Ficheros
- `pathlib.Path`: rutas portables; `/` para unir; `.glob("*.xlsx")`, `.stem`, `.suffix`, `.stat().st_size`.
- `pd.read_excel(sheet_name=None)` devuelve un dict con **todas** las hojas. `header=N` y `usecols` para quitar el ruido.
- Patrón **"normalizar"**: una función por tipo de fichero que devuelve siempre el mismo esquema (nombres de columna, tipos). Cuando el sistema cambia (julio), se añade una entrada al `MAPA_COLUMNAS` y nada más.
- **Números con formato español** (`'1.234,56'`): primero se quitan los puntos de miles y después se cambia la coma por punto. El orden importa. Para CSV: `pd.read_csv(sep=";", decimal=",", thousands=".")`.
- **Fechas** en texto: `pd.to_datetime(format="%d/%m/%Y")`. Hay que dar siempre el formato explícito, porque `dayfirst` sin formato puede confundir 03/04 con 4 de marzo.

### Validación y control

| Tipo | Implementación | Decisión de tratamiento en el caso |
|---|---|---|
| Duplicados | `df.duplicated(subset=clave)` | Eliminar (`drop_duplicates`) y reportar |
| Nulos en campos obligatorios | `df[cols].isna().sum()` | Bloquear si los hay |
| Integridad referencial | `~df.id.isin(maestro.id)` | **Mantener** (el coste es real) y reportar a Siniestros |
| Rangos | `(x < min) | (x > max)` | Recobros negativos = **aviso**, no error |
| Cuadre con totales de control | `math.isclose(calc, esperado, abs_tol=0.01)` | Septiembre: KO por −3.204 €, hay que investigar |
| Dominio | `set(valores) - set(validos)` | Normalizar mayúsculas y espacios antes de validar |

- **`pandera`** (0.34): `import pandera.pandas as pa` (el import de nivel superior está obsoleto para pandas); `DataFrameSchema` + `Column` + `Check`; `validate(df, lazy=True)` reúne **todos** los fallos en `e.failure_cases`. Great Expectations es demasiado pesado para este público.
- **`logging`** frente a `print`: niveles (INFO/WARNING/ERROR), fecha y hora, y salida a fichero (`ejecucion.log`). En un proceso desatendido el log es la única evidencia de lo que pasó.

### Real vs presupuesto
- **Formato largo** (una fila por canal × concepto × mes) para calcular, y **ancho** para presentar. `melt` (= "anular dinamización" de Power Query) y `pivot_table` son operaciones inversas.
- **Signos**: se guardan los costes en positivo y se calcula el margen como ingresos − costes. Una desviación es **favorable** si sube el ingreso o el margen o si baja el coste.
- **Reparto de gastos de estructura** (contabilidad analítica): cada centro de coste se reparte con su clave (nº siniestros, pólizas en vigor, prima, 100 % a un canal). Implementación: tabla de drivers en formato largo → `groupby().transform("sum")` para los pesos → `merge` con los gastos.
- **Caso para discutir:** la desviación de gastos de **Directo** (+86 %) no es una mala gestión, sino que el presupuesto repartió por prima y el real imputa Marketing digital al 100 % a Directo. **Las desviaciones dependen del criterio de reparto.** Es una conversación muy típica de FP&A.

### Salidas
- **XlsxWriter** (para crear libros nuevos): `workbook.add_format({"num_format": '#,##0 "€";[Red]-#,##0 "€"'})`, `set_column`, `freeze_panes`, `autofilter`, `conditional_format` (semáforos) y `add_chart` (gráficos **nativos** de Excel, que el destinatario puede editar). **openpyxl** sirve para *modificar* una plantilla corporativa existente. **xlwings** necesita Excel instalado, así que no funciona en Colab.
- **fpdf2**: Python puro, ideal para Colab. ⚠️ Las fuentes estándar del PDF no tienen el **€**, así que se registra una TTF (DejaVu viene con matplotlib: `matplotlib.get_data_path()/fonts/ttf`). Tablas con `pdf.table()` e imágenes PNG de matplotlib. Alternativa para informes complejos: plantilla HTML + Jinja2 + WeasyPrint.
- **Correo**: `email.message.EmailMessage` + `add_attachment`; `bytes(msg)` → fichero `.eml` (Outlook lo abre). **Siempre en modo simulacro primero.**
  - Desde Colab no se puede enviar: Google Cloud bloquea el puerto 25 saliente.
  - En la empresa: **Microsoft Graph** (`sendMail`, OAuth) o Outlook con `win32com` (Windows). Microsoft está retirando la autenticación básica SMTP en Exchange Online (según fuente secundaria, desactivada por defecto a finales de 2026; conviene confirmarlo con IT).

### Del notebook al script
- `if __name__ == "__main__":` + `argparse` (parámetros como `--periodo 2025-09`) + `yaml.safe_load` para la configuración + `logging` a fichero + código de salida (0 = OK, 1 = error).
- **Programación**: Programador de tareas de Windows (acción: `python.exe` con el script como argumento y "Iniciar en" la carpeta del proyecto). En servidor: cron, Airflow, Azure Data Factory o GitHub Actions.
- **papermill** permite ejecutar un notebook parametrizado como si fuera un script; útil, pero preferimos `.py` para producción.
- **Secretos**: variables de entorno (`os.environ["SMTP_PASS"]`), ficheros `.env` (excluidos en `.gitignore`) o el gestor de secretos corporativo.

---

## S4. Estadística aplicada

### Frecuencia
- **Poisson**: $P(N=k) = e^{-\lambda}\lambda^k / k!$, con $E[N] = Var[N] = \lambda$. Con exposición, $\lambda_i = \text{frecuencia} \times e_i$.
- **Sobredispersión**: si $Var > E$ (heterogeneidad entre pólizas), la Poisson subestima la probabilidad de 2 o más siniestros. En el notebook hay 1.298 pólizas con 2 siniestros frente a 713 esperadas. La **binomial negativa** ($Var = \mu + \mu^2/k$) lo recoge. En un GLM, la Poisson "cuasi" o sobredispersa da los mismos coeficientes con errores estándar ajustados por $\hat\phi = \chi^2_{Pearson}/(n-p)$.

### Severidad
- Candidatas: lognormal, gamma, Weibull y, para la cola, Pareto/Lomax o la Pareto generalizada (GPD) por encima de un umbral.
- `scipy.stats.<dist>.fit(x, floc=0)`: máxima verosimilitud con la localización fijada en 0. **Sin `floc=0`**, el optimizador mueve la localización y produce ajustes absurdos.
- **Parametrizaciones** (fuente habitual de errores al pasar a Excel):
  - `lognorm(s, loc, scale)`: `s` = σ y `scale` = $e^{\mu}$. En Excel, `DISTR.LOGNORM(x; μ; σ; VERDADERO)` con μ = `ln(scale)`.
  - `gamma(a, loc, scale)`: forma `a` y escala θ (media = aθ). En Excel, `DISTR.GAMMA(x; a; θ; VERDADERO)`.
- **AIC** = 2k − 2 ln L (k = parámetros libres; con `floc=0`, k = 2).
- **El hallazgo didáctico del notebook:** la lognormal gana por AIC pero da una media de **1.781 €** frente a **2.266 €** reales (−21 %), porque no capta la cola. La gamma por MLE reproduce exactamente la media muestral (propiedad de su ecuación de verosimilitud), aunque ajusta peor la forma. Mensaje: **el modelo se valida con las métricas que importan al negocio** (media y cuantiles altos), no solo con el AIC.
- **QQ-plot** en escala log-log: los puntos de la derecha por encima de la diagonal significan una cola más pesada que la del modelo.
- **Tests de bondad de ajuste**: con 26.000 datos, KS y AD rechazan cualquier modelo paramétrico. Además, si los parámetros se estiman con los mismos datos, los p-valores clásicos de KS no son válidos (`scipy.stats.goodness_of_fit` lo corrige por Monte Carlo). Mensaje: el p-valor responde a "¿hay alguna diferencia detectable?", no a "¿el modelo sirve?".

### Monte Carlo (modelo colectivo)
$$S = \sum_{j=1}^{N} X_j,\quad N \sim \text{Poisson}(\lambda),\quad X_j \text{ iid}$$
$$E[S] = \lambda E[X], \qquad Var[S] = \lambda E[X^2]$$
- Se puede simular la severidad con un modelo ajustado o **remuestreando los importes empíricos**. El empírico conserva los picos y la cola, pero no genera nada mayor que el máximo observado. Para colas largas y en serio se usa *splicing*: cuerpo empírico o lognormal + cola GPD.
- Resultados del notebook: la lognormal infravalora el coste anual en unos 13 M€ frente al empírico. Hay que presentar **P50, P90 y P99**. El P99,5 a un año es la métrica de Solvencia II.
- **Forecast de cierre**: real a la fecha + simulación de la exposición pendiente. Se comunica como rango ("con un 80 % de confianza, entre X e Y").

### Intervalos de confianza
- **Frecuencia (exacto de Garwood)**, con N siniestros y exposición E:
  $$\left[\tfrac{1}{2E}\chi^2_{2N,\,\alpha/2},\ \tfrac{1}{2E}\chi^2_{2(N+1),\,1-\alpha/2}\right]$$
  Implementado en `curso_seguros.kpis.ic_frecuencia`.
- **Aproximación normal** y regla de bolsillo: $\hat\lambda \pm 1.96\sqrt{N}/E$. La **precisión relativa** es ≈ ±2/√N y **solo depende del número de siniestros** (100 → ±20 %, 1.000 → ±6 %). Es la introducción natural a la **credibilidad** (el estándar clásico de credibilidad total, 1.082 siniestros, corresponde a ±5 % con un 90 % de confianza).
- **Coste medio**: intervalo t, $\bar x \pm t_{n-1}\, s/\sqrt n$. Con colas pesadas es optimista (la convergencia al normal es lenta).
- **Siniestralidad** (cociente): método delta o bootstrap.

### Bootstrap
- Remuestrear con reemplazo la **unidad independiente**, que aquí es la **póliza** (no el siniestro: remuestrear siniestros ignora la variabilidad del número de siniestros). Recalcular el estadístico y tomar los percentiles 2,5 y 97,5.
- `scipy.stats.bootstrap(data, statistic, paired=True, vectorized=False, method=...)`. El método por defecto es **BCa** con 9.999 remuestras. BCa necesita un *jackknife* (n reevaluaciones), que es inviable con cientos de miles de filas, así que con datos grandes se usa `method="percentile"`.
- **Diferencia entre canales**: bootstrap independiente de cada canal y resta. En el notebook, el IC de Agentes − Corredores incluye el 0, así que **no hay evidencia suficiente** de que Agentes sea peor. La frecuencia de los jóvenes, en cambio, es claramente distinta (IC sin solape).
- **Cuándo falla**: con colas muy pesadas (varianza infinita o casi), poca muestra y estadísticos extremos (máximos, cuantiles altos). El bootstrap no genera valores mayores que el máximo observado (Athreya, 1987; Knight, 1989).
- **Comparaciones múltiples**: si se comparan 20 segmentos, uno saldrá "significativo" por azar al 95 %. Conviene mencionarlo si surge.

---

## S5. GLM y segmentación

### El modelo
- Tres componentes: **distribución** de la familia exponencial (Poisson, Gamma, Tweedie…), **predictor lineal** $\eta = X\beta$ y **enlace** $g(\mu) = \eta$.
- Con **enlace log**, $\mu = e^{\beta_0} \prod_k e^{\beta_k x_k}$: el modelo es **multiplicativo** y $e^{\beta}$ es la **relatividad** frente al nivel base. Es la tabla de factores de la tarifa.
- **Frecuencia:** Poisson con *offset* $\ln(e_i)$:
  $\ln E[N_i] = \ln e_i + X_i\beta$.
  Equivale a modelizar la tasa $N_i/e_i$ con **peso** $e_i$ (CAS Monograph 5, §2.6). Así es como lo hace scikit-learn, que no admite *offset*: `PoissonRegressor().fit(X, y=N/e, sample_weight=e)`.
- **Severidad:** Gamma con enlace log sobre el coste medio por póliza, con `var_weights` = nº de siniestros.
  - ⚠️ En statsmodels el enlace por defecto de la Gamma es el **inverso**: hay que pasar `links.Log()`.
  - ⚠️ `freq_weights` ≠ `var_weights`: el primero trata la fila como N observaciones idénticas (infla la significación); para medias se usa el segundo.
- **Prima pura** = frecuencia × severidad, o directamente una **Tweedie** (compuesta Poisson-Gamma, potencia 1 < p < 2, típicamente 1,5–1,8).
- **Nivel base**: el de **mayor exposición** (no el primero alfabético). Un nivel base pequeño infla los errores estándar de todos los demás (Monograph 5, §2.4.3). En la fórmula: `C(var, Treatment('36-50'))`.
- **Variables continuas**: en el curso se agrupan en tramos (interpretables, como en una tarifa). Alternativas avanzadas: splines o GAM.
- **Grandes siniestros**: se limitan (aquí a 100 k€ por siniestro) para estimar los factores y el exceso se reparte como **carga** (aquí 1,215). Si no se hace así, un siniestro de 4 M€ "decide" el factor de un segmento entero.

### El hallazgo del caso (para contar con calma)
1. **Univariante**: los 18–25 años tienen el **doble de frecuencia** (factor 2,0).
2. **GLM**: controlando el **bonus-malus**, el factor de 18–25 es ≈ 0,97 y **no significativo**. Los jóvenes no tienen bonificación (empiezan en BM 100), y la tarifa actual **ya cobra el bonus-malus**: su frecuencia "extra" ya está pagada.
3. **GLM de severidad**: los siniestros de los jóvenes son **un 30 % más caros** (IC 13–50 %) y además concentran los siniestros de varios millones. **Ese** es el sobrecoste que la tarifa no recoge.
4. **26–35 años**: factor 0,67. Tienen un tercio menos de siniestros de lo que su BM sugiere, así que están **sobretarifados**: es un segmento donde se puede crecer bajando precio.

Es el ejemplo de manual de **variables de confusión**: el análisis variable a variable lleva a la decisión equivocada.

### Árboles y segmentación
- `DecisionTreeRegressor(criterion="poisson")` con `y = N/e` y `sample_weight = e`. `min_weight_fraction_leaf` garantiza **segmentos creíbles** (`min_samples_leaf` ignora los pesos). `max_depth=3` limita a ≤ 8 segmentos explicables.
- `export_text` da reglas trasladables a Excel o al sistema de suscripción, y `arbol.apply(X)` la hoja (segmento) de cada póliza.
- Resultado del caso: el segmento **BM > 90** tiene una frecuencia de ~0,22 (3 veces la media) y destruye unos **7,8 M€** de margen. En el extremo contrario, BM bajo, densidad baja y vehículo de más de 12 años tienen una siniestralidad de ~34 %.
- **k-means**: no supervisado, agrupa por parecido y no por riesgo. Separa la frecuencia 2,6 veces frente a 6,5 del árbol. Sirve para describir perfiles de cliente, no para tarificar.

### Validación
- **Train/test** (80/20) por póliza. Con varios años de datos, mejor validar **fuera de tiempo** (entrenar con 2023–24 y validar con 2025).
- **Devianza Poisson** media (`sklearn.metrics.mean_poisson_deviance`). Solo es comparable dentro del mismo *pipeline* (mismos recortes y la misma partición); los valores publicados para freMTPL2 (0,594, 0,458, 0,375…) no se comparan entre sí.
- **Curva de lift**: deciles de **igual exposición** ordenados por la predicción; observado frente a predicho.
- **Gini / curva de Lorenz**: mide la capacidad de **ordenar** el riesgo. No mide la calibración, así que siempre va acompañado de un control del total predicho frente al real. En el caso, el GLM obtiene un Gini de ~0,27 frente a ~0,24 de la tarifa actual: una mejora moderada, lo realista.
- **Doble lift**: deciles del ratio prima modelo / prima actual. Si en los deciles altos la siniestralidad con la tarifa actual es alta, el modelo detecta infratarificación.
- **D² y expectativas**: en freMTPL2 el modelo explica poco a nivel de póliza individual (D² de frecuencia ≈ 0,04 y de severidad ≈ 0,004 en el ejemplo de scikit-learn) y aun así **calibra bien el total y ordena el riesgo**. Mensaje: el valor está en los agregados y en la ordenación, no en "predecir cada póliza".

### Simulación de negocio
- Tarifa **neutral en ingresos** (misma prima total, redistribuida) con cambios limitados a ±25 %. La siniestralidad por segmento se **homogeneiza**: la dispersión ponderada entre segmentos pasa del ~33 % al ~28 % en test.
- **Supuesto fuerte**: sin bajas por subida de precio. En la realidad hay que modelizar la elasticidad (retención y conversión), que es otro proyecto, y respetar las restricciones regulatorias (en la UE no se puede tarificar por género, entre otras).

### statsmodels frente a scikit-learn

| | statsmodels (`smf.glm`) | scikit-learn (`PoissonRegressor`…) |
|---|---|---|
| Errores estándar, p-valores, IC | ✅ | ❌ |
| Fórmulas (`C(var, Treatment(...))`) | ✅ | ❌ (requiere one-hot) |
| Offset | ✅ `offset=` / `exposure=` | ❌ → `sample_weight` + tasa |
| Regularización por defecto | No | **Sí** (`alpha=1.0`): poner `alpha=0` para el GLM clásico |
| Pipelines y validación cruzada | Manual | ✅ |
| Recomendado para | **Explicar** (relatividades) | **Predecir** a escala, comparar con boosting |

---

## C1. Grandes volúmenes y SQL
- **Memoria**: `memory_usage(deep=True)`. Texto repetido → `category`; enteros → `int16`/`int32`; decimales → `float32` (con cuidado con importes). Con `usecols` + `dtype` la memoria baja unas 20 veces en el notebook.
- **`chunksize`**: se agregan **sumas y conteos** por trozo y se combinan; las medias se calculan al final (cociente de sumas). Medianas y percentiles no se pueden combinar por trozos (hacen falta algoritmos aproximados, o DuckDB).
- **Parquet**: columnar, comprimido y tipado. En el notebook ocupa 6 veces menos y lee 2 columnas unas 8 veces más rápido. Se convierte una vez y se trabaja siempre con el Parquet.
- **DuckDB**: SQL sobre CSV, Parquet y DataFrames sin servidor, multinúcleo y *out-of-core*. Es la herramienta por defecto recomendada para FP&A (el SQL ya es conocido). El benchmark PDS-H de Polars (mayo de 2025, del propio fabricante) a escala SF-100 da DuckDB 19,7 s, Polars 23,9 s, PySpark 312 s, Dask 549 s y pandas sin memoria. ⚠️ DuckDB 2.0 está previsto para el 21 de octubre de 2026: conviene fijar `duckdb<2`.
- **SQL desde Python**: SQLAlchemy 2.x `create_engine` + `pd.read_sql(text(sql), engine, params={...})`. **Nunca f-strings con valores externos** (inyección SQL; el notebook lo demuestra con `' OR '1'='1`). Para SQL Server: `mssql+pyodbc://@SERVIDOR/BD?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes`.
- **Polars** (modo lazy, `scan_parquet` → `collect`): muy rápido, con una API distinta de pandas. Polars 2.0 (6 de octubre de 2026) trae cambios: conviene fijar `<2` durante el curso.
- **Dask** (API tipo pandas, paralelismo) y **PySpark** (clústeres). Spark solo tiene sentido si la empresa ya usa Databricks o Fabric.

---

## C2. Reservas y chain-ladder
- **Provisión de siniestros** = pagos futuros esperados por siniestros ya ocurridos (declarados pendientes + IBNR). Su variación forma parte del coste del periodo, así que una reserva corta **infla el resultado de hoy**.
- En la cartera simulada, el 3,6 % de los siniestros de 2025 (2,9 % del coste) se declara en 2026, con un retraso medio de 169 días.
- **Triángulo**: filas = año de ocurrencia; columnas = desarrollo (meses); valores = pagos (o incurridos) **acumulados**.
- **Factores ponderados por volumen** (cociente de sumas): $f_j = \sum_i C_{i,j+1} / \sum_i C_{i,j}$ sobre los años con ambos valores. **CDF** $= \prod_{k \ge j} f_k$. **Última** = último conocido × CDF. **Reserva** = última − pagado.
- RAA (resultado verificado con el paquete): reserva **52.135**; error estándar de Mack **26.881** (52 %); bootstrap ODP (5.000 simulaciones): media ≈ 53.800 y **P99,5 ≈ 2,1 veces la media**.
- **Mack (1993)**: error estándar sin supuestos de distribución. **Bootstrap ODP** (England & Verrall, 2002): distribución completa. Enlace con Solvencia II: el SCR de reservas se calibra al P99,5 a un año.
- **Back-test** con la CAS Loss Reserving Database (actualización de diciembre de 2025, ocurrencias 1998–2007 con triángulo inferior). ⚠️ Las columnas cambiaron respecto a los ficheros clásicos de Meyers–Shi (1988–1997): `IncurLoss_B` → `IncurredLosses`. Los notebooks antiguos no funcionan con los nuevos ficheros.
- Paquete `chainladder` 0.10.1 (licencia MPL-2.0, apoyado por la CAS): `cl.Triangle(df, origin, development, columns, cumulative=True)`, `cl.Chainladder()`, `cl.MackChainladder()`, `cl.BootstrapODPSample(n_sims)`.

---

## Guía de Git para el equipo

**Analogía:** Git es el *control de cambios* de una carpeta entera; un *commit* es una versión con comentario; un *pull request* es "enviar a revisión y firma".

**Flujo mínimo diario** (GitHub Desktop o el panel de control de código de VS Code):
1. **Pull** (traer lo último) antes de empezar.
2. Trabajar. Para algo que no sea trivial, crear una **rama** (`feature/informe-trimestral`).
3. **Commit** con un mensaje que explique el *porqué*: "Añade control de cuadre contra Resumen", no "cambios".
4. **Push** y abrir un **pull request**; un compañero revisa y aprueba (*merge*).

**Comandos equivalentes:** `git clone URL` · `git pull` · `git switch -c rama` · `git add .` · `git commit -m "..."` · `git push` · `git log --oneline` · `git restore fichero` (descartar cambios locales).

**Qué no se sube nunca:** datos confidenciales, `output/`, `.env` y contraseñas. Tampoco las **salidas de los notebooks**, que pueden llevar cifras reales: hay que instalar `nbstripout` (`pip install nbstripout && nbstripout --install`) para que Git las elimine automáticamente.

**Estructura de proyecto recomendada** (la de este repositorio, inspirada en *cookiecutter-data-science* v2): `config/`, `data/` (con `entrada/` inmutable), `notebooks/` numerados, `src/<paquete>/`, `scripts/`, `output/` (ignorado), `requirements.txt`, `README.md`. Herramientas modernas que vale la pena conocer: `uv` (entornos e instalación rápida) y `ruff` (estilo y errores).

---

## Glosario financiero-actuarial

| Término | Significado breve |
|---|---|
| Prima emitida / devengada (imputada) | Facturada en el periodo / correspondiente al riesgo cubierto en el periodo |
| Prima no consumida (PPNC) | Parte de la prima emitida que corresponde a periodos futuros (pasivo) |
| Exposición | Años-póliza en vigor |
| Siniestralidad (loss ratio) | Coste de siniestros / prima devengada |
| Ratio combinado | Siniestralidad + gastos (incluidas comisiones) / prima |
| Bordereau | Listado periódico de siniestros o de primas (habitual con intermediarios y reaseguro) |
| Recobro | Importe recuperado de un tercero o de otra aseguradora |
| IBNR | Siniestros ocurridos y no declarados |
| Chain-ladder | Método de proyección de triángulos de desarrollo |
| Bonus-malus | Sistema de descuentos o recargos según la siniestralidad histórica del conductor |
| Relatividad | Factor multiplicativo de tarifa respecto a un nivel base |
| IFRS 17: CSM | Margen contractual de servicio: beneficio no devengado de un grupo de contratos |
| IFRS 17: LRC / LIC | Pasivo por cobertura restante / pasivo por siniestros ocurridos |
| Solvencia II: mejor estimación | Media ponderada por probabilidad de los flujos futuros, descontada (art. 77) |
| Solvencia II: SCR | Capital para soportar una pérdida 1 en 200 años (VaR 99,5 % a 1 año) |

---

## Preguntas frecuentes de los alumnos

- **"¿Por qué no lo hago en Excel/Power Query?"** Power Query es estupendo para transformar datos. Python añade estadística, modelos, automatización completa (PDF, correos, programación), control de versiones y escala. Además, conviven: Python genera el Excel final.
- **"¿Puedo usar esto con los datos de la empresa?"** En Colab, **no**. En local (Anaconda/VS Code), con las herramientas aprobadas por IT, sí.
- **"Me sale `ModuleNotFoundError: curso_seguros`."** No se ha ejecutado la celda ⚙️ de preparación (o se reinició la sesión). Hay que ejecutarla de nuevo.
- **"La celda ⚙️ dice que no encuentra mi copia y usa una temporal."** O no se ha hecho la copia (celda 📥 del notebook 00), o la carpeta no está en *Mi unidad* con el nombre `curso-python-finanzas`, o no se aceptó el permiso de Drive. Mientras tanto se puede seguir la clase, pero lo que se genere se perderá al cerrar.
- **"He perdido lo que hice en el ejercicio."** Seguramente trabajaba en la versión de GitHub (se ve el botón *Copiar en Drive*). A partir de ahora, abrir siempre desde Drive.
- **"¿Tengo que volver a copiar el curso cada sesión?"** No. La copia se hace una vez. Cada sesión basta con abrir el notebook desde Drive y ejecutar la ⚙️.
- **"Me sale `FileNotFoundError`."** Lo mismo: la carpeta de trabajo no es la raíz del curso.
- **"¿Por qué mi resultado no coincide exactamente con la solución?"** Las celdas de comprobación toleran pequeñas diferencias de decimales; si sale ❌, la pista indica el error conceptual más probable (normalmente, media de ratios frente a cociente de sumas).
- **"¿Cuándo uso pandas, DuckDB o Polars?"** pandas por defecto. DuckDB si se piensa en SQL o los datos no caben en memoria. Polars si se quiere máxima velocidad con sintaxis de DataFrame.
- **"¿Un GLM es machine learning?"** Es un modelo estadístico clásico. Comparte técnicas de validación con el ML (train/test, lift). Su ventaja es la **interpretabilidad**: cada factor se puede explicar a Dirección y al regulador.

---

## Referencias
- Werner, G. & Modlin, C. *Basic Ratemaking*. Casualty Actuarial Society.
- Goldburd, M., Khare, A., Tevet, D. & Guller, D. *Generalized Linear Models for Insurance Rating*. CAS Monograph 5, 2.ª ed. (rev. 2025).
- Wüthrich, M. & Merz, M. *Statistical Foundations of Actuarial Learning and its Applications*. Springer, 2023 (acceso abierto).
- Noll, A., Salzmann, R. & Wüthrich, M. *Case Study: French Motor Third-Party Liability Claims*. SSRN 3164764.
- scikit-learn: *Tweedie regression on insurance claims* y *Poisson regression and non-normal loss* (ejemplos oficiales con freMTPL2).
- Mack, T. (1993). *Distribution-free calculation of the standard error of chain ladder reserve estimates*. ASTIN Bulletin.
- England, P. & Verrall, R. (2002). *Stochastic claims reserving in general insurance*. BAJ.
- Zumstein, F. *Python for Excel*. O'Reilly.
- The Carpentries, *Instructor Training* (live coding, faded examples, ejercicios de Parsons).
- Tutoriales de la Asociación Suiza de Actuarios: https://www.actuarialdatascience.org
- Documentación oficial: pandas (*Comparison with spreadsheets*), statsmodels, SciPy, DuckDB, XlsxWriter, fpdf2, pandera, chainladder-python.
- Informe completo de la investigación previa: `docs/investigacion/Informe de investigación.md`.
