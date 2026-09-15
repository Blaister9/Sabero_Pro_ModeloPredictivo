# Auditoría diferencial estricta del camera-ready

Fecha: 14 de septiembre de 2026, hora local de Colombia.

## Dictamen

**El camera-ready no contiene exclusivamente cambios de formato.** Cambian ocho párrafos existentes —dos de autoría/afiliación y seis del cuerpo/bibliografía— y se añade un párrafo de correos. También se sustituye ampliamente el paquete de estilos y metadatos. Los cambios de uniones, rezagos, codificación, número de árboles y generalización sobre Salud afectan la descripción científica.

La Tabla 1 conserva todas sus celdas y las cinco figuras científicas conservan sus bytes y dimensiones. Los títulos, ambos resúmenes y las conclusiones mantienen su texto. Esto no valida automáticamente las afirmaciones intactas: persisten problemas preexistentes de validación interna, codificación/SHAP, MAE, alcance y bibliografía.

Hallazgos adicionales: 241 referencias de estilo de carácter y una de tabla quedan sin definición en el DOCX nuevo; subsisten metadatos de terceros y una caché de página `61`; las reglas actuales de confianza reproducen los tamaños de grupo, pero no los RMSE citados en el paper.

No se modificaron los DOCX ni los resultados aceptados. No se entrenaron modelos, no se reescribió texto para reducir detección de IA y no se generó video. La presentación y el guion se mantuvieron sin cambios durante esta auditoría. Este informe es el único entregable creado.

## 1. Base, método y límites

- **A, original:** `entrega_congreso/Saber_pro_paper_CONGRESO_10P_FINAL.docx`. SHA-256 `5657e9af580c1c555c32128930b7c98cbeb3358cbdd511cd1b7f7ab706db7bcb`. 107 párrafos de cuerpo, una tabla, cinco figuras.
- **B, nuevo:** `outputs/CONACIC2026/CAMERA_READY_DRAFT.docx`. SHA-256 `938bcc7b9bd0cb6e4bca89bc6052a4846edc020af933b2d7adb7aa5318d360f0`. 108 párrafos de cuerpo, una tabla, cinco figuras.

Se compararon directamente texto, celdas, propiedades de párrafos y segmentos de texto, dibujos, relaciones, estilos, tema, fuentes, sección, encabezados, pies, notas y propiedades dentro de los paquetes ZIP/OOXML. `CAMBIOS_CAMERA_READY.json` se contrastó con los documentos, no se usó como única fuente de verdad. El anexo incluye las transcripciones literales de todos los párrafos modificados y las diferencias XML de todos los componentes.

**Localizadores:** A:Pn y B:Pn son índices de párrafos desde cero, incluyen párrafos vacíos y excluyen párrafos de tablas. Coinciden con `Document(...).paragraphs` e `INVENTARIO_BASE.md`. Después de insertar el correo, A:Pn corresponde a B:P(n+1) para n≥5. Se acompañan de secciones; no se infieren números de página.

Se recalcularon en memoria las predicciones de los tres PKL locales sobre las 28.762 filas de 2024, se inspeccionaron sus configuraciones y se reconstruyeron los índices de los splits. No se ejecutaron scripts de generación que sobrescriben entregables. El código ejecutable tiene prioridad sobre sus comentarios cuando discrepan. No se ha demostrado la causa histórica de cada discrepancia entre reportes.

**Límite de formato:** comparación estructural, sin un nuevo render. No se certifica ausencia de defectos visuales. `VERIFICACION_VISUAL.md` registra una inspección previa; `VERIFICACION_PAQUETE.json` declara diez páginas del PDF conservado. Ese antecedente no sustituye una nueva inspección del DOCX. Los estilos huérfanos se demuestran en OOXML aunque Word pueda mostrar el documento usando formatos de reserva.

Se adopta A como base aceptada indicada por el usuario. La auditoría previa declara que no se dispone de recibo de EasyChair que certifique por hash el archivo sometido; no se amplía esa afirmación.

**Recomendaciones:** CONSERVAR significa mantener el cambio concreto, sin aprobar todo el documento; REVERTIR significa deshacer ese cambio o su efecto accidental en una edición futura; REVISAR CON NATHALIA identifica decisiones que afectan metodología, interpretación, alcance o identificación bibliográfica. Ninguna se ejecuta aquí.

## 2. Diferencias de contenido

El anexo A transcribe completos los párrafos originales y nuevos. Aquí se separan los cambios internos, para no tratar una sustitución de párrafo como una única corrección editorial.

### D01 — Autoría, A:P3 → B:P3

- **Original:** Edwin Santiago Paz Bedoya.
- **Nuevo:** Edwin Santiago Paz Bedoya¹, Nathalia Orozco Morales¹.
- **Tipo:** metadato.
- **Motivo:** incorporar coautora; documentado previamente.
- **Evidencia:** `AUDITORIA_CAMERA_READY.md`, Base y trazabilidad; `REUNION_ASESORA.md`, punto 2; `fuentes/build_camera_ready.py`, sustitución de autores. Los registros indican confirmación de Santiago.
- **Riesgo científico:** bajo en resultados; relevante para atribución de autoría.
- **Recomendación:** **CONSERVAR**.

### D02 — Afiliación, A:P4 → B:P4

- **Original:** UNIMINUTO, Bogotá, Colombia.
- **Nuevo:** ¹UNIMINUTO Virtual – Bogotá, Colombia.
- **Tipo:** metadato.
- **Motivo:** precisar afiliación compartida.
- **Evidencia:** registros de D01 y párrafos de los DOCX.
- **Riesgo científico:** bajo; no modifica población ni institución objeto del análisis.
- **Recomendación:** **CONSERVAR**.

### D03 — Correo nuevo, B:P5

- **Original:** ausente.
- **Nuevo:** edwin.paz@uniminuto.edu, nathalia.orozco@uniminuto.edu.
- **Tipo:** metadato.
- **Motivo:** completar contacto con datos registrados como confirmados.
- **Evidencia:** `REUNION_ASESORA.md`, punto 2; inserción `email` del generador.
- **Riesgo científico:** nulo en resultados.
- **Recomendación:** **CONSERVAR**.

### D04 — Transformación de datos, sección 3.2, A:P29 → B:P30

- **Original:** declara pivot long→wide con inner join de las tres capas sobre año, institución, programa y prueba, preservando solo entidades con las tres capas presentes.
- **Nuevo:** inner join entre pruebas y global por año, institución y programa; left join de niveles añadiendo prueba a la llave. Se conserva 127.716 y target disponible al 100 %.
- **Tipo:** metodología; redacción.
- **Motivo:** corregir descripción de uniones. El generador registra una razón genérica de «corrección objetiva».
- **Evidencia:** `src/cleaning.py`, constantes KEY3/KEY4 y `_pivot_long_to_wide`; inner con global y left con niveles. CSV procesado confirma 127.716 filas. No se reconstruyó la ejecución desde los Excel crudos.
- **Riesgo científico:** medio: cambia la regla declarada de inclusión, aunque el código actual respalda el texto nuevo. Código y CSV actuales no prueban por sí solos toda la procedencia histórica de A.
- **Recomendación:** **REVISAR CON NATHALIA**.

Otros cambios dentro del mismo párrafo:

| Original → nuevo | Tipo | Motivo y evidencia | Riesgo | Recomendación |
|---|---|---|---|---|
| Se eliminan las definiciones «promedio por prueba», «target PROMEDIO_GLOBAL» y «proporciones por nivel» | redacción | Simplificación inferida; no hay motivo individual registrado. Las definiciones concuerdan con las capas del código. | Bajo; pierde precisión explicativa | **REVERTIR** esa supresión |
| «crecimiento de filas limpias por año» → «filas por año» | redacción | Descripción neutral; Figura 1 y recuentos del CSV | Bajo | **CONSERVAR** |
| Se omiten «resultante», «limpias», «del panel» y se elimina un espacio doble | redacción; formato | Simplificación asociada al reemplazo; visible en anexo A | Bajo; 127.716 y años permanecen | **CONSERVAR** |

### D05 — Ingeniería de variables, sección 3.4, A:P36 → B:P37

| Original | Nuevo | Tipo | Motivo y evidencia | Riesgo | Recomendación |
|---|---|---|---|---|---|
| «15 features causalmente válidas» | «15 variables de entrada» | alcance; metodología | Retirada de garantía amplia; motivación inferida de auditoría. Código de variables y disponibilidad de CANTIDADEVALUADOS no prueban causalidad. | Alto en garantía metodológica | **REVISAR CON NATHALIA** |
| «rezagos temporales lag_1 y lag_2» | «rezagos lag_1 y lag_2 de las observaciones anteriores disponibles» | metodología; alcance | `src/features.py:206,215,216` ordena por entidad y usa shift; se comprobaron 2.022 saltos de más de un año. | Medio: precisa horizonte efectivo de historial | **REVISAR CON NATHALIA** |
| Tendencia histórica y desviación estándar histórica | Tendencias y volatilidad histórica | redacción; metodología | Terminología más genérica; código incluye tendencia, desviación y coeficiente de variación | Bajo, pero reduce especificidad | **REVISAR CON NATHALIA** conjuntamente |
| NBC y departamento codificados con TargetEncoder | Variables categóricas; los tres modelos tabulares usan TargetEncoder | metodología | Tres pipelines locales usan el codificador; también codifican NOMBRE_PRUEBA. Se omiten nombres explícitos. | Medio para reproducibilidad | **REVISAR CON NATHALIA** |
| No se describen clases ni dimensión transformada | Modo automático multiclase, 135 valores del objetivo, 417 columnas | cifra; metodología | Inspección de los tres PKL; ver §4.2 y hashes. Son 15 entradas y 417 columnas transformadas. | Alto para interpretación SHAP; no es solo formato | **REVISAR CON NATHALIA** |
| «split temporal estricto» | «split externo» | alcance; metodología | Entrenamiento 2020–2023 y prueba 2024 se conservan; se evita extender esa separación a CV interno | Medio; no resuelve los cortes internos | **REVISAR CON NATHALIA** |

Los recuentos 98.954/28.762 y los años no cambian. La motivación general está en `AUDITORIA_CAMERA_READY.md` y el generador, pero cada efecto debe evaluarse por separado.

### D06 — Modelos, sección 3.5, A:P38 → B:P39

- **Original:** LightGBM con 50 trials Optuna y n_estimators = 500.
- **Nuevo:** 50 trials y 188 árboles finales (mejor iteración 168 + 20).
- **Tipo:** cifra; metodología.
- **Motivo:** distinguir parámetro intermedio de número final de árboles.
- **Evidencia:** `fase5_lightgbm.py:86` guarda el JSON antes de ajustar árboles; `:94–95` obtiene curva validando en 2023; `:100` aplica max(best_iter+20,100). `outputs/reports/narrativa_lgbm.txt:28–30` registra 188; el booster serializado contiene 188 árboles. A:P43 ya menciona mejor iteración 168.
- **Riesgo científico:** medio: cambia una cifra de configuración aceptada, aunque no las métricas. 500, 800, 225, 168 y 188 pertenecen a etapas o registros diferentes; no deben sustituirse indistintamente.
- **Recomendación:** **REVISAR CON NATHALIA** como corrección de configuración respaldada, conservando resultados.

### D07 — Errores por área, sección 4.3, A:P56 → B:P57

- **Original:** «Los programas de Salud concentran los errores más bajos».
- **Nuevo:** «Algunas áreas de Salud presentan errores bajos».
- **Tipo:** resultado; alcance; redacción.
- **Motivo:** matizar generalización; explícito en auditoría anterior.
- **Evidencia:** `outputs/metrics/metricas_lgbm_por_nbc.csv`: Salud Pública 11,7652; Medicina 6,2174; Optometría 4,687; Formación militar/policial 4,1089.
- **Riesgo científico:** medio. El rango 4,1–6,2 permanece en B y su extremo 4,1 no corresponde a un área de Salud identificada en ese CSV. La corrección es parcial. Tampoco las tablas prueban las explicaciones causales sobre heterogeneidad/desarrollo económico que siguen intactas.
- **Recomendación:** **REVISAR CON NATHALIA**.

### D08 — Implicaciones educativas, sección 5.4, A:P69 → B:P70

- **Original:** recoleción.
- **Nuevo:** recolección.
- **Tipo:** redacción.
- **Motivo:** corrección ortográfica.
- **Evidencia:** comparación literal y `CAMBIOS_CAMERA_READY.json`; no hay otro cambio textual en ese párrafo.
- **Riesgo científico:** nulo por la errata. Las afirmaciones intactas se revisan en §4.4.
- **Recomendación:** **CONSERVAR**.

### D09 — Referencia [20], A:P100 → B:P101

- **Original:** Anónimo; Proc. EDM, 2020; sin páginas.
- **Nuevo:** P. J. L. Adeodato y R. L. C. Silva Filho; nombre completo del 13th International Conference on Educational Data Mining; pp. 545–549.
- **Tipo:** referencia.
- **Motivo:** identificar correctamente la misma obra.
- **Evidencia:** `AUDITORIA_CAMERA_READY.md` y nueva consulta al [PDF oficial EDM 2020](https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_55.pdf), primera y última página. Título sin cambio.
- **Riesgo científico:** bajo: se identifica la misma obra, no se sustituye por otra.
- **Recomendación:** **CONSERVAR**.

## 3. Diferencias de formato y metadatos

El anexo XML proporciona los valores íntegros, incluidos cambios técnicos sin contenido científico. Cada registro distingue motivo documentado de efecto accidental.

### F01 — Espaciadores A:P1/B:P1 y A:P5/B:P6

- **Original:** párrafos vacíos, before=0 y after=40 twips, sin interlineado exacto.
- **Nuevo:** before=0, after=0, line=80, lineRule=exact.
- **Tipo:** formato.
- **Motivo:** reducir espacio vacío, explícito en `build_camera_ready.py`.
- **Evidencia:** pPr de esos párrafos y bloque «Reduce inherited empty spacer» del generador.
- **Riesgo científico:** bajo, solo maquetación.
- **Recomendación:** **CONSERVAR**.

### F02 — Formato de autor, afiliación y correo

- **Original:** autor 12 pt, Times New Roman explícita, espacio antes 120/después 40 twips; afiliación 10 pt, Times New Roman explícita, después 40; sin correo.
- **Nuevo:** autor/afiliación 12 pt, fuente heredada, antes 0/después 20; correo 12 pt centrado; marcador ¹ literal, retirada de vertAlign heredado.
- **Tipo:** formato.
- **Motivo:** reutilizar roles de plantilla; documentado en generador.
- **Evidencia:** A:P3/P4 y B:P3/P4/P5, plantilla retenida.
- **Riesgo científico:** bajo; la fuente heredada depende de F06.
- **Recomendación:** **CONSERVAR**.

### F03 — Colapso de segmentos de texto

- **Original:** A:P29 tiene dos runs; A:P38 tiene 21; los demás párrafos corregidos tienen uno.
- **Nuevo:** cada párrafo sustituido queda en un run, conservando solo propiedades del primer run original. Se pierde la diferenciación interna de idioma de A:P29.
- **Tipo:** formato.
- **Motivo:** efecto técnico de `replace_text`, sin decisión científica individual registrada.
- **Evidencia:** función `replace_text` en `build_camera_ready.py` y XML, D04–D09.
- **Riesgo científico:** bajo en texto; puede perderse formato/idioma de fragmentos.
- **Recomendación:** **REVISAR CON NATHALIA** junto con control editorial.

### F04 — Tabla 1, ancho y rejilla

- **Original:** columnas 2880/1440/1440/1440/2560 twips; total 9760.
- **Nuevo:** 2450/1350/1350/1300/2388; total 8838; ancho de tabla/celdas ajustado y layout fixed.
- **Tipo:** formato.
- **Motivo:** ajustar al ancho útil; explícito en generador.
- **Evidencia:** tblPr/tblGrid/tcPr; ancho útil 12240−1701−1701=8838. Todas las celdas textuales son idénticas.
- **Riesgo científico:** bajo; puede cambiar saltos de línea, no valores.
- **Recomendación:** **CONSERVAR**.

### F05 — Sección y numeración

- **Original:** Carta 12240×15840 twips, márgenes 1417 verticales/1701 laterales; numeración inicia en 3; referencias a pies default/even vacíos.
- **Nuevo:** mismo papel/márgenes; inicio en 1; se eliminan esas referencias a pies vacíos y cambian rId. Se omiten atributos equivalentes por defecto: portrait, una columna, charSpace=0.
- **Tipo:** formato.
- **Motivo:** adoptar geometría oficial y comenzar en 1; explícito en generador.
- **Evidencia:** sectPr y relaciones de encabezados/pies de ambos paquetes.
- **Riesgo científico:** bajo; no cambia área útil.
- **Recomendación:** **CONSERVAR**.

### F06 — Estilos, tema y fuentes: referencias huérfanas

- **Original:** IDs 17 (tlid-translation) y 3 (Normal Table) definidos. Defaults: Times New Roman/SimSun y pPrDefault sin espaciado.
- **Nuevo:** estilos/tema/fuentes de plantilla. El cuerpo sigue usando IDs 17 y 3, pero no existen en styles.xml: **241 referencias rStyle y una tblStyle**. Defaults: minorHAnsi/minorBidi, tamaño 22 (=11 pt), idioma es-MX; after=160, line=259 auto.
- **Tipo:** formato.
- **Motivo:** copiar paquete de plantilla; la pérdida de resolución de estilos es accidental, no tiene respaldo científico.
- **Evidencia:** `word/styles.xml`, `document.xml`, `theme/theme1.xml`, `fontTable.xml`; el generador copia el cuerpo sin remapear IDs de estilo.
- **Riesgo científico:** bajo en cifras, medio para representación y reproducibilidad editorial. No significa que todo el cuerpo se muestre a 11 pt: el formato directo puede prevalecer.
- **Recomendación:** **REVERTIR** el efecto accidental de referencias huérfanas, mediante una futura corrección de estilos. No implica restaurar fechas ficticias ni abandonar la plantilla. Requiere render posterior.

### F07 — Encabezado predeterminado, header1.xml

- **Original:** D. Beltrán et al. / Abstraction & Application 41 (2023) 3 - 16, en tabla.
- **Nuevo:** Saber Pro · Paz Bedoya y Orozco Morales · DRAFT; párrafo Calibri 9 pt, tabulador derecho en 8838 twips y campo PAGE con caché 2.
- **Tipo:** metadato; formato.
- **Motivo:** retirar identificación de otro artículo; explícito en generador.
- **Evidencia:** header1.xml y bloque de encabezados.
- **Riesgo científico:** bajo.
- **Recomendación:** **CONSERVAR**.

### F08 — Encabezado par, header2.xml

- **Original:** título corrido «Predicción del promedio  global de Saber Pro mediante LightGBM y auditorría de fuga temporal: Un estudio a nivel de programa académico en Colombia».
- **Nuevo:** mismo encabezado breve DRAFT y PAGE de F07.
- **Tipo:** metadato; formato.
- **Motivo:** normalización de encabezados, documentada; no cambia el título principal.
- **Evidencia:** header2.xml y generador.
- **Riesgo científico:** bajo.
- **Recomendación:** **CONSERVAR**.

### F09 — Encabezado de primera página, header3.xml

- **Original:** Abstraction & Application (2026), UADY y logo.
- **Nuevo:** Abstraction & Application · CONACIC 2026 · DRAFT, UADY y logo de plantilla.
- **Tipo:** metadato; formato.
- **Motivo:** identificar estado/evento sin inventar volumen editorial.
- **Evidencia:** header3.xml; generador y plantilla retenida.
- **Riesgo científico:** bajo.
- **Recomendación:** **CONSERVAR**; geometría del logo en F11.

### F10 — Pie de primera página y caché de numeración

- **Original:** Fecha de recepción: septiembre 1, 2020 / Fecha de aceptación: octubre 5, 2020.
- **Nuevo:** DRAFT · Pendiente de análisis de similitud e IA y revisión final; incorpora PAGE con caché **61**.
- **Tipo:** metadato; formato.
- **Motivo:** retirar fechas ficticias, explícito. La caché 61 procede de plantilla y no representa la página real.
- **Evidencia:** footer1.xml contiene instrText PAGE, separador y valor 61; settings.xml pide actualizar campos.
- **Riesgo científico:** nulo; riesgo editorial si el lector no actualiza campos.
- **Recomendación:** **CONSERVAR** la retirada de fechas; **REVERTIR** la caché heredada incorrecta en una edición posterior. La marca de pendientes no es una instrucción de evasión de detección de IA.

### F11 — Logo, imágenes y remapeo de relaciones

- **Original:** logo del paquete A, 433705×751205 EMU en encabezado; medios de A con nombres originales.
- **Nuevo:** logo de plantilla, 434123×751224 EMU; image1.png/image2.jpeg de plantilla y siete medios de A copiados con prefijo conacic_. Cinco son las figuras del cuerpo; las dos copias restantes no aparecen como figuras científicas del cuerpo.
- **Tipo:** formato.
- **Motivo:** heredar recursos oficiales y evitar colisión de relaciones; explícito en generador.
- **Evidencia:** relaciones de documento/header3, medios y anexo de hashes. Las cinco figuras del cuerpo conservan bytes y dimensiones.
- **Riesgo científico:** bajo; sin cambios de gráficas de resultados.
- **Recomendación:** **CONSERVAR**.

### F12 — Propiedades core corregidas

- **Original:** sin título/descripción; creator=Francisco Alejandro Madera Ramírez.
- **Nuevo:** título principal exacto; creator=Edwin Santiago Paz Bedoya; Nathalia Orozco Morales; description=DRAFT. No enviar. Pendiente de análisis de similitud e IA y revisión final.
- **Tipo:** metadato.
- **Motivo:** identificar artículo/autores/estado; explícito en generador.
- **Evidencia:** docProps/core.xml y bloque core del generador.
- **Riesgo científico:** nulo en resultados.
- **Recomendación:** **CONSERVAR**.

### F13 — Propiedades core heredadas indebidamente

- **Original:** lastModifiedBy=NATHALIA OROZCO MORALES; modified=2026-07-03T18:21:58.0618949Z; revision=33.
- **Nuevo:** lastModifiedBy=Raul Antonio Aguilar Vera; modified=2023-03-22T00:04:00Z; revision=30; subject/keywords vacíos. created/lastPrinted mantienen instantes de 2020 con distinta serialización.
- **Tipo:** metadato.
- **Motivo:** herencia opaca de plantilla; no existe justificación para atribuir esa edición o retrotraer fecha.
- **Evidencia:** core.xml; generador solo sustituye title/creator/description.
- **Riesgo científico:** nulo en métricas, medio en trazabilidad.
- **Recomendación:** **REVERTIR** los cambios accidentales; no inventar fechas nuevas ni autor de última edición.

