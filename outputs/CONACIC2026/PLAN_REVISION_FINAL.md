# Plan de revisión final del paper aceptado

**Rama:** `feat/conacic-2026-camera-ready`. **Estado:** plan para decisión; ninguna propuesta aplicada. La etiqueta «CORREGIR YA» expresa prioridad editorial para una edición posterior, no autorización para editar los DOCX en esta fase.

Este documento integra [DIFF_CAMERA_READY.md](DIFF_CAMERA_READY.md), [REVISION_TURNITIN.md](REVISION_TURNITIN.md) y los dos informes oficiales. El único archivo nuevo de esta fase es este plan. Se preservan original aceptado, camera-ready, modelos, cifras, tablas, figuras, citas, referencias, presentación y video.

## 1. Evidencia, límites y reglas de decisión

### 1.1 Fuentes y localizadores

- **Aceptado (A):** `entrega_congreso/Saber_pro_paper_CONGRESO_10P_FINAL.docx`, SHA-256 `5657e9af580c1c555c32128930b7c98cbeb3358cbdd511cd1b7f7ab706db7bcb`.
- **Borrador (B):** `outputs/CONACIC2026/CAMERA_READY_DRAFT.docx`, SHA-256 `938bcc7b9bd0cb6e4bca89bc6052a4846edc020af933b2d7adb7aa5318d360f0`.
- **IA:** [CONAC2026_paper_17_IA_72.pdf](evidencia_turnitin/CONAC2026_paper_17_IA_72.pdf), 12 páginas; SHA-256 `0e8111069834aa54b1b7e174f9218f5e6818d167bd757b2861f39a32d5ba8f33`.
- **Similitud:** [CONAC2026_paper_17_Simi_5.pdf](evidencia_turnitin/CONAC2026_paper_17_Simi_5.pdf), 13 páginas; SHA-256 `f0f39c9b3723ab2fa5d145f8850f2c8d83c2babf59ae87e335974da79d29939f`.
- **Procedencia oficial:** [PROCEDENCIA.json](evidencia_turnitin/PROCEDENCIA.json). Ambas portadas identifican entrega `trn:oid:::1:3645328474`, archivo `CONAC2026_paper_17.docx`, 252.1 KB, diez páginas, 3370 palabras y 18.990 caracteres; entrega 10 sep 2026, 9:16 a.m. GMT-6, descarga ese día a las 2:29 p.m. GMT-6.

`A:Pn` es el índice desde cero del párrafo del cuerpo del original, contando vacíos y excluyendo celdas de tabla. Después de A:P4, el correspondiente en B es P(n+1), por el correo insertado. Los localizadores son del DIFF, no números de párrafo de Turnitin. Página física IA 3 equivale a artículo 1; similitud 4 equivale a artículo 1.

La revisión previa localizó los 95 párrafos no vacíos de título/cuerpo/referencias, excluyendo autor y afiliación, en el PDF IA tras normalizar la extracción. La autoría/afiliación de A no aparece en los PDF oficiales. Falta el DOCX exacto sometido para establecer identidad binaria o explicar esa omisión: no se presume error ni anonimización deliberada.

Este plan consolida verificaciones ya registradas; **no ejecuta entrenamiento, predicción ni una nueva evaluación Turnitin**. Los valores «verificados» que difieren del paper se citan como evidencia histórica de la auditoría previa, nunca como resultados sustitutivos. No se repitió la verificación externa de referencias: se utiliza la evidencia primaria enlazada en el DIFF, con sus límites.

### 1.2 Clasificación única y protección científica

Cada asunto tiene un responsable único Axx, Bxx, Cxx o Dxx. La matriz de resaltados de §5 es un índice de localización: sus remisiones a C no reclasifican problemas científicos como estilo. B significa conservar la versión aceptada ante incertidumbre; los asuntos expresamente requeridos en C también quedan congelados, pero su categoría única es C.

- **A:** corrección editorial objetiva, sin cambio de proposición científica; algunas ya están bien realizadas en B y se propone conservarlas.
- **B:** mantener el contenido aceptado o la evidencia mientras no exista procedencia suficiente o error demostrado.
- **C:** cambio de método descrito, interpretación, alcance, referencia problemática o procedencia de resultados; decisión de Nathalia antes de editar.
- **D:** claridad expresiva semánticamente equivalente, motivada por lectura académica de los bloques resaltados.

Las propuestas C son fragmentos **condicionales para deliberación**, no reemplazos aprobados. Moderar causalidad, novedad o certeza sí cambia alcance científico, aunque conserve todos los números. No se fija porcentaje objetivo ni se sugiere evasión, sustitución artificial de palabras o paráfrasis sistemática. Una marca IA no obliga a reescribir.

### 1.3 Lectura correcta de los indicadores oficiales

**Turnitin IA, p. 2: 72 % de texto calificado señalado como probable escritura con IA.** No es 72 % de las palabras totales ni probabilidad de conducta indebida. El propio informe advierte que la detección puede ser inexacta, tanto para texto humano como generado, y que no debe emplearse como único fundamento para sancionar: requiere juicio humano y revisión adicional. El indicador «27» no equivale a 27 párrafos Word.

**Similitud, p. 2: 5 % general, sin alertas de manipulación de texto.** El informe dice «No se han detectado manipulaciones de texto sospechosas». Internet 4 %, publicaciones 3 % y trabajos de estudiantes 2 % son conjuntos solapados, no sumandos. Están filtrados bibliografía, texto citado y texto mencionado. No certifica la corrección de todas las citas ni resuelve los problemas de bibliografía del DIFF.

## 2. A. CORREGIR YA — EDITORIAL/OBJETIVO

**Decisión común a A01–A14:** registrar en la cola editorial; ejecutar solamente en una fase posterior autorizada. **Significado científico:** no se altera. Cuando el objeto es XML, «texto aceptado» se refiere al contenido o propiedad original. El riesgo principal es de identidad, trazabilidad o maquetación, no de resultados.

