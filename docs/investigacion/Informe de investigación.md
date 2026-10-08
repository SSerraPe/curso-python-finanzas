# freMTPL2 vertebra un curso de Python asegurador

El curso debería construirse sobre **un único hilo conductor, la cartera pública de autos francesa freMTPL2 (678.013 pólizas, OpenML 41214/41215)**, y cada bloque debería terminar en una tabla exportada a Excel. Así, los cinco módulos de 2 h avanzan como un solo caso de pricing no vida y no como una colección de temas sueltos. La secuencia recomendada empieza por los fundamentos de pandas con KPIs actuariales. Sigue con la automatización (Excel, PDF, email, controles), la estadística aplicada (ajuste frecuencia/severidad, intervalos y bootstrap) y los GLM con segmentación. Cierra con una sesión de escalado y productivización (DuckDB/Polars/SQL, estructura de proyecto, Git, programación de ejecuciones) que incluye un anexo de 20 minutos de chain-ladder sobre triángulos que vienen dentro del paquete `chainladder`. La decisión técnica más importante es enseñar a agregar KPIs como **cociente de sumas y no como media de cocientes**. Ese principio conecta la frecuencia, la siniestralidad, los pesos de los GLM y los factores de desarrollo del chain-ladder. La decisión operativa más importante es que Colab sigue con pandas 2.2 en octubre de 2026 mientras el upstream va por pandas 3.0, Polars 2.0 y, en breve, DuckDB 2.0. Por eso los notebooks deben fijar versiones e instalar explícitamente lo que falta. Hay que contar con dos limitaciones. Diez horas no bastan para todo el temario sin un notebook previo autónomo de Python básico. Y en una aseguradora como Zurich solo pueden usarse datos sintéticos o públicos en Colab, así que hay que confirmar con IT antes de la primera sesión que Colab, GitHub y PyPI son accesibles.

## Diez horas exigen un hilo conductor y un notebook cero

No existe un temario de referencia publicado por IFoA, SOA o CAS para enseñar Python al personal financiero (no actuarial) de una aseguradora. Los referentes abiertos más cercanos son materiales actuariales construidos sobre el mismo dataset:

- los tutoriales de la Asociación Suiza de Actuarios en actuarialdatascience.org, cuyo Tutorial 1 analiza freMTPL con notebooks en R y Python ([ADS Tutorials](https://www.actuarialdatascience.org/ADS-Tutorials/));
- el ejemplo completo de pricing Poisson/Gamma/Tweedie de scikit-learn ([scikit-learn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html));
- los tutoriales del paquete `chainladder`, respaldado por la CAS ([chainladder](https://chainladder-python.readthedocs.io/stable/getting_started/tutorials/stochastic-tutorial.html)).

Los tiempos propuestos aquí son, por tanto, criterio de diseño y no un estándar contrastado. La SAA tiene además eventos presenciales en Zúrich, como "Fit4AI compact" el 19–20 de noviembre de 2026, una posible continuación para los alumnos más avanzados ([ADS](https://www.actuarialdatascience.org/ADS-Tutorials/)).

El temario pedido abarca nueve áreas en 10 horas lectivas. Para que quepa hacen falta tres decisiones de diseño:

- **Un notebook 0 autónomo (60–90 minutos) antes del curso.** Cubre tipos, listas, diccionarios, funciones, f-strings y el manejo de Colab. Así la sesión 1 puede dedicarse directamente a pandas.
- **Un único dataset durante todo el curso.** La carga cognitiva se gasta en conceptos nuevos y no en entender cada vez un esquema distinto.
- **Un anexo, no una sesión, para la parte técnicamente más densa.** El chain-ladder y las equivalencias statsmodels/scikit-learn van como notebooks autónomos con solo una demo en clase.

El orden pone la automatización en la sesión 2 y no al final, porque es lo que el personal financiero usará el lunes siguiente. Las Carpentries insisten en que "cualquier técnica puede fracasar si los alumnos no están motivados" ([Carpentries](https://carpentries.github.io/instructor-training/aio.html)).

| Sesión | Tema | Bloques (minutos) | Entregable Excel/PDF |
|---|---|---|---|
| 0 (autónoma) | Python mínimo y Colab | Tipos, colecciones, funciones, "Reiniciar y ejecutar todo" | — |
| 1 | pandas/numpy, KPIs y visualización | 0–10 demo "informe mensual en un clic" y reglas de datos · 10–40 lectura, filtros, `merge` como BUSCARV, `pivot_table` · 40–70 carga y unión de freMTPL2, limpieza · 70–80 pausa · 80–110 exposición, frecuencia, severidad, prima pura por segmento y gráficos · 110–120 cierre | Tabla de KPIs por Area/Region/tramo de BonusMalus |
| 2 | Automatización y reporting | 10–40 Excel desordenado de entrada → informe con XlsxWriter · 40–70 controles (hoja "Controles", pandera) · 80–110 PDF con fpdf2 y emails `.eml` por línea de negocio, con logging | Informe formateado, PDF y borradores de correo |
| 3 | Estadística aplicada | 10–45 severidad: histograma log, MLE con `floc=0`, AIC, QQ · 45–60 frecuencia y sobredispersión · 70–105 IC Poisson, t, método delta, bootstrap y cuándo falla · 105–120 ejercicio | Tabla de ajustes y de IC por segmento |
| 4 | GLM y segmentación | 0–10 tarifa multiplicativa · 10–45 GLM Poisson con offset · 45–60 Gamma y Tweedie · 70–90 árbol Poisson y tiers · 90–110 lift, doble lift, Gini · 110–120 exportar relatividades | Tabla de relatividades con IC |
| 5 | Escalar y productivizar | 10–35 Parquet, DuckDB, Polars · 35–50 SQL parametrizado · 50–75 estructura, uv, Git · 85–95 `run_report.py`, papermill, programador de tareas · 95–115 anexo chain-ladder · 115–120 cierre | Informe mensual reproducible e IBNR con incertidumbre |

Cada sesión sigue la plantilla de 120 minutos de las Carpentries:

- repaso inicial con una pregunta de opción múltiple diagnóstica, en la que cada respuesta errónea apunta a un error conceptual concreto;
- bloques con demo en *participatory live coding*: el instructor teclea, narra y comete y corrige errores delante del grupo;
- *faded examples*: ejemplos resueltos a los que se van quitando partes;
- *Parsons problems*: reordenar líneas de código dadas;
- *sticky notes* en la pausa;
- un "uno arriba, uno abajo" de feedback al cierre.

Todo ello está recogido en el material de formación de instructores de las Carpentries ([Carpentries](https://carpentries.github.io/instructor-training/aio.html)). Para que los notebooks funcionen sin instructor, cada concepto tiene cinco celdas:

1. explicación en castellano con la equivalencia Excel ("En Excel harías… / En pandas…");
2. ejemplo resuelto;
3. celda con huecos `___`;
4. ejercicio;
5. celda de comprobación con `assert` y una pista.

Las comprobaciones deben ser tolerantes con decimales y tipos (`np.isclose`) para que las soluciones alternativas correctas también pasen, y las soluciones van en un notebook aparte. La página oficial de pandas "Comparison with spreadsheets" sirve de chuleta para BUSCARV, tablas dinámicas y filtros ([pandas](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_spreadsheets.html)).

## Colab necesita fijar versiones porque va un ciclo por detrás

El runtime 2026.07 de Colab trae **Python 3.12.13, pandas 2.2.2, numpy 2.0.2, duckdb 1.3.2, polars 1.35.2, statsmodels 0.14.6 y openpyxl 3.1.5** ([backend-info pip-freeze](https://github.com/googlecolab/backend-info/blob/ec53f93fe44a9cab118dc5451527b18e36e1a643/pip-freeze.txt)). La rama principal del repositorio ya muestra Python 3.13.16 sobre Ubuntu 24.04 con pandas 2.2.3, scipy 1.16.3 y statsmodels 0.15.0 ([pip-freeze main](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt); [os-info](https://github.com/googlecolab/backend-info/blob/main/os-info.txt)). El runtime puede cambiar entre la preparación y la impartición del curso. Conviene probar los notebooks la semana anterior y explicar cómo elegir un runtime anterior en *Entorno de ejecución → Cambiar tipo → Versión*, que sigue disponible alrededor de un año ([Colab FAQ](https://research.google.com/colaboratory/runtime-version-faq.html)).

El upstream va claramente por delante:

- pandas 3.0.6;
- Polars 2.0.0, publicado el 6 de octubre de 2026;
- DuckDB 1.5.6, con **DuckDB 2.0 previsto para el 21 de octubre de 2026** ([PyPI pandas](https://pypi.org/project/pandas/); [Polars 2.0](https://github.com/pola-rs/polars/releases/tag/py-2.0.0); [DuckDB release calendar](https://duckdb.org/release_calendar.html)).

Varias librerías que el curso necesita **no vienen preinstaladas** en Colab: XlsxWriter, fpdf2, pandera, papermill, pyodbc y weasyprint ([pip-freeze main](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt)). Por eso la primera celda de cada notebook debe instalar con versión fijada, por ejemplo `%pip install -q xlsxwriter fpdf2 pandera "duckdb==1.5.*" "polars<2"`, seguida de un `git clone` del repositorio del curso para tener `data/` sin depender de Google Drive. Los alumnos abren los notebooks con el patrón `colab.research.google.com/github/<org>/<repo>/blob/<rama>/<ruta>.ipynb` o con la insignia "Open in Colab" ([Colab GitHub demo](https://github.com/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb)).

pandas 3.0 rompe idiomas que aún aparecen en muchos tutoriales ([pandas 3.0 what's new](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html); [v3.0.0.rst](https://github.com/pandas-dev/pandas/blob/main/doc/source/whatsnew/v3.0.0.rst)):

- Copy-on-Write está siempre activo, así que la asignación encadenada `df["a"][mask] = 0` deja de modificar `df`;
- el tipo de texto por defecto pasa a ser `str`;
- `applymap` y `fillna(method=)` desaparecen;
- los alias `M`/`Q`/`Y` se sustituyen por `ME`/`QE`/`YE`;
- `ser[0]` pasa a ser siempre acceso por etiqueta;
- `groupby(observed=True)` es el nuevo valor por defecto;
- `to_excel` ya no aplica estilos.

Los notebooks deben escribirse para que funcionen igual en 2.2 (Colab) y en 3.0 (el portátil futuro del alumno). Las reglas son: escribir siempre con `.loc[mask, col] = …`, usar `.iloc` para posiciones, usar alias `ME`, `DataFrame.map`, `.ffill()` y `pd.api.types.is_string_dtype`. La pérdida de estilos en `to_excel` es, de hecho, un buen puente pedagógico hacia XlsxWriter.

El paquete `chainladder` 0.10.1 exige **pandas ≥ 2.3.3 y numpy ≥ 2.0** ([PyPI chainladder](https://pypi.org/pypi/chainladder/json)). Eso choca con el pandas 2.2 de Colab: instalarlo actualizará pandas y probablemente obligará a reiniciar el entorno. Por eso el anexo de reservas debe vivir en **un notebook independiente** cuya primera celda sea `%pip install -q chainladder==0.10.1` con la instrucción explícita de reiniciar.

La gobernanza también condiciona el diseño. Los administradores de Google Workspace pueden desactivar Colab por organización o por grupo ([Google Workspace Admin Help](https://knowledge.workspace.google.com/admin/users/access/turn-google-colab-on-or-off-for-users)). Colab procesa los datos fuera del perímetro de la aseguradora, así que el curso solo debe usar datos públicos o sintéticos, y la sesión 1 debe decirlo expresamente. Las alternativas razonables si Colab no está disponible son VS Code con un entorno uv en el portátil corporativo o JupyterLite en el navegador, aunque esta última pierde red y SMTP.

## freMTPL2 da un caso de pricing completo, salvo la prima

### Qué contiene y cómo cargarlo

**freMTPL2freq (OpenML 41214)** tiene 678.013 filas y 12 columnas sin valores perdidos:

- `IDpol`, identificador de póliza;
- `ClaimNb`, número de siniestros;
- `Exposure`, exposición en años;
- `Area`, de A (rural) a F (centro urbano);
- `VehPower`, `VehAge` y `VehBrand`, potencia, antigüedad y marca del vehículo;
- `DrivAge`, edad del conductor;
- `BonusMalus`, entre 50 y 350 (por debajo de 100 es bonificación);
- `VehGas`, tipo de combustible;
- `Density`, habitantes/km² del municipio;
- `Region`, 22 regiones.

**freMTPL2sev (OpenML 41215)** contiene 26.639 filas de siniestros con `IDpol` y `ClaimAmount` ([OpenML 41214](https://www.openml.org/api/v1/json/data/41214); [OpenML qualities](https://www.openml.org/api/v1/json/data/qualities/41214); [OpenML 41215](https://www.openml.org/api/v1/json/data/41215)). Los datos proceden de una aseguradora privada no identificada, cubren aproximadamente 2011–2013, y parte de los importes son **cantidades fijas del convenio francés IRSA-IDA** ([CASdatasets freMTPL.Rd](https://raw.githubusercontent.com/dutangc/CASdatasets/master/man/freMTPL.Rd)).

Las licencias no coinciden: OpenML los publica como CC0, pero el paquete R original CASdatasets es GPL ≥ 2 ([CASdatasets DESCRIPTION](https://raw.githubusercontent.com/dutangc/CASdatasets/master/DESCRIPTION)). Para formación interna no es un problema práctico, pero conviene citar ambas fuentes.

La carga recomendada es `fetch_openml(data_id=41214, as_frame=True)`, con el mismo patrón que usa scikit-learn ([sklearn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html)). Hay que tratar cuatro detalles:

- convertir `IDpol` a entero en **ambas** tablas antes del join, porque OpenML lo declara numérico y llega como float;
- agregar `freMTPL2sev` por `IDpol`, porque una póliza puede tener varias filas de siniestro;
- hacer un left join y rellenar `ClaimAmount` con cero;
- quitar las comillas de las columnas de texto como `VehGas`.

OpenML también publica copias en Parquet (por ejemplo `data.openml.org/datasets/0004/41214/dataset_41214.pq`) que se leen con `pd.read_parquet` sin pasar por ARFF ([OpenML 41214](https://www.openml.org/api/v1/json/data/41214)). Los espejos de Kaggle exigen token o login y no sirven para un aula sin cuentas.

### Limpieza: las anomalías como contenido

Las anomalías del dataset son material didáctico, no un estorbo. El ejemplo de scikit-learn hace estas correcciones ([sklearn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html)):

- `ClaimNb` se limita a 4;
- `Exposure` se limita a 1;
- `ClaimAmount` se limita a 200.000;
- las pólizas con siniestros pero sin importe se recodifican a cero siniestros, porque la severidad necesita importes positivos.

El tutorial de glum hace otra cosa: limita cada siniestro individual a 100.000 *antes* de agregar. Lo justifica porque ese umbral es el cuantil 0,9984 y aun así los siniestros que lo superan suponen **cerca del 25 % del coste total** ([glum](https://glum.readthedocs.io/en/latest/tutorials/glm_french_motor_tutorial/glm_french_motor.html)). Esa cifra enseña mejor que cualquier fórmula por qué los grandes siniestros se tratan aparte.

Los benchmarks de devianza publicados no son comparables entre sí, porque usan escalas, recortes y particiones distintas: 0,594 en el ejemplo Poisson de scikit-learn, 0,4579 en glum y 0,3749 en un artículo de arXiv ([sklearn Poisson](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html); [glum](https://glum.readthedocs.io/en/latest/tutorials/glm_french_motor_tutorial/glm_french_motor.html); [arXiv 2209.08030](https://arxiv.org/pdf/2209.08030)). La regla para los alumnos es comparar modelos solo dentro de un mismo pipeline.

### La prima hay que construirla

El dataset **no tiene columna de prima**. Para calcular siniestralidad y para el doble lift hay que fabricar una "tarifa actual". La propuesta de diseño es usar un GLM sencillo (por ejemplo, solo BonusMalus y Area) con un recargo, y marcarlo claramente como prima simulada. Como ancla de mercado para las diapositivas de KPIs, el ratio combinado no vida del mercado español fue del **93,1 % en 2025**, con 50.000 M€ de primas no vida, según datos ICEA recogidos por Mapfre Economics ([Mapfre Economics 2025](https://www.mapfre.com/media/2026/06/presentacion_Informe-mercado-espanol-seg-2025.pdf)). No se localizó un ratio combinado específico de autos con fuente verificable.

## Las sesiones 1 y 2 enseñan a agregar bien y a automatizar con control

### KPIs: cocientes de sumas

Las definiciones deben tomarse del texto de ratemaking de la CAS (Werner & Modlin) ([Werner & Modlin](https://www.casact.org/sites/default/files/old/studynotes_werner_modlin_ratemaking.pdf)):

- la exposición es "la unidad básica de riesgo" y se mide como emitida, devengada, no devengada o en vigor;
- frecuencia = siniestros / exposición devengada;
- severidad = pérdidas / siniestros;
- prima pura = pérdidas / exposición = frecuencia × severidad;
- loss ratio = pérdidas / prima devengada;
- ratio combinado = loss ratio + LAE/prima devengada + gastos de suscripción/prima emitida (forma histórica).

La terminología española de la UCM/AHERAS (*prima pura* P = E(N)·E(X), *coste medio*, *factores de tarificación*, MLG = GLM) permite presentar cada KPI con su nombre local ([UCM/AHERAS](https://www.ucm.es/data/cont/docs/305-2015-12-10-Introducción%20a%20la%20Tarificación%20en%20Seguros%20No%20Vida_AHERAS.pdf)).

El mensaje central de la sesión 1 es **cómo se agrega**. La frecuencia de un segmento es ΣN/ΣE, que equivale a la media de las frecuencias individuales **ponderada por exposición**. La media simple de N/E es sesgada y ruidosa: una póliza con 0,01 años de exposición y un siniestro aporta una "frecuencia" de 100. En lenguaje Excel: SUMAR.SI.CONJUNTO dividido por SUMAR.SI.CONJUNTO, nunca PROMEDIO.SI.CONJUNTO sobre una columna de ratios. Es exactamente la lógica de pesos del ejemplo de scikit-learn, que usa la exposición como peso para frecuencia y el número de siniestros para severidad ([sklearn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html)). El ejercicio canónico es un `groupby().agg()` de sumas, el cálculo posterior de los cocientes y un `assert np.allclose(pp, freq*sev)`.

Para conectar con el lenguaje contable del departamento conviene añadir un glosario breve:

- bajo IFRS 17, el CSM es el beneficio no devengado de un grupo de contratos;
- los *fulfilment cash flows* son la estimación probabilística del valor actual de los flujos más el ajuste por riesgo no financiero;
- el LRC es la obligación por siniestros aún no ocurridos y el LIC la obligación por siniestros ya ocurridos ([AASB 17 Appendix A](https://standards.aasb.gov.au/node/4058));
- en Solvencia II, la mejor estimación es "la media ponderada por probabilidad de los flujos de caja futuros" descontada ([EIOPA Art. 77](https://www.eiopa.europa.eu/rulebook/solvency-ii/article-2160_en)), y el SCR se calibra para que la ruina no ocurra "más de una vez de cada 200 casos" en 12 meses ([Directiva 2009/138/CE](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32009L0138)).

El matiz que hay que explicar es que frecuencia, severidad y prima pura son magnitudes técnicas previas a la contabilidad, mientras que el ratio combinado que finanzas reporta hoy suele estar en base IFRS 17.

### Visualización

La visualización debe ir unida a los KPIs, no ser un bloque aparte. Las herramientas son matplotlib 3.10 y seaborn 0.13.2, ya presentes en Colab, para gráficos estáticos que luego se incrustan en PNG en el PDF y en Excel. plotly está en Colab en la versión 5.24.1, frente a la 7.1.0 en PyPI, así que conviene dejarlo como extra opcional ([pip-freeze main](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt); [PyPI plotly](https://pypi.org/project/plotly/)). Los gráficos que el curso necesita son:

- barras de frecuencia por Area con su intervalo;
- histograma de severidad en escala logarítmica, donde se ven los picos IRSA-IDA;
- QQ-plots;
- curva de lift y curva de Lorenz.

Las dos últimas deben darse como funciones auxiliares ya escritas para que el tiempo de clase se dedique a interpretar, no a programar ejes.

### Automatización de Excel

La sesión 2 combina tres herramientas con papeles distintos:

- `pd.read_excel(sheet_name=None, header=…, usecols=…)` para libros desordenados de varias hojas, y `read_csv(sep=";", decimal=",")` para exportaciones con configuración regional española;
- **XlsxWriter**, vía `pd.ExcelWriter(engine="xlsxwriter")`, para generar informes nuevos con formato numérico en euros, formato condicional, paneles inmovilizados, autofiltro y gráficos nativos;
- **openpyxl** solo para rellenar una plantilla corporativa existente.

openpyxl 3.1.5 sigue siendo la última versión y viene preinstalado; XlsxWriter 3.2.9 hay que instalarlo ([PyPI openpyxl](https://pypi.org/project/openpyxl/); [PyPI XlsxWriter](https://pypi.org/project/XlsxWriter/)). xlwings 0.37.5 requiere Excel de escritorio, así que es un "siguiente paso en tu portátil" y no algo para Colab ([PyPI xlwings](https://pypi.org/project/xlwings/)).

### PDF y correo

Para PDF, lo más fluido en Colab es **fpdf2** 2.8.9, que es Python puro ([PyPI fpdf2](https://pypi.org/project/fpdf2/)). Hay una trampa que conviene anticipar: las fuentes básicas no cubren "€" ni todas las tildes, así que hay que registrar una TTF como DejaVu. La alternativa más mantenible para informes "de verdad" es una plantilla HTML con Jinja2 renderizada con WeasyPrint. Colab ya trae Jinja2 3.1.6 y las librerías Pango que WeasyPrint necesita, pero su instalación no se ha probado ([apt-list](https://github.com/googlecolab/backend-info/blob/main/apt-list.txt)).

El correo debe enseñarse **en modo simulacro**:

- construir objetos `EmailMessage` con adjuntos;
- generar en un bucle un Excel filtrado y un `.eml` por destinatario o línea de negocio (el momento "combinar correspondencia" que más gusta a los usuarios de Excel);
- usar un indicador `DRY_RUN` y registrar en el log lo que se enviaría.

Hay dos razones para no enviar desde Colab. Google Compute Engine bloquea el puerto 25 saliente ([Google Cloud](https://docs.cloud.google.com/compute/docs/tutorials/sending-mail)). Y Microsoft va a desactivar por defecto la autenticación básica SMTP en Exchange Online para los tenants existentes a finales de diciembre de 2026, recomendando Microsoft Graph `sendMail` con OAuth. Esto viene de una fuente secundaria que conviene contrastar con el blog de Microsoft ([CaptainDNS](https://www.captaindns.com/en/blog/microsoft-exchange-basic-auth-smtp-end)). En producción, el envío real en Zurich será cosa de IT, vía Graph u Outlook.

### Controles y validación

Los controles deben replicar las checklists que el departamento ya mantiene en Excel. Primero se construye una función `check()` que acumula resultados OK/KO en un DataFrame exportado como hoja "Controles" con semáforo. Esa función cubre:

- cuadre de totales con `math.isclose`, para mostrar por qué `==` falla con decimales;
- claves duplicadas;
- nulos en campos obligatorios;
- rangos;
- integridad referencial con `merge(indicator=True)`;
- variaciones mes a mes.

Después se introduce **pandera** 0.34 con su import recomendado `import pandera.pandas as pa`, porque el import de nivel superior para pandas emite un `FutureWarning`. `lazy=True` reúne todos los fallos en un solo informe ([pandera docs](https://pandera.readthedocs.io/en/stable/); [PyPI pandera](https://pypi.org/project/pandera/)). great_expectations es demasiado pesado para este público.

## Las sesiones 3 y 4 enseñan a dudar de los números antes de modelizarlos

### Severidad

La sesión 3 ajusta lognormal, gamma, Weibull y Lomax (la "Pareto" actuarial) con `scipy.stats.<dist>.fit(x, floc=0)`. El ajuste es por máxima verosimilitud por defecto, y SciPy advierte que el óptimo "no está garantizado globalmente" ([SciPy fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.fit.html)). Fijar `floc=0` es imprescindible: con la localización libre, el optimizador tiende a colocarla justo bajo el mínimo y produce formas absurdas, y el AIC debe contar entonces solo dos parámetros libres. Otra trampa son las parametrizaciones de SciPy, que no coinciden con las de Excel: en `lognorm`, `s` es σ y `scale` es exp(μ), mientras que `DISTR.LOGNORM` de Excel recibe μ directamente.

Para la bondad de ajuste, `scipy.stats.goodness_of_fit` reajusta los parámetros en cada muestra Monte Carlo. En el ejemplo de la documentación, el p-valor KS cae de ≈0,28 a ≈0,02 al corregir por estimación ([SciPy goodness_of_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.goodness_of_fit.html)). Con decenas de miles de siniestros, sin embargo, cualquier test rechaza cualquier modelo paramétrico. El mensaje es que el p-valor responde a "¿puedo detectar algún desajuste?" y no a "¿el ajuste sirve?". Lo que decide es el QQ-plot más los cuantiles y la media ajustada frente a la empírica. Los picos IRSA-IDA del dataset ilustran visualmente por qué una sola gamma o lognormal no basta. La idea de "cuerpo + cola GPD" o "recortar y cargar el exceso" debe quedarse en demostración. `fitter` 1.8.0 y `distfit` 2.0.3 están mantenidos, pero ordenan los ajustes por error cuadrático del histograma; sirven como cribado rápido, no como criterio ([PyPI fitter](https://pypi.org/project/fitter/); [PyPI distfit](https://pypi.org/project/distfit/)).

### Frecuencia

La frecuencia se trata comparando Poisson con offset de exposición frente a la sobredispersión φ̂ = χ²de Pearson/(n−p). La CAS Monograph 5 señala que el Poisson sobredisperso da los mismos coeficientes que el Poisson pero errores estándar más realistas ([CAS Monograph 5](https://www.casact.org/sites/default/files/2021-01/05-Goldburd-Khare-Tevet.pdf)).

### Intervalos y bootstrap

La incertidumbre se enseña en tres escalones:

1. **IC analíticos.** Wald o Garwood para la tasa de Poisson; t para la severidad media.
2. **Método delta** para el loss ratio como cociente de sumas.
3. **`scipy.stats.bootstrap`**, con BCa y 9.999 remuestras por defecto. Para un cociente como pérdidas/primas hace falta `paired=True`, que remuestrea pólizas manteniendo juntos pérdida y prima ([SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)).

La unidad de remuestreo es la póliza, no el siniestro, porque remuestrear siniestros ignora la variabilidad de la frecuencia. La intuición más valiosa para finanzas sale del propio álgebra: la anchura relativa del IC de una frecuencia es aproximadamente ±2/√N y depende solo del **número de siniestros**, no de la exposición. Con 100 siniestros la incertidumbre es de ±20 % y con 1.000 de ±6 %. Es una introducción natural a la credibilidad.

La sesión debe cerrar con una simulación de 20 líneas sobre una Pareto de cola pesada. Muestra que el bootstrap no puede generar siniestros mayores que el máximo observado y que, por eso, infracubre la media y los cuantiles extremos. Existe literatura formal sobre este fallo ([Annals of Probability 18(3)](https://projecteuclid.org/journals/annals-of-probability/volume-18/issue-3/Asymptotic-Properties-of-the-Bootstrap-for-Heavy-Tailed-Distributions/10.1214/aop/1176990748.short)).

### GLM para tarificación

La sesión 4 sigue el flujo de la **CAS Monograph 5** (Goldburd, Khare, Tevet y Guller, 2.ª ed., revisada en 2025), que está en el temario del Exam 8 ([CAS Monograph 5](https://www.casact.org/monograph/cas-monograph-no-5)):

- **Frecuencia:** Poisson con enlace log y offset ln(exposición). Es equivalente a modelizar la tasa con la exposición como peso, y da predicciones y errores idénticos.
- **Severidad:** Gamma con enlace log y número de siniestros como peso.
- **Prima pura:** frecuencia × severidad, o una Tweedie con 1 < p < 2 (típicamente 1,5–1,8).
- **Nivel base:** debe ser el más poblado, no el primero alfabético, porque un nivel base escaso infla los errores estándar de todos los demás ([CAS Monograph 5 PDF](https://www.casact.org/sites/default/files/2021-01/05-Goldburd-Khare-Tevet.pdf)).

El puente con Excel es inmediato: exp(β) es la relatividad frente al nivel base, y la tarifa es prima base × Π relatividades, exactamente una tabla de coeficientes.

Para enseñar conviene usar la API de fórmulas de **statsmodels**, porque da errores estándar, offsets e IC de las relatividades. El argumento `exposure` solo es válido con enlace log, y los `var_weights` son los adecuados para un endógeno que es una media ([statsmodels GLM](https://www.statsmodels.org/stable/generated/statsmodels.genmod.generalized_linear_model.GLM.html)). Hay tres trampas que deben aparecer como celdas de "error deliberado":

- el enlace por defecto de la familia Gamma en statsmodels es el inverso, no el log, así que sin `links.Log()` los coeficientes no son relatividades multiplicativas;
- `freq_weights` en lugar de `var_weights` trata una media de tres siniestros como tres filas independientes;
- los regresores de scikit-learn están penalizados por defecto y no admiten offset, así que se usa y = N/E con `sample_weight = E`.

### Lo que dicen los benchmarks

Los resultados publicados son la mejor vacuna contra expectativas irreales. En el ejemplo de scikit-learn 1.9.1, el D² de test es **0,0427 para frecuencia, 0,0044 para severidad y 0,0137 para la Tweedie**. Aun así, el total predicho en test, 1,313·10⁷ (frecuencia × severidad), queda muy cerca del observado, 1,300·10⁷. Solo 6.237 de 169.504 pólizas de test tienen siniestros ([sklearn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html)). Dicho en términos de negocio: el modelo apenas explica la severidad individual, pero calibra bien el agregado y ordena el riesgo. Por eso la validación debe combinar tres cosas:

- curvas de lift por deciles de **igual exposición**;
- un doble lift contra la "tarifa actual" simulada;
- el índice de Gini de la curva de Lorenz, que solo mide ordenación y por eso va siempre acompañado de un control de calibración.

Las técnicas de validación están en los capítulos 6–7 de la monografía ([CAS Monograph 5 PDF](https://www.casact.org/sites/default/files/2021-01/05-Goldburd-Khare-Tevet.pdf)). La versión de scikit-learn de Colab no figura en las notas de entorno; el ejemplo oficial está escrito para la 1.9.1, así que hay que comprobarla antes del curso.

### Segmentación

Para segmentar se recomienda una herramienta **supervisada**: `DecisionTreeRegressor(criterion="poisson")` sobre la frecuencia con la exposición como peso. scikit-learn indica que este criterio es adecuado para conteos o frecuencias. También advierte que `min_samples_split` ignora los pesos, así que hay que controlar el tamaño de los segmentos con `min_weight_fraction_leaf` ([scikit-learn trees](https://scikit-learn.org/stable/modules/tree.html)). Las reglas "si/entonces" de `export_text` se trasladan directamente a Excel. Como complemento, los *tiers* por quintiles de prima pura predicha reutilizan la misma maquinaria que la curva de lift. El k-means queda como contraste: agrupa por parecido de variables, no por riesgo, y comprobar que sus clusters separan mal la siniestralidad es en sí una lección valiosa. Los splines, el boosting y SHAP van a "siguientes pasos", con los Tutoriales 4 y 14 de la SAA como ruta ([ADS](https://www.actuarialdatascience.org/ADS-Tutorials/)).

## La sesión 5 convierte notebooks en procesos reproducibles

### Volumen de datos

freMTPL2 cabe holgadamente en la RAM de Colab, así que el bloque de datos grandes necesita un fichero sintético de varios GB, por ejemplo freMTPL2 replicado con ruido, en el que pandas sufra. La progresión recomendada es:

1. pandas con `usecols`, `dtype="category"` y conversión a **Parquet**;
2. **DuckDB**, SQL directo sobre CSV, Parquet o DataFrames en memoria, fuera de memoria y con una sola instalación;
3. **Polars** en modo lazy/streaming para quien prefiera la sintaxis de DataFrame;
4. Spark o Dask solo si Zurich ya tiene Databricks.

El benchmark PDS-H que publica Polars (mayo de 2025, una máquina de 96 vCPU) apoya esta jerarquía: a escala SF-100, **DuckDB tarda 19,65 s, Polars streaming 23,94 s, PySpark 312 s y Dask 549 s, mientras que pandas se queda sin memoria** ([Polars benchmarks](https://pola.rs/posts/benchmarks/)). Es un benchmark del propio fabricante y no oficial. Aun así, la recomendación de **DuckDB como herramienta por defecto** se sostiene sobre todo porque los analistas financieros ya entienden SQL ("una tabla dinámica con palabras") y porque Colab ya trae Dask 2026.8.0 y PySpark 4.0.4 para una demostración breve ([pip-freeze main](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt)). Polars 2.0 cambia la semántica SQL y depreca `cut`/`qcut` ([Polars 2.0](https://github.com/pola-rs/polars/releases/tag/py-2.0.0)), y DuckDB 2.0 llega días después de esta fecha. Ambos deben fijarse (`polars<2`, `duckdb==1.5.*` o la LTS 1.4) ([DuckDB release calendar](https://duckdb.org/release_calendar.html)).

### SQL

Para SQL basta sqlite3 o DuckDB en local, con `pd.read_sql` sobre un engine de SQLAlchemy 2.x y parámetros enlazados con `text()`. Colab trae SQLAlchemy 2.1.1 ([PyPI SQLAlchemy](https://pypi.org/project/SQLAlchemy/)). La diferencia con construir el SQL con f-strings debe explicarse con un ejemplo de inyección. La cadena de conexión a SQL Server con pyodbc se enseña pero no se ejecuta, porque desde Colab no hay acceso a los servidores de Zurich y pyodbc tampoco viene instalado ([PyPI pyodbc](https://pypi.org/project/pyodbc/)).

### Estructura de proyecto y Git

La estructura de proyecto toma como modelo **cookiecutter-data-science v2**: `data/raw` inmutable, `data/processed`, notebooks numerados, `reports/`, un paquete `src` con funciones reutilizables y `pyproject.toml`. Su generador ya ofrece uv como gestor de entornos y ruff como linter ([CCDS docs](https://cookiecutter-data-science.drivendata.org/)). La variante financiera añade:

- `config/params.yaml` para el periodo y los umbrales;
- un `run_report.py` como punto de entrada;
- un `.gitignore` que excluye `data/`, `output/` y `.env`;
- **nbstripout**, para que las cifras confidenciales de las salidas de las celdas nunca lleguen a Git.

Las versiones de referencia son uv 0.12.23, ruff 0.16.10 y nbstripout 0.9.1 ([PyPI uv](https://pypi.org/project/uv/); [PyPI ruff](https://pypi.org/project/ruff/); [PyPI nbstripout](https://pypi.org/project/nbstripout/)). Git debe enseñarse con GitHub Desktop o el panel de control de código de VS Code, no con la terminal. El ciclo mínimo es clonar, commit con un mensaje que explique el porqué, push, pull, rama y pull request. La analogía útil es "control de cambios de Word para una carpeta entera, y el pull request es enviar a firma".

### Programación de ejecuciones

En producción, el informe se ejecuta como un script `.py` desde el Programador de tareas de Windows o el orquestador corporativo, no como un notebook. **papermill** 2.7.0 permite parametrizar notebooks por mes cuando se prefiera ese formato ([PyPI papermill](https://pypi.org/project/papermill/)). Colab no tiene programador nativo, así que el ejercicio final ejecuta `run_report.py` sobre el mes elegido y regenera el Excel, el PDF y los borradores `.eml` de la sesión 2 en un solo paso.

### Anexo de reservas (20 minutos)

El anexo de 20 minutos tiene cuatro partes:

1. **5′** triángulo acumulado en pandas, como el triángulo de desarrollo de Excel, con factores ponderados por volumen ΣC_{j+1}/ΣC_j. Es otra vez un cociente de sumas.
2. **5′** CDF, últimas e IBNR.
3. **5′** `MackChainladder().summary_`.
4. **5′** histograma de `BootstrapODPSample` con su percentil 99,5, enlazado con el 1-en-200 de Solvencia II ([chainladder tutorial](https://chainladder-python.readthedocs.io/stable/getting_started/tutorials/stochastic-tutorial.html)).

El triángulo clásico `raa` viene dentro del paquete y no necesita descarga. Ejecutado con chainladder 0.10.1 da:

- **IBNR 52.135 y última 213.122**;
- **error estándar de Mack 26.881**, es decir, ≈52 % del IBNR;
- con 5.000 simulaciones bootstrap, una media de 53.826, desviación típica de 19.059 y **percentil 99,5 de 111.466**, más del doble de la estimación puntual.

Estos resultados están verificados ejecutando el paquete ([PyPI chainladder](https://pypi.org/pypi/chainladder/json)). Esa distancia entre estimación puntual y percentil 99,5 es el mensaje para finanzas.

Como ejercicio autónomo de back-testing, la actualización de diciembre de 2025 de la base Schedule P de la CAS (años de ocurrencia 1998–2007, triángulos superior e inferior) permite comprobar cuánto acertó la reserva ([CAS Loss Reserving Data](https://www.casact.org/publications-research/research/research-resources/loss-reserving-data-pulled-naic-schedule-p)). Hay que tener en cuenta que renombra las columnas respecto a los ficheros Meyers–Shi (`IncurLoss_B` → `IncurredLosses`), lo que rompe los notebooks antiguos. El triángulo superior debe construirse filtrando `DevelopmentYear <= 2007` en el DataFrame.

## Conclusión

El hallazgo que más simplifica el diseño es que **un mismo principio estadístico recorre todo el temario**: agregar como cociente de sumas ponderado por exposición, siniestros o prima. Aparece en el SUMAR.SI.CONJUNTO/SUMAR.SI.CONJUNTO de la sesión 1, en el `paired=True` del bootstrap del loss ratio, en los `sample_weight` y `var_weights` de los GLM, en la exposición mínima por hoja del árbol Poisson y en los factores ponderados por volumen del chain-ladder. Si el curso hace explícito ese hilo, el personal financiero no se lleva diez técnicas, sino un único modo de razonar que ya practica en Excel y que ahora puede auditar, escalar y automatizar. La segunda lección es de humildad cuantitativa: un D² de severidad de 0,0044 y un percentil 99,5 del IBNR que duplica la estimación puntual enseñan que el valor está en calibrar agregados y cuantificar incertidumbre, no en predecir pólizas individuales.

Los riesgos del curso son más operativos que conceptuales:

- un entorno que se mueve (Colab con pandas 2.2 frente a pandas 3, Polars 2.0 recién publicado, DuckDB 2.0 inminente, el conflicto de `chainladder` con el pandas de Colab);
- dependencias de IT que aún no se conocen: si Colab está habilitado en el Workspace de Zurich, qué plataforma Git corporativa se usa y cómo se envía correo vía Graph.

Lo que conviene cerrar antes de impartirlo: un ensayo completo de los notebooks en el runtime vigente la semana previa, con versiones fijadas; la confirmación con IT de que colab.research.google.com, github.com y pypi.org son accesibles; y la validación del glosario español (prima imputada, ratio combinado, IBNR) contra la terminología interna de Zurich España, para lo que no se encontró una fuente oficial publicada.