### F14 — Propiedades app y custom

- **Original:** Application=Microsoft Word for the web; propiedades custom de WPS; sin estadísticas extensas.
- **Nuevo:** Application=Microsoft Office Word; Pages=3, Words=457, Paragraphs=5, Lines=20, Characters=2516, CharactersWithSpaces=2968, TotalTime=84; nuevas propiedades de estado/vacías y eliminación de custom.xml.
- **Tipo:** metadato.
- **Motivo:** sustitución por plantilla; estadísticas no recalculadas por generador.
- **Evidencia:** docProps/app.xml/custom.xml, relaciones/tipos; valores completos en anexo XML.
- **Riesgo científico:** nulo; riesgo de trazabilidad. Pages=3 no demuestra que el artículo tenga tres páginas.
- **Recomendación:** **REVERTIR** estadísticas heredadas incorrectas; **CONSERVAR** eliminación de propiedades WPS sin contenido científico. No restaurarlas solo por igualdad binaria.

### F15 — Configuración, notas y partes auxiliares

- **Original:** settings/notas separadoras de A; sin numbering.xml ni webSettings.xml; footer2/3 vacíos.
- **Nuevo:** settings de plantilla y updateFields=true; numbering/webSettings añadidos; separadores de notas sustituidos sin texto científico; footer2/3 eliminados; tipos y relaciones ajustados.
- **Tipo:** formato; metadato.
- **Motivo:** herencia técnica de plantilla/conexión de recursos; explícito en generador. No hay justificación individual para cada preferencia de Word heredada.
- **Evidencia:** anexo XML de settings, numbering, webSettings, footnotes, endnotes, relaciones y Content_Types.
- **Riesgo científico:** bajo; revisar dependencia de estilos en F06. No se identificó texto científico de notas perdido.
- **Recomendación:** **CONSERVAR** infraestructura coherente; los efectos accidentales se tratan en F06/F10/F13/F14.

## 4. Pendientes específicos

### 4.1 Validación interna

**Problema demostrado:** TimeSeriesSplit se aplica a filas ordenadas por entidad, no globalmente por año. En cada uno de los cuatro folds, ambos lados contienen 2020, 2021, 2022 y 2023. El corte posicional 80/20 de Optuna también mezcla esos cuatro años en entrenamiento/validación. Usar un objeto llamado TimeSeriesSplit no garantiza cronología por año.

**Dónde:** A:P36/B:P37 describe el split externo; el paper no dice literalmente que haya usado cuatro folds internos de TimeSeriesSplit. Las afirmaciones internas problemáticas están en `fase4_baseline.py:90–93`, su narrativa, `fase5_lightgbm.py:78` y comentarios de pipeline. Afectan la justificación de control temporal, pero no son un nuevo cambio textual del camera-ready. A:P43/B:P44 y caption P45/P46 usan la curva para afirmar regularización adecuada.

**Evidencia ejecutable:** `src/features.py:206,300,436` ordena por entidad/año; scripts leen CSV y filtran años sin ordenamiento cronológico global. `src/models/boosting.py:269–272` usa iloc 80/20 y no usa tscv en el objetivo Optuna. `src/models/baseline.py:292–298,372–384` sitúa RidgeCV/LassoCV después del preprocesador: este se ajusta antes del CV interno del estimador, no en cada fold de selección de alpha. El cross-fitting de TargetEncoder (cv=2) es otra división y no corrige esa arquitectura ni garantiza temporalidad.

La reconstrucción independiente de índices realizada aquí coincide con `VERIFICACION_DATOS_MODELOS.json.fold_years` y `optuna80_years`. No se entrenó nada.

**Matiz importante:** la curva LightGBM **sí usa un corte por año en el código actual**. `fase5_lightgbm.py:94–95` pasa val_year=2023 y df_with_year=df_train; `src/models/boosting.py:439–444` separa <2023 de 2023. Sería incorrecto afirmar que toda validación interna mezcla años. Esto no valida temporalmente Optuna ni los folds lineales. El holdout externo 2024 está separado y las predicciones se reproducen; no se cuantificó cuánto cambiaría la selección interna al corregirla.

**Riesgo alto** al afirmar garantía temporal completa. No demuestra por sí solo que las métricas externas sean falsas. **REVISAR CON NATHALIA** cómo describir el límite y separar cualquier reevaluación de la entrega aceptada.

### 4.2 Codificación

**Problema demostrado:** el objetivo es regresión, pero TargetEncoder no fija target_type=continuous. Los tres artefactos tienen target_type_=multiclass, 135 clases y 417 columnas transformadas. Los estimadores finales siguen siendo regresores; multiclase describe el preprocesamiento.

**Dónde:** D05 añade el hecho en B:P37; A:P36 solo nombra TargetEncoder. Las lecturas intactas de «efectos de intercepto por área disciplinar» (A:P51/B:P52) y «NBC con SHAP negativo» (A:P69/B:P70) deben revisarse. `outputs/reports/narrativa_lgbm.txt:40` identifica NBC_129.0 como componente importante.

**Evidencia:** tres PKL inspeccionados; `src/models/baseline.py:221`, `src/models/boosting.py:149`. Se usan 10 numéricas + 3 categóricas×135 componentes + 2 indicadores one-hot = 417, a partir de 15 entradas. cat__NBC_129.0 representa el componente de codificación de NBC para el objetivo 129; no es un identificador directo de una disciplina. Esto no demuestra que SHAP esté numéricamente mal calculado; limita la interpretación de sus etiquetas.

**Riesgo alto** en explicación. Cambiar ahora a codificación continua produciría otro modelo; no se hizo. **REVISAR CON NATHALIA**, distinguiendo implementación ejecutada de implementación deseable y conservando resultados.

### 4.3 MAE

**Problema demostrado:** los MAE de Ridge/Lasso publicados coinciden con `outputs/metrics/baseline_metrics.csv`, pero no con los PKL actuales ni con `outputs/reports/narrativa_baseline.txt:30,39`. Es una inconsistencia preexistente del repositorio.

**Dónde:** Tabla 1, filas Ridge/Lasso, columna MAE; idéntica en A/B. LightGBM sí coincide al redondeo publicado. Transformer permanece n/d.

| Modelo | A y B / CSV histórico | Recalculado aquí | A 4 decimales | Diferencia frente al aceptado |
|---|---:|---:|---:|---:|
| Ridge | 7,2967 | 7,296436898959 | 7,2964 | −0,000263101041 |
| Lasso | 7,0622 | 7,058887577037 | 7,0589 | −0,003312422963 |
| LightGBM | 6,2109 | 6,210937441010 | 6,2109 | +0,000037441010 |

**Evidencia reproducible:** e=PROMEDIO_GLOBAL−pipeline.predict(filas_2024); MAE=media(|e|). Los hashes coinciden con la verificación previa. Ridge/Lasso no difieren por el redondeo correcto de esos valores a cuatro decimales. La causa —transcripción, reporte, artefacto previo u otra— **no está establecida**; no se atribuye automáticamente a serialización.

RMSE/R² coinciden al redondeo publicado en los tres modelos. **Riesgo medio** de trazabilidad, sin evidencia aquí de cambio de ranking. **REVISAR CON NATHALIA** y conservar cifras aceptadas hasta identificar su corrida/reporte de origen.

### 4.4 Alcance

Los siguientes problemas permanecen intactos o parcialmente corregidos. No se presentan como nuevas modificaciones de B.

| Problema y ubicación A → B | Evidencia y límite | Riesgo / recomendación |
|---|---|---|
| «Un año de anticipación», P69→70/P74→75; intervención antes de publicación, P7→8/P9→10 | `src/features.py:484–485` usa CANTIDADEVALUADOS del registro corriente sin rezago. El comentario dice disponible antes de resultados, pero no prueba disponibilidad un año antes. El corte externo prueba evaluación retrospectiva; no calendario operativo de cada entrada. Hay 2.022 saltos de historial >1 año. | Alto; **REVISAR CON NATHALIA** momento real de predicción y disponibilidad |
| Cuantificación de incertidumbre, P14→15; confianza, P60→61/P75→76 | `src/inference.py:588–606` implementa reglas, no intervalos calibrados. Ver discrepancia de RMSE de grupos debajo. | Alto; **REVISAR CON NATHALIA** |
| Interpretación causal de SHAP, errores regionales y causas de desempeño Transformer, P51→52/P56→57/P63→64/P65→66/P69→70 | SHAP explica predicciones; tablas agrupan errores. `decision_transformer.txt` documenta una configuración, no una ablación controlada de cuatro causas. No hay en la evidencia examinada una estimación causal de impacto curricular/desarrollo regional. | Alto en interpretación; **REVISAR CON NATHALIA** |
| Exclusividad/novedad, P14→15/P67→68/P75→76 | «No existe», «ningún trabajo previo», «inédita» dependen de referencias inciertas, especialmente [16]/[21]. Búsquedas sin coincidencia no prueban ausencia universal. | Alto; **REVISAR CON NATHALIA** |
| ΔR²≈0,22 atribuido a catálogo L1–L6, P31→32/P67→68/P75→76 | Comparar históricamente ≈0,88→0,658 da ≈0,22; no aísla seis efectos individuales. P31 menciona percentiles ausentes de las 15 entradas finales; hace falta enlazar cada fuga con su ejecución histórica. Esa ausencia no prueba que nunca se usaran. | Alto; **REVISAR CON NATHALIA** |
| Generalización de Salud, P56→57 | CSV contradice universalidad y extremo ≈4,1 para Salud; D07 es parcial | Medio; **REVISAR CON NATHALIA** |

**Hallazgo adicional de confianza:** se ejecutó en memoria `src.inference.predict_batch` con LightGBM local y CSV 2024. Se reproducen los tamaños de `outputs/reports/demo_inferencia.txt:32–33`, pero no los errores de P60/P75:

| Grupo | Filas verificadas | RMSE aceptado, A y B | RMSE de reglas/artefacto actuales |
|---|---:|---:|---:|
| MEDIA | 24.288 (84,4 %) | ≈9,1 | 6,596797235424 |
| BAJA | 4.474 (15,6 %) | ≈11,4 | 17,980199345751 |

El diferencial aceptado es ≈2,3; aquí ≈11,3834. Ponderar cuadrados de 9,1 y 11,4 por esos tamaños implica RMSE total ≈9,49, frente a 9,3293 publicado. Esto requiere reconciliar procedencia, **no sustituir resultados en el paper**. La dirección —BAJA tiene mayor error— coincide. No está demostrada la causa histórica. El código marca extrapolación para todo 2024 por MAX_AÑO_TRAIN=2023, explicando que no aparezca ALTA. Los flags no constituyen probabilidades calibradas.

### 4.5 Bibliografía

Solo [20] cambia. Las otras 25 entradas y las citas en el cuerpo permanecen. Identificar correctamente la misma obra no equivale a reemplazar una referencia incierta por una de título parecido.

| Referencia y ubicación | Problema exacto / evidencia | Recomendación |
|---|---|---|
| [20], A:P100/B:P101 | D09 está respaldado por PDF oficial: autores, evento y pp. 545–549 | **CONSERVAR** |
| [8], A:P88/B:P89; discusión P63→64 | Dice J. Behr, J. Educ. Comput. Res. 60(5), 1109–1148, 2022. Manuscrito institucional identifica Andreas Behr, Marco Giese, Herve D. Teguim K., Katja Theune; anexo de tesis identifica publicación de 2020 en Jahrbücher für Nationalökonomie und Statistik. Contradicción de inicial, revista/año, no solo falta de DOI. La tesis no cierra volumen/páginas definitivos. | **REVISAR CON NATHALIA** ficha de la misma obra y pertinencia de la afirmación |
| [16], A:P96/B:P97; P67→68 | Sin coincidencia exacta de título/autores en búsquedas realizadas. Su repetición en `paper/revised/paper_content.py:873` es fuente interna derivada, no verificación. Falta DOI/URL/PDF identificable. | **REVISAR CON NATHALIA**; no declararla inexistente |
| [21], A:P101/B:P102; P67→68 y marco teórico | Ficha Chafla/Morocho/Ortega no identificada. Artículo similar Frontiers 2025, DOI 10.3389/feduc.2025.1632315, tiene autores Guevara-Reyes, Ortiz-Garcés, Andrade, Cox-Riquetti y Villegas-Ch. No coincide con autores/título exactos aceptados. | **REVISAR CON NATHALIA**; no reemplazar automáticamente |
| [22], A:P102/B:P103; P67→68 | Springer confirma obra de Acıslı-Celik/Yesilkanat, 2023, vol. 35, pp. 21201–21228, DOI 10.1007/s00521-023-08901-6. El paper abrevia título y omite páginas/DOI. Identidad ahora comprobada; no se ha demostrado la exclusividad global sobre auditoría de fugas que apoya P67. | **REVISAR CON NATHALIA** argumento; completar ficha posteriormente |
| [1]/[23], A:P81/P103 → B:P82/P104; introducción P12→13 | P12 vincula Rasch, escala 0–300 y promedio de módulos al puntaje global. Ficha genérica ICFES y referencia histórica Rasch no indican manual técnico/edición/página que pruebe esa definición operativa. | **REVISAR CON NATHALIA** con manual ICFES específico; falta respaldo preciso, no se declara falsa cada frase |
| [26], A:P106/B:P107; P69→70 | Registro institucional identifica título y DOI 10.1016/j.orp.2023.100292. No verifica por sí solo toda la analogía de política educativa. | Identificación apoyada; **REVISAR CON NATHALIA** cualquier cambio de alcance |
| [2–7], [9–15], [17–19], [24–25] | Texto idéntico; no se validaron externamente todas las fichas y cada cita contextual. No se certifica toda la bibliografía como verificada. | **CONSERVAR** en este diferencial; validación integral pendiente si se requiere certificación |

Fuentes primarias consultadas para los hallazgos anteriores:

- [EDM 2020, Adeodato y Silva Filho](https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_55.pdf), primera/última página.
- [Tesis de Marco Giese, Duisburg-Essen](https://duepublico2.uni-due.de/servlets/MCRFileNodeServlet/duepublico_derivate_00074078/Diss_Giese.pdf), capítulo 4 y anexo de contribuciones.
- [Frontiers, artículo con título similar a [21]](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1632315/full), autoría visible; no se equipara con la ficha aceptada.
- [Springer, Acıslı-Celik y Yesilkanat](https://link.springer.com/article/10.1007/s00521-023-08901-6), ficha editorial.
- [Universitat de València, registro de [26]](https://producciocientifica.uv.es/documentos/6574e34dc27a3a35855955ee?lang=eu).

Consultas sin coincidencia exacta: combinación Rangel-Mora/Pérez-Roa con Saber y título [16]; Chafla/Morocho/Ortega con Frontiers 2025, rendimiento y explainability. Un resultado negativo no prueba inexistencia.

## 5. Conservación, trazabilidad y decisiones

`CAMBIOS_CAMERA_READY.json` coincide exactamente con los seis cambios D04–D09. Omite autoría/correo y modificaciones de formato/paquete. Su razón genérica «Corrección objetiva documentada…» no distingue metodología, supresión editorial ni efectos técnicos accidentales; no constituye inventario completo.

No cambian títulos, resúmenes, tabla, captions ni sección de conclusiones/trabajo futuro. «Sin cambio» no significa «sin pendientes científicos». Los anexos documentan identidad de tabla/figuras y hashes de modelos/CSV.

Para revisión con Nathalia:

1. Decidir por separado sobre uniones, codificación/SHAP, rezagos, número final de árboles y alcance de Salud.
2. Reconciliar MAE lineales y RMSE por grupos de confianza sin sustituir cifras aceptadas ni reentrenar en este cierre.
3. Resolver anticipación, incertidumbre, causalidad y novedad; identificar [8]/[16]/[21] y completar [22].
4. En una edición editorial posterior, resolver estilos huérfanos, propiedades heredadas y cachés de campos; renderizar y revisar antes de declarar formato cerrado.

No se registra aprobación de Nathalia ni decisión del comité. Ninguna recomendación se ejecutó durante esta auditoría.


## Anexo A. Texto completo de cada diferencia

Transcripción directa de los DOCX. Motivo, evidencia, tipo, riesgo y recomendación: registros D01–D09 de §2. Se preserva el texto, incluido el contenido que no cambió dentro de cada párrafo.

### D01, A:P3 → B:P3

**Original**

> Edwin Santiago Paz Bedoya

**Nuevo**

> Edwin Santiago Paz Bedoya¹, Nathalia Orozco Morales¹

### D02, A:P4 → B:P4

**Original**

> UNIMINUTO, Bogotá, Colombia.

**Nuevo**

> ¹UNIMINUTO Virtual – Bogotá, Colombia

### D04, A:P29 → B:P30

**Original**

> Los archivos ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo de estadística de cada fila. Se identificaron tres capas utilizables: (a) PUNTAJE_PRUEBA, promedio por prueba; (b) PUNTAJE_GLOBAL, target PROMEDIO_GLOBAL; y (c) NIVEL_DESEMPEÑO_PRUEBA, proporciones por nivel. Se aplicó un pivot long→wide con inner join sobre la llave (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA), preservando únicamente entidades con las tres capas presentes. El resultado es 127.716 filas wide con el target disponible al 100 %.  La Figura 1 ilustra la distribución del PROMEDIO_GLOBAL resultante, el crecimiento de filas limpias por año y las pruebas y NBCs más frecuentes del panel.

**Nuevo**

> Los archivos ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo de estadística de cada fila. Se identificaron tres capas utilizables: PUNTAJE_PRUEBA, PUNTAJE_GLOBAL y NIVEL_DESEMPEÑO_PRUEBA. Se unieron las pruebas con el puntaje global mediante inner join por año, institución y programa; los niveles se añadieron mediante left join incluyendo NOMBRE_PRUEBA. El resultado es 127.716 filas wide con el target disponible al 100 %. La Figura 1 ilustra la distribución del PROMEDIO_GLOBAL, las filas por año y las pruebas y NBCs más frecuentes.

### D05, A:P36 → B:P37

**Original**

> Se construyeron 15 features causalmente válidas: rezagos temporales lag_1 y lag_2 del PROMEDIO_GLOBAL y de cada prueba, tendencia histórica, desviación estándar histórica, logaritmo del número de evaluados, año, identificadores de NBC y departamento codificados con TargetEncoder. El split temporal estricto usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas).

**Nuevo**

> Se emplearon 15 variables de entrada: rezagos lag_1 y lag_2 de las observaciones anteriores disponibles del PROMEDIO_GLOBAL y de cada prueba, tendencias, volatilidad histórica, logaritmo del número de evaluados, año y variables categóricas. Los tres modelos tabulares usan TargetEncoder; en los artefactos evaluados, su modo automático produjo codificación multiclase (135 valores del objetivo), con 417 columnas transformadas en total. El split externo usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas).

### D06, A:P38 → B:P39

**Original**

> Finalmente se evaluaron cuatro familias: (1) Ridge con α automático (RidgeCV); (2) Lasso con α automático (LassoCV); (3) LightGBM con 50 trials de búsqueda Optuna [4] y n_estimators = 500; (4) Transformer encoder con early stopping (época 53/200). Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6].

**Nuevo**

> Finalmente se evaluaron cuatro familias: (1) Ridge con α automático (RidgeCV); (2) Lasso con α automático (LassoCV); (3) LightGBM con 50 trials de búsqueda Optuna [4] y 188 árboles en el artefacto final (mejor iteración 168 + 20); (4) Transformer encoder con early stopping (época 53/200). Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6].

### D07, A:P56 → B:P57

**Original**

> La Figura 5 desagrega el RMSE de LightGBM por Núcleo Básico del Conocimiento (top 25), revelando diferencias sustanciales entre áreas disciplinares. Los programas de Salud concentran los errores más bajos (RMSE entre 4,1 y 6,2 puntos), mientras que Educación (RMSE = 11,71) y Sin Clasificar (RMSE = 17,76) concentran los más altos, explicados por la alta heterogeneidad interna de esas categorías. El análisis geográfico complementario muestra que Sucre (≈ 13), Chocó (≈ 12) y Putumayo (≈ 11) presentan los mayores errores, coincidiendo con regiones de menor desarrollo económico relativo.

**Nuevo**

> La Figura 5 desagrega el RMSE de LightGBM por Núcleo Básico del Conocimiento (top 25), revelando diferencias sustanciales entre áreas disciplinares. Algunas áreas de Salud presentan errores bajos (RMSE entre 4,1 y 6,2 puntos), mientras que Educación (RMSE = 11,71) y Sin Clasificar (RMSE = 17,76) concentran los más altos, explicados por la alta heterogeneidad interna de esas categorías. El análisis geográfico complementario muestra que Sucre (≈ 13), Chocó (≈ 12) y Putumayo (≈ 11) presentan los mayores errores, coincidiendo con regiones de menor desarrollo económico relativo.

### D08, A:P69 → B:P70

**Original**

> El SACES colombiano incorpora Saber Pro como insumo central para registro calificado y acreditación [15]. Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva. Esta lógica es análoga a la propuesta por López-García et al. [26] para detección de fracaso estudiantil en la Universidad Industrial de Santander, aunque el presente trabajo opera a nivel programa-institución, complementándola. Los NBC con SHAP negativo y los departamentos con mayor RMSE señalan prioridades concretas de intervención y de recoleción de datos socioeconómicos externos.

**Nuevo**

> El SACES colombiano incorpora Saber Pro como insumo central para registro calificado y acreditación [15]. Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva. Esta lógica es análoga a la propuesta por López-García et al. [26] para detección de fracaso estudiantil en la Universidad Industrial de Santander, aunque el presente trabajo opera a nivel programa-institución, complementándola. Los NBC con SHAP negativo y los departamentos con mayor RMSE señalan prioridades concretas de intervención y de recolección de datos socioeconómicos externos.

### D09, A:P100 → B:P101

**Original**

> [20] Anónimo, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. EDM, 2020.

**Nuevo**

> [20] P. J. L. Adeodato y R. L. C. Silva Filho, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. 13th International Conference on Educational Data Mining, 2020, pp. 545–549.

### D03, inserción B:P5

**Original:** ∅

**Nuevo**

> edwin.paz@uniminuto.edu, nathalia.orozco@uniminuto.edu

## Anexo B. Controles de conservación y métricas

Las predicciones y lecturas de esta auditoría corroboraron los siguientes valores/hashes del informe previo, sin guardar predicciones ni modificar el JSON.