| ID / ubicación | Texto o contenido aceptado; estado en B | Problema y evidencia | Redacción o acción propuesta, aún no aplicada |
|---|---|---|---|
| A01 · autoría/afiliación/correo, A:P3–4 / B:P3–5 | A: «Edwin Santiago Paz Bedoya»; «UNIMINUTO, Bogotá, Colombia.» B añade Nathalia Orozco Morales, afiliación Virtual y los dos correos | DIFF D01–D03 documenta respaldo de identidad en el repositorio/sesión. Los PDF sin autoría no invalidan ese respaldo ni prueban causa de omisión | Conservar B: «Edwin Santiago Paz Bedoya¹, Nathalia Orozco Morales¹»; «¹UNIMINUTO Virtual – Bogotá, Colombia.» y correos `edwin.paz@uniminuto.edu`, `nathalia.orozco@uniminuto.edu`. No inferir autores a partir de metadatos de plantilla |
| A02 · pies/encabezados | A: «septiembre 1, 2020 / octubre 5, 2020», «D. Beltrán et al. / Abstraction & Application 41 (2023) 3-16» | Fechas, autor y paginación de otro artículo, DIFF F07/F10; informes oficiales reproducen herencia | Conservar eliminación ya hecha en B; no sustituir por fechas editoriales inventadas. Usar cabecera de autores reales y estado DRAFT; dejar fechas de recepción/aceptación sujetas a datos del congreso |
| A03 · encabezado largo y A:P69 | «auditorría», «promedio  global», «recoleción» | Errores ortográficos/espaciado visibles en original; DIFF F08/D08. B reemplazó cabecera y corrigió recolección | Si se utiliza ese título: «auditoría» y «promedio global». Conservar «recolección» en B. No reescribir la afirmación científica que contiene el typo |
| A04 · referencia [20], A:P100 / B:P101 | «[20] Anónimo, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. EDM, 2020.» | DIFF D09/§4.5: PDF oficial EDM acredita P. J. L. Adeodato y R. L. C. Silva Filho, 13th EDM, pp. 545–549. Es la misma obra, ya verificada | Conservar la ficha corregida de B: autores identificados, mismo título, evento 2020 y pp. 545–549. Mantener número [20] y citas. Fuente: [PDF oficial](https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_55.pdf) |
| A05 · docProps/core.xml | A creator Francisco Alejandro Madera Ramírez; B title/creator de los autores reales | Propiedad de tercero en A; DIFF F12 | Conservar título del paper y creator de Edwin Santiago Paz Bedoya y Nathalia Orozco Morales ya incorporados; no atribuir a terceros la autoría del manuscrito |
| A06 · docProps/core.xml | A lastModifiedBy=NATHALIA OROZCO MORALES, modified=2026-07-03…, revision=33; B Raul Antonio Aguilar Vera, 2023-03-22…, revision=30; fechas created/lastPrinted de 2020 | Herencia accidental, DIFF F13. La fecha 2023 no representa la generación de B | Eliminar atribuciones/fechas heredadas no sustentadas o restituir el historial verificable; no fabricar hora de edición ni copiar una fecha como si fuera la última edición real de B. Preservar trazabilidad de A en el registro, no falsificarla en B |
| A07 · docProps/app.xml | A sin esas estadísticas extensas; B Pages=3, Words=457, Paragraphs=5, Lines=20, Characters=2516, CharactersWithSpaces=2968, TotalTime=84 | Valores de plantilla, DIFF F14; no prueban longitud del paper | Retirar estadísticas obsoletas o recalcularlas al guardar/renderizar la futura versión final. No copiar 3370 palabras de Turnitin: pertenecen a otro archivo evaluado |
| A08 · word/styles.xml | A define IDs 17 y 3; B conserva 241 referencias rStyle y una tblStyle que ya no tienen definición | DIFF F06 y anexo XML: estilos huérfanos; cambio de fuentes/espaciados por defecto puede afectar formato | Restaurar definiciones necesarias o reasignar referencias a estilos equivalentes definidos. Revisar TNR/SimSun frente a minorHAnsi/minorBidi, 11 pt, es-MX, after=160 y line=259. Comprobar visualmente antes de cerrar; no asumir que todos los runs heredaron el nuevo tipo de letra |
| A09 · campo PAGE / pie | B hereda caché PAGE «61»; cabecera tiene caché «2» | DIFF F10/F07: resultado guardado del campo no actualizado | Mantener campos PAGE dinámicos y actualizar sus resultados durante la futura paginación. No reemplazar todas las páginas por un literal «1». Revisar también caché de cabecera |
| A10 · descripción alternativa del logo, header3.xml | A y B: ruta `C:\Users\mramirez\Documents\2016\sem2-2016\Abstraction & Application\Template\uady.jpg` | REVISION_TURNITIN §C: docPr/cNvPr arrastran ruta privada ajena | Reemplazar únicamente la descripción alternativa por «Logotipo de la Universidad Autónoma de Yucatán». Preservar imagen y marca editorial legítimas |
| A11 · estado de pie de B | A tenía fechas 2020; B dice «Pendiente de análisis de similitud e IA» | REVISION_TURNITIN §C y PDF recibidos: análisis ya realizados, revisión académica aún pendiente | «DRAFT · Informes de Turnitin recibidos; revisión académica pendiente». No afirmar aprobación del comité ni que un porcentaje haya sido corregido |
| A12 · espaciadores, autores y tabla | A espaciadores after=40, tabla 9760 twips; B after=0/line=80, tabla 8838; autoría/afiliación pasan a 12 pt y nuevo espaciado | DIFF F01–F04. Celdas idénticas; ancho de B cabe en caja de texto. D04/D06 colapsan runs de A:P29/P38 y pierden segmentación de formato/idioma | Conservar ajuste de ancho/espaciado si la revisión visual confirma legibilidad; corregir solamente formato/idioma perdido. Una restauración de runs no autoriza cambiar joins o árboles, asignados a C01/C05 |
| A13 · secciones/paginación/cabeceras | Carta y márgenes iguales; inicio 3→1; cabeceras de B con autores y DRAFT; logo conserva identidad | DIFF F05/F07–F11: ligerísimo cambio de tamaño del logo, imágenes científicas idénticas | Conservar inicio en 1, cabeceras pertinentes, retirada de pies vacíos y ajustes de geometría que no deformen el logo. Preservar UADY y Abstraction & Application; no tratarlos como autores intrusos |
| A14 · registro de cambios | CAMBIOS_CAMERA_READY.json llama a D04–D09 «Corrección objetiva documentada…» y omite autoría/paquete | DIFF §5: clasificación genérica insuficiente; no toda modificación es editorial | En un registro futuro, distinguir «editorial» de «metodología/resultado/alcance pendiente de Nathalia» y enlazar este plan. No modificar ese JSON ahora ni considerar su etiqueta aprobación científica |

## 3. B. MANTENER COMO PAPER ACEPTADO POR AHORA

Aquí no se propone sustitución de texto. **Redacción propuesta: conservar literalmente el contenido aceptado indicado. Significado científico: sin cambio. Decisión: mantener hasta disponer de evidencia adicional; ninguna corrección automática.** Las cifras discutidas obligatoriamente con Nathalia están en C06/C07, no se duplican como asuntos B.

| ID | Contenido aceptado / ubicación | Discrepancia, evidencia y límite que justifican mantener |
|---|---|---|
| B01 | A:P27: 1.730.805 filas crudas, cinco archivos y 97,3 % de nulos | Recuentos históricos no reproducidos integralmente desde los archivos crudos en esta fase. DIFF/REVISION no demuestran un valor alternativo válido. D02 podrá dividir la frase sin cambiar ningún dato |
| B02 | Tabla 1, figuras 1–5, títulos, métricas LightGBM y RMSE/R² lineales; Transformer MAE n/d | DIFF acredita igualdad de tabla y cinco imágenes entre A/B; verificación previa concuerda con redondeo de esas métricas. No completar n/d con un experimento nuevo. MAE Ridge/Lasso y errores de grupos tienen decisión científica propia C06/C07 |
| B03 | A:P38: Transformer «early stopping (época 53/200)»; métricas aceptadas | 53 corresponde a épocas ejecutadas, mientras mejor época registrada es 33. No hay justificación para sustituir automáticamente 53 por 33: son conceptos distintos. Mantener ejecución aceptada; no introducir «mejor época 53» |
| B04 | A:P51/P53: lag_1_promedio_global dominante; A:P56: Sin Clasificar RMSE=17,76 | README presenta otro orden de SHAP y narrativa_lgbm denomina RMSE a 12,237, que corresponde a MAE; CSV tiene RMSE≈17,755. El error de una narrativa derivada no obliga a alterar la figura/ranking o la cifra correcta del paper. Interpretación de SHAP sigue en C04 |
| B05 | [2–7], [9–15], [17–19], [24–25]; fichas sin diferencia demostrada | DIFF no validó externamente cada ficha y cada uso contextual. Mantener; no certificar toda la bibliografía por el 5 % de similitud. Usos causales o normativos cuestionados se resuelven en C10/C12/C17, sin cambiar estas fichas de oficio |
| B06 | Documento sometido y sus bloques de identidad; PDF oficiales íntegros | Falta DOCX binario sometido; autores no visibles en PDF, presentes en A. Correspondencia textual no permite explicar procedencia exacta. Conservar evidencia y registrar límite. «Microsoft Word - Document1», QuickSubmit, marcas Turnitin y rótulos de su interfaz pertenecen al informe, no son placeholders que deban limpiarse del paper |
| B07 | Notas separadoras, relaciones, numbering/webSettings, footers vacíos y propiedades WPS | DIFF F11/F14/F15: partes técnicas distintas sin texto científico perdido; dos medios adicionales no son figuras del cuerpo. Conservar infraestructura coherente y eliminación de propiedades WPS. No restaurar diferencias binarias inocuas; defectos concretos de estilo/metadatos están en A |
| B08 | Coincidencias de similitud detalladas abajo | No hay un pasaje sustancial de copia indebida demostrado por estos resaltados. Mantener términos técnicos, nombres propios, encabezados y citas; no alterar tablas por coincidencias mínimas. El informe no permite cotejar exhaustivamente fuentes completas no accesibles |