| Artefacto | SHA-256 |
|---|---|
| outputs/ridge_model.pkl | `36289ba5ff5f4792d7e17e63790bf8082e4c7d47ce7aa385eb245d1d6faf3555` |
| outputs/lasso_model.pkl | `4dd090dbe17b2b6ba46ad91398fc6468688d7b8f0e30aefceec2b8285386bc1c` |
| outputs/lgbm_model.pkl | `0c3094932c9f511e31e09a2b659aa787de10725ef09fa4a81c874ff320b1150d` |
| data/processed/saber_pro_features.csv | `01d43c09f449f6868009188fddc961512e025798212129787e1f79ec9dd035ee` |

| Modelo | RMSE recalculado | R² recalculado |
|---|---:|---:|
| ridge | 10.229386307306 | 0.646746635002 |
| lasso | 10.072242497108 | 0.657516625245 |
| lgbm | 9.329341949418 | 0.706174711597 |

Transformer se contrastó solo con `outputs/reports/decision_transformer.txt`, sin ejecución nueva. Ese reporte distingue 53 épocas completadas de mejor época 33; no convertir «época 53/200» en «mejor época 53».

### Tabla 1, contenido idéntico

| Modelo | RMSE | MAE | R² | Config. |
|---|---:|---:|---:|---|
| Ridge (ref.) | 10,2294 | 7,2967 | 0,6467 | RidgeCV |
| Lasso (ref.) | 10,0722 | 7,0622 | 0,6575 | LassoCV |
| LightGBM (prop.) | 9,3293 | 6,2109 | 0,7062 | Optuna 50t |
| Transformer enc. | 16,8588 | n/d | 0,0405 | early stop ép.53 |

### Cinco figuras, bytes y dimensiones idénticos

| Figura | SHA-256 de la imagen en A y B | Dimensiones EMU en ambos |
|---|---|---|
| 1 | `573dd59c8d428c36be4356131d3c7a17379ab630f97eba3186f5015fbefd4438` | 4370070 × 3177540 |
| 2 | `1c2bc51fa385254a80bee621fcf61f629464583558f1159392d61ba5dff36168` | 3950335 × 1946910 |
| 3 | `171942cbbaefe0e2618b2f2353382b25ffe60554c1d6f4810348f53aa1e5e50d` | 2673350 × 2665095 |
| 4 | `ea18539c74d5183e7ca5c6ad5c619944e6c274dc96d507742f17f90ea6c13984` | 2942646 × 2769583 |
| 5 | `3d2405ca77232d85ad0899358b064ddcaf81adfd5df8e69488f92f699bd0ed23` | 3199130 × 2785745 |

La secuencia de figuras y sus captions permanece. Los cambios de maquetación pueden moverlas de página; la identidad binaria no certifica la ubicación visual final.

## Anexo C. Inventario completo del paquete

Cada fila identifica contenido original/nuevo por hash de bytes descomprimidos. Las altas/bajas de medios no implican pérdida de figuras: véase anexo B y remapeo de relaciones. Motivo, riesgo y recomendación corresponden al registro D/F indicado. El anexo D detalla cada diferencia XML.

| Parte | Estado | Original SHA-256 | Nuevo SHA-256 | Registro |
|---|---|---|---|---|
| [Content_Types].xml | modificada | `e833ae02892461573b7e6ae400a07cd7cc3728cb5cede678246b320351f736c1` | `23fba0adea05203b550f0913139245e75950d935370d2b7f766583f846466b56` | F15 |
| _rels/.rels | modificada | `c6bab4bd55e95630b507ea5c0f1aeb46124705d793a14f15de67eca266b21ca4` | `e19238d7a71fa7a2490776252686f70e2de6238c87cd509b5e3a3cc07c2ea4df` | F15 |
| docProps/app.xml | modificada | `46ae4755d14dc08964c1be1ad5cf275db9dd65d1b2abeb4eedac9278a955347b` | `63eaf5c02afc57b96f904544db568c3925d3715d675fd0f76ddc35f741160dc8` | F14 |
| docProps/core.xml | modificada | `45227b9f4c2306605e4854c2561f521944e0de4524cf8203a9f38641bde35b3e` | `7472138bc2e0e9c1b75e8b4a986ad8706d72b66bdc5f31eb1133d19c03be6f9b` | F12–F13 |
| docProps/custom.xml | eliminada | `e35f5ff0c619fd7687a63547e3012aae999b4f46c3092d3c3f7608114c0c482d` | ∅ | F14 |
| word/_rels/document.xml.rels | modificada | `b6fec96ae5d630a01095221e6a9431d2eca8015cf18da6b7058d1d123cd8c1e9` | `6e79921cbfe78728bcd8011a0345ef7173eebf6203f690b59d60fde3258213e9` | F15 |
| word/_rels/header3.xml.rels | modificada | `f506b4d8a8992a8851d24c90dbf352e1035a592fad1d436f511fa6336773f617` | `ccca8dda585f688e5b105cdfde8612dd6ebfcd0b9e44cf135f45eea5b2fbaa45` | F11 |
| word/document.xml | modificada | `feb70cb38baa36641e5a68f120a8aa72d9ca5749f11edba1723a24309ff9e0a1` | `35feb25bf43d55de7d56364d29852e295e3f25d41df80d091d8a7ac7344a1aea` | D01–D09, F01–F06, F11 |
| word/endnotes.xml | modificada | `a3d4ddaa44472bb2629c3a86001609142cf5333d5ecf0898e5aac7f5a0350dc4` | `14927aefaa2a00a8efdfb0b21ad49f60c632b3aecd8b564f0c145e0d94cbc14b` | F15 |
| word/fontTable.xml | modificada | `0b1835b857ebda34f6f663e83f28b6d0a8c82a61f1d23a08fcfb1a253c569c6b` | `1e9045b8b0b4d389bef8d2bf24a33dd9189518ca89d5059eaf89509dadc01c63` | F06 |
| word/footer1.xml | modificada | `3696f2d49d0addc575f49b131a58c246cacc4f6e45b9b77a6eb7587b85eb7301` | `9a7cebdd60b242b8572211595f9de117fbe43283ac4d6600429d57f318985091` | F10 |
| word/footer2.xml | eliminada | `4e0e16aba8c4eeb1905d20a1a5e960abda9f398c49cc1e1d059d037ff7f7c500` | ∅ | F15 |
| word/footer3.xml | eliminada | `e6586e4c7e87510cfca787f155777560a31e5cde452ec8240eaac4bc2f6af662` | ∅ | F15 |
| word/footnotes.xml | modificada | `5e56b401ea986a33030e0f14786b7d9bccb6e1987de1c611e327312b4eb8c8db` | `1febac1c1d2d7ee52ab664990470281e78d57cc8da3cdc8a79545d5f52f3f11e` | F15 |
| word/header1.xml | modificada | `8efbbe9f4978b7b65a4118ab06f763f36e4b16a5d3aff03bcdd1dfa160fac287` | `49666b7fa1e64049965f7cb3d2e4fc4d65258f2232b6ffcbe90c64854a00ac2e` | F07 |
| word/header2.xml | modificada | `7c2074bf623b51a78b9d0f75ce4398f762612745d75e7d260503203d9258bef7` | `49666b7fa1e64049965f7cb3d2e4fc4d65258f2232b6ffcbe90c64854a00ac2e` | F08 |
| word/header3.xml | modificada | `1fa700d61918b97f4d03d8e246c43010c46850a1a8fc1ba5ca33924cae274f79` | `654886f80b5ef9f423d67a3970576188fb62b98ea4269cf296fe1b9edcec87b5` | F09/F11 |
| word/media/conacic_image2.jpeg | añadida | ∅ | `573dd59c8d428c36be4356131d3c7a17379ab630f97eba3186f5015fbefd4438` | F11 |
| word/media/conacic_image3.jpeg | añadida | ∅ | `1c2bc51fa385254a80bee621fcf61f629464583558f1159392d61ba5dff36168` | F11 |
| word/media/conacic_image4.jpeg | añadida | ∅ | `171942cbbaefe0e2618b2f2353382b25ffe60554c1d6f4810348f53aa1e5e50d` | F11 |
| word/media/conacic_image5.jpeg | añadida | ∅ | `ea18539c74d5183e7ca5c6ad5c619944e6c274dc96d507742f17f90ea6c13984` | F11 |
| word/media/conacic_image6.jpeg | añadida | ∅ | `3d2405ca77232d85ad0899358b064ddcaf81adfd5df8e69488f92f699bd0ed23` | F11 |
| word/media/conacic_image7.jpeg | añadida | ∅ | `cc2f0ae174e55a4ccf55eb034789af83590ae4ea368192ff7bc404ad5f5de075` | F11 |
| word/media/conacic_image8.jpeg | añadida | ∅ | `6ab313927e3dae6757f0ae4c2e0785aedd107218aaf546d7e32c1984b19e140b` | F11 |
| word/media/image1.jpeg | eliminada | `7c926f74eef1635fb5390134159b2d08974ec7845bbc3dc94ef41d96ad844193` | ∅ | F11 |
| word/media/image1.png | añadida | ∅ | `df87b253b719e996da78cdf1ae566816dfe3e1f9416a651d93c92619eed237f3` | F11 |
| word/media/image2.jpeg | modificada | `573dd59c8d428c36be4356131d3c7a17379ab630f97eba3186f5015fbefd4438` | `7c926f74eef1635fb5390134159b2d08974ec7845bbc3dc94ef41d96ad844193` | F11 |
| word/media/image3.jpeg | eliminada | `1c2bc51fa385254a80bee621fcf61f629464583558f1159392d61ba5dff36168` | ∅ | F11 |
| word/media/image4.jpeg | eliminada | `171942cbbaefe0e2618b2f2353382b25ffe60554c1d6f4810348f53aa1e5e50d` | ∅ | F11 |
| word/media/image5.jpeg | eliminada | `ea18539c74d5183e7ca5c6ad5c619944e6c274dc96d507742f17f90ea6c13984` | ∅ | F11 |
| word/media/image6.jpeg | eliminada | `3d2405ca77232d85ad0899358b064ddcaf81adfd5df8e69488f92f699bd0ed23` | ∅ | F11 |
| word/media/image7.jpeg | eliminada | `cc2f0ae174e55a4ccf55eb034789af83590ae4ea368192ff7bc404ad5f5de075` | ∅ | F11 |
| word/media/image8.jpeg | eliminada | `6ab313927e3dae6757f0ae4c2e0785aedd107218aaf546d7e32c1984b19e140b` | ∅ | F11 |
| word/numbering.xml | añadida | ∅ | `816e43e4f869b65fef7aa7ae9c67bba1062ea9ae3446c7e25d333c0979504d51` | F15 |
| word/settings.xml | modificada | `0d8f5ee5504b83c6f172f5eccc4841d269b123e315b4b5cf1d8fb183cd7c28aa` | `025c6c08dffe9c914d3c1ac6d183e0050f178d6d49cc4d9b6a9afe3ee0d80ec0` | F15 |
| word/styles.xml | modificada | `fb63f12e82afe0ff24716d25bfd2c74dd411680647d8557d3891e88c9f57c90c` | `ca8e49cbd0718fb137f5ace32e61e6a6ff281b900aece021da20ecc25a93b4ae` | F06 |
| word/theme/theme1.xml | modificada | `c5977ec7928f56c4fef2e45d4b2f38cd935e1ef20a2ac686f195956e08440e04` | `13d22b45f33b95b79904c5f70b7dd6d311819ee829ee0142bae7044d204e65d7` | F06 |
| word/webSettings.xml | añadida | ∅ | `4059b85fcb46ab00d39a03774e58681c144594236f3c39efe70601b36917eb76` | F15 |

<details><summary>Metadatos ZIP por entrada, original → nuevo</summary>

```text
[Content_Types].xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=2383; comprimidos=407; método=8; CRC=1185735083; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=2322; comprimidos=419; método=8; CRC=1969897136; atributos=25165824
_rels/.rels
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=736; comprimidos=246; método=8; CRC=3255008058; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=590; comprimidos=233; método=8; CRC=3071971614; atributos=25165824
docProps/app.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=576; comprimidos=275; método=8; CRC=2429098834; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=989; comprimidos=477; método=8; CRC=2108031509; atributos=25165824
docProps/core.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=683; comprimidos=389; método=8; CRC=951867930; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=1054; comprimidos=589; método=8; CRC=3652601304; atributos=25165824
docProps/custom.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=754; comprimidos=404; método=8; CRC=2366272288; atributos=25165824
  B: ∅
word/_rels/document.xml.rels
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=2676; comprimidos=394; método=8; CRC=2717050352; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=2897; comprimidos=412; método=8; CRC=178137344; atributos=25165824
word/_rels/header3.xml.rels
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=289; comprimidos=180; método=8; CRC=1305411636; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=290; comprimidos=180; método=8; CRC=777967115; atributos=25165824
word/document.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=99215; comprimidos=15260; método=8; CRC=2513872096; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=89520; comprimidos=15419; método=8; CRC=2248141988; atributos=25165824
word/endnotes.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=1823; comprimidos=499; método=8; CRC=230784213; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=3015; comprimidos=689; método=8; CRC=1147494395; atributos=25165824
word/fontTable.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=3144; comprimidos=653; método=8; CRC=686118906; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=2765; comprimidos=655; método=8; CRC=870935490; atributos=25165824
word/footer1.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=2087; comprimidos=597; método=8; CRC=72666016; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=3531; comprimidos=926; método=8; CRC=3313809171; atributos=25165824
word/footer2.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=1665; comprimidos=528; método=8; CRC=567518621; atributos=25165824
  B: ∅
word/footer3.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=1665; comprimidos=529; método=8; CRC=1779288037; atributos=25165824
  B: ∅
word/footnotes.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=1879; comprimidos=513; método=8; CRC=489130952; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=3021; comprimidos=690; método=8; CRC=2004493367; atributos=25165824
word/header1.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=3875; comprimidos=852; método=8; CRC=1878527266; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=525; comprimidos=311; método=8; CRC=3763010902; atributos=25165824
word/header2.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=2001; comprimidos=663; método=8; CRC=4059208253; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=525; comprimidos=311; método=8; CRC=3763010902; atributos=25165824
word/header3.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=5752; comprimidos=1366; método=8; CRC=3366953430; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=6205; comprimidos=1579; método=8; CRC=3566640653; atributos=25165824
word/media/conacic_image2.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=87760; comprimidos=67165; método=8; CRC=1066196957; atributos=25165824
word/media/conacic_image3.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=28894; comprimidos=19615; método=8; CRC=1194402134; atributos=25165824
word/media/conacic_image4.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=33955; comprimidos=25368; método=8; CRC=2704715966; atributos=25165824
word/media/conacic_image5.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=50640; comprimidos=44439; método=8; CRC=4024654691; atributos=25165824
word/media/conacic_image6.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=74927; comprimidos=54430; método=8; CRC=1030006745; atributos=25165824
word/media/conacic_image7.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=50985; comprimidos=22398; método=8; CRC=961916443; atributos=25165824
word/media/conacic_image8.jpeg
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=38522; comprimidos=25169; método=8; CRC=3641919690; atributos=25165824
word/media/image1.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=15128; comprimidos=14782; método=8; CRC=4240479564; atributos=25165824
  B: ∅
word/media/image1.png
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=64360; comprimidos=61619; método=8; CRC=3329673542; atributos=25165824
word/media/image2.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=87760; comprimidos=67165; método=8; CRC=1066196957; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=15128; comprimidos=14782; método=8; CRC=4240479564; atributos=25165824
word/media/image3.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=28894; comprimidos=19615; método=8; CRC=1194402134; atributos=25165824
  B: ∅
word/media/image4.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=33955; comprimidos=25368; método=8; CRC=2704715966; atributos=25165824
  B: ∅
word/media/image5.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=50640; comprimidos=44439; método=8; CRC=4024654691; atributos=25165824
  B: ∅
word/media/image6.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=74927; comprimidos=54430; método=8; CRC=1030006745; atributos=25165824
  B: ∅
word/media/image7.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=50985; comprimidos=22398; método=8; CRC=961916443; atributos=25165824
  B: ∅
word/media/image8.jpeg
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=38522; comprimidos=25169; método=8; CRC=3641919690; atributos=25165824
  B: ∅
word/numbering.xml
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=19528; comprimidos=1274; método=8; CRC=471988978; atributos=25165824
word/settings.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=7055; comprimidos=1999; método=8; CRC=3729333710; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=6953; comprimidos=1907; método=8; CRC=2454834639; atributos=25165824
word/styles.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=16548; comprimidos=2412; método=8; CRC=110452457; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=34560; comprimidos=3748; método=8; CRC=1392703130; atributos=25165824
word/theme/theme1.xml
  A: fecha=(2026, 7, 8, 18, 17, 38); bytes=6568; comprimidos=1336; método=8; CRC=2370820352; atributos=25165824
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=6801; comprimidos=1538; método=8; CRC=884922582; atributos=25165824
word/webSettings.xml
  A: ∅
  B: fecha=(2026, 9, 14, 19, 57, 16); bytes=19219; comprimidos=972; método=8; CRC=893383816; atributos=25165824
```

Tipo: metadato de contenedor. Motivo: reconstrucción del ZIP por generador. Evidencia: directorio ZIP. Riesgo científico nulo por sí solo. Recomendación: CONSERVAR empaquetado, salvo contenido problemático identificado en los registros principales.

</details>

## Anexo D. Diferencias XML exhaustivas

Formato unificado: `-` original y `+` nuevo. Se normalizan prefijos y orden de atributos; se conservan todos los nodos, atributos y textos significativos. Se omiten el envoltorio de declaración XML, prefijos redundantes y whitespace de indentación entre etiquetas. Se conservan los atributos de edición rsid/paraId/textId aunque no alteren contenido científico. El tratamiento de cada diferencia técnica se hereda del registro D/F señalado; no implica una autorización nueva. 20 twips=1 pt; w:sz se mide en medios puntos; 914400 EMU=1 pulgada.

<details><summary>Clave de namespaces de los anexos XML</summary>

```text
w = http://schemas.openxmlformats.org/wordprocessingml/2006/main
r = http://schemas.openxmlformats.org/officeDocument/2006/relationships
a = http://schemas.openxmlformats.org/drawingml/2006/main
wp = http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing
pic = http://schemas.openxmlformats.org/drawingml/2006/picture
ns5 = http://schemas.openxmlformats.org/package/2006/content-types
ns6 = http://schemas.openxmlformats.org/package/2006/relationships
ns7 = http://schemas.openxmlformats.org/officeDocument/2006/extended-properties
ns8 = http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes
ns9 = http://schemas.openxmlformats.org/package/2006/metadata/core-properties
ns10 = http://purl.org/dc/terms/
ns11 = http://www.w3.org/2001/XMLSchema-instance
ns12 = http://purl.org/dc/elements/1.1/
ns13 = http://schemas.openxmlformats.org/officeDocument/2006/custom-properties
ns14 = http://schemas.openxmlformats.org/markup-compatibility/2006
ns15 = http://schemas.microsoft.com/office/word/2010/wordml
ns16 = http://www.w3.org/XML/1998/namespace
ns17 = http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing
ns18 = http://schemas.microsoft.com/office/drawing/2010/main
ns19 = http://schemas.microsoft.com/office/word/2012/wordml
ns20 = http://schemas.microsoft.com/office/word/2016/wordml/cid
ns21 = http://schemas.openxmlformats.org/officeDocument/2006/math
ns22 = http://www.wps.cn/officeDocument/2013/wpsCustomData
ns23 = urn:schemas-microsoft-com:office:office
ns24 = urn:schemas-microsoft-com:vml
ns25 = http://schemas.microsoft.com/office/thememl/2012/main
```

</details>

<details><summary>[Content_Types].xml — F15</summary>

```diff
--- A/[Content_Types].xml
+++ B/[Content_Types].xml
@@ -2,2 +2,4 @@
   <ns5:Default ContentType="image/jpeg" Extension="jpeg">
+  </ns5:Default>
+  <ns5:Default ContentType="image/png" Extension="png">
   </ns5:Default>
@@ -7,21 +9,15 @@
   </ns5:Default>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml" PartName="/docProps/app.xml">
-  </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-package.core-properties+xml" PartName="/docProps/core.xml">
-  </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml" PartName="/docProps/custom.xml">
-  </ns5:Override>
   <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml" PartName="/word/document.xml">
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml" PartName="/word/endnotes.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml" PartName="/word/numbering.xml">
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml" PartName="/word/fontTable.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml" PartName="/word/styles.xml">
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" PartName="/word/footer1.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml" PartName="/word/settings.xml">
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" PartName="/word/footer2.xml">
-  </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" PartName="/word/footer3.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml" PartName="/word/webSettings.xml">
   </ns5:Override>
   <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml" PartName="/word/footnotes.xml">
+  </ns5:Override>
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml" PartName="/word/endnotes.xml">
   </ns5:Override>
@@ -33,5 +29,5 @@
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml" PartName="/word/settings.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" PartName="/word/footer1.xml">
   </ns5:Override>
-  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml" PartName="/word/styles.xml">
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml" PartName="/word/fontTable.xml">
   </ns5:Override>
@@ -39,2 +35,6 @@
   </ns5:Override>
+  <ns5:Override ContentType="application/vnd.openxmlformats-package.core-properties+xml" PartName="/docProps/core.xml">
+  </ns5:Override>
+  <ns5:Override ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml" PartName="/docProps/app.xml">
+  </ns5:Override>
 </ns5:Types>
```

</details>

<details><summary>_rels/.rels — F15</summary>

```diff
--- A/_rels/.rels
+++ B/_rels/.rels
@@ -1,3 +1,3 @@
 <ns6:Relationships>
-  <ns6:Relationship Id="rId4" Target="word/document.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument">
+  <ns6:Relationship Id="rId3" Target="docProps/app.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties">
   </ns6:Relationship>
@@ -5,5 +5,3 @@
   </ns6:Relationship>
-  <ns6:Relationship Id="rId1" Target="docProps/app.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties">
-  </ns6:Relationship>
-  <ns6:Relationship Id="rId3" Target="docProps/custom.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties">
+  <ns6:Relationship Id="rId1" Target="word/document.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument">
   </ns6:Relationship>
```

</details>

<details><summary>docProps/app.xml — F14</summary>

```diff
--- A/docProps/app.xml
+++ B/docProps/app.xml
@@ -4,7 +4,16 @@
   </ns7:Template>
-  <ns7:ScaleCrop>
-    TEXT "false"
-  </ns7:ScaleCrop>
+  <ns7:TotalTime>
+    TEXT "84"
+  </ns7:TotalTime>
+  <ns7:Pages>
+    TEXT "3"
+  </ns7:Pages>
+  <ns7:Words>
+    TEXT "457"
+  </ns7:Words>
+  <ns7:Characters>
+    TEXT "2516"
+  </ns7:Characters>
   <ns7:Application>
-    TEXT "Microsoft Word for the web"
+    TEXT "Microsoft Office Word"
   </ns7:Application>
@@ -13,2 +22,45 @@
   </ns7:DocSecurity>
+  <ns7:Lines>
+    TEXT "20"
+  </ns7:Lines>
+  <ns7:Paragraphs>
+    TEXT "5"
+  </ns7:Paragraphs>
+  <ns7:ScaleCrop>
+    TEXT "false"
+  </ns7:ScaleCrop>
+  <ns7:HeadingPairs>
+    <ns8:vector baseType="variant" size="2">
+      <ns8:variant>
+        <ns8:lpstr>
+          TEXT "Título"
+        </ns8:lpstr>
+      </ns8:variant>
+      <ns8:variant>
+        <ns8:i4>
+          TEXT "1"
+        </ns8:i4>
+      </ns8:variant>
+    </ns8:vector>
+  </ns7:HeadingPairs>
+  <ns7:TitlesOfParts>
+    <ns8:vector baseType="lpstr" size="1">
+      <ns8:lpstr>
+      </ns8:lpstr>
+    </ns8:vector>
+  </ns7:TitlesOfParts>
+  <ns7:Company>
+  </ns7:Company>
+  <ns7:LinksUpToDate>
+    TEXT "false"
+  </ns7:LinksUpToDate>
+  <ns7:CharactersWithSpaces>
+    TEXT "2968"
+  </ns7:CharactersWithSpaces>
+  <ns7:SharedDoc>
+    TEXT "false"
+  </ns7:SharedDoc>
+  <ns7:HyperlinksChanged>
+    TEXT "false"
+  </ns7:HyperlinksChanged>
   <ns7:AppVersion>
@@ -16,5 +68,2 @@
   </ns7:AppVersion>
-  <ns7:LinksUpToDate>
-    TEXT "false"
-  </ns7:LinksUpToDate>
 </ns7:Properties>
```

</details>

<details><summary>docProps/core.xml — F12–F13</summary>

```diff
--- A/docProps/core.xml
+++ B/docProps/core.xml
@@ -1,20 +1,30 @@
 <ns9:coreProperties>
+  <ns12:title>
+    TEXT "Predicción del PROMEDIO_GLOBAL de Saber Pro mediante LightGBM y auditoría de fuga temporal: un estudio a nivel de programa académico en Colombia"
+  </ns12:title>
+  <ns12:subject>
+  </ns12:subject>
+  <ns12:creator>
+    TEXT "Edwin Santiago Paz Bedoya; Nathalia Orozco Morales"
+  </ns12:creator>
+  <ns9:keywords>
+  </ns9:keywords>
+  <ns12:description>
+    TEXT "DRAFT. No enviar. Pendiente de análisis de similitud e IA y revisión final."
+  </ns12:description>
+  <ns9:lastModifiedBy>
+    TEXT "Raul Antonio Aguilar Vera"
+  </ns9:lastModifiedBy>
+  <ns9:revision>
+    TEXT "30"
+  </ns9:revision>
+  <ns9:lastPrinted>
+    TEXT "2020-08-25T00:11:00Z"
+  </ns9:lastPrinted>
   <ns10:created ns11:type="dcterms:W3CDTF">
-    TEXT "2020-08-25T06:42:00.0000000Z"
+    TEXT "2020-08-25T06:42:00Z"
   </ns10:created>
-  <ns12:creator>
-    TEXT "Francisco Alejandro Madera Ramírez"
-  </ns12:creator>
-  <ns9:lastModifiedBy>
-    TEXT "NATHALIA OROZCO MORALES"
-  </ns9:lastModifiedBy>
-  <ns9:lastPrinted>
-    TEXT "2020-08-25T00:11:00.0000000Z"
-  </ns9:lastPrinted>
   <ns10:modified ns11:type="dcterms:W3CDTF">
-    TEXT "2026-07-03T18:21:58.0618949Z"
+    TEXT "2023-03-22T00:04:00Z"
   </ns10:modified>
-  <ns9:revision>
-    TEXT "33"
-  </ns9:revision>
 </ns9:coreProperties>
```

</details>

<details><summary>docProps/custom.xml — F14</summary>

```diff
--- A/docProps/custom.xml
+++ B/docProps/custom.xml
@@ -1,17 +0,0 @@
-<ns13:Properties>
-  <ns13:property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" name="KSOTemplateDocerSaveRecord" pid="2">
-    <ns8:lpwstr>
-      TEXT "eyJoZGlkIjoiMTYyZDIzM2ExOTJiZGUzZDQzZGQ4ZTMwZGYxMTZiMmUiLCJ1c2VySWQiOiIyMTk5MDIzOTgxMTA2In0="
-    </ns8:lpwstr>
-  </ns13:property>
-  <ns13:property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" name="KSOProductBuildVer" pid="3">
-    <ns8:lpwstr>
-      TEXT "3082-12.1.0.26880"
-    </ns8:lpwstr>
-  </ns13:property>
-  <ns13:property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" name="ICV" pid="4">
-    <ns8:lpwstr>
-      TEXT "2AA1ECEDCF2046C9AF18151D06CC0EBD_13"
-    </ns8:lpwstr>
-  </ns13:property>
-</ns13:Properties>
```

</details>

<details><summary>word/_rels/document.xml.rels — F15</summary>

```diff
--- A/word/_rels/document.xml.rels
+++ B/word/_rels/document.xml.rels
@@ -1,39 +1,41 @@
 <ns6:Relationships>
-  <ns6:Relationship Id="rId9" Target="theme/theme1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme">
+  <ns6:Relationship Id="rId8" Target="header1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId8" Target="footer1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer">
+  <ns6:Relationship Id="rId13" Target="theme/theme1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId7" Target="header3.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
+  <ns6:Relationship Id="rId3" Target="settings.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId6" Target="header2.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
+  <ns6:Relationship Id="rId7" Target="media/image1.png" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId5" Target="header1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
+  <ns6:Relationship Id="rId12" Target="fontTable.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId4" Target="endnotes.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes">
+  <ns6:Relationship Id="rId2" Target="styles.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId3" Target="footnotes.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes">
+  <ns6:Relationship Id="rId1" Target="numbering.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId2" Target="settings.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings">
+  <ns6:Relationship Id="rId6" Target="endnotes.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId17" Target="fontTable.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable">
+  <ns6:Relationship Id="rId11" Target="footer1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId16" Target="media/image8.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rId5" Target="footnotes.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId15" Target="media/image7.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rId10" Target="header3.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId14" Target="media/image6.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rId4" Target="webSettings.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId13" Target="media/image5.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rId9" Target="header2.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId12" Target="media/image4.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rIdConacic1" Target="media/conacic_image8.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId11" Target="media/image3.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rIdConacic2" Target="media/conacic_image7.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId10" Target="media/image2.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rIdConacic3" Target="media/conacic_image6.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="rId1" Target="styles.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles">
+  <ns6:Relationship Id="rIdConacic4" Target="media/conacic_image5.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="R497aee37872648f0" Target="footer2.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer">
+  <ns6:Relationship Id="rIdConacic5" Target="media/conacic_image4.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
-  <ns6:Relationship Id="R18526df984d849b3" Target="footer3.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer">
+  <ns6:Relationship Id="rIdConacic6" Target="media/conacic_image3.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  </ns6:Relationship>
+  <ns6:Relationship Id="rIdConacic7" Target="media/conacic_image2.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
```

</details>

<details><summary>word/_rels/header3.xml.rels — F11</summary>

```diff
--- A/word/_rels/header3.xml.rels
+++ B/word/_rels/header3.xml.rels
@@ -1,3 +1,3 @@
 <ns6:Relationships>
-  <ns6:Relationship Id="rId1" Target="media/image1.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
+  <ns6:Relationship Id="rId1" Target="media/image2.jpeg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image">
   </ns6:Relationship>
```

</details>

<details><summary>word/document.xml — D01–D09, F01–F06, F11</summary>

```diff
--- A/word/document.xml
+++ B/word/document.xml
@@ -1,2 +1,2 @@
-<w:document ns14:Ignorable="w14 w15 wp14">
+<w:document ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
   <w:body>
@@ -41,3 +41,3 @@
       <w:pPr>
-        <w:spacing w:after="40" w:before="0">
+        <w:spacing w:after="0" w:before="0" w:line="80" w:lineRule="exact">
         </w:spacing>
@@ -86,5 +86,5 @@
     </w:p>
-    <w:p ns15:paraId="3497AAC0" ns15:textId="77777777">
-      <w:pPr>
-        <w:spacing w:after="40" w:before="120">
+    <w:p ns15:paraId="5FCE8C49" ns15:textId="17D81AFA" w:rsidP="00247B94" w:rsidR="00FB33CD" w:rsidRDefault="006632C2" w:rsidRPr="00DA4300">
+      <w:pPr>
+        <w:spacing w:after="20" w:before="0">
         </w:spacing>
@@ -92,23 +92,46 @@
         </w:jc>
-      </w:pPr>
-      <w:r>
-        <w:rPr>
-          <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:hAnsi="Times New Roman">
-          </w:rFonts>
+        <w:rPr>
           <w:sz w:val="24">
           </w:sz>
-          <w:szCs w:val="24">
-          </w:szCs>
-        </w:rPr>
-        <w:t>
-          TEXT "Edwin Santiago Paz Bedoya"
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="24F40184" ns15:textId="77777777">
-      <w:pPr>
-        <w:spacing w:after="40" w:before="0">
+        </w:rPr>
+      </w:pPr>
+      <w:r>
+        <w:rPr>
+          <w:sz w:val="24">
+          </w:sz>
+        </w:rPr>
+        <w:t>
+          TEXT "Edwin Santiago Paz Bedoya¹, Nathalia Orozco Morales¹"
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="2517CB09" ns15:textId="6370A54E" w:rsidP="00316941" w:rsidR="00FB33CD" w:rsidRDefault="00DA4300" w:rsidRPr="00DA4300">
+      <w:pPr>
+        <w:jc w:val="center">
+        </w:jc>
+        <w:rPr>
+          <w:sz w:val="24">
+          </w:sz>
+        </w:rPr>
+        <w:spacing w:after="20" w:before="0">
         </w:spacing>
+      </w:pPr>
+      <w:r>
+        <w:rPr>
+          <w:sz w:val="24">
+          </w:sz>
+        </w:rPr>
+        <w:t>
+          TEXT "¹UNIMINUTO Virtual – Bogotá, Colombia"
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="3920E81F" ns15:textId="4F76611B" w:rsidP="0007482E" w:rsidR="00FB33CD" w:rsidRDefault="0007482E" w:rsidRPr="006413B2">
+      <w:pPr>
         <w:jc w:val="center">
         </w:jc>
+        <w:rPr>
+          <w:sz w:val="24">
+          </w:sz>
+        </w:rPr>
       </w:pPr>
@@ -116,39 +139,7 @@
         <w:rPr>
-          <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:hAnsi="Times New Roman">
-          </w:rFonts>
-          <w:sz w:val="20">
+          <w:sz w:val="24">
           </w:sz>
-          <w:szCs w:val="20">
-          </w:szCs>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT "UNIMINUTO, "
-        </w:t>
-      </w:r>
-      <w:r>
-        <w:rPr>
-          <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:hAnsi="Times New Roman" w:hint="default">
-          </w:rFonts>
-          <w:sz w:val="20">
-          </w:sz>
-          <w:szCs w:val="20">
-          </w:szCs>
-          <w:lang w:val="es-CO">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "Bogotá"
-        </w:t>
-      </w:r>
-      <w:r>
-        <w:rPr>
-          <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:hAnsi="Times New Roman">
-          </w:rFonts>
-          <w:sz w:val="20">
-          </w:sz>
-          <w:szCs w:val="20">
-          </w:szCs>
-        </w:rPr>
-        <w:t>
-          TEXT ", Colombia."
+        </w:rPr>
+        <w:t>
+          TEXT "edwin.paz@uniminuto.edu, nathalia.orozco@uniminuto.edu"
         </w:t>
@@ -158,3 +149,3 @@
       <w:pPr>
-        <w:spacing w:after="40" w:before="0">
+        <w:spacing w:after="0" w:before="0" w:line="80" w:lineRule="exact">
         </w:spacing>
@@ -758,16 +749,3 @@
         <w:t>
-          TEXT "Los archivos ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo de estadística de cada fila. Se identificaron tres capas utilizables: (a) PUNTAJE_PRUEBA, promedio por prueba; (b) PUNTAJE_GLOBAL, target PROMEDIO_GLOBAL; y (c) NIVEL_DESEMPEÑO_PRUEBA, proporciones por nivel. Se aplicó un pivot long→wide con inner join sobre la llave (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA), preservando únicamente entidades con las tres capas presentes. El resultado es 127.716 filas wide con el target disponible al 100 %."
-        </w:t>
-      </w:r>
-      <w:r>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:rFonts w:hint="default">
-          </w:rFonts>
-          <w:lang w:val="es-CO">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT "  La Figura 1 ilustra la distribución del PROMEDIO_GLOBAL resultante, el crecimiento de filas limpias por año y las pruebas y NBCs más frecuentes del panel."
+          TEXT "Los archivos ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo de estadística de cada fila. Se identificaron tres capas utilizables: PUNTAJE_PRUEBA, PUNTAJE_GLOBAL y NIVEL_DESEMPEÑO_PRUEBA. Se unieron las pruebas con el puntaje global mediante inner join por año, institución y programa; los niveles se añadieron mediante left join incluyendo NOMBRE_PRUEBA. El resultado es 127.716 filas wide con el target disponible al 100 %. La Figura 1 ilustra la distribución del PROMEDIO_GLOBAL, las filas por año y las pruebas y NBCs más frecuentes."
         </w:t>
@@ -881,3 +859,3 @@
                   <pic:blipFill>
-                    <a:blip r:embed="rId10">
+                    <a:blip r:embed="rIdConacic7">
                     </a:blip>
@@ -968,2 +946,25 @@
       </w:pPr>
+      <w:r>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "Se emplearon 15 variables de entrada: rezagos lag_1 y lag_2 de las observaciones anteriores disponibles del PROMEDIO_GLOBAL y de cada prueba, tendencias, volatilidad histórica, logaritmo del número de evaluados, año y variables categóricas. Los tres modelos tabulares usan TargetEncoder; en los artefactos evaluados, su modo automático produjo codificación multiclase (135 valores del objetivo), con 417 columnas transformadas en total. El split externo usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas)."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="7D73621B" ns15:textId="77777777" w:rsidP="473E729D">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
       <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
@@ -976,25 +977,2 @@
         <w:t>
-          TEXT "Se construyeron 15 features causalmente válidas: rezagos temporales lag_1 y lag_2 del PROMEDIO_GLOBAL y de cada prueba, tendencia histórica, desviación estándar histórica, logaritmo del número de evaluados, año, identificadores de NBC y departamento codificados con TargetEncoder. El split temporal estricto usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas)."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="7D73621B" ns15:textId="77777777" w:rsidP="473E729D">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
           TEXT "3.5 Modelos Evaluados"
@@ -1014,3 +992,3 @@
       </w:pPr>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
+      <w:r>
         <w:rPr>
@@ -1022,221 +1000,3 @@
         <w:t>
-          TEXT "Finalmente se evaluaron cuatro familias: (1) Ridge con α automático ("
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "RidgeCV"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "); (2) Lasso con α automático ("
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "LassoCV"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT "); (3) "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "LightGBM"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " con 50 "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "trials"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " de búsqueda "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "Optuna"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " [4] y "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "n_estimators"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " = 500; (4) "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "Transformer"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "encoder"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " con "
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "early"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "stopping"
-        </w:t>
-      </w:r>
-      <w:r w:rsidR="7118E9F6" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="es-ES">
-          </w:lang>
-        </w:rPr>
-        <w:t ns16:space="preserve">
-          TEXT " (época 53/200). Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6]."
+          TEXT "Finalmente se evaluaron cuatro familias: (1) Ridge con α automático (RidgeCV); (2) Lasso con α automático (LassoCV); (3) LightGBM con 50 trials de búsqueda Optuna [4] y 188 árboles en el artefacto final (mejor iteración 168 + 20); (4) Transformer encoder con early stopping (época 53/200). Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6]."
         </w:t>
@@ -1329,3 +1089,3 @@
         </w:tblOverlap>
-        <w:tblW w:type="dxa" w:w="9760">
+        <w:tblW w:type="dxa" w:w="8838">
         </w:tblW>
@@ -1347,3 +1107,3 @@
         </w:tblBorders>
-        <w:tblLayout w:type="autofit">
+        <w:tblLayout w:type="fixed">
         </w:tblLayout>
@@ -1361,11 +1121,11 @@
       <w:tblGrid>
-        <w:gridCol w:w="2880">
+        <w:gridCol w:w="2450">
         </w:gridCol>
-        <w:gridCol w:w="1440">
+        <w:gridCol w:w="1350">
         </w:gridCol>
-        <w:gridCol w:w="1440">
+        <w:gridCol w:w="1350">
         </w:gridCol>
-        <w:gridCol w:w="1440">
+        <w:gridCol w:w="1300">
         </w:gridCol>
-        <w:gridCol w:w="2560">
+        <w:gridCol w:w="2388">
         </w:gridCol>
@@ -1405,3 +1165,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2880">
+            <w:tcW w:type="dxa" w:w="2450">
             </w:tcW>
@@ -1462,3 +1222,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -1517,3 +1277,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -1572,3 +1332,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1300">
             </w:tcW>
@@ -1627,3 +1387,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2560">
+            <w:tcW w:type="dxa" w:w="2388">
             </w:tcW>
@@ -1716,3 +1476,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2880">
+            <w:tcW w:type="dxa" w:w="2450">
             </w:tcW>
@@ -1771,3 +1531,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -1826,3 +1586,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -1881,3 +1641,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1300">
             </w:tcW>
@@ -1936,3 +1696,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2560">
+            <w:tcW w:type="dxa" w:w="2388">
             </w:tcW>
@@ -2023,3 +1783,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2880">
+            <w:tcW w:type="dxa" w:w="2450">
             </w:tcW>
@@ -2078,3 +1838,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2133,3 +1893,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2188,3 +1948,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1300">
             </w:tcW>
@@ -2243,3 +2003,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2560">
+            <w:tcW w:type="dxa" w:w="2388">
             </w:tcW>
@@ -2330,3 +2090,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2880">
+            <w:tcW w:type="dxa" w:w="2450">
             </w:tcW>
@@ -2385,3 +2145,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2440,3 +2200,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2495,3 +2255,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1300">
             </w:tcW>
@@ -2550,3 +2310,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2560">
+            <w:tcW w:type="dxa" w:w="2388">
             </w:tcW>
@@ -2637,3 +2397,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2880">
+            <w:tcW w:type="dxa" w:w="2450">
             </w:tcW>
@@ -2692,3 +2452,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2747,3 +2507,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1350">
             </w:tcW>
@@ -2802,3 +2562,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="1440">
+            <w:tcW w:type="dxa" w:w="1300">
             </w:tcW>
@@ -2857,3 +2617,3 @@
           <w:tcPr>
-            <w:tcW w:type="dxa" w:w="2560">
+            <w:tcW w:type="dxa" w:w="2388">
             </w:tcW>
@@ -3035,3 +2795,3 @@
                   <pic:blipFill>
-                    <a:blip r:embed="rId11">
+                    <a:blip r:embed="rIdConacic6">
                     </a:blip>
@@ -3167,3 +2927,3 @@
                   <pic:blipFill>
-                    <a:blip r:embed="rId12">
+                    <a:blip r:embed="rIdConacic5">
                     </a:blip>
@@ -3349,3 +3109,3 @@
                   <pic:blipFill>
-                    <a:blip r:embed="rId13">
+                    <a:blip r:embed="rIdConacic4">
                     </a:blip>
@@ -3466,3 +3226,3 @@
         <w:t>
-          TEXT "La Figura 5 desagrega el RMSE de LightGBM por Núcleo Básico del Conocimiento (top 25), revelando diferencias sustanciales entre áreas disciplinares. Los programas de Salud concentran los errores más bajos (RMSE entre 4,1 y 6,2 puntos), mientras que Educación (RMSE = 11,71) y Sin Clasificar (RMSE = 17,76) concentran los más altos, explicados por la alta heterogeneidad interna de esas categorías. El análisis geográfico complementario muestra que Sucre (≈ 13), Chocó (≈ 12) y Putumayo (≈ 11) presentan los mayores errores, coincidiendo con regiones de menor desarrollo económico relativo."
+          TEXT "La Figura 5 desagrega el RMSE de LightGBM por Núcleo Básico del Conocimiento (top 25), revelando diferencias sustanciales entre áreas disciplinares. Algunas áreas de Salud presentan errores bajos (RMSE entre 4,1 y 6,2 puntos), mientras que Educación (RMSE = 11,71) y Sin Clasificar (RMSE = 17,76) concentran los más altos, explicados por la alta heterogeneidad interna de esas categorías. El análisis geográfico complementario muestra que Sucre (≈ 13), Chocó (≈ 12) y Putumayo (≈ 11) presentan los mayores errores, coincidiendo con regiones de menor desarrollo económico relativo."
         </w:t>
@@ -3502,3 +3262,3 @@
                   <pic:blipFill>
-                    <a:blip r:embed="rId14">
+                    <a:blip r:embed="rIdConacic3">
                     </a:blip>
@@ -3794,11 +3554,11 @@
       </w:pPr>
-      <w:r w:rsidR="36A5FF65" w:rsidRPr="36A5FF65">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "El SACES colombiano incorpora Saber Pro como insumo central para registro calificado y acreditación [15]. Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva. Esta lógica es análoga a la propuesta por López-García et al. [26] para detección de fracaso estudiantil en la Universidad Industrial de Santander, aunque el presente trabajo opera a nivel programa-institución, complementándola. Los NBC con SHAP negativo y los departamentos con mayor RMSE señalan prioridades concretas de intervención y de recoleción de datos socioeconómicos externos."
+      <w:r>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "El SACES colombiano incorpora Saber Pro como insumo central para registro calificado y acreditación [15]. Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva. Esta lógica es análoga a la propuesta por López-García et al. [26] para detección de fracaso estudiantil en la Universidad Industrial de Santander, aunque el presente trabajo opera a nivel programa-institución, complementándola. Los NBC con SHAP negativo y los departamentos con mayor RMSE señalan prioridades concretas de intervención y de recolección de datos socioeconómicos externos."
         </w:t>
@@ -4537,2 +4297,52 @@
       </w:pPr>
+      <w:r>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "[20] P. J. L. Adeodato y R. L. C. Silva Filho, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. 13th International Conference on Educational Data Mining, 2020, pp. 545–549."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="1295AD52" ns15:textId="77777777">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:rFonts w:hint="default">
+          </w:rFonts>
+          <w:lang w:val="en">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
+      <w:r>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:rFonts w:hint="default">
+          </w:rFonts>
+          <w:lang w:val="en">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "[21] D. Chafla, M. Morocho y J. Ortega, “Machine learning models for academic performance prediction with explainability,” Frontiers in Education, vol. 10, 2025."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="6765FFC7" ns15:textId="77777777" w:rsidP="473E729D">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
       <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
@@ -4545,7 +4355,76 @@
         <w:t>
-          TEXT "[20] Anónimo, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. EDM, 2020."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="1295AD52" ns15:textId="77777777">
+          TEXT "[22] S. Acıslı-Celik y C. M. Yesilkanat, “Predicting science achievement scores with ML: PISA 2015–2018,” Neural Comput. Appl., vol. 35, 2023."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="255A3E6D" ns15:textId="77777777" w:rsidP="473E729D">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
+      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "[23] G. Rasch, “An item analysis which takes individual differences into account,” British J. Math. Stat. Psychol., vol. 19, n.º 1, pp. 49–57, 1966."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="016ECDFC" ns15:textId="77777777" w:rsidP="473E729D">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
+      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "[24] A. E. Hoerl y R. W. Kennard, “Ridge regression: Biased estimation for nonorthogonal problems,” Technometrics, vol. 12, n.º 1, pp. 55–67, 1970."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="0CC51E40" ns15:textId="77777777" w:rsidP="473E729D">
+      <w:pPr>
+        <w:jc w:val="both">
+        </w:jc>
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+      </w:pPr>
+      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
+        <w:rPr>
+          <w:rStyle w:val="17">
+          </w:rStyle>
+          <w:lang w:val="en-US">
+          </w:lang>
+        </w:rPr>
+        <w:t>
+          TEXT "[25] R. Tibshirani, “Regression shrinkage and selection via the lasso,” J. Royal Stat. Soc. B, vol. 58, n.º 1, pp. 267–288, 1996."
+        </w:t>
+      </w:r>
+    </w:p>
+    <w:p ns15:paraId="7BB120C4" ns15:textId="77777777">
       <w:pPr>
@@ -4572,121 +4451,2 @@
         <w:t>
-          TEXT "[21] D. Chafla, M. Morocho y J. Ortega, “Machine learning models for academic performance prediction with explainability,” Frontiers in Education, vol. 10, 2025."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="6765FFC7" ns15:textId="77777777" w:rsidP="473E729D">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "[22] S. Acıslı-Celik y C. M. Yesilkanat, “Predicting science achievement scores with ML: PISA 2015–2018,” Neural Comput. Appl., vol. 35, 2023."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="255A3E6D" ns15:textId="77777777" w:rsidP="473E729D">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "[23] G. Rasch, “An item analysis which takes individual differences into account,” British J. Math. Stat. Psychol., vol. 19, n.º 1, pp. 49–57, 1966."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="016ECDFC" ns15:textId="77777777" w:rsidP="473E729D">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "[24] A. E. Hoerl y R. W. Kennard, “Ridge regression: Biased estimation for nonorthogonal problems,” Technometrics, vol. 12, n.º 1, pp. 55–67, 1970."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="0CC51E40" ns15:textId="77777777" w:rsidP="473E729D">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r w:rsidR="473E729D" w:rsidRPr="473E729D">
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:lang w:val="en-US">
-          </w:lang>
-        </w:rPr>
-        <w:t>
-          TEXT "[25] R. Tibshirani, “Regression shrinkage and selection via the lasso,” J. Royal Stat. Soc. B, vol. 58, n.º 1, pp. 267–288, 1996."
-        </w:t>
-      </w:r>
-    </w:p>
-    <w:p ns15:paraId="7BB120C4" ns15:textId="77777777">
-      <w:pPr>
-        <w:jc w:val="both">
-        </w:jc>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:rFonts w:hint="default">
-          </w:rFonts>
-          <w:lang w:val="en">
-          </w:lang>
-        </w:rPr>
-      </w:pPr>
-      <w:r>
-        <w:rPr>
-          <w:rStyle w:val="17">
-          </w:rStyle>
-          <w:rFonts w:hint="default">
-          </w:rFonts>
-          <w:lang w:val="en">
-          </w:lang>
-        </w:rPr>
-        <w:t>
           TEXT "[26] A. López-García et al., “Early detection of students’ failure using machine learning techniques,” Operations Research Perspectives, vol. 11, 2023."
@@ -4695,12 +4455,12 @@
     </w:p>
-    <w:sectPr>
-      <w:headerReference r:id="rId7" w:type="first">
+    <w:sectPr w:rsidR="00BE6CF2" w:rsidRPr="00C7650B" w:rsidSect="00537C1D">
+      <w:headerReference r:id="rId8" w:type="even">
       </w:headerReference>
-      <w:footerReference r:id="rId8" w:type="first">
+      <w:headerReference r:id="rId9" w:type="default">
+      </w:headerReference>
+      <w:headerReference r:id="rId10" w:type="first">
+      </w:headerReference>
+      <w:footerReference r:id="rId11" w:type="first">
       </w:footerReference>
-      <w:headerReference r:id="rId5" w:type="default">
-      </w:headerReference>
-      <w:headerReference r:id="rId6" w:type="even">
-      </w:headerReference>
-      <w:pgSz w:h="15840" w:orient="portrait" w:w="12240">
+      <w:pgSz w:h="15840" w:w="12240">
       </w:pgSz>
@@ -4708,5 +4468,5 @@
       </w:pgMar>
-      <w:pgNumType w:start="3">
+      <w:pgNumType w:start="1">
       </w:pgNumType>
-      <w:cols w:num="1" w:space="708">
+      <w:cols w:space="708">
       </w:cols>
@@ -4714,8 +4474,4 @@
       </w:titlePg>
-      <w:docGrid w:charSpace="0" w:linePitch="360">
+      <w:docGrid w:linePitch="360">
       </w:docGrid>
-      <w:footerReference r:id="R497aee37872648f0" w:type="default">
-      </w:footerReference>
-      <w:footerReference r:id="R18526df984d849b3" w:type="even">
-      </w:footerReference>
     </w:sectPr>
```