### 3.1 B08 — Fuentes principales de similitud y relevancia

Todas las once fuentes listadas por Turnitin aportan **menos del 1 % cada una**. Páginas físicas del PDF de similitud. Los títulos truncados se conservan como truncados; no se inventan DOI o autores faltantes.

| N.º / fuente según informe | Página / sección real | Coincidencia y decisión académica |
|---|---|---|
| 1 · Fundación Universidad de San Andrés, trabajo estudiantil | 5 / A:P15, organización del artículo | Fórmula de organización; no se demuestra apropiación de aporte científico. Mantener |
| 2 · Universidad Autónoma de Chile, trabajo estudiantil | 7–8 / A:P41–42, introducción y rótulo de Tabla 1 | Lenguaje de evaluación/comparación. Mantener tabla y métricas |
| 3 · Sergio Merino Fidalgo, Eduardo Zalama Casanova, Jaime Gómez García-Bermejo, J…; publicación | 5 / organización y encabezados del marco teórico | Fuente abreviada en informe; coincidencia estructural. No reconstruir ficha ni añadir cita sin necesidad |
| 4 · Universidad de Manizales, trabajo estudiantil | 4 / A:P12 | Frase introductoria sobre calidad. Similitud no prueba plagio; precisión del constructo se revisa en C17 |
| 5 · tesisdigitales.umich.mx | 11 / conclusiones | Encabezados y «El presente trabajo». Expresión genérica, no evidencia de copia sustancial |
| 6 · www.scribd.com | 4 / A:P12 | Nombre institucional completo del ICFES. Conservar denominación oficial |
| 7 · repository.poligran.edu.co | 5 / A:P18 | «aseguramiento de calidad de la educación superior». Terminología común |
| 8 · www.economia.puc.cl | 6 / secciones 3 y 3.1 | Encabezados y «Los datos». Mantener |
| 9 · www.grade.org.pe | 5 / A:P18 | «teoría de respuesta al ítem». Término técnico que no debe sustituirse artificialmente |
| 10 · www2.icfes.gov.co | 5 / A:P18 | Relación habilidad del evaluado/dificultad del ítem. Conservar terminología y revisar atribución técnica únicamente si C17 lo requiere |
| 11 · Diofanto Arce Tovar, «Análisis Crítico de la Reforma del Sistema Educativo Colom…» | 4 / A:P12 | Nombre del MEN. No justifica reescritura ni nueva referencia |

**Problema real demostrado por similitud:** ninguno de copia sustancial o manipulación en los fragmentos revisados. Esta conclusión está limitada a los informes y marcas examinados; no equivale a una certificación universal de originalidad. Los errores editoriales y referencias problemáticas son independientes del 5 %.

## 4. C. REVISAR CON NATHALIA ANTES DE CAMBIAR

En todos los registros siguientes: **no aplicar**, no reentrenar y no sustituir cifras. La propuesta indica qué se podría decir solo después de resolver la evidencia. «Sin sustitución propuesta» es una decisión deliberada cuando escribir una alternativa supondría inventar resultados o una referencia.

### C01 — Descripción real de joins y capas

- **Ubicación:** A:P29, §3.2; DIFF D04.
- **Texto aceptado:** «Se aplicó un pivot long→wide con inner join sobre la llave (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA), preservando únicamente entidades con las tres capas presentes.»
- **Problema y evidencia:** B cambia a inner entre pruebas/global por tres claves y left para niveles por cuatro, y pierde las definiciones de las capas. DIFF D04 y código de limpieza sustentan la implementación actual; falta vincularla inequívocamente a la ejecución sometida.
- **Redacción propuesta / alternativa de decisión:** Condicionada a confirmar la ejecución: «Se integraron las capas PUNTAJE_PRUEBA (promedio por prueba) y PUNTAJE_GLOBAL (target PROMEDIO_GLOBAL) mediante inner join por (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD). La capa NIVEL_DESEMPEÑO_PRUEBA (proporciones por nivel) se incorporó mediante left join, añadiendo NOMBRE_PRUEBA a la llave.» Mantener la oración de 127.716 filas y disponibilidad del target; no usarla para inferir otra población.
- **¿Altera significado científico? / decisión requerida:** Sí: cambia el método de unión y el criterio de inclusión descritos. Nathalia debe identificar script/commit/CSV de la corrida aceptada y decidir si B describe esa ejecución. No dar D04 por aprobado.

### C02 — Validación temporal interna y suficiencia de la curva

- **Ubicación:** A:P36/P43/P45, §§3.4 y 4.1; DIFF §4.1.
- **Texto aceptado:** «El split temporal estricto usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas).» / «La brecha pequeña y estable confirma regularización adecuada.»
- **Problema y evidencia:** src/features.py:206,300,436 ordena por entidad/año. Los cuatro folds internos y el 80/20 posicional Optuna contienen 2020–2023 en ambos lados; boosting.py:269–272 no usa tscv en el objetivo. baseline.py:292–298,372–384 ajusta preprocesador antes de CV interno de RidgeCV/LassoCV. TargetEncoder cv=2 no lo vuelve temporal. En cambio, fase5_lightgbm.py:94–95 y boosting.py:439–444 sí separan <2023/2023 para la curva. El holdout 2024 está separado; no se ha cuantificado efecto sobre métricas.
- **Redacción propuesta / alternativa de decisión:** Conservar literalmente el split externo. Adición condicional: «La separación externa reserva 2024 para prueba. La selección interna de hiperparámetros no garantiza separación cronológica global por año; la curva LightGBM utiliza 2023 como validación.» Para la garantía de la curva: «La brecha observada describe el comportamiento en esa partición de validación.» Mantener 225 y 168 hasta resolver C05.
- **¿Altera significado científico? / decisión requerida:** Sí: explicita una limitación y reduce una garantía; no invalida automáticamente resultados externos. Decidir qué limitación corresponde a la ejecución aceptada y cómo declararla; cualquier nueva evaluación queda fuera de esta fase.

### C03 — TargetEncoder multiclass, 417 columnas y rezagos

- **Ubicación:** A:P15/P36, §3.4; DIFF D05/§4.2.
- **Texto aceptado:** «Se construyeron 15 features causalmente válidas: rezagos temporales lag_1 y lag_2 del PROMEDIO_GLOBAL y de cada prueba, tendencia histórica, desviación estándar histórica, logaritmo del número de evaluados, año, identificadores de NBC y departamento codificados con TargetEncoder.»
- **Problema y evidencia:** Los tres PKL inspeccionados en el DIFF tienen target_type_=multiclass y 135 clases: 10 numéricas + 3 categóricas×135 + 2 one-hot = 417 columnas a partir de 15 entradas. baseline.py:221/boosting.py:149 no fijan continuous. Siguen siendo regresores. shift produce observaciones previas disponibles: 2.022 filas presentan saltos >1 año. B añade estos hechos pero no acredita por sí solo procedencia histórica.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «El preprocesamiento transforma 15 variables de entrada en 417 columnas. En los artefactos inspeccionados, TargetEncoder infirió un objetivo multiclass de 135 valores; los estimadores finales son regresores. Los rezagos corresponden a observaciones previas disponibles de cada entidad.» No cambiar el encoder ni omitir el split aceptado.
- **¿Altera significado científico? / decisión requerida:** Sí: modifica descripción y garantía de validez/rezago. Confirmar artefactos sometidos, semántica de lag_1/lag_2 y disponibilidad de cada variable; distinguir lo ejecutado de una implementación deseable.

### C04 — Interpretación SHAP, etiquetas NBC y suficiencia del historial

- **Ubicación:** A:P7/P9/P51/P53/P63/P69, §4.2 y §5.1; DIFF §4.2.
- **Texto aceptado:** «Los indicadores NBC aparecen como efectos de intercepto por área disciplinar.» / «La variable log_cantidadevaluados muestra que programas con cohortes pequeñas tienen SHAP negativo, reflejando mayor volatilidad en el promedio histórico.» / «Los NBC con SHAP negativo… señalan prioridades concretas de intervención…».
- **Problema y evidencia:** cat__NBC_129.0 es el componente de NBC para valor objetivo 129, no código de disciplina. narrativa_lgbm.txt:40 y el preprocesador documentan esa expansión. SHAP explica predicciones, no estima efecto causal ni demuestra que solo el historial baste cuando hay otras entradas. No se demostró que SHAP esté numéricamente mal calculado.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «Los valores SHAP describen contribuciones a las predicciones del modelo; las columnas codificadas de NBC requieren interpretarse según el preprocesamiento utilizado.» Mantener ranking de la figura, +28, citas y cifras; no traducir automáticamente un componente a una disciplina. Para la suficiencia: «El desempeño observado corresponde al conjunto de variables utilizado, que incluye el historial de PROMEDIO_GLOBAL.»
- **¿Altera significado científico? / decisión requerida:** Sí: cambia interpretación y alcance explicativo. Nathalia debe validar correspondencia columnas/figura/artefacto y retirar o sostener con evidencia independiente interpretaciones de volatilidad e intervención.

### C05 — 188 frente a 500 árboles

- **Ubicación:** A:P38/P43/P45, §3.5/4.1; DIFF D06.
- **Texto aceptado:** «LightGBM con 50 trials de búsqueda Optuna [4] y n_estimators = 500»; curva con 225 iteraciones y mejor iteración 168.
- **Problema y evidencia:** fase5_lightgbm.py guarda JSON en línea 86 antes del ajuste de línea 100 max(best_iter+20,100). El artefacto actual tiene 188 árboles =168+20; 500 es configuración intermedia y 800 máximo de la curva. Son etapas distintas, no cuatro estimaciones de la misma cantidad. No está demostrada la correspondencia binaria con la ejecución sometida.
- **Redacción propuesta / alternativa de decisión:** Sin sustitución inmediata de 500. Si se confirma el artefacto histórico: «LightGBM se evaluó con 50 trials de búsqueda Optuna [4]; el ajuste final utiliza 188 árboles tras la selección de 168 iteraciones en la curva y la adición de 20.» Esta frase es solo alternativa deliberativa; las cifras 225 de curva y 500 de configuración deben documentarse por etapa, no borrarse.
- **¿Altera significado científico? / decisión requerida:** Sí: cambia configuración reportada. Identificar corrida/JSON/PKL y resolver D06 antes de aceptar 188. Que 500 no esté resaltado por Turnitin no reduce este problema.

### C06 — MAE Ridge/Lasso

- **Ubicación:** Tabla 1, columna MAE; DIFF §4.3.
- **Texto aceptado:** Ridge 7,2967; Lasso 7,0622; LightGBM 6,2109; Transformer n/d.
- **Problema y evidencia:** CSV baseline_metrics.csv coincide con aceptado. Auditoría previa de PKL: Ridge 7,296436898959→7,2964; Lasso 7,058887577037→7,0589. narrativa_baseline.txt:30,39 coincide con esa reproducción. LightGBM redondea a 6,2109. RMSE/R² coinciden. No es el redondeo correcto de las mismas cantidades; causa histórica desconocida.
- **Redacción propuesta / alternativa de decisión:** Sin sustitución propuesta: conservar todas las celdas aceptadas. Texto para registro de decisión, no para insertar automáticamente: «Los MAE publicados y los artefactos actuales requieren reconciliación de procedencia.»
- **¿Altera significado científico? / decisión requerida:** Cambiar cualquier celda sí altera resultados. Nathalia debe identificar predicciones, muestra, commit y cálculo usados para el CSV aceptado. No atribuir causa a serialización ni corregir por proximidad numérica.

### C07 — RMSE MEDIA/BAJA y diferencial

- **Ubicación:** A:P60/P75, §4.4 y conclusiones; DIFF §4.4.
- **Texto aceptado:** «Las predicciones de confianza MEDIA (84,4 %) obtienen RMSE aprox. 9,1 frente a RMSE aprox. 11,4 de confianza BAJA (15,6 %). El diferencial de 2,3 puntos confirma que los tres flags empíricos son informativos…».
- **Problema y evidencia:** Verificación previa predict_batch: tamaños 24.288/4.474 concuerdan; RMSE actuales 6,596797235424/17,980199345751 no concuerdan. Diferencia actual≈11,3834, no 2,3. Ponderar cuadrados de 9,1 y 11,4 con esos tamaños implica total≈9,49 frente a 9,3293 publicado. src/inference.py:588–606 y demo_inferencia.txt:32–33 describen grupos; todos los 2024 son extrapolación respecto a max_train=2023.
- **Redacción propuesta / alternativa de decisión:** Sin sustitución propuesta para 9,1, 11,4, 2,3, porcentajes o texto asociado. Mantenerlos congelados y solicitar tabla de predicciones/grupos original. La lectura de certeza se decide en C09, sin ocultar esta discrepancia.
- **¿Altera significado científico? / decisión requerida:** Sí, riesgo muy alto de alterar resultados. Identificar versión de reglas, artefacto, conjunto y cálculo histórico; no reemplazar por la reproducción actual aunque la dirección del efecto coincida.

### C08 — Generalización sobre Salud

- **Ubicación:** A:P56, §4.3; DIFF D07.
- **Texto aceptado:** «Los programas de Salud concentran los errores más bajos (RMSE entre 4,1 y 6,2 puntos)».
- **Problema y evidencia:** B pasa a «Algunas áreas de Salud…» pero conserva rango problemático. CSV: Salud Pública≈11,7652, Medicina≈6,2174, Optometría≈4,687; ≈4,1089 es formación militar. El extremo 4,1 no queda acreditado como Salud. La corrección parcial de B no basta.
- **Redacción propuesta / alternativa de decisión:** Sin nuevo rango propuesto. Alternativa de alcance para discutir: «Los errores varían entre los NBC; las áreas de Salud no presentan un comportamiento uniforme.» No aplicar ni sustituir la oración/rango aceptados hasta reconciliar las categorías de la figura y CSV.
- **¿Altera significado científico? / decisión requerida:** Sí: modifica generalización y eventualmente cifras. Nathalia debe decidir qué categorías concretas respaldan el enunciado; no aceptar D07 como simple estilo.

### C09 — Cuantificación de incertidumbre y certeza

- **Ubicación:** A:P14/P60/P75; objetivo y §4.4.
- **Texto aceptado:** «…módulo de inferencia deployable con cuantificación de incertidumbre»; «…cuantificar la incertidumbre asociada a cada predicción mediante flags de confianza»; «según nivel de certeza».
- **Problema y evidencia:** src/inference.py:588–606 implementa reglas sobre historial, tamaño y extrapolación; no probabilidades ni intervalos calibrados. L6 ya reconoce ausencia de intervalos formales. C07 impide presentar el diferencial como validación resuelta de certeza.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «El módulo de inferencia acompaña cada predicción con flags empíricos definidos mediante reglas sobre la información disponible.» Mantener número de flags; no llamarlos probabilidades, intervalos calibrados ni medidas de cobertura.
- **¿Altera significado científico? / decisión requerida:** Sí: reduce alcance de cuantificación a señalización heurística. Nathalia debe acordar significado de confianza y qué evidencia de utilidad puede sostenerse sin cambiar resultados.