</details>

<details><summary>word/endnotes.xml — F15</summary>

```diff
--- A/word/endnotes.xml
+++ B/word/endnotes.xml
@@ -1,6 +1,6 @@
-<w:endnotes ns14:Ignorable="w14 w15 wp14">
-  <w:endnote w:id="0" w:type="separator">
-    <w:p ns15:paraId="672A6659" ns15:textId="77777777">
+<w:endnotes ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
+  <w:endnote w:id="-1" w:type="separator">
+    <w:p ns15:paraId="3795C7AB" ns15:textId="77777777" w:rsidP="003148F9" w:rsidR="0098426C" w:rsidRDefault="0098426C">
       <w:pPr>
-        <w:spacing w:line="240" w:lineRule="auto">
+        <w:spacing w:after="0" w:line="240" w:lineRule="auto">
         </w:spacing>
@@ -13,6 +13,6 @@
   </w:endnote>
-  <w:endnote w:id="1" w:type="continuationSeparator">
-    <w:p ns15:paraId="0A37501D" ns15:textId="77777777">
+  <w:endnote w:id="0" w:type="continuationSeparator">
+    <w:p ns15:paraId="60EAB46C" ns15:textId="77777777" w:rsidP="003148F9" w:rsidR="0098426C" w:rsidRDefault="0098426C">
       <w:pPr>
-        <w:spacing w:line="240" w:lineRule="auto">
+        <w:spacing w:after="0" w:line="240" w:lineRule="auto">
         </w:spacing>
```

</details>

<details><summary>word/fontTable.xml — F06</summary>

```diff
--- A/word/fontTable.xml
+++ B/word/fontTable.xml
@@ -1,2 +1,14 @@
-<w:fonts ns14:Ignorable="w14">
+<w:fonts ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh">
+  <w:font w:name="Symbol">
+    <w:panose1 w:val="05050102010706020507">
+    </w:panose1>
+    <w:charset w:val="02">
+    </w:charset>
+    <w:family w:val="roman">
+    </w:family>
+    <w:pitch w:val="variable">
+    </w:pitch>
+    <w:sig w:csb0="80000000" w:csb1="00000000" w:usb0="00000000" w:usb1="10000000" w:usb2="00000000" w:usb3="00000000">
+    </w:sig>
+  </w:font>
   <w:font w:name="Times New Roman">
@@ -4,19 +16,5 @@
     </w:panose1>
-    <w:charset w:val="86">
+    <w:charset w:val="00">
     </w:charset>
-    <w:family w:val="auto">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="400001FF" w:csb1="FFFF0000" w:usb0="E0002EFF" w:usb1="C000785B" w:usb2="00000009" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="宋体">
-    <w:altName w:val="SimSun">
-    </w:altName>
-    <w:panose1 w:val="02010600030101010101">
-    </w:panose1>
-    <w:charset w:val="86">
-    </w:charset>
-    <w:family w:val="auto">
+    <w:family w:val="roman">
     </w:family>
@@ -24,27 +22,3 @@
     </w:pitch>
-    <w:sig w:csb0="00040001" w:csb1="00000000" w:usb0="00000003" w:usb1="080E0000" w:usb2="00000010" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="SimSun">
-    <w:panose1 w:val="02010600030101010101">
-    </w:panose1>
-    <w:charset w:val="86">
-    </w:charset>
-    <w:family w:val="auto">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="00040001" w:csb1="00000000" w:usb0="00000203" w:usb1="288F0000" w:usb2="00000006" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="Arial">
-    <w:panose1 w:val="020B0604020202020204">
-    </w:panose1>
-    <w:charset w:val="00">
-    </w:charset>
-    <w:family w:val="swiss">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="400001FF" w:csb1="FFFF0000" w:usb0="E0002EFF" w:usb1="C000785B" w:usb2="00000009" w:usb3="00000000">
+    <w:sig w:csb0="000001FF" w:csb1="00000000" w:usb0="E0002EFF" w:usb1="C000785B" w:usb2="00000009" w:usb3="00000000">
     </w:sig>
@@ -58,19 +32,5 @@
     </w:family>
-    <w:pitch w:val="default">
+    <w:pitch w:val="fixed">
     </w:pitch>
-    <w:sig w:csb0="400001FF" w:csb1="FFFF0000" w:usb0="E0002EFF" w:usb1="C0007843" w:usb2="00000009" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="黑体">
-    <w:altName w:val="SimSun">
-    </w:altName>
-    <w:panose1 w:val="02010609060101010101">
-    </w:panose1>
-    <w:charset w:val="86">
-    </w:charset>
-    <w:family w:val="modern">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="00040001" w:csb1="00000000" w:usb0="800002BF" w:usb1="38CF7CFA" w:usb2="00000016" w:usb3="00000000">
+    <w:sig w:csb0="000001FF" w:csb1="00000000" w:usb0="E0002EFF" w:usb1="C0007843" w:usb2="00000009" w:usb3="00000000">
     </w:sig>
@@ -84,29 +44,5 @@
     </w:family>
-    <w:pitch w:val="default">
+    <w:pitch w:val="variable">
     </w:pitch>
-    <w:sig w:csb0="80000000" w:csb1="00000000" w:usb0="00000000" w:usb1="00000000" w:usb2="00000000" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="Calibri">
-    <w:panose1 w:val="020F0502020204030204">
-    </w:panose1>
-    <w:charset w:val="86">
-    </w:charset>
-    <w:family w:val="swiss">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="200001FF" w:csb1="00000000" w:usb0="E4002EFF" w:usb1="C200247B" w:usb2="00000009" w:usb3="00000000">
-    </w:sig>
-  </w:font>
-  <w:font w:name="Calibri">
-    <w:panose1 w:val="020F0502020204030204">
-    </w:panose1>
-    <w:charset w:val="86">
-    </w:charset>
-    <w:family w:val="swiss">
-    </w:family>
-    <w:pitch w:val="default">
-    </w:pitch>
-    <w:sig w:csb0="200001FF" w:csb1="00000000" w:usb0="E4002EFF" w:usb1="C200247B" w:usb2="00000009" w:usb3="00000000">
+    <w:sig w:csb0="80000000" w:csb1="00000000" w:usb0="00000000" w:usb1="10000000" w:usb2="00000000" w:usb3="00000000">
     </w:sig>
@@ -118,7 +54,35 @@
     </w:charset>
+    <w:family w:val="swiss">
+    </w:family>
+    <w:pitch w:val="variable">
+    </w:pitch>
+    <w:sig w:csb0="000001FF" w:csb1="00000000" w:usb0="E4002EFF" w:usb1="C000247B" w:usb2="00000009" w:usb3="00000000">
+    </w:sig>
+  </w:font>
+  <w:font w:name="SimSun">
+    <w:altName w:val="宋体">
+    </w:altName>
+    <w:panose1 w:val="02010600030101010101">
+    </w:panose1>
+    <w:charset w:val="86">
+    </w:charset>
     <w:family w:val="auto">
     </w:family>
-    <w:pitch w:val="default">
+    <w:notTrueType>
+    </w:notTrueType>
+    <w:pitch w:val="variable">
     </w:pitch>
-    <w:sig w:csb0="200001FF" w:csb1="00000000" w:usb0="E4002EFF" w:usb1="C200247B" w:usb2="00000009" w:usb3="00000000">
+    <w:sig w:csb0="00040000" w:csb1="00000000" w:usb0="00000001" w:usb1="080E0000" w:usb2="00000010" w:usb3="00000000">
+    </w:sig>
+  </w:font>
+  <w:font w:name="Calibri Light">
+    <w:panose1 w:val="020F0302020204030204">
+    </w:panose1>
+    <w:charset w:val="00">
+    </w:charset>
+    <w:family w:val="swiss">
+    </w:family>
+    <w:pitch w:val="variable">
+    </w:pitch>
+    <w:sig w:csb0="000001FF" w:csb1="00000000" w:usb0="E4002EFF" w:usb1="C000247B" w:usb2="00000009" w:usb3="00000000">
     </w:sig>
```

</details>

<details><summary>word/footer1.xml — F10</summary>

```diff
--- A/word/footer1.xml
+++ B/word/footer1.xml
@@ -1,2 +1,2 @@
-<w:ftr ns14:Ignorable="w14 w15 wp14">
+<w:ftr ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
   <w:sdt>
@@ -6,4 +6,6 @@
       <w:docPartObj>
-        <w:docPartGallery w:val="autotext">
+        <w:docPartGallery w:val="Page Numbers (Bottom of Page)">
         </w:docPartGallery>
+        <w:docPartUnique>
+        </w:docPartUnique>
       </w:docPartObj>
@@ -11,5 +13,5 @@
     <w:sdtContent>
-      <w:p ns15:paraId="3F423570" ns15:textId="77777777">
+      <w:p ns15:paraId="3F423570" ns15:textId="184D38DE" w:rsidP="00433632" w:rsidR="00433632" w:rsidRDefault="00433632" w:rsidRPr="00EC6D1E">
         <w:pPr>
-          <w:pStyle w:val="7">
+          <w:pStyle w:val="Piedepgina">
           </w:pStyle>
@@ -26,3 +28,3 @@
           <w:t>
-            TEXT "Fecha de recepción: septiembre 1, 2020 / Fecha de aceptación: octubre 5, 2020"
+            TEXT "DRAFT · Pendiente de análisis de similitud e IA y revisión final"
           </w:t>
@@ -30,5 +32,5 @@
       </w:p>
-      <w:p ns15:paraId="6A08D909" ns15:textId="77777777">
+      <w:p ns15:paraId="6A08D909" ns15:textId="77777777" w:rsidP="00433632" w:rsidR="00433632" w:rsidRDefault="00433632">
         <w:pPr>
-          <w:pStyle w:val="7">
+          <w:pStyle w:val="Piedepgina">
           </w:pStyle>
@@ -37,2 +39,24 @@
         </w:pPr>
+        <w:r>
+          <w:fldChar w:fldCharType="begin">
+          </w:fldChar>
+        </w:r>
+        <w:r>
+          <w:instrText>
+            TEXT "PAGE   \\* MERGEFORMAT"
+          </w:instrText>
+        </w:r>
+        <w:r>
+          <w:fldChar w:fldCharType="separate">
+          </w:fldChar>
+        </w:r>
+        <w:r>
+          <w:t>
+            TEXT "61"
+          </w:t>
+        </w:r>
+        <w:r>
+          <w:fldChar w:fldCharType="end">
+          </w:fldChar>
+        </w:r>
       </w:p>
@@ -40,5 +64,5 @@
   </w:sdt>
-  <w:p ns15:paraId="3780FA6E" ns15:textId="77777777">
+  <w:p ns15:paraId="3780FA6E" ns15:textId="77777777" w:rsidR="00CF2CE6" w:rsidRDefault="00CF2CE6">
     <w:pPr>
-      <w:pStyle w:val="7">
+      <w:pStyle w:val="Piedepgina">
       </w:pStyle>
```

</details>

<details><summary>word/footer2.xml — F15</summary>

```diff
--- A/word/footer2.xml
+++ B/word/footer2.xml
@@ -1,94 +0,0 @@
-<w:ftr>
-  <w:tbl>
-    <w:tblPr>
-      <w:tblStyle w:val="3">
-      </w:tblStyle>
-      <w:bidiVisual w:val="0">
-      </w:bidiVisual>
-      <w:tblW w:type="auto" w:w="0">
-      </w:tblW>
-      <w:tblLook w:firstColumn="1" w:firstRow="1" w:lastColumn="0" w:lastRow="0" w:noHBand="1" w:noVBand="1" w:val="06A0">
-      </w:tblLook>
-    </w:tblPr>
-    <w:tblGrid>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-    </w:tblGrid>
-    <w:tr ns15:paraId="6E207A22" w:rsidR="473E729D" w:rsidTr="473E729D">
-      <w:trPr>
-        <w:trHeight w:val="300">
-        </w:trHeight>
-      </w:trPr>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="3D906825" ns15:textId="6AF8BEC9" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:ind w:left="-115">
-            </w:ind>
-            <w:jc w:val="left">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="5752338E" ns15:textId="1A5066E5" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:jc w:val="center">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="15F4523A" ns15:textId="39D571DA" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:ind w:right="-115">
-            </w:ind>
-            <w:jc w:val="right">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-    </w:tr>
-  </w:tbl>
-  <w:p ns15:paraId="5EB20CE7" ns15:textId="639BEF31" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-    <w:pPr>
-      <w:pStyle w:val="7">
-      </w:pStyle>
-      <w:bidi w:val="0">
-      </w:bidi>
-    </w:pPr>
-  </w:p>
-</w:ftr>
```

</details>

<details><summary>word/footer3.xml — F15</summary>

```diff
--- A/word/footer3.xml
+++ B/word/footer3.xml
@@ -1,94 +0,0 @@
-<w:ftr>
-  <w:tbl>
-    <w:tblPr>
-      <w:tblStyle w:val="3">
-      </w:tblStyle>
-      <w:bidiVisual w:val="0">
-      </w:bidiVisual>
-      <w:tblW w:type="auto" w:w="0">
-      </w:tblW>
-      <w:tblLook w:firstColumn="1" w:firstRow="1" w:lastColumn="0" w:lastRow="0" w:noHBand="1" w:noVBand="1" w:val="06A0">
-      </w:tblLook>
-    </w:tblPr>
-    <w:tblGrid>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-      <w:gridCol w:w="2945">
-      </w:gridCol>
-    </w:tblGrid>
-    <w:tr ns15:paraId="32E4FE96" w:rsidR="473E729D" w:rsidTr="473E729D">
-      <w:trPr>
-        <w:trHeight w:val="300">
-        </w:trHeight>
-      </w:trPr>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="225C7A9A" ns15:textId="6276DE1A" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:ind w:left="-115">
-            </w:ind>
-            <w:jc w:val="left">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="47FBA2BA" ns15:textId="1858D725" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:jc w:val="center">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2945">
-          </w:tcW>
-          <w:tcMar>
-          </w:tcMar>
-        </w:tcPr>
-        <w:p ns15:paraId="75BDF01C" ns15:textId="0B664CB4" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:bidi w:val="0">
-            </w:bidi>
-            <w:ind w:right="-115">
-            </w:ind>
-            <w:jc w:val="right">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-    </w:tr>
-  </w:tbl>
-  <w:p ns15:paraId="69AF5CCB" ns15:textId="42C3DD17" w:rsidP="473E729D" w:rsidR="473E729D" w:rsidRDefault="473E729D">
-    <w:pPr>
-      <w:pStyle w:val="7">
-      </w:pStyle>
-      <w:bidi w:val="0">
-      </w:bidi>
-    </w:pPr>
-  </w:p>
-</w:ftr>
```

</details>

<details><summary>word/footnotes.xml — F15</summary>

```diff
--- A/word/footnotes.xml
+++ B/word/footnotes.xml
@@ -1,6 +1,6 @@
-<w:footnotes ns14:Ignorable="w14 w15 wp14">
-  <w:footnote w:id="0" w:type="separator">
-    <w:p ns15:paraId="5DAB6C7B" ns15:textId="77777777">
+<w:footnotes ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
+  <w:footnote w:id="-1" w:type="separator">
+    <w:p ns15:paraId="5B4D8DB9" ns15:textId="77777777" w:rsidP="003148F9" w:rsidR="0098426C" w:rsidRDefault="0098426C">
       <w:pPr>
-        <w:spacing w:after="0" w:before="0" w:line="259" w:lineRule="auto">
+        <w:spacing w:after="0" w:line="240" w:lineRule="auto">
         </w:spacing>
@@ -13,6 +13,6 @@
   </w:footnote>
-  <w:footnote w:id="1" w:type="continuationSeparator">
-    <w:p ns15:paraId="02EB378F" ns15:textId="77777777">
+  <w:footnote w:id="0" w:type="continuationSeparator">
+    <w:p ns15:paraId="245E05BB" ns15:textId="77777777" w:rsidP="003148F9" w:rsidR="0098426C" w:rsidRDefault="0098426C">
       <w:pPr>
-        <w:spacing w:after="0" w:before="0" w:line="259" w:lineRule="auto">
+        <w:spacing w:after="0" w:line="240" w:lineRule="auto">
         </w:spacing>
```