### C10 — Un año de anticipación y uso curricular

- **Ubicación:** A:P7/P9/P69/P74; abstract, resumen, §5.4 y conclusión.
- **Texto aceptado:** «…con un año de anticipación…»; «Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva.»
- **Problema y evidencia:** src/features.py:484–485 usa CANTIDADEVALUADOS del registro corriente, sin rezago. Comentario de disponibilidad antes de publicación no prueba disponibilidad un año antes. Evaluación externa retrospectiva 2024 no acredita calendario operativo ni impacto institucional. [26] es una analogía a otro nivel, no prueba de despliegue del proyecto.
- **Redacción propuesta / alternativa de decisión:** Condicionada para A:P74: «El trabajo evalúa la predicción del PROMEDIO_GLOBAL de Saber Pro a nivel de programa académico, alcanzando R² = 0,706 y RMSE = 9,33 puntos sobre el conjunto de prueba 2024, a partir de datos públicos del ICFES.» Para uso: «Su utilización anticipada requiere verificar la disponibilidad de todas las entradas en el momento de predicción.» La versión inglesa deberá reflejar la misma decisión, sin nuevos resultados.
- **¿Altera significado científico? / decisión requerida:** Sí: retira horizonte operativo no acreditado y reduce inferencia de impacto. Decidir fecha de corte real, disponibilidad de cada entrada y alcance de [15]/[26]; preservar horizonte de evaluación documentado sin confundirlo con un año de disponibilidad anticipada.

### C11 — Afirmaciones causales sobre errores y Transformer

- **Ubicación:** A:P46/P56/P58/P65/P75; resultados y discusión.
- **Texto aceptado:** «…explicados por la alta heterogeneidad interna…»; «La brecha (R² = 0,706 vs. 0,041) confirma cuatro factores estructurales…»; «…el Transformer no resulta competitivo por cuatro factores estructurales…».
- **Problema y evidencia:** Gráficos de error y agrupaciones no son estimaciones causales de heterogeneidad/desarrollo regional. decision_transformer.txt describe una configuración, no una ablación controlada de cuatro causas. Se conservan ratio 3,05×, brecha 6,4, padding 51,7 %, R² y [11]/[12]. El scatter no identifica por sí solo causas de errores extremos.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «La brecha (R² = 0,706 vs. 0,041) se observa en una configuración con asimetría de muestras efectivas (ratio 3,05×), ausencia de features categóricas aprendibles en el Transformer, brecha val/test de 6,4 puntos y 51,7 % de secuencias con padding. El experimento no aísla el efecto individual de estas condiciones.» Mantener [11]/[12] en su contexto. Para grupos: «Las diferencias de error describen heterogeneidad predictiva entre categorías.»
- **¿Altera significado científico? / decisión requerida:** Sí: de explicación causal a descripción/hipótesis. Nathalia debe revisar también atribuciones SHAP (C04), causas de extremos y recomendaciones regionales; no alterar tablas ni presentar una nueva ablación.

### C12 — Novedad, exclusividad y transferencia

- **Ubicación:** A:P14/P67/P75; introducción, §5.3, conclusión.
- **Texto aceptado:** «A la fecha no existe un sistema abierto…»; «…ningún trabajo previo audita sistemáticamente fugas en paneles con publicación anual»; «…inédita en la literatura EDM…»; «El catálogo es transferible a PISA…».
- **Problema y evidencia:** DIFF §4.4–4.5: referencias [16]/[21] sin identidad exacta, [22] identificada pero no prueba ausencia universal; una búsqueda negativa no acredita exclusividad. No se documenta aplicación del catálogo a PISA.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «El trabajo documenta seis tipos de fuga considerados en este proyecto y un procedimiento de revisión para el panel estudiado.» Para transferencia: «La aplicabilidad del catálogo a otros exámenes requiere evaluar sus estructuras de datos y calendarios de publicación.» No eliminar [9]/[16]/[21]/[22] ni ΔR² para resolver por estilo: dependen de C13–C16.
- **¿Altera significado científico? / decisión requerida:** Sí: reduce novedad universal y transferencia asegurada a aporte documentado. Nathalia debe decidir evidencia de búsqueda y alcance defendible, sin declarar inexistentes referencias no localizadas.

### C13 — ΔR²≈0,22 atribuido a seis fugas

- **Ubicación:** A:P7/P9/P15/P31/P67/P75, §3.3 y contribución.
- **Texto aceptado:** «Se identificaron seis tipos de fuga (L1–L6) con impacto conjunto ΔR² ≈ 0,22. El baseline Lasso con fugas presentes reportaba R² ≈ 0,88; tras las correcciones, R² = 0,658.»
- **Problema y evidencia:** Restar valores históricos ≈0,88 y 0,658 produce ≈0,22; no identifica contribución de cada fuga ni controla otros cambios de corrida. Los percentiles mencionados no aparecen en las 15 entradas finales, lo que tampoco demuestra que nunca se usaran. DIFF §4.4 exige enlaces entre catálogo, cambios y ejecuciones.
- **Redacción propuesta / alternativa de decisión:** Sin sustitución de cifras. Fragmento condicional si se acredita comparabilidad histórica: «La diferencia histórica entre las dos ejecuciones Lasso reportadas es ΔR²≈0,22; esta comparación no estima el efecto individual de cada tipo de fuga.» Mantener catálogo y valores; no usar esta frase si ni siquiera se identifica el par de ejecuciones.
- **¿Altera significado científico? / decisión requerida:** Sí: modifica atribución metodológica del aporte principal. Nathalia debe identificar ambas corridas y qué cambió entre ellas antes de decidir si puede llamarse impacto conjunto del catálogo.

### C14 — Referencia [8] y uso en discusión

- **Ubicación:** A:P88/P63 y limitación L2.
- **Texto aceptado:** «[8] J. Behr et al., “Early prediction of university dropouts — A random forest approach,” J. Educ. Comput. Res., vol. 60, n.º 5, pp. 1109–1148, 2022.»
- **Problema y evidencia:** DIFF §4.5 enlaza tesis/manuscrito institucional de Marco Giese: Andreas Behr, Marco Giese, Herve D. Teguim K., Katja Theune; publicación 2020 en Jahrbücher für Nationalökonomie und Statistik. Contradicción de inicial, revista y año; volumen/páginas finales aún no cerrados. Además, abandono individual no equivale directamente a desempeño agregado.
- **Redacción propuesta / alternativa de decisión:** Sin ficha definitiva propuesta. Conservar [8] hasta obtener versión editorial y comprobar la afirmación «confirman este hallazgo» en A:P63. Después completar la misma obra, no sustituirla por otra parecida.
- **¿Altera significado científico? / decisión requerida:** Potencial cambio de referencia y soporte argumental. Nathalia debe aportar DOI/PDF y pasaje pertinente; no se aprueba por analogía de títulos.

### C15 — Referencias [16] y [21] no identificadas exactamente

- **Ubicación:** A:P96/P101/P67 y marco teórico.
- **Texto aceptado:** «[16] J. C. Rangel-Mora y A. Pérez-Roa, “Predicción del rendimiento en pruebas Saber mediante minería de datos: revisión sistemática,” Rev. Colomb. Educ., n.º 82, 2021.» / «[21] D. Chafla, M. Morocho y J. Ortega, “Machine learning models for academic performance prediction with explainability,” Frontiers in Education, vol. 10, 2025.»
- **Problema y evidencia:** DIFF §4.5: búsquedas sin coincidencia exacta; repetición de [16] en paper/revised/paper_content.py:873 es derivada. DOI 10.3389/feduc.2025.1632315 corresponde a autores Guevara-Reyes, Ortiz-Garcés, Andrade, Cox-Riquetti y Villegas-Ch., no a los autores aceptados de [21].
- **Redacción propuesta / alternativa de decisión:** Sin reemplazo propuesto para ninguna ficha ni cita. Solicitar separadamente PDF/DOI/URL de [16] y de [21]. Si no se acreditan, decidir revisión del argumento C12 antes de retirar o sustituir cualquier referencia.
- **¿Altera significado científico? / decisión requerida:** Sí, si se cambia identidad o respaldo del argumento. Dos decisiones bibliográficas individuales con Nathalia; no declarar inexistencia ni reemplazar [21] por coincidencia temática.