</details>

<details><summary>word/header1.xml — F07</summary>

```diff
--- A/word/header1.xml
+++ B/word/header1.xml
@@ -1,156 +1,37 @@
-<w:hdr ns14:Ignorable="w14 w15 wp14">
-  <w:tbl>
-    <w:tblPr>
-      <w:tblStyle w:val="9">
-      </w:tblStyle>
-      <w:tblW w:type="auto" w:w="0">
-      </w:tblW>
-      <w:tblInd w:type="dxa" w:w="0">
-      </w:tblInd>
-      <w:tblBorders>
-        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:top>
-        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:left>
-        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:bottom>
-        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:right>
-        <w:insideH w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:insideH>
-        <w:insideV w:color="auto" w:space="0" w:sz="0" w:val="none">
-        </w:insideV>
-      </w:tblBorders>
-      <w:tblLayout w:type="autofit">
-      </w:tblLayout>
-      <w:tblCellMar>
-        <w:top w:type="dxa" w:w="0">
-        </w:top>
-        <w:left w:type="dxa" w:w="108">
-        </w:left>
-        <w:bottom w:type="dxa" w:w="0">
-        </w:bottom>
-        <w:right w:type="dxa" w:w="108">
-        </w:right>
-      </w:tblCellMar>
-    </w:tblPr>
-    <w:tblGrid>
-      <w:gridCol w:w="6521">
-      </w:gridCol>
-      <w:gridCol w:w="2307">
-      </w:gridCol>
-    </w:tblGrid>
-    <w:tr ns15:paraId="273ABDA2" ns15:textId="77777777">
-      <w:tblPrEx>
-        <w:tblBorders>
-          <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:top>
-          <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:left>
-          <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:bottom>
-          <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:right>
-          <w:insideH w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:insideH>
-          <w:insideV w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:insideV>
-        </w:tblBorders>
-        <w:tblCellMar>
-          <w:top w:type="dxa" w:w="0">
-          </w:top>
-          <w:left w:type="dxa" w:w="108">
-          </w:left>
-          <w:bottom w:type="dxa" w:w="0">
-          </w:bottom>
-          <w:right w:type="dxa" w:w="108">
-          </w:right>
-        </w:tblCellMar>
-      </w:tblPrEx>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="6521">
-          </w:tcW>
-        </w:tcPr>
-        <w:p ns15:paraId="097B0769" ns15:textId="77777777">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:rPr>
-              <w:lang w:val="en-US">
-              </w:lang>
-            </w:rPr>
-          </w:pPr>
-          <w:r>
-            <w:rPr>
-              <w:lang w:val="en-US">
-              </w:lang>
-            </w:rPr>
-            <w:t ns16:space="preserve">
-              TEXT "D. Beltrán et al. / Abstraction & Application "
-            </w:t>
-          </w:r>
-          <w:r>
-            <w:rPr>
-              <w:b>
-              </w:b>
-              <w:lang w:val="en-US">
-              </w:lang>
-            </w:rPr>
-            <w:t>
-              TEXT "41"
-            </w:t>
-          </w:r>
-          <w:r>
-            <w:rPr>
-              <w:lang w:val="en-US">
-              </w:lang>
-            </w:rPr>
-            <w:t ns16:space="preserve">
-              TEXT " (2023) 3 - 16"
-            </w:t>
-          </w:r>
-        </w:p>
-      </w:tc>
-      <w:tc>
-        <w:tcPr>
-          <w:tcW w:type="dxa" w:w="2307">
-          </w:tcW>
-        </w:tcPr>
-        <w:p ns15:paraId="4FD80E8D" ns15:textId="77777777">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:jc w:val="right">
-            </w:jc>
-            <w:rPr>
-              <w:rFonts w:hint="default">
-              </w:rFonts>
-              <w:lang w:val="es-CO">
-              </w:lang>
-            </w:rPr>
-          </w:pPr>
-        </w:p>
-        <w:p ns15:paraId="2EB31509" ns15:textId="77777777">
-          <w:pPr>
-            <w:pStyle w:val="6">
-            </w:pStyle>
-            <w:jc w:val="right">
-            </w:jc>
-          </w:pPr>
-        </w:p>
-      </w:tc>
-    </w:tr>
-  </w:tbl>
-  <w:p ns15:paraId="1389AEA5" ns15:textId="77777777">
+<w:hdr>
+  <w:p>
     <w:pPr>
-      <w:pStyle w:val="6">
-      </w:pStyle>
+      <w:tabs>
+        <w:tab w:pos="8838" w:val="right">
+        </w:tab>
+      </w:tabs>
+      <w:spacing w:after="0" w:before="0">
+      </w:spacing>
     </w:pPr>
-  </w:p>
-  <w:p ns15:paraId="23FDABA9" ns15:textId="77777777">
-    <w:pPr>
-      <w:pStyle w:val="6">
-      </w:pStyle>
-    </w:pPr>
+    <w:r>
+      <w:rPr>
+        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri">
+        </w:rFonts>
+        <w:sz w:val="18">
+        </w:sz>
+      </w:rPr>
+      <w:t>
+        TEXT "Saber Pro · Paz Bedoya y Orozco Morales · DRAFT"
+      </w:t>
+    </w:r>
+    <w:r>
+      <w:tab>
+      </w:tab>
+    </w:r>
+    <w:fldSimple w:instr="PAGE">
+      <w:r>
+        <w:rPr>
+          <w:sz w:val="18">
+          </w:sz>
+        </w:rPr>
+        <w:t>
+          TEXT "2"
+        </w:t>
+      </w:r>
+    </w:fldSimple>
   </w:p>
```

</details>

<details><summary>word/header2.xml — F08</summary>

```diff
--- A/word/header2.xml
+++ B/word/header2.xml
@@ -1,36 +1,37 @@
-<w:hdr ns14:Ignorable="w14 w15 wp14">
-  <w:p ns15:paraId="40F23D78" ns15:textId="77777777">
+<w:hdr>
+  <w:p>
     <w:pPr>
-      <w:pStyle w:val="6">
-      </w:pStyle>
+      <w:tabs>
+        <w:tab w:pos="8838" w:val="right">
+        </w:tab>
+      </w:tabs>
+      <w:spacing w:after="0" w:before="0">
+      </w:spacing>
     </w:pPr>
-    <w:sdt>
-      <w:sdtPr>
-        <w:id w:val="-1765987065">
-        </w:id>
-        <w:docPartObj>
-          <w:docPartGallery w:val="autotext">
-          </w:docPartGallery>
-        </w:docPartObj>
-      </w:sdtPr>
-      <w:sdtContent>
-        <w:r>
-          <w:rPr>
-            <w:rFonts w:hint="default">
-            </w:rFonts>
-            <w:lang w:val="es-CO">
-            </w:lang>
-          </w:rPr>
-          <w:t ns16:space="preserve">
-            TEXT "Predicción del promedio  global de Saber Pro mediante LightGBM y auditorría de fuga temporal: Un estudio a nivel de programa académico en Colombia "
-          </w:t>
-        </w:r>
-      </w:sdtContent>
-    </w:sdt>
-  </w:p>
-  <w:p ns15:paraId="282CEDBA" ns15:textId="77777777">
-    <w:pPr>
-      <w:pStyle w:val="6">
-      </w:pStyle>
-    </w:pPr>
+    <w:r>
+      <w:rPr>
+        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri">
+        </w:rFonts>
+        <w:sz w:val="18">
+        </w:sz>
+      </w:rPr>
+      <w:t>
+        TEXT "Saber Pro · Paz Bedoya y Orozco Morales · DRAFT"
+      </w:t>
+    </w:r>
+    <w:r>
+      <w:tab>
+      </w:tab>
+    </w:r>
+    <w:fldSimple w:instr="PAGE">
+      <w:r>
+        <w:rPr>
+          <w:sz w:val="18">
+          </w:sz>
+        </w:rPr>
+        <w:t>
+          TEXT "2"
+        </w:t>
+      </w:r>
+    </w:fldSimple>
   </w:p>
```

</details>

<details><summary>word/header3.xml — F09/F11</summary>

```diff
--- A/word/header3.xml
+++ B/word/header3.xml
@@ -1,5 +1,5 @@
-<w:hdr ns14:Ignorable="w14 w15 wp14">
+<w:hdr ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
   <w:tbl>
     <w:tblPr>
-      <w:tblStyle w:val="9">
+      <w:tblStyle w:val="Tablaconcuadrcula">
       </w:tblStyle>
@@ -7,4 +7,2 @@
       </w:tblW>
-      <w:tblInd w:type="dxa" w:w="0">
-      </w:tblInd>
       <w:tblBorders>
@@ -23,14 +21,4 @@
       </w:tblBorders>
-      <w:tblLayout w:type="autofit">
-      </w:tblLayout>
-      <w:tblCellMar>
-        <w:top w:type="dxa" w:w="0">
-        </w:top>
-        <w:left w:type="dxa" w:w="108">
-        </w:left>
-        <w:bottom w:type="dxa" w:w="0">
-        </w:bottom>
-        <w:right w:type="dxa" w:w="108">
-        </w:right>
-      </w:tblCellMar>
+      <w:tblLook w:firstColumn="1" w:firstRow="1" w:lastColumn="0" w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0">
+      </w:tblLook>
     </w:tblPr>
@@ -42,29 +30,3 @@
     </w:tblGrid>
-    <w:tr ns15:paraId="2C68E7BA" ns15:textId="77777777">
-      <w:tblPrEx>
-        <w:tblBorders>
-          <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:top>
-          <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:left>
-          <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:bottom>
-          <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:right>
-          <w:insideH w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:insideH>
-          <w:insideV w:color="auto" w:space="0" w:sz="0" w:val="none">
-          </w:insideV>
-        </w:tblBorders>
-        <w:tblCellMar>
-          <w:top w:type="dxa" w:w="0">
-          </w:top>
-          <w:left w:type="dxa" w:w="108">
-          </w:left>
-          <w:bottom w:type="dxa" w:w="0">
-          </w:bottom>
-          <w:right w:type="dxa" w:w="108">
-          </w:right>
-        </w:tblCellMar>
-      </w:tblPrEx>
+    <w:tr ns15:paraId="2C68E7BA" ns15:textId="77777777" w:rsidR="00354B44" w:rsidTr="00354B44">
       <w:tc>
@@ -74,5 +36,5 @@
         </w:tcPr>
-        <w:p ns15:paraId="3FB65ADC" ns15:textId="77777777">
+        <w:p ns15:paraId="3FB65ADC" ns15:textId="77777777" w:rsidR="00354B44" w:rsidRDefault="00354B44" w:rsidRPr="00354B44">
           <w:pPr>
-            <w:pStyle w:val="6">
+            <w:pStyle w:val="Encabezado">
             </w:pStyle>
@@ -84,5 +46,5 @@
         </w:p>
-        <w:p ns15:paraId="51C87AFE" ns15:textId="77777777">
+        <w:p ns15:paraId="51C87AFE" ns15:textId="77777777" w:rsidR="00354B44" w:rsidRDefault="00354B44" w:rsidRPr="00354B44">
           <w:pPr>
-            <w:pStyle w:val="6">
+            <w:pStyle w:val="Encabezado">
             </w:pStyle>
@@ -94,5 +56,5 @@
         </w:p>
-        <w:p ns15:paraId="132350A5" ns15:textId="77777777">
+        <w:p ns15:paraId="132350A5" ns15:textId="77777777" w:rsidR="00354B44" w:rsidRDefault="00354B44" w:rsidRPr="00354B44">
           <w:pPr>
-            <w:pStyle w:val="6">
+            <w:pStyle w:val="Encabezado">
             </w:pStyle>
@@ -104,5 +66,5 @@
         </w:p>
-        <w:p ns15:paraId="4CD992C5" ns15:textId="77777777">
+        <w:p ns15:paraId="4CD992C5" ns15:textId="29735672" w:rsidR="00354B44" w:rsidRDefault="00354B44" w:rsidRPr="00354B44">
           <w:pPr>
-            <w:pStyle w:val="6">
+            <w:pStyle w:val="Encabezado">
             </w:pStyle>
@@ -119,23 +81,3 @@
             <w:t>
-              TEXT "Abstraction & Application (202"
-            </w:t>
-          </w:r>
-          <w:r>
-            <w:rPr>
-              <w:rFonts w:hint="default">
-              </w:rFonts>
-              <w:lang w:val="es-CO">
-              </w:lang>
-            </w:rPr>
-            <w:t>
-              TEXT "6"
-            </w:t>
-          </w:r>
-          <w:r>
-            <w:rPr>
-              <w:lang w:val="en-US">
-              </w:lang>
-            </w:rPr>
-            <w:t ns16:space="preserve">
-              TEXT ") "
+              TEXT "Abstraction & Application · CONACIC 2026 · DRAFT"
             </w:t>
@@ -149,5 +91,5 @@
         </w:tcPr>
-        <w:p ns15:paraId="51E07EAF" ns15:textId="77777777">
+        <w:p ns15:paraId="51E07EAF" ns15:textId="77777777" w:rsidP="00354B44" w:rsidR="00354B44" w:rsidRDefault="00354B44">
           <w:pPr>
-            <w:pStyle w:val="6">
+            <w:pStyle w:val="Encabezado">
             </w:pStyle>
@@ -163,2 +105,4 @@
             <w:rPr>
+              <w:noProof>
+              </w:noProof>
               <w:lang w:val="en-US">
@@ -167,4 +111,4 @@
             <w:drawing>
-              <wp:inline distB="0" distL="0" distR="0" distT="0" ns17:anchorId="185771DF" ns17:editId="7777777">
-                <wp:extent cx="433705" cy="751205">
+              <wp:inline distB="0" distL="0" distR="0" distT="0" ns17:anchorId="55A823B7" ns17:editId="2E6EFF45">
+                <wp:extent cx="434123" cy="751224">
                 </wp:extent>
@@ -182,3 +126,3 @@
                       <pic:nvPicPr>
-                        <pic:cNvPr descr="C:\\Users\\mramirez\\Documents\\2016\\sem2-2016\\Abstraction & Application\\Template\\uady.jpg" id="4" name="Imagen 4">
+                        <pic:cNvPr descr="C:\\Users\\mramirez\\Documents\\2016\\sem2-2016\\Abstraction & Application\\Template\\uady.jpg" id="0" name="Picture 3">
                         </pic:cNvPr>
@@ -205,3 +149,3 @@
                       </pic:blipFill>
-                      <pic:spPr>
+                      <pic:spPr bwMode="auto">
                         <a:xfrm flipH="1">
@@ -233,5 +177,5 @@
   </w:tbl>
-  <w:p ns15:paraId="4F8E907A" ns15:textId="77777777">
+  <w:p ns15:paraId="4F8E907A" ns15:textId="77777777" w:rsidR="00902151" w:rsidRDefault="00902151">
     <w:pPr>
-      <w:pStyle w:val="6">
+      <w:pStyle w:val="Encabezado">
       </w:pStyle>
```

</details>

<details><summary>word/numbering.xml — F15</summary>

```diff
--- A/word/numbering.xml
+++ B/word/numbering.xml
@@ -0,0 +1,1030 @@
+<w:numbering ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="0">
+    <w:nsid w:val="0B090D4B">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="4C2ED638">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="1">
+    <w:nsid w:val="11F2290C">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="CC5A2870">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="FFFFFFFF">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="•">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="2">
+    <w:nsid w:val="550F68E0">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="52DE7032">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="FFFFFFFF">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="•">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="3">
+    <w:nsid w:val="59F67E19">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="C50CF50E">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="FFFFFFFF">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="•">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="4">
+    <w:nsid w:val="5EBC0EE1">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="DB640A2E">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:abstractNum ns19:restartNumberingAfterBreak="0" w:abstractNumId="5">
+    <w:nsid w:val="6FA72CCA">
+    </w:nsid>
+    <w:multiLevelType w:val="hybridMultilevel">
+    </w:multiLevelType>
+    <w:tmpl w:val="0DD2B546">
+    </w:tmpl>
+    <w:lvl w:ilvl="0" w:tplc="FFFFFFFF">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="•">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="720">
+        </w:ind>
+      </w:pPr>
+    </w:lvl>
+    <w:lvl w:ilvl="1" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="1440">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="2" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2160">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="3" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="2880">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="4" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="3600">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="5" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="4320">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="6" w:tentative="1" w:tplc="080A0001">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5040">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="7" w:tentative="1" w:tplc="080A0003">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="o">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="5760">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Courier New" w:cs="Courier New" w:hAnsi="Courier New" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+    <w:lvl w:ilvl="8" w:tentative="1" w:tplc="080A0005">
+      <w:start w:val="1">
+      </w:start>
+      <w:numFmt w:val="bullet">
+      </w:numFmt>
+      <w:lvlText w:val="">
+      </w:lvlText>
+      <w:lvlJc w:val="left">
+      </w:lvlJc>
+      <w:pPr>
+        <w:ind w:hanging="360" w:left="6480">
+        </w:ind>
+      </w:pPr>
+      <w:rPr>
+        <w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default">
+        </w:rFonts>
+      </w:rPr>
+    </w:lvl>
+  </w:abstractNum>
+  <w:num ns20:durableId="2122914136" w:numId="1">
+    <w:abstractNumId w:val="1">
+    </w:abstractNumId>
+  </w:num>
+  <w:num ns20:durableId="1428845920" w:numId="2">
+    <w:abstractNumId w:val="5">
+    </w:abstractNumId>
+  </w:num>
+  <w:num ns20:durableId="238103284" w:numId="3">
+    <w:abstractNumId w:val="2">
+    </w:abstractNumId>
+  </w:num>
+  <w:num ns20:durableId="325548940" w:numId="4">
+    <w:abstractNumId w:val="3">
+    </w:abstractNumId>
+  </w:num>
+  <w:num ns20:durableId="2030787272" w:numId="5">
+    <w:abstractNumId w:val="0">
+    </w:abstractNumId>
+  </w:num>
+  <w:num ns20:durableId="1493764500" w:numId="6">
+    <w:abstractNumId w:val="4">
+    </w:abstractNumId>
+  </w:num>
+</w:numbering>
```

</details>

<details><summary>word/settings.xml — F15</summary>

```diff
--- A/word/settings.xml
+++ B/word/settings.xml
@@ -1,12 +1,6 @@
-<w:settings ns14:Ignorable="w14 wp14 w15">
-  <w:zoom w:percent="80">
+<w:settings ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh">
+  <w:zoom w:percent="100">
   </w:zoom>
-  <w:bordersDoNotSurroundHeader w:val="0">
-  </w:bordersDoNotSurroundHeader>
-  <w:bordersDoNotSurroundFooter w:val="0">
-  </w:bordersDoNotSurroundFooter>
-  <w:trackRevisions w:val="false">
-  </w:trackRevisions>
-  <w:documentProtection w:enforcement="0">
-  </w:documentProtection>
+  <w:proofState w:grammar="clean" w:spelling="clean">
+  </w:proofState>
   <w:defaultTabStop w:val="708">
@@ -15,16 +9,14 @@
   </w:hyphenationZone>
-  <w:evenAndOddHeaders w:val="1">
+  <w:evenAndOddHeaders>
   </w:evenAndOddHeaders>
-  <w:displayHorizontalDrawingGridEvery w:val="1">
-  </w:displayHorizontalDrawingGridEvery>
-  <w:displayVerticalDrawingGridEvery w:val="1">
-  </w:displayVerticalDrawingGridEvery>
-  <w:noPunctuationKerning w:val="1">
-  </w:noPunctuationKerning>
   <w:characterSpacingControl w:val="doNotCompress">
   </w:characterSpacingControl>
+  <w:hdrShapeDefaults>
+    <ns23:shapedefaults spidmax="2050" ns24:ext="edit">
+    </ns23:shapedefaults>
+  </w:hdrShapeDefaults>
   <w:footnotePr>
+    <w:footnote w:id="-1">
+    </w:footnote>
     <w:footnote w:id="0">
-    </w:footnote>
-    <w:footnote w:id="1">
     </w:footnote>
@@ -32,5 +24,5 @@
   <w:endnotePr>
+    <w:endnote w:id="-1">
+    </w:endnote>
     <w:endnote w:id="0">
-    </w:endnote>
-    <w:endnote w:id="1">
     </w:endnote>
@@ -38,8 +30,2 @@
   <w:compat>
-    <w:doNotExpandShiftReturn>
-    </w:doNotExpandShiftReturn>
-    <w:doNotWrapTextWithPunct>
-    </w:doNotWrapTextWithPunct>
-    <w:doNotUseEastAsianBreakRules>
-    </w:doNotUseEastAsianBreakRules>
     <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15">
@@ -53,2 +39,4 @@
     <w:compatSetting w:name="differentiateMultirowTableHeaders" w:uri="http://schemas.microsoft.com/office/word" w:val="1">
+    </w:compatSetting>
+    <w:compatSetting w:name="useWord2013TrackBottomHyphenation" w:uri="http://schemas.microsoft.com/office/word" w:val="1">
     </w:compatSetting>
@@ -339,28 +327,2 @@
     <w:rsid w:val="00FE2640">
-    </w:rsid>
-    <w:rsid w:val="0666039B">
-    </w:rsid>
-    <w:rsid w:val="2E047574">
-    </w:rsid>
-    <w:rsid w:val="342BDDA3">
-    </w:rsid>
-    <w:rsid w:val="342BDDA3">
-    </w:rsid>
-    <w:rsid w:val="36A5FF65">
-    </w:rsid>
-    <w:rsid w:val="42BDCB48">
-    </w:rsid>
-    <w:rsid w:val="473E729D">
-    </w:rsid>
-    <w:rsid w:val="4A63C43C">
-    </w:rsid>
-    <w:rsid w:val="4B915CC7">
-    </w:rsid>
-    <w:rsid w:val="60A79DC1">
-    </w:rsid>
-    <w:rsid w:val="617C5E13">
-    </w:rsid>
-    <w:rsid w:val="65904230">
-    </w:rsid>
-    <w:rsid w:val="7118E9F6">
     </w:rsid>
@@ -391,3 +353,3 @@
   </ns21:mathPr>
-  <w:themeFontLang w:eastAsia="zh-CN" w:val="es-MX">
+  <w:themeFontLang w:val="es-MX">
   </w:themeFontLang>
@@ -395,12 +357,22 @@
   </w:clrSchemeMapping>
-  <ns15:docId ns15:val="0C8D3697">
+  <w:shapeDefaults>
+    <ns23:shapedefaults spidmax="2050" ns24:ext="edit">
+    </ns23:shapedefaults>
+    <ns23:shapelayout ns24:ext="edit">
+      <ns23:idmap data="2" ns24:ext="edit">
+      </ns23:idmap>
+    </ns23:shapelayout>
+  </w:shapeDefaults>
+  <w:decimalSymbol w:val=".">
+  </w:decimalSymbol>
+  <w:listSeparator w:val=",">
+  </w:listSeparator>
+  <ns15:docId ns15:val="0953BD6B">
   </ns15:docId>
-  <ns19:docId ns19:val="{E89F9E52-5C94-428B-89EF-D63C9AF9EB0A}">
+  <ns19:chartTrackingRefBased>
+  </ns19:chartTrackingRefBased>
+  <ns19:docId ns19:val="{53362516-0A2C-415D-A461-D336EFC7FFBA}">
   </ns19:docId>
-  <ns14:AlternateContent>
-    <ns14:Choice Requires="wpsCustomData">
-      <ns22:typoFeatureVersion val="1">
-      </ns22:typoFeatureVersion>
-    </ns14:Choice>
-  </ns14:AlternateContent>
+  <w:updateFields w:val="true">
+  </w:updateFields>
 </w:settings>
```