### C16 — Referencia [22], ficha y exclusividad

- **Ubicación:** A:P102/P67.
- **Texto aceptado:** «[22] S. Acıslı-Celik y C. M. Yesilkanat, “Predicting science achievement scores with ML: PISA 2015–2018,” Neural Comput. Appl., vol. 35, 2023.»
- **Problema y evidencia:** Ficha Springer enlazada en DIFF confirma identidad, vol.35, 2023, pp.21201–21228, DOI10.1007/s00521-023-08901-6. Título aceptado abreviado, páginas/DOI ausentes; la obra no prueba por sí sola que nadie audite fugas anuales.
- **Redacción propuesta / alternativa de decisión:** Completar posteriormente título exacto de la ficha editorial, pp.21201–21228 y DOI10.1007/s00521-023-08901-6, manteniendo [22] y la misma obra. No se propone nueva oración de exclusividad: remisión C12.
- **¿Altera significado científico? / decisión requerida:** Completar datos de la misma obra no cambia su identidad; revisar el uso sí puede cambiar significado científico. Por solicitud expresa, todo el asunto queda en C y requiere decisión de Nathalia, no en A.

### C17 — Definición del examen, calidad, citas normativas y agradecimiento

- **Ubicación:** A:P12/P18/P69/P79; [1]/[15]/[23]/[26].
- **Texto aceptado:** «El examen Saber Pro mide la calidad de los programas de educación superior universitaria en Colombia.» / «…cada módulo se califica con el modelo de Rasch [23] en una escala de 0 a 300 puntos, y el PROMEDIO_GLOBAL del estudiante es el promedio de esos módulos.» / «…microdatos agregados…».
- **Problema y evidencia:** DIFF §4.5: referencia ICFES genérica y obra Rasch no identifican manual/edición/página para toda la definición; usos MEN/SACES necesitan atribución precisa. DOI10.1016/j.orp.2023.100292 identifica [26], pero no acredita toda analogía de política. src/cleaning.py/A:P27 trabajan reportes agregados, por lo que «microdatos agregados» requiere precisar unidad, sin insinuar acceso individual.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «Los resultados de Saber Pro se utilizan como uno de los insumos para evaluar los programas de educación superior universitaria en Colombia.» Para agradecimiento: «Los autores agradecen al ICFES por la publicación abierta de los datos agregados de Saber Pro 2020–2024.» Sin sustitución de la definición Rasch/global hasta consultar manual. Preservar todas las citas.
- **¿Altera significado científico? / decisión requerida:** Sí para el alcance de calidad/definición; precisión terminológica sobre unidad en agradecimiento. Nathalia debe confirmar manual técnico, norma pertinente y naturaleza de datos; no se declara falsa toda frase por falta de referencia específica.

### C18 — Cobertura, distribución y fuerza de la evidencia

- **Ubicación:** A:P41/P43/P46, resultados 4.1.
- **Texto aceptado:** «…confirmando que la mayor cobertura institucional reciente no introdujo distorsiones sistemáticas en la distribución del target.»
- **Problema y evidencia:** Recuentos 411.946,127.716 y n=28.762 no son por sí solos una prueba de ausencia de sesgo de distribución. Figuras descriptivas y único holdout no acreditan significancia de diferencias ni causalidad de extremos. A:P43 reconoce necesidad futura de walk-forward; esa limitación debe permanecer.
- **Redacción propuesta / alternativa de decisión:** Condicionada: «El crecimiento de filas crudas por año incluye 411.946 filas en 2024. El panel resultante contiene 127.716 filas wide y el conjunto de prueba comprende 28.762 filas.» No añadir una nueva prueba estadística ni borrar la cautela sobre único split. Interpretaciones causales de extremos remiten a C11 y curva a C02.
- **¿Altera significado científico? / decisión requerida:** Sí: elimina inferencia de ausencia de distorsión; cifras intactas. Nathalia debe decidir si existe análisis de distribución suficiente o si corresponde mantener una descripción limitada.

### C19 — Formulación de trabajo futuro y limitaciones

- **Ubicación:** A:P71/P77, §5.5/6.2.
- **Texto aceptado:** «TF1: incorporar variables socioeconómicas externas (…) para reducir el error…»; «L7: la categoría Sin Clasificar requiere reclasificador previo.»
- **Problema y evidencia:** Trabajo futuro es explícitamente prospectivo; no demuestra que añadir variables reduzca errores ni que reclasificador sea única solución. No hay resultado experimental para estas extensiones. L1–L7 y TF1–TF6 deben mantenerse completos, incluidos walk-forward, equidad y ausencia de intervalos.
- **Redacción propuesta / alternativa de decisión:** No se propone reescritura general. Solo si se decide moderar TF1: «TF1: evaluar si la incorporación de variables socioeconómicas externas (…) reduce el error en departamentos como Sucre, Chocó y Putumayo.» Los puntos suspensivos aquí conservan la lista aceptada (Sisbén, IDH municipal, gasto por estudiante); no son texto final. Mantener L7 hasta decidir su fundamento.
- **¿Altera significado científico? / decisión requerida:** Sí, si pasa de expectativa de efecto a pregunta de evaluación. Nathalia decide si la formulación actual se entiende suficientemente como propósito; puede conservarla. No ejecutar las extensiones.

## 5. D. REVISIÓN DE REDACCIÓN POR TURNITIN

Solo D01–D03 proponen cambios de expresión sin modificar significado científico. D04 conserva los bloques claros. La localización completa de marcas aparece después: los asuntos científicos detectados al leerlas tienen como categoría única C, aunque su origen de revisión incluya Turnitin.

### D01 — Abstract y resumen: función del módulo

- **Ubicación:** A:P7/P9; IA p.3; sin cambio previo en B.
- **Texto aceptado (inglés):** «A deployable inference module with three empirical confidence flags is delivered.»
- **Redacción propuesta:** «The accompanying deployable inference module provides three empirical confidence flags.»
- **Texto aceptado (español):** «Se entrega un módulo de inferencia deployable con tres flags empíricos de confianza.»
- **Redacción propuesta:** «El módulo de inferencia desarrollado puede desplegarse y proporciona tres flags empíricos de confianza.»
- **Problema:** construcción centrada en el acto genérico de entrega; puede explicitarse la función del artefacto.
- **Evidencia:** src/inference.py y REVISION_TURNITIN R01; el módulo y sus reglas existen. No se afirma que se haya desplegado institucionalmente.
- **Justificación académica:** sujeto y función más explícitos, equivalencia bilingüe; no sustituir palabras para influir en el detector.
- **Significado científico:** no cambia. Mantiene tres flags empíricos y condición desplegable; no promete incertidumbre calibrada.
- **Decisión requerida:** revisión editorial posterior de equivalencia y aprobación de aplicación. C09/C10 siguen pendientes para otras frases del mismo resumen.

### D02 — Fuente de datos: separar volumen, unidad y estructura

- **Ubicación:** A:P27, §3.1; IA p.5.
- **Texto aceptado:** «El dataset crudo consolidado suma 1.730.805 filas distribuidas en cinco archivos anuales; cada fila corresponde a una combinación de programa académico, prueba específica y tipo de medida estadística, no a un programa individual, lo que produce una estructura long-format.»
- **Redacción propuesta:** «El dataset crudo consolidado suma 1.730.805 filas distribuidas en cinco archivos anuales. Cada fila corresponde a una combinación de programa académico, prueba específica y tipo de medida estadística, no a un programa individual. Esta organización produce una estructura long-format.»
- **Problema:** una sola oración contiene tres funciones explicativas.
- **Evidencia:** A:P27, src/cleaning.py y REVISION_TURNITIN R03. B01 explicita que el recuento histórico no se volvió a reproducir.
- **Justificación académica:** facilitar la distinción entre tamaño, unidad de registro y disposición de datos.
- **Significado científico:** no cambia hechos, cifras o agrupación. Se conserva la oración inicial con [1]/2020–2024 y la posterior con 97,3 %/PUNTAJE_GLOBAL.
- **Decisión requerida:** revisión editorial posterior. Esta separación de frases no resuelve ni sustituye C01 sobre joins.

### D03 — Métricas y método de interpretación

- **Ubicación:** últimas dos oraciones de A:P38, §3.5; IA p.6.
- **Texto aceptado:** «Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6].»
- **Redacción propuesta:** «Evaluamos los modelos con RMSE, MAE y R². Para interpretar el modelo final, utilizamos SHAP [6].»
- **Problema:** formulación abstracta que puede expresar de modo directo qué hizo el estudio.
- **Evidencia:** artefactos de evaluación/SHAP y REVISION_TURNITIN R06; se conservan exactamente métricas y cita.
- **Justificación académica:** explicitar las acciones de evaluación e interpretación, sin añadir una técnica nueva ni una garantía.
- **Significado científico:** no cambia. No modifica configuración de árboles anterior en el párrafo ni valida interpretaciones causales.
- **Decisión requerida:** revisión editorial posterior; C04 y C05 se resuelven separadamente.

### D04 — Fragmentos marcados sin razón académica para reescribir

**Texto aceptado:** palabras clave A:P10; encabezados de secciones; descripciones visuales de figuras 1/3/4, explicación de colores y métricas; advertencia de único split en A:P43; limitaciones explícitas y extensiones en A:P71/P77, salvo los matices C19.

**Problema:** no hay error demostrado por el hecho de estar marcados. **Evidencia:** mapa geométrico/visual del informe IA, registrado en REVISION_TURNITIN §A.2; consistencia de figuras/tabla demostrada en DIFF. **Redacción propuesta:** ninguna, conservar literalmente. **Significado:** sin cambio. **Decisión:** mantener términos correctos, indexación, citas, títulos y estructura. En pies con garantías de regularización o explicación causal, el asunto concreto se remite a C02/C11; no se propone editar globalmente el pie.

### 5.1 Mapa completo de fragmentos marcados a las secciones reales

«Parcial» significa que no debe atribuirse la marca al resto del párrafo. Las referencias D/C son decisiones, no conteo de detecciones. Para cada bloque, la última columna explica la razón académica real o su ausencia; textos y alternativas de los cambios propuestos están en los registros indicados.

| IA física / artículo | Sección y localizador A | Extensión de la marca | Tratamiento y razón académica |
|---|---|---|---|
| 3 / 1 | Abstract P7 | Desde «LightGBM achieves…» hasta «ICFES official publication.» | D01: aclarar función. C04/C10: interpretación y alcance; conservar métricas. La atribución ΔR² inicial no está marcada, pero C13 sigue siendo necesaria |
| 3 / 1 | Resumen P9 | Completo | D01; C04/C09/C10/C13: separar función, evidencia y alcance, sin cambiar cifras |
| 3 / 1 | Palabras clave P10 | Línea completa | D04: no hay razón de reescritura; mantener terminología |
| 3 / 1 | Introducción P12 | Solo primera oración sobre calidad | C17: indicador frente a constructo completo. El resto no se presenta como resaltado |
| 4 / 2 | Contribuciones P15 | Solo oraciones de pivot y 15 features causalmente válidas | C01/C03: precisión de decisiones metodológicas. No atribuir marca al catálogo ni a toda la contribución |
| 5 / 3 | Fuente de datos P27 | Desde «El dataset crudo consolidado suma…» hasta PUNTAJE_GLOBAL | D02: dividir explicación; B01 conserva cantidades históricas. Oración inicial de fuente no marcada |
| 5 / 3 | §3.2 P28/P29 | Encabezado y párrafo completo | C01: describir ejecución acreditada; D04 conserva título |
| 5 / 3 | §3.3 P30/P31 | Encabezado y párrafo completo | C13: atribución de ΔR² requiere evidencia de corridas; no borrar catálogo o cifras |
| 6 / 4 | Figura 1 P34 | Título descriptivo, bloque superior derecho e inferiores; no superior izquierdo ni media | D04: descripción visual útil, sin propuesta de paráfrasis |
| 6 / 4 | §3.4 P35/P36 | Encabezado y párrafo completos | C02/C03: distinguir split externo, selección interna, codificación y rezagos |
| 6 / 4 | Modelos P38 | Solo métricas y SHAP [6], últimas dos oraciones | D03: acción más directa. **500 árboles no está marcado**, C05 procede del DIFF |
| 6 / 4 | Resultados §4.1 P41 | Primera oración hasta «distribución del target»; no introducción de tabla | C18: recuentos no prueban ausencia de distorsión; no tocar Tabla 1 |
| 7 / 5 | Comparativa P43 | Desde «Esta mejora se reporta…» hasta «225 iteraciones de boosting» | D04 mantiene cautela de único split; C02 revisa garantía de no sobreajuste. Inicio comparativo y cierre no marcados |
| 7 / 5 | Figura 2 P45 | Últimas dos oraciones: 168 y regularización | D04 conserva descripción de iteración; C02 revisa fuerza de «confirma» |
| 7 / 5 | Dispersión P46 | Completo | C11/C18: distinguir observación de distribución de explicación de extremos; figura y métricas intactas |
| 8 / 6 | Figura 3 P49 | Título descriptivo y frase de extremos; no métricas intermedias | D04: no razón para reformular la descripción correcta |
| 8 / 6 | §4.2 P50/P51 | Encabezado, primera y dos últimas oraciones; «Le siguen…» sin marca | C04: interpretación de codificación y SHAP. Conservar ranking/+28 |
| 8 / 6 | Figura 4 P53 | Texto posterior a «Figura 4» | D04 conserva descripción, colores y ranking; C04 trata alcance interpretativo |
| 9 / 7 | §4.3 P55/P56 | Encabezado y párrafo completos | C08/C11: generalización de Salud y causalidad no demostrada; no reemplazar rangos |
| 9 / 7 | Figura 5 P58 | Todo después de «Figura 5» | D04 conserva descripción; C11 revisa atribución «por alta heterogeneidad interna» |
| 9 / 7 | §4.4 P59/P60 | Encabezado; inicio hasta «RMSE aprox.»; luego «El diferencial…» hasta fin. «11,4 de confianza BAJA (15,6 %)» no marcado | C07/C09/C11: procedencia de métricas, certeza y explicación Transformer. La ausencia de marca en una cifra no la valida |
| 9–10 / 7–8 | §5.1 P62/P63 | Encabezado y texto de p.9 hasta «lo que justifica que el»; continuación p.10 sin marca | C04/C14: atribuir correctamente evidencia y referencia [8] |
| 10 / 8 | §5.2 P64/P65 | Encabezado y párrafo completos | C11: condiciones observadas frente a causas aisladas; conservar [11]/[12] y valores |
| 10 / 8 | §5.3 P67 | Completo; encabezado P66 sin marca | C12–C16: precisión de novedad, atribución y bibliografía; no sustituir citas automáticamente |
| 10 / 8 | §5.4 P68/P69 | Encabezado y párrafo completos | A03 corrige typo; C04/C10/C17 revisan uso curricular, horizonte y atribución |
| 10 / 8 | Limitaciones P71 | L2–L4, L6–L7; L1 y L5 no marcados | D04 conserva límites; C19 solo revisa eventual obligatoriedad del reclasificador |
| 10 / 8 | Conclusiones P72/P74 | Título §6 y P74 completos; subtítulo P73 no marcado | C04/C10: evidencia predictiva frente a garantía operativa/impacto. Mantener resultados |
| 10–11 / 8–9 | Conclusiones P75 | En p.10 todo; en p.11 desde «El módulo…». Inicio continuado «resulta competitivo… [11] y [12]» sin marca | C07/C09/C11/C12/C13: errores de grupos, certeza, causas y contribución. No borrar resultados incómodos |
| 11 / 9 | Trabajo futuro P77 | Completo; encabezado 6.2 sin marca | D04 conserva líneas concretas; C19 contempla solo moderación de efecto esperado |
| 11 / 9 | Agradecimientos P79 | Primera línea hasta «Saber Pro»; 2020–2024 sin marca | C17: precisión de unidad agregada; mantener autores agradecidos y período |