</details>

<details><summary>word/styles.xml — F06</summary>

```diff
--- A/word/styles.xml
+++ B/word/styles.xml
@@ -1,2 +1,2 @@
-<w:styles ns14:Ignorable="w14 wp14">
+<w:styles ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh">
   <w:docDefaults>
@@ -4,4 +4,10 @@
       <w:rPr>
-        <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman">
+        <w:rFonts w:asciiTheme="minorHAnsi" w:cstheme="minorBidi" w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi">
         </w:rFonts>
+        <w:sz w:val="22">
+        </w:sz>
+        <w:szCs w:val="22">
+        </w:szCs>
+        <w:lang w:bidi="ar-SA" w:eastAsia="en-US" w:val="es-MX">
+        </w:lang>
       </w:rPr>
@@ -9,309 +15,757 @@
     <w:pPrDefault>
+      <w:pPr>
+        <w:spacing w:after="160" w:line="259" w:lineRule="auto">
+        </w:spacing>
+      </w:pPr>
     </w:pPrDefault>
   </w:docDefaults>
-  <w:latentStyles w:count="260" w:defLockedState="0" w:defQFormat="0" w:defSemiHidden="1" w:defUIPriority="99" w:defUnhideWhenUsed="1">
-    <w:lsdException w:name="Normal" w:qFormat="1" w:semiHidden="0" w:uiPriority="0" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="heading 1" w:qFormat="1" w:semiHidden="0" w:uiPriority="9" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="heading 2" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 3" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 4" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 5" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 6" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 7" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 8" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="heading 9" w:qFormat="1" w:uiPriority="9">
-    </w:lsdException>
-    <w:lsdException w:name="index 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 6" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 7" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 8" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index 9" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="toc 1" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 2" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 3" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 4" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 5" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 6" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 7" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 8" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="toc 9" w:uiPriority="39">
-    </w:lsdException>
-    <w:lsdException w:name="Normal Indent" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="footnote text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="annotation text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="header" w:qFormat="1" w:semiHidden="0" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="footer" w:qFormat="1" w:semiHidden="0" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="index heading" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="caption" w:qFormat="1" w:uiPriority="35">
-    </w:lsdException>
-    <w:lsdException w:name="table of figures" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="envelope address" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="envelope return" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="footnote reference" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="annotation reference" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="line number" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="page number" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="endnote reference" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="endnote text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="table of authorities" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="macro" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="toa heading" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Bullet" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Number" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Bullet 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Bullet 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Bullet 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Bullet 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Number 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Number 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Number 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Number 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Title" w:qFormat="1" w:semiHidden="0" w:uiPriority="10" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Closing" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Signature" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Default Paragraph Font" w:qFormat="1" w:uiPriority="1">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text" w:qFormat="1" w:semiHidden="0" w:uiPriority="0" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text Indent" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Continue" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Continue 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Continue 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Continue 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="List Continue 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Message Header" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Subtitle" w:qFormat="1" w:semiHidden="0" w:uiPriority="11" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Salutation" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Date" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text First Indent" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text First Indent 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Note Heading" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text Indent 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Body Text Indent 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Block Text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Hyperlink" w:qFormat="1" w:semiHidden="0" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="FollowedHyperlink" w:qFormat="1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Strong" w:qFormat="1" w:semiHidden="0" w:uiPriority="22" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Emphasis" w:qFormat="1" w:semiHidden="0" w:uiPriority="20" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Document Map" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Plain Text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="E-mail Signature" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Normal (Web)" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Acronym" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Address" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Cite" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Code" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Definition" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Keyboard" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Preformatted" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Sample" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Typewriter" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="HTML Variable" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Normal Table" w:qFormat="1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="annotation subject" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Simple 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Simple 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Simple 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Classic 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Classic 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Classic 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Classic 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Colorful 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Colorful 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Colorful 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Columns 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Columns 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Columns 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Columns 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Columns 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 6" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 7" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid 8" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 4" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 5" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 6" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 7" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table List 8" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table 3D effects 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table 3D effects 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table 3D effects 3" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Contemporary" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Elegant" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Professional" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Subtle 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Subtle 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Web 1" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Web 2" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Web 3" w:semiHidden="0" w:uiPriority="99" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Balloon Text" w:uiPriority="99">
-    </w:lsdException>
-    <w:lsdException w:name="Table Grid" w:qFormat="1" w:semiHidden="0" w:uiPriority="39" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="Table Theme" w:semiHidden="0" w:uiPriority="99" w:unhideWhenUsed="0">
-    </w:lsdException>
-    <w:lsdException w:name="List Paragraph" w:qFormat="1" w:semiHidden="0" w:uiPriority="34" w:unhideWhenUsed="0">
+  <w:latentStyles w:count="376" w:defLockedState="0" w:defQFormat="0" w:defSemiHidden="0" w:defUIPriority="99" w:defUnhideWhenUsed="0">
+    <w:lsdException w:name="Normal" w:qFormat="1" w:uiPriority="0">
+    </w:lsdException>
+    <w:lsdException w:name="heading 1" w:qFormat="1" w:uiPriority="9">
+    </w:lsdException>
+    <w:lsdException w:name="heading 2" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 3" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 4" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 5" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 6" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 7" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 8" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="heading 9" w:qFormat="1" w:semiHidden="1" w:uiPriority="9" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 6" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 7" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 8" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index 9" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 1" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 2" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 3" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 4" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 5" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 6" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 7" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 8" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toc 9" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Normal Indent" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="footnote text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="annotation text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="header" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="footer" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="index heading" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="caption" w:qFormat="1" w:semiHidden="1" w:uiPriority="35" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="table of figures" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="envelope address" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="envelope return" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="footnote reference" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="annotation reference" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="line number" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="page number" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="endnote reference" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="endnote text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="table of authorities" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="macro" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="toa heading" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Bullet" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Number" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Bullet 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Bullet 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Bullet 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Bullet 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Number 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Number 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Number 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Number 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Title" w:qFormat="1" w:uiPriority="10">
+    </w:lsdException>
+    <w:lsdException w:name="Closing" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Signature" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Default Paragraph Font" w:semiHidden="1" w:uiPriority="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text" w:semiHidden="1" w:uiPriority="0" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text Indent" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Continue" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Continue 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Continue 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Continue 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Continue 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Message Header" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Subtitle" w:qFormat="1" w:uiPriority="11">
+    </w:lsdException>
+    <w:lsdException w:name="Salutation" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Date" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text First Indent" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text First Indent 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Note Heading" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text Indent 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Body Text Indent 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Block Text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Hyperlink" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="FollowedHyperlink" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Strong" w:qFormat="1" w:uiPriority="22">
+    </w:lsdException>
+    <w:lsdException w:name="Emphasis" w:qFormat="1" w:uiPriority="20">
+    </w:lsdException>
+    <w:lsdException w:name="Document Map" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="E-mail Signature" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Top of Form" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Bottom of Form" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Normal (Web)" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Acronym" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Address" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Cite" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Code" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Definition" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Keyboard" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Preformatted" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Sample" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Typewriter" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="HTML Variable" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="annotation subject" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="No List" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Outline List 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Outline List 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Outline List 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Simple 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Simple 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Simple 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Classic 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Classic 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Classic 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Classic 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Colorful 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Colorful 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Colorful 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Columns 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Columns 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Columns 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Columns 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Columns 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 6" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 7" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid 8" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 4" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 5" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 6" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 7" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table List 8" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table 3D effects 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table 3D effects 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table 3D effects 3" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Contemporary" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Elegant" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Professional" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Subtle 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Subtle 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Web 1" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Web 2" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Balloon Text" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Table Grid" w:uiPriority="39">
+    </w:lsdException>
+    <w:lsdException w:name="Placeholder Text" w:semiHidden="1">
+    </w:lsdException>
+    <w:lsdException w:name="No Spacing" w:qFormat="1" w:uiPriority="1">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 1" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 1" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 1" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 1" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 1" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 1" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Revision" w:semiHidden="1">
+    </w:lsdException>
+    <w:lsdException w:name="List Paragraph" w:qFormat="1" w:uiPriority="34">
+    </w:lsdException>
+    <w:lsdException w:name="Quote" w:qFormat="1" w:uiPriority="29">
+    </w:lsdException>
+    <w:lsdException w:name="Intense Quote" w:qFormat="1" w:uiPriority="30">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 1" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 1" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 1" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 1" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 1" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 1" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 1" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 1" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 2" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 2" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 2" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 2" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 2" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 2" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 2" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 2" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 2" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 2" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 2" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 2" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 2" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 2" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 3" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 3" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 3" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 3" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 3" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 3" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 3" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 3" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 3" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 3" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 3" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 3" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 3" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 3" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 4" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 4" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 4" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 4" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 4" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 4" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 4" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 4" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 4" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 4" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 4" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 4" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 4" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 4" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 5" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 5" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 5" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 5" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 5" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 5" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 5" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 5" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 5" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 5" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 5" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 5" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 5" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 5" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Light Shading Accent 6" w:uiPriority="60">
+    </w:lsdException>
+    <w:lsdException w:name="Light List Accent 6" w:uiPriority="61">
+    </w:lsdException>
+    <w:lsdException w:name="Light Grid Accent 6" w:uiPriority="62">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 1 Accent 6" w:uiPriority="63">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Shading 2 Accent 6" w:uiPriority="64">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 1 Accent 6" w:uiPriority="65">
+    </w:lsdException>
+    <w:lsdException w:name="Medium List 2 Accent 6" w:uiPriority="66">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 1 Accent 6" w:uiPriority="67">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 2 Accent 6" w:uiPriority="68">
+    </w:lsdException>
+    <w:lsdException w:name="Medium Grid 3 Accent 6" w:uiPriority="69">
+    </w:lsdException>
+    <w:lsdException w:name="Dark List Accent 6" w:uiPriority="70">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Shading Accent 6" w:uiPriority="71">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful List Accent 6" w:uiPriority="72">
+    </w:lsdException>
+    <w:lsdException w:name="Colorful Grid Accent 6" w:uiPriority="73">
+    </w:lsdException>
+    <w:lsdException w:name="Subtle Emphasis" w:qFormat="1" w:uiPriority="19">
+    </w:lsdException>
+    <w:lsdException w:name="Intense Emphasis" w:qFormat="1" w:uiPriority="21">
+    </w:lsdException>
+    <w:lsdException w:name="Subtle Reference" w:qFormat="1" w:uiPriority="31">
+    </w:lsdException>
+    <w:lsdException w:name="Intense Reference" w:qFormat="1" w:uiPriority="32">
+    </w:lsdException>
+    <w:lsdException w:name="Book Title" w:qFormat="1" w:uiPriority="33">
+    </w:lsdException>
+    <w:lsdException w:name="Bibliography" w:semiHidden="1" w:uiPriority="37" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="TOC Heading" w:qFormat="1" w:semiHidden="1" w:uiPriority="39" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Table 1" w:uiPriority="41">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Table 2" w:uiPriority="42">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Table 3" w:uiPriority="43">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Table 4" w:uiPriority="44">
+    </w:lsdException>
+    <w:lsdException w:name="Plain Table 5" w:uiPriority="45">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table Light" w:uiPriority="40">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 1" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 1" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 1" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 1" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 1" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 1" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 1" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 2" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 2" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 2" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 2" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 2" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 2" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 2" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 3" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 3" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 3" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 3" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 3" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 3" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 3" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 4" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 4" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 4" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 4" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 4" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 4" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 4" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 5" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 5" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 5" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 5" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 5" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 5" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 5" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 1 Light Accent 6" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 2 Accent 6" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 3 Accent 6" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 4 Accent 6" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 5 Dark Accent 6" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 6 Colorful Accent 6" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="Grid Table 7 Colorful Accent 6" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 1" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 1" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 1" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 1" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 1" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 1" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 1" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 2" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 2" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 2" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 2" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 2" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 2" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 2" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 3" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 3" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 3" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 3" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 3" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 3" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 3" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 4" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 4" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 4" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 4" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 4" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 4" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 4" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 5" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 5" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 5" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 5" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 5" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 5" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 5" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 1 Light Accent 6" w:uiPriority="46">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 2 Accent 6" w:uiPriority="47">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 3 Accent 6" w:uiPriority="48">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 4 Accent 6" w:uiPriority="49">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 5 Dark Accent 6" w:uiPriority="50">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 6 Colorful Accent 6" w:uiPriority="51">
+    </w:lsdException>
+    <w:lsdException w:name="List Table 7 Colorful Accent 6" w:uiPriority="52">
+    </w:lsdException>
+    <w:lsdException w:name="Mention" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Smart Hyperlink" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Hashtag" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Unresolved Mention" w:semiHidden="1" w:unhideWhenUsed="1">
+    </w:lsdException>
+    <w:lsdException w:name="Smart Link" w:semiHidden="1" w:unhideWhenUsed="1">
     </w:lsdException>
   </w:latentStyles>
-  <w:style w:default="1" w:styleId="1" w:type="paragraph">
+  <w:style w:default="1" w:styleId="Normal" w:type="paragraph">
     <w:name w:val="Normal">
@@ -320,22 +774,8 @@
     </w:qFormat>
-    <w:uiPriority w:val="0">
+  </w:style>
+  <w:style w:default="1" w:styleId="Fuentedeprrafopredeter" w:type="character">
+    <w:name w:val="Default Paragraph Font">
+    </w:name>
+    <w:uiPriority w:val="1">
     </w:uiPriority>
-    <w:pPr>
-      <w:spacing w:after="160" w:line="259" w:lineRule="auto">
-      </w:spacing>
-    </w:pPr>
-    <w:rPr>
-      <w:rFonts w:asciiTheme="minorHAnsi" w:cstheme="minorBidi" w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi">
-      </w:rFonts>
-      <w:sz w:val="22">
-      </w:sz>
-      <w:szCs w:val="22">
-      </w:szCs>
-      <w:lang w:bidi="ar-SA" w:eastAsia="en-US" w:val="es-MX">
-      </w:lang>
-    </w:rPr>
-  </w:style>
-  <w:style w:default="1" w:styleId="2" w:type="character">
-    <w:name w:val="Default Paragraph Font">
-    </w:name>
     <w:semiHidden>
@@ -344,10 +784,8 @@
     </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="1">
+  </w:style>
+  <w:style w:default="1" w:styleId="Tablanormal" w:type="table">
+    <w:name w:val="Normal Table">
+    </w:name>
+    <w:uiPriority w:val="99">
     </w:uiPriority>
-  </w:style>
-  <w:style w:default="1" w:styleId="3" w:type="table">
-    <w:name w:val="Normal Table">
-    </w:name>
     <w:semiHidden>
@@ -356,7 +794,5 @@
     </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
     <w:tblPr>
+      <w:tblInd w:type="dxa" w:w="0">
+      </w:tblInd>
       <w:tblCellMar>
@@ -373,13 +809,23 @@
   </w:style>
-  <w:style w:styleId="4" w:type="character">
-    <w:name w:val="Hyperlink">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
+  <w:style w:default="1" w:styleId="Sinlista" w:type="numbering">
+    <w:name w:val="No List">
+    </w:name>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
+    <w:semiHidden>
+    </w:semiHidden>
     <w:unhideWhenUsed>
     </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
+  </w:style>
+  <w:style w:styleId="Hipervnculo" w:type="character">
+    <w:name w:val="Hyperlink">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
     <w:uiPriority w:val="99">
     </w:uiPriority>
+    <w:unhideWhenUsed>
+    </w:unhideWhenUsed>
+    <w:rsid w:val="00FB33CD">
+    </w:rsid>
     <w:rPr>
@@ -389,49 +835,35 @@
       </w:u>
-      <ns15:textFill>
-        <ns15:solidFill>
-          <ns15:schemeClr ns15:val="hlink">
-          </ns15:schemeClr>
-        </ns15:solidFill>
-      </ns15:textFill>
     </w:rPr>
   </w:style>
-  <w:style w:styleId="5" w:type="character">
-    <w:name w:val="FollowedHyperlink">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:semiHidden>
-    </w:semiHidden>
+  <w:style w:styleId="Prrafodelista" w:type="paragraph">
+    <w:name w:val="List Paragraph">
+    </w:name>
+    <w:basedOn w:val="Normal">
+    </w:basedOn>
+    <w:uiPriority w:val="34">
+    </w:uiPriority>
+    <w:qFormat>
+    </w:qFormat>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
+    <w:pPr>
+      <w:ind w:left="720">
+      </w:ind>
+      <w:contextualSpacing>
+      </w:contextualSpacing>
+    </w:pPr>
+  </w:style>
+  <w:style w:styleId="Encabezado" w:type="paragraph">
+    <w:name w:val="header">
+    </w:name>
+    <w:basedOn w:val="Normal">
+    </w:basedOn>
+    <w:link w:val="EncabezadoCar">
+    </w:link>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
     <w:unhideWhenUsed>
     </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
-    <w:rPr>
-      <w:color w:themeColor="followedHyperlink" w:val="954F72">
-      </w:color>
-      <w:u w:val="single">
-      </w:u>
-      <ns15:textFill>
-        <ns15:solidFill>
-          <ns15:schemeClr ns15:val="folHlink">
-          </ns15:schemeClr>
-        </ns15:solidFill>
-      </ns15:textFill>
-    </w:rPr>
-  </w:style>
-  <w:style w:styleId="6" w:type="paragraph">
-    <w:name w:val="header">
-    </w:name>
-    <w:basedOn w:val="1">
-    </w:basedOn>
-    <w:link w:val="11">
-    </w:link>
-    <w:unhideWhenUsed>
-    </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
     <w:pPr>
@@ -447,15 +879,27 @@
   </w:style>
-  <w:style w:styleId="7" w:type="paragraph">
+  <w:style w:customStyle="1" w:styleId="EncabezadoCar" w:type="character">
+    <w:name w:val="Encabezado Car">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:link w:val="Encabezado">
+    </w:link>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
+  </w:style>
+  <w:style w:styleId="Piedepgina" w:type="paragraph">
     <w:name w:val="footer">
     </w:name>
-    <w:basedOn w:val="1">
-    </w:basedOn>
-    <w:link w:val="12">
+    <w:basedOn w:val="Normal">
+    </w:basedOn>
+    <w:link w:val="PiedepginaCar">
     </w:link>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
     <w:unhideWhenUsed>
     </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
     <w:pPr>
@@ -471,13 +915,153 @@
   </w:style>
-  <w:style w:styleId="8" w:type="paragraph">
+  <w:style w:customStyle="1" w:styleId="PiedepginaCar" w:type="character">
+    <w:name w:val="Pie de página Car">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:link w:val="Piedepgina">
+    </w:link>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
+  </w:style>
+  <w:style w:styleId="Tablaconcuadrcula" w:type="table">
+    <w:name w:val="Table Grid">
+    </w:name>
+    <w:basedOn w:val="Tablanormal">
+    </w:basedOn>
+    <w:uiPriority w:val="39">
+    </w:uiPriority>
+    <w:rsid w:val="003148F9">
+    </w:rsid>
+    <w:pPr>
+      <w:spacing w:after="0" w:line="240" w:lineRule="auto">
+      </w:spacing>
+    </w:pPr>
+    <w:tblPr>
+      <w:tblBorders>
+        <w:top w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:right>
+        <w:insideH w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:insideH>
+        <w:insideV w:color="auto" w:space="0" w:sz="4" w:val="single">
+        </w:insideV>
+      </w:tblBorders>
+    </w:tblPr>
+  </w:style>
+  <w:style w:styleId="Hipervnculovisitado" w:type="character">
+    <w:name w:val="FollowedHyperlink">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
+    <w:semiHidden>
+    </w:semiHidden>
+    <w:unhideWhenUsed>
+    </w:unhideWhenUsed>
+    <w:rsid w:val="001A0190">
+    </w:rsid>
+    <w:rPr>
+      <w:color w:themeColor="followedHyperlink" w:val="954F72">
+      </w:color>
+      <w:u w:val="single">
+      </w:u>
+    </w:rPr>
+  </w:style>
+  <w:style w:customStyle="1" w:styleId="Mencinsinresolver1" w:type="character">
+    <w:name w:val="Mención sin resolver1">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:uiPriority w:val="99">
+    </w:uiPriority>
+    <w:semiHidden>
+    </w:semiHidden>
+    <w:unhideWhenUsed>
+    </w:unhideWhenUsed>
+    <w:rsid w:val="009076C0">
+    </w:rsid>
+    <w:rPr>
+      <w:color w:val="605E5C">
+      </w:color>
+      <w:shd w:color="auto" w:fill="E1DFDD" w:val="clear">
+      </w:shd>
+    </w:rPr>
+  </w:style>
+  <w:style w:customStyle="1" w:styleId="Default" w:type="paragraph">
+    <w:name w:val="Default">
+    </w:name>
+    <w:rsid w:val="00E462E9">
+    </w:rsid>
+    <w:pPr>
+      <w:autoSpaceDE w:val="0">
+      </w:autoSpaceDE>
+      <w:autoSpaceDN w:val="0">
+      </w:autoSpaceDN>
+      <w:adjustRightInd w:val="0">
+      </w:adjustRightInd>
+      <w:spacing w:after="0" w:line="240" w:lineRule="auto">
+      </w:spacing>
+    </w:pPr>
+    <w:rPr>
+      <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:hAnsi="Times New Roman">
+      </w:rFonts>
+      <w:color w:val="000000">
+      </w:color>
+      <w:sz w:val="24">
+      </w:sz>
+      <w:szCs w:val="24">
+      </w:szCs>
+    </w:rPr>
+  </w:style>
+  <w:style w:customStyle="1" w:styleId="keywords" w:type="paragraph">
+    <w:name w:val="key words">
+    </w:name>
+    <w:rsid w:val="0031679F">
+    </w:rsid>
+    <w:pPr>
+      <w:spacing w:after="120" w:line="240" w:lineRule="auto">
+      </w:spacing>
+      <w:ind w:firstLine="288">
+      </w:ind>
+      <w:jc w:val="both">
+      </w:jc>
+    </w:pPr>
+    <w:rPr>
+      <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman">
+      </w:rFonts>
+      <w:b>
+      </w:b>
+      <w:bCs>
+      </w:bCs>
+      <w:i>
+      </w:i>
+      <w:iCs>
+      </w:iCs>
+      <w:noProof>
+      </w:noProof>
+      <w:sz w:val="18">
+      </w:sz>
+      <w:szCs w:val="18">
+      </w:szCs>
+      <w:lang w:val="en-US">
+      </w:lang>
+    </w:rPr>
+  </w:style>
+  <w:style w:styleId="Textoindependiente" w:type="paragraph">
     <w:name w:val="Body Text">
     </w:name>
-    <w:basedOn w:val="1">
-    </w:basedOn>
-    <w:link w:val="16">
+    <w:basedOn w:val="Normal">
+    </w:basedOn>
+    <w:link w:val="TextoindependienteCar">
     </w:link>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
+    <w:rsid w:val="00387225">
+    </w:rsid>
     <w:pPr>
@@ -503,167 +1087,11 @@
   </w:style>
-  <w:style w:styleId="9" w:type="table">
-    <w:name w:val="Table Grid">
-    </w:name>
-    <w:basedOn w:val="3">
-    </w:basedOn>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="39">
-    </w:uiPriority>
-    <w:pPr>
-      <w:spacing w:after="0" w:line="240" w:lineRule="auto">
-      </w:spacing>
-    </w:pPr>
-    <w:tblPr>
-      <w:tblBorders>
-        <w:top w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:top>
-        <w:left w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:left>
-        <w:bottom w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:bottom>
-        <w:right w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:right>
-        <w:insideH w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:insideH>
-        <w:insideV w:color="auto" w:space="0" w:sz="4" w:val="single">
-        </w:insideV>
-      </w:tblBorders>
-    </w:tblPr>
-  </w:style>
-  <w:style w:styleId="10" w:type="paragraph">
-    <w:name w:val="List Paragraph">
-    </w:name>
-    <w:basedOn w:val="1">
-    </w:basedOn>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="34">
-    </w:uiPriority>
-    <w:pPr>
-      <w:ind w:left="720">
-      </w:ind>
-      <w:contextualSpacing>
-      </w:contextualSpacing>
-    </w:pPr>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="11" w:type="character">
-    <w:name w:val="Encabezado Car">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:link w:val="6">
+  <w:style w:customStyle="1" w:styleId="TextoindependienteCar" w:type="character">
+    <w:name w:val="Texto independiente Car">
+    </w:name>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:link w:val="Textoindependiente">
     </w:link>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="12" w:type="character">
-    <w:name w:val="Pie de página Car">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:link w:val="7">
-    </w:link>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="13" w:type="character">
-    <w:name w:val="Mención sin resolver1">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:semiHidden>
-    </w:semiHidden>
-    <w:unhideWhenUsed>
-    </w:unhideWhenUsed>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="99">
-    </w:uiPriority>
-    <w:rPr>
-      <w:color w:val="605E5C">
-      </w:color>
-      <w:shd w:color="auto" w:fill="E1DFDD" w:val="clear">
-      </w:shd>
-    </w:rPr>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="14" w:type="paragraph">
-    <w:name w:val="Default">
-    </w:name>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
-    <w:pPr>
-      <w:autoSpaceDE w:val="0">
-      </w:autoSpaceDE>
-      <w:autoSpaceDN w:val="0">
-      </w:autoSpaceDN>
-      <w:adjustRightInd w:val="0">
-      </w:adjustRightInd>
-      <w:spacing w:after="0" w:line="240" w:lineRule="auto">
-      </w:spacing>
-    </w:pPr>
-    <w:rPr>
-      <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsiaTheme="minorHAnsi" w:hAnsi="Times New Roman">
-      </w:rFonts>
-      <w:color w:val="000000">
-      </w:color>
-      <w:sz w:val="24">
-      </w:sz>
-      <w:szCs w:val="24">
-      </w:szCs>
-      <w:lang w:bidi="ar-SA" w:eastAsia="en-US" w:val="es-MX">
-      </w:lang>
-    </w:rPr>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="15" w:type="paragraph">
-    <w:name w:val="key words">
-    </w:name>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
-    <w:pPr>
-      <w:spacing w:after="120" w:line="240" w:lineRule="auto">
-      </w:spacing>
-      <w:ind w:firstLine="288">
-      </w:ind>
-      <w:jc w:val="both">
-      </w:jc>
-    </w:pPr>
-    <w:rPr>
-      <w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman">
-      </w:rFonts>
-      <w:b>
-      </w:b>
-      <w:bCs>
-      </w:bCs>
-      <w:i>
-      </w:i>
-      <w:iCs>
-      </w:iCs>
-      <w:sz w:val="18">
-      </w:sz>
-      <w:szCs w:val="18">
-      </w:szCs>
-      <w:lang w:bidi="ar-SA" w:eastAsia="en-US" w:val="en-US">
-      </w:lang>
-    </w:rPr>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="16" w:type="character">
-    <w:name w:val="Texto independiente Car">
-    </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:link w:val="8">
-    </w:link>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
+    <w:rsid w:val="00387225">
+    </w:rsid>
     <w:rPr>
@@ -681,21 +1109,17 @@
   </w:style>
-  <w:style w:customStyle="1" w:styleId="17" w:type="character">
+  <w:style w:customStyle="1" w:styleId="tlid-translation" w:type="character">
     <w:name w:val="tlid-translation">
     </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
-  </w:style>
-  <w:style w:customStyle="1" w:styleId="18" w:type="character">
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:rsid w:val="00276974">
+    </w:rsid>
+  </w:style>
+  <w:style w:customStyle="1" w:styleId="rynqvb" w:type="character">
     <w:name w:val="rynqvb">
     </w:name>
-    <w:basedOn w:val="2">
-    </w:basedOn>
-    <w:qFormat>
-    </w:qFormat>
-    <w:uiPriority w:val="0">
-    </w:uiPriority>
+    <w:basedOn w:val="Fuentedeprrafopredeter">
+    </w:basedOn>
+    <w:rsid w:val="008F7405">
+    </w:rsid>
   </w:style>
```