**Controles sin marca:** referencias P81–P106 en IA pp.11–12, títulos bilingües, resto de introducción, §§2.1–2.4, celdas de Tabla 1 e imágenes no presentan resaltados IA en la revisión registrada. Se conservan; la falta de marca no certifica su exactitud. Los errores de plantilla y las referencias pendientes se corrigen o deliberan por evidencia independiente.

## 6. Cobertura del DIFF y de la revisión previa

Esta tabla comprueba que ningún cambio identificado en el DIFF queda sin categoría. Cuando un registro original mezcla objetos distintos se separan por objeto (por ejemplo, F14 distingue estadísticas incorrectas de propiedades WPS inocuas).

| Hallazgo del DIFF | Asunto único que lo resuelve |
|---|---|
| D01–D03 autoría, afiliación y correo | A01 |
| D04 joins, supresión de definiciones de capas | C01; formato de runs separado en A12 |
| D05 features, codificación, rezagos y split | C02/C03, por validación y preprocesamiento respectivamente |
| D06 árboles | C05; formato del párrafo separado en A12 |
| D07 Salud | C08 |
| D08 ortografía | A03 |
| D09 [20] | A04 |
| F01–F04 espaciado, tipografía, runs y ancho de tabla | A12 |
| F05 secciones/paginación | A13 |
| F06 estilos/defaults | A08 |
| F07/F08/F09 cabeceras | A02/A03/A13 según texto ajeno, typo o composición válida |
| F10 pie | A02 fechas, A09 caché PAGE, A11 estado desactualizado |
| F11 imágenes/relaciones | A13 geometría del logo; B02 figuras científicas; B07 medios auxiliares |
| F12 title/creator | A05 |
| F13 core heredado | A06 |
| F14 app/custom | A07 estadísticas; B07 eliminación WPS |
| F15 configuración/notas/paquete | B07; efectos accidentales específicos A08/A09/A06/A07 |
| §4.1 validación interna | C02 |
| §4.2 codificación/SHAP | C03/C04 |
| §4.3 MAE | C06 |
| §4.4 alcance, incertidumbre, causalidad, novedad, fugas, Salud y grupos | C07–C13, C04 y C18 según objeto |
| §4.5 bibliografía | A04 [20]; C14 [8]; C15 [16]/[21]; C16 [22]; C17 usos [1]/[15]/[23]/[26]; B05 resto |
| §5 registro incompleto | A14 |
| Anexos de igualdad y diferencias XML/artefactos | B02/B07 y A05–A13 cubren contenido, metadatos, formato y dependencias; no convertir cada atributo serializado inocuo en una nueva edición |

Correspondencia con las propuestas previas de REVISION_TURNITIN: R01→D01; R02→C17; R03→D02; R04→C01; R05→C02/C03/C13; R06→D03; R07→C02/C11/C18; R08→C04/C08/C11/C14; R09→C07/C09/C10; R10→C11; R11→C12/C15/C16; R12→C17. Los placeholders adicionales están en A10/A11 y los metadatos de interfaz del informe en B06.

### 6.1 Orden de ejecución posterior, sin ejecución en esta fase

1. Mantener este plan y los informes oficiales como evidencia. La recepción de Turnitin no equivale a autorización de cambios científicos.
2. Resolver las decisiones C con evidencia identificable de corrida, fuente o calendario; documentar por separado qué se aprueba y qué permanece aceptado. No reemplazar un número sin su procedencia.
3. En una fase de edición expresamente autorizada, aplicar A y únicamente los D/C aprobados; conservar citas, tablas, figuras, estructura y resultados salvo decisión científica explícita posterior.
4. Comparar la versión editada contra A y contra este plan. Renderizar DOCX, revisar todas las páginas y actualizar campos/estadísticas antes de declarar cierre editorial. No declarar ahora que el diseño final está validado.
5. El criterio de cierre es precisión académica y trazabilidad. No se estima ni exige reducción del indicador de Turnitin.

## DECISIONES PARA REUNIÓN CON NATHALIA

Ordenadas por riesgo; cada punto debe cerrar con decisión y evidencia pendiente, sin abrir experimentos durante la reunión.

1. **RMSE MEDIA/BAJA (C07/C09):** identificar predicciones y reglas que produjeron 9,1/11,4 y 2,3; acordar qué significa confianza y preservar cifras hasta reconciliar procedencia.
2. **Aporte ΔR²≈0,22 (C13):** localizar las dos ejecuciones y cambios L1–L6; decidir si se sostiene atribución conjunta al catálogo o solo comparación histórica.
3. **Validación interna (C02):** confirmar corrida sometida, separar folds/Optuna de curva por año y holdout 2024; acordar límite metodológico que debe declararse sin reentrenar.
4. **Codificación, rezagos y SHAP (C03/C04):** confirmar TargetEncoder multiclass/417 columnas, significado de NBC_129.0 y lag previo disponible; decidir interpretación válida del historial y contribuciones SHAP.
5. **Joins (C01):** vincular script y CSV aceptados; decidir inner/left y claves reales, preservando definiciones de las tres capas y población reportada.
6. **Horizonte e impacto (C10/C17):** acreditar disponibilidad de CANTIDADEVALUADOS y demás entradas un año antes; decidir alcance operativo, curricular y respaldo [15]/[26].
7. **MAE Ridge/Lasso y árboles (C06/C05):** reconciliar CSV/PKL históricos y etapas 500/168+20=188; conservar números aceptados mientras no se identifique su ejecución.
8. **Referencias y novedad (C12/C14/C15/C16):** resolver individualmente [8], [16], [21], [22] con fuentes primarias y pasajes pertinentes; decidir qué afirmación de exclusividad/transferencia es sostenible. [20] ya está resuelta editorialmente.
9. **Salud (C08):** identificar categorías que sustentan el rango y descartar una corrección parcial que mantenga 4,1 sin respaldo en Salud; no sustituir rangos en esta fase.
10. **Causalidad y fuerza de resultados (C11/C18):** decidir formulaciones sobre Transformer, heterogeneidad, regiones, extremos y cobertura; distinguir asociaciones de causas sin tocar valores, figuras o tablas.
11. **Definiciones y límites (C17/C19):** aportar manual ICFES para Rasch/global/calidad; confirmar unidad agregada del agradecimiento y formulación de reclasificador/trabajo futuro. Preservar todas las limitaciones.
12. **Cierre editorial (A01–A14, D01–D04):** acordar correcciones objetivas y tres mejoras equivalentes de redacción para una fase posterior; no usar Turnitin como objetivo de reescritura. Registrar qué queda pendiente y exigir comparación/renderizado antes del cierre.

---

**Resultado de esta fase:** plan único de revisión; propuestas no aplicadas. No se modificaron documentos, informes oficiales, resultados, modelos, presentación ni video. Las discrepancias científicas permanecen visibles y pendientes de decisión; ningún porcentaje de Turnitin se utiliza para resolverlas.