</details>

<details><summary>word/theme/theme1.xml — F06</summary>

```diff
--- A/word/theme/theme1.xml
+++ B/word/theme/theme1.xml
@@ -54,3 +54,3 @@
       <a:majorFont>
-        <a:latin typeface="Calibri Light">
+        <a:latin panose="020F0302020204030204" typeface="Calibri Light">
         </a:latin>
@@ -122,3 +122,3 @@
       <a:minorFont>
-        <a:latin typeface="Calibri">
+        <a:latin panose="020F0502020204030204" typeface="Calibri">
         </a:latin>
@@ -377,2 +377,10 @@
   </a:objectDefaults>
+  <a:extraClrSchemeLst>
+  </a:extraClrSchemeLst>
+  <a:extLst>
+    <a:ext uri="{05A4C25C-085E-4340-85A3-A5531E510DB2}">
+      <ns25:themeFamily id="{62F939B6-93AF-4DB8-9C6B-D6C7DFDC589F}" name="Office Theme" vid="{4A3C46E8-61CC-4603-A589-7422A47A8E4A}">
+      </ns25:themeFamily>
+    </a:ext>
+  </a:extLst>
 </a:theme>
```

</details>

<details><summary>word/webSettings.xml — F15</summary>

```diff
--- A/word/webSettings.xml
+++ B/word/webSettings.xml
@@ -0,0 +1,1000 @@
+<w:webSettings ns14:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh">
+  <w:divs>
+    <w:div w:id="304283762">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+    </w:div>
+    <w:div w:id="512183537">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+    </w:div>
+    <w:div w:id="1160271566">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+      <w:divsChild>
+        <w:div w:id="78916035">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="1712418136">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+              <w:divsChild>
+                <w:div w:id="398865741">
+                  <w:marLeft w:val="0">
+                  </w:marLeft>
+                  <w:marRight w:val="0">
+                  </w:marRight>
+                  <w:marTop w:val="0">
+                  </w:marTop>
+                  <w:marBottom w:val="0">
+                  </w:marBottom>
+                  <w:divBdr>
+                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:top>
+                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:left>
+                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:bottom>
+                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:right>
+                  </w:divBdr>
+                  <w:divsChild>
+                    <w:div w:id="460268624">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                    </w:div>
+                  </w:divsChild>
+                </w:div>
+              </w:divsChild>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+        <w:div w:id="1031110618">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="225192441">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+              <w:divsChild>
+                <w:div w:id="1177035445">
+                  <w:marLeft w:val="0">
+                  </w:marLeft>
+                  <w:marRight w:val="0">
+                  </w:marRight>
+                  <w:marTop w:val="0">
+                  </w:marTop>
+                  <w:marBottom w:val="0">
+                  </w:marBottom>
+                  <w:divBdr>
+                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:top>
+                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:left>
+                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:bottom>
+                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:right>
+                  </w:divBdr>
+                  <w:divsChild>
+                    <w:div w:id="1914780742">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                      <w:divsChild>
+                        <w:div w:id="1090420434">
+                          <w:marLeft w:val="0">
+                          </w:marLeft>
+                          <w:marRight w:val="0">
+                          </w:marRight>
+                          <w:marTop w:val="0">
+                          </w:marTop>
+                          <w:marBottom w:val="0">
+                          </w:marBottom>
+                          <w:divBdr>
+                            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:top>
+                            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:left>
+                            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:bottom>
+                            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:right>
+                          </w:divBdr>
+                        </w:div>
+                      </w:divsChild>
+                    </w:div>
+                    <w:div w:id="1496992381">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                    </w:div>
+                    <w:div w:id="1774739785">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                      <w:divsChild>
+                        <w:div w:id="313069752">
+                          <w:marLeft w:val="0">
+                          </w:marLeft>
+                          <w:marRight w:val="0">
+                          </w:marRight>
+                          <w:marTop w:val="0">
+                          </w:marTop>
+                          <w:marBottom w:val="0">
+                          </w:marBottom>
+                          <w:divBdr>
+                            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:top>
+                            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:left>
+                            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:bottom>
+                            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:right>
+                          </w:divBdr>
+                          <w:divsChild>
+                            <w:div w:id="871192092">
+                              <w:marLeft w:val="0">
+                              </w:marLeft>
+                              <w:marRight w:val="0">
+                              </w:marRight>
+                              <w:marTop w:val="0">
+                              </w:marTop>
+                              <w:marBottom w:val="0">
+                              </w:marBottom>
+                              <w:divBdr>
+                                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:top>
+                                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:left>
+                                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:bottom>
+                                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:right>
+                              </w:divBdr>
+                              <w:divsChild>
+                                <w:div w:id="1168716638">
+                                  <w:marLeft w:val="0">
+                                  </w:marLeft>
+                                  <w:marRight w:val="0">
+                                  </w:marRight>
+                                  <w:marTop w:val="0">
+                                  </w:marTop>
+                                  <w:marBottom w:val="0">
+                                  </w:marBottom>
+                                  <w:divBdr>
+                                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:top>
+                                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:left>
+                                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:bottom>
+                                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:right>
+                                  </w:divBdr>
+                                </w:div>
+                              </w:divsChild>
+                            </w:div>
+                          </w:divsChild>
+                        </w:div>
+                      </w:divsChild>
+                    </w:div>
+                  </w:divsChild>
+                </w:div>
+              </w:divsChild>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+        <w:div w:id="71398471">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="122507340">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+              <w:divsChild>
+                <w:div w:id="2054841288">
+                  <w:marLeft w:val="0">
+                  </w:marLeft>
+                  <w:marRight w:val="0">
+                  </w:marRight>
+                  <w:marTop w:val="0">
+                  </w:marTop>
+                  <w:marBottom w:val="0">
+                  </w:marBottom>
+                  <w:divBdr>
+                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:top>
+                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:left>
+                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:bottom>
+                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:right>
+                  </w:divBdr>
+                  <w:divsChild>
+                    <w:div w:id="1916355108">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                    </w:div>
+                  </w:divsChild>
+                </w:div>
+              </w:divsChild>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+        <w:div w:id="1278028268">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="1743328463">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+        <w:div w:id="293996631">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="1370060121">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+        <w:div w:id="1298878718">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="1689133691">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+              <w:divsChild>
+                <w:div w:id="1380326745">
+                  <w:marLeft w:val="0">
+                  </w:marLeft>
+                  <w:marRight w:val="0">
+                  </w:marRight>
+                  <w:marTop w:val="0">
+                  </w:marTop>
+                  <w:marBottom w:val="0">
+                  </w:marBottom>
+                  <w:divBdr>
+                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:top>
+                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:left>
+                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:bottom>
+                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                    </w:right>
+                  </w:divBdr>
+                  <w:divsChild>
+                    <w:div w:id="1874537733">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                      <w:divsChild>
+                        <w:div w:id="2129202600">
+                          <w:marLeft w:val="0">
+                          </w:marLeft>
+                          <w:marRight w:val="0">
+                          </w:marRight>
+                          <w:marTop w:val="0">
+                          </w:marTop>
+                          <w:marBottom w:val="0">
+                          </w:marBottom>
+                          <w:divBdr>
+                            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:top>
+                            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:left>
+                            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:bottom>
+                            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:right>
+                          </w:divBdr>
+                        </w:div>
+                      </w:divsChild>
+                    </w:div>
+                    <w:div w:id="110513369">
+                      <w:marLeft w:val="0">
+                      </w:marLeft>
+                      <w:marRight w:val="0">
+                      </w:marRight>
+                      <w:marTop w:val="0">
+                      </w:marTop>
+                      <w:marBottom w:val="0">
+                      </w:marBottom>
+                      <w:divBdr>
+                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:top>
+                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:left>
+                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:bottom>
+                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                        </w:right>
+                      </w:divBdr>
+                      <w:divsChild>
+                        <w:div w:id="1697730582">
+                          <w:marLeft w:val="0">
+                          </w:marLeft>
+                          <w:marRight w:val="0">
+                          </w:marRight>
+                          <w:marTop w:val="0">
+                          </w:marTop>
+                          <w:marBottom w:val="0">
+                          </w:marBottom>
+                          <w:divBdr>
+                            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:top>
+                            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:left>
+                            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:bottom>
+                            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                            </w:right>
+                          </w:divBdr>
+                          <w:divsChild>
+                            <w:div w:id="9574763">
+                              <w:marLeft w:val="0">
+                              </w:marLeft>
+                              <w:marRight w:val="0">
+                              </w:marRight>
+                              <w:marTop w:val="0">
+                              </w:marTop>
+                              <w:marBottom w:val="0">
+                              </w:marBottom>
+                              <w:divBdr>
+                                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:top>
+                                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:left>
+                                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:bottom>
+                                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:right>
+                              </w:divBdr>
+                              <w:divsChild>
+                                <w:div w:id="1177501567">
+                                  <w:marLeft w:val="0">
+                                  </w:marLeft>
+                                  <w:marRight w:val="0">
+                                  </w:marRight>
+                                  <w:marTop w:val="0">
+                                  </w:marTop>
+                                  <w:marBottom w:val="0">
+                                  </w:marBottom>
+                                  <w:divBdr>
+                                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:top>
+                                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:left>
+                                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:bottom>
+                                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:right>
+                                  </w:divBdr>
+                                  <w:divsChild>
+                                    <w:div w:id="1556619568">
+                                      <w:marLeft w:val="0">
+                                      </w:marLeft>
+                                      <w:marRight w:val="0">
+                                      </w:marRight>
+                                      <w:marTop w:val="0">
+                                      </w:marTop>
+                                      <w:marBottom w:val="0">
+                                      </w:marBottom>
+                                      <w:divBdr>
+                                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:top>
+                                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:left>
+                                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:bottom>
+                                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:right>
+                                      </w:divBdr>
+                                    </w:div>
+                                  </w:divsChild>
+                                </w:div>
+                              </w:divsChild>
+                            </w:div>
+                            <w:div w:id="720985089">
+                              <w:marLeft w:val="0">
+                              </w:marLeft>
+                              <w:marRight w:val="0">
+                              </w:marRight>
+                              <w:marTop w:val="0">
+                              </w:marTop>
+                              <w:marBottom w:val="0">
+                              </w:marBottom>
+                              <w:divBdr>
+                                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:top>
+                                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:left>
+                                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:bottom>
+                                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:right>
+                              </w:divBdr>
+                              <w:divsChild>
+                                <w:div w:id="2135253150">
+                                  <w:marLeft w:val="0">
+                                  </w:marLeft>
+                                  <w:marRight w:val="0">
+                                  </w:marRight>
+                                  <w:marTop w:val="0">
+                                  </w:marTop>
+                                  <w:marBottom w:val="0">
+                                  </w:marBottom>
+                                  <w:divBdr>
+                                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:top>
+                                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:left>
+                                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:bottom>
+                                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:right>
+                                  </w:divBdr>
+                                  <w:divsChild>
+                                    <w:div w:id="334965032">
+                                      <w:marLeft w:val="0">
+                                      </w:marLeft>
+                                      <w:marRight w:val="0">
+                                      </w:marRight>
+                                      <w:marTop w:val="0">
+                                      </w:marTop>
+                                      <w:marBottom w:val="0">
+                                      </w:marBottom>
+                                      <w:divBdr>
+                                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:top>
+                                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:left>
+                                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:bottom>
+                                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:right>
+                                      </w:divBdr>
+                                    </w:div>
+                                  </w:divsChild>
+                                </w:div>
+                              </w:divsChild>
+                            </w:div>
+                            <w:div w:id="244195503">
+                              <w:marLeft w:val="0">
+                              </w:marLeft>
+                              <w:marRight w:val="0">
+                              </w:marRight>
+                              <w:marTop w:val="0">
+                              </w:marTop>
+                              <w:marBottom w:val="0">
+                              </w:marBottom>
+                              <w:divBdr>
+                                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:top>
+                                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:left>
+                                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:bottom>
+                                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                </w:right>
+                              </w:divBdr>
+                              <w:divsChild>
+                                <w:div w:id="177744179">
+                                  <w:marLeft w:val="0">
+                                  </w:marLeft>
+                                  <w:marRight w:val="0">
+                                  </w:marRight>
+                                  <w:marTop w:val="0">
+                                  </w:marTop>
+                                  <w:marBottom w:val="0">
+                                  </w:marBottom>
+                                  <w:divBdr>
+                                    <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:top>
+                                    <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:left>
+                                    <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:bottom>
+                                    <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                    </w:right>
+                                  </w:divBdr>
+                                  <w:divsChild>
+                                    <w:div w:id="1499035269">
+                                      <w:marLeft w:val="0">
+                                      </w:marLeft>
+                                      <w:marRight w:val="0">
+                                      </w:marRight>
+                                      <w:marTop w:val="0">
+                                      </w:marTop>
+                                      <w:marBottom w:val="0">
+                                      </w:marBottom>
+                                      <w:divBdr>
+                                        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:top>
+                                        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:left>
+                                        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:bottom>
+                                        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                                        </w:right>
+                                      </w:divBdr>
+                                    </w:div>
+                                  </w:divsChild>
+                                </w:div>
+                              </w:divsChild>
+                            </w:div>
+                          </w:divsChild>
+                        </w:div>
+                      </w:divsChild>
+                    </w:div>
+                  </w:divsChild>
+                </w:div>
+              </w:divsChild>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+      </w:divsChild>
+    </w:div>
+    <w:div w:id="1215003498">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+      <w:divsChild>
+        <w:div w:id="1283994609">
+          <w:marLeft w:val="0">
+          </w:marLeft>
+          <w:marRight w:val="0">
+          </w:marRight>
+          <w:marTop w:val="0">
+          </w:marTop>
+          <w:marBottom w:val="0">
+          </w:marBottom>
+          <w:divBdr>
+            <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:top>
+            <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:left>
+            <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:bottom>
+            <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+            </w:right>
+          </w:divBdr>
+          <w:divsChild>
+            <w:div w:id="149954197">
+              <w:marLeft w:val="0">
+              </w:marLeft>
+              <w:marRight w:val="0">
+              </w:marRight>
+              <w:marTop w:val="0">
+              </w:marTop>
+              <w:marBottom w:val="0">
+              </w:marBottom>
+              <w:divBdr>
+                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:top>
+                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:left>
+                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:bottom>
+                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+                </w:right>
+              </w:divBdr>
+            </w:div>
+          </w:divsChild>
+        </w:div>
+      </w:divsChild>
+    </w:div>
+    <w:div w:id="1302733794">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+    </w:div>
+    <w:div w:id="1489050434">
+      <w:bodyDiv w:val="1">
+      </w:bodyDiv>
+      <w:marLeft w:val="0">
+      </w:marLeft>
+      <w:marRight w:val="0">
+      </w:marRight>
+      <w:marTop w:val="0">
+      </w:marTop>
+      <w:marBottom w:val="0">
+      </w:marBottom>
+      <w:divBdr>
+        <w:top w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:top>
+        <w:left w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:left>
+        <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:bottom>
+        <w:right w:color="auto" w:space="0" w:sz="0" w:val="none">
+        </w:right>
+      </w:divBdr>
+    </w:div>
+  </w:divs>
+  <w:optimizeForBrowser>
+  </w:optimizeForBrowser>
+  <w:allowPNG>
+  </w:allowPNG>
+</w:webSettings>
```

</details>

## Integridad al cierre

SHA-256 de ambos DOCX idénticos a los registrados en §1. Se confirmó que solo los ocho párrafos existentes enumerados cambian de texto, además del correo insertado; los seis cambios del JSON coinciden literalmente. Tabla y cinco figuras conservadas. Las recomendaciones no se ejecutaron.
