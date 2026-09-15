# Revisión académica de los informes oficiales de Turnitin

Rama: `feat/conacic-2026-camera-ready`.

**Estado:** evidencia incorporada y propuestas contrastadas con `DIFF_CAMERA_READY.md`; ninguna propuesta de este informe se ha aplicado al artículo. La presentación y el video no se modificaron. Los PDF oficiales se conservan íntegros.

## Resultado de la revisión

Turnitin reporta **72 % de texto calificado detectado como probable escritura con IA** y **5 % de similitud general**, sin manipulaciones de texto sospechosas detectadas. Son indicadores distintos. Ninguno demuestra por sí solo plagio, autoría artificial, exactitud científica o validez de una metodología.

La revisión de los resaltados identifica oportunidades de claridad y problemas de afirmaciones categóricas que ya aparecían en la auditoría diferencial. Los números, tablas, figuras, citas, referencias, estructura y significado técnico quedan preservados. Cuando moderar una afirmación modifica su alcance científico, la propuesta se clasifica como **CAMBIO CIENTÍFICO — REQUIERE REVISIÓN**, aunque no cambie cifras.

No se fija un porcentaje objetivo, no se predice un porcentaje posterior y no se propone reescritura para influir en el detector. Se mantienen expresiones correctas aunque estén resaltadas, incluidos términos técnicos, palabras clave y pies de figura.

## 0. Evidencia y correspondencia de versiones

### Archivos incorporados sin modificar

| Informe | Copia en la rama | Páginas PDF | SHA-256 |
|---|---|---:|---|
| IA | [CONAC2026_paper_17_IA_72.pdf](evidencia_turnitin/CONAC2026_paper_17_IA_72.pdf) | 12 | `0e8111069834aa54b1b7e174f9218f5e6818d167bd757b2861f39a32d5ba8f33` |
| Similitud | [CONAC2026_paper_17_Simi_5.pdf](evidencia_turnitin/CONAC2026_paper_17_Simi_5.pdf) | 13 | `f0f39c9b3723ab2fa5d145f8850f2c8d83c2babf59ae87e335974da79d29939f` |

Procedencia: archivos oficiales recibidos según el usuario y localizados en `C:/Users/santi/Downloads`. Se copiaron conservando bytes; los hashes de origen y destino coinciden. Registro: [PROCEDENCIA.json](evidencia_turnitin/PROCEDENCIA.json). No se accedió a la cuenta de Turnitin ni se ejecutó otra evaluación.

Ambas portadas identifican:

- Entrega `trn:oid:::1:3645328474`.
- Archivo evaluado `CONAC2026_paper_17.docx`, 252.1 KB.
- Entrega: **10 sep 2026, 9:16 a.m. GMT-6**; descarga: **10 sep 2026, 2:29 p.m. GMT-6**.
- Documento de diez páginas, 3370 palabras y 18.990 caracteres. Estas son estadísticas del archivo descrito por Turnitin, no del camera-ready actual.

**Correspondencia, no identidad binaria:** los 95 párrafos no vacíos de título/cuerpo/referencias de la base local, excluidos autor y afiliación, se localizaron en el texto del PDF IA tras normalizar espacios/signos y retirar las cabeceras de página. La copia de Turnitin **no muestra** el bloque «Edwin Santiago Paz Bedoya / UNIMINUTO, Bogotá, Colombia.» que sí contiene la base local. No se infiere por qué se omitió ni se afirma que ambos DOCX sean binariamente idénticos. El DOCX exacto evaluado no está entre estos dos PDF. Esta evidencia amplía la trazabilidad previa sin borrar el límite descrito en `DIFF_CAMERA_READY.md`.

**Localizadores:** `A:Pn` corresponde al índice desde cero del párrafo en `entrega_congreso/Saber_pro_paper_CONGRESO_10P_FINAL.docx`, según el DIFF; después de A:P4, su equivalente actual es `B:P(n+1)` en `CAMERA_READY_DRAFT.docx`. Es una correspondencia textual de consulta, no numeración producida por Turnitin. Las páginas citadas abajo son las páginas físicas del PDF: IA 3–12 = artículo 1–10; similitud 4–13 = artículo 1–10.

Método: extracción textual y geométrica de los resaltados, revisión visual de todas las páginas del informe IA y de todas las páginas con coincidencias del informe de similitud, además de portadas/resúmenes. Las marcas son dibujos de color incrustados, no comentarios PDF. La localización se apoya en su posición sobre las palabras, no en atribuir el 72 % a páginas completas.

## A. Informe de escritura con IA

### A.1 Qué reporta y qué no permite concluir

- **Herramienta:** Turnitin.
- **Porcentaje reportado:** **72 %**, página 2 del PDF IA. Se refiere al texto calificado por la herramienta; no debe reinterpretarse como 72 % de las 3370 palabras totales, de las páginas, de los resultados o de probabilidad de conducta indebida.
- El panel muestra la categoría «Sólo generado con IA» y el indicador 27 junto a ella. Ese indicador no se convierte aquí en un recuento de párrafos Word: una marca puede cruzar párrafos o cubrir solo parte de ellos.
- El propio informe advierte que la evaluación **puede ser inexacta**, con errores de clasificación tanto de escritura humana como de escritura generada con IA, y que **no debe utilizarse como único fundamento para sancionar**. Requiere escrutinio adicional, juicio humano y las políticas académicas aplicables (p. 2).
- La lectura editorial se basa en claridad, exactitud, evidencia y alcance de las afirmaciones. Una marca no demuestra un error académico; ausencia de marca tampoco certifica la corrección del texto.

### A.2 Secciones y párrafos efectivamente marcados

En la columna «tratamiento», Rxx remite a las propuestas de A.3. «Conservar» indica que no se propone modificar ese elemento. En marcas parciales se identifica qué fragmento está coloreado; no se atribuye el marcado a todo el párrafo.

| PDF IA / artículo | Sección y localizador de base | Extensión visible de la marca | Tratamiento académico |
|---|---|---|---|
| 3 / 1 | Abstract, A:P7 | Desde «LightGBM achieves…» hasta «ICFES official publication.»; no el inicio del abstract | R01 para función del módulo; R09 para alcance; métricas intactas |
| 3 / 1 | Resumen, A:P9 | Párrafo completo | R01 y R09; conservar todas las cifras |
| 3 / 1 | Palabras clave, A:P10 | Línea completa de palabras clave | Conservar: terminología e indexación |
| 3 / 1 | Introducción, A:P12 | Solo primera oración, «El examen Saber Pro mide la calidad… Colombia.» | R02; resto del párrafo no se trata como marcado |
| 4 / 2 | Contribuciones, A:P15 | Dos oraciones: «Se diseña una estrategia de pivot…» y «Se construyen 15 features… cobertura desigual.» | R04/R05; no borrar los seis tipos de fuga ni las contribuciones |
| 5 / 3 | Fuente de datos, A:P27 | Desde «El dataset crudo consolidado suma…» hasta «tipo PUNTAJE_GLOBAL.» | R03; preservar 1.730.805, cinco archivos y 97,3 % |
| 5 / 3 | 3.2, A:P28/P29 | Encabezado 3.2 y todo su párrafo | R04; título conservado |
| 5 / 3 | 3.3, A:P30/P31 | Encabezado 3.3 y todo su párrafo | R05; título/cifras/catálogo conservados |
| 6 / 4 | Pie de Figura 1, A:P34 | «Dataset Saber Pro post-pivot y limpieza», bloque superior derecho e inferior; no toda la descripción | Conservar figura y pie |
| 6 / 4 | 3.4, A:P35/P36 | Encabezado y párrafo completos | R05; resolver el DIFF antes de cualquier redacción |
| 6 / 4 | Modelos, A:P38 | Últimas dos oraciones: métricas y SHAP [6] | R06; el «n_estimators = 500» anterior no está resaltado |
| 6 / 4 | Resultados 4.1, A:P41 | Primera oración, hasta «distribución del target»; no la oración de presentación de Tabla 1 | R07; cifras preservadas |
| 7 / 5 | Comparativa, A:P43 | Desde «Esta mejora se reporta…» hasta «225 iteraciones de boosting» | R07; no toda la conclusión del párrafo está marcada |
| 7 / 5 | Pie de Figura 2, A:P45 | Últimas dos oraciones: iteración 168 y regularización | Conservar pie; revisar alcance en R07 |
| 7 / 5 | Dispersión, A:P46 | Párrafo completo | R07; conservar Figura 3, n y R² |
| 8 / 6 | Pie de Figura 3, A:P49 | Título descriptivo y oración sobre extremos; las métricas intermedias no están coloreadas | Conservar figura y pie |
| 8 / 6 | SHAP, A:P50/P51 | Encabezado; primera oración y las dos últimas. La enumeración «Le siguen…» no está marcada | R08; preservar ranking y +28 |
| 8 / 6 | Pie de Figura 4, A:P53 | Texto posterior a «Figura 4», incluida explicación del color | Conservar figura y pie |
| 9 / 7 | Errores por área, A:P55/P56 | Encabezado y párrafo completos | R08; no sustituir rangos ni categorías |
| 9 / 7 | Pie de Figura 5, A:P58 | Texto después de «Figura 5», incluida explicación por heterogeneidad | Conservar figura y pie; alcance pendiente R08 |
| 9 / 7 | Confianza, A:P59/P60 | Encabezado; primera parte hasta «RMSE aprox.»; luego desde «El diferencial…» hasta fin. «11,4 de confianza BAJA (15,6 %)» no está coloreado | R09; congelar todas las métricas de grupos |
| 9–10 / 7–8 | Discusión 5.1, A:P62/P63 | Encabezado y fragmento de p. 9 hasta «lo que justifica que el»; continuación en p. 10 sin marca | R08; preservar [7]/[8] |
| 10 / 8 | Discusión 5.2, A:P64/P65 | Encabezado y párrafo completos | R10; preservar ratios, métricas, [11]/[12] |
| 10 / 8 | Discusión 5.3, A:P67 | Párrafo completo; no su encabezado A:P66 | R11; conservar [9]/[16]/[21]/[22] |
| 10 / 8 | Política educativa, A:P68/P69 | Encabezado y párrafo completos | R09 y obligatoria C04; conservar [15]/[26] |
| 10 / 8 | Limitaciones, A:P71 | L2–L4 y L6–L7. L1 y L5 no están coloreadas | Conservar L1–L7; no ocultar limitaciones |
| 10 / 8 | Conclusiones, A:P72/P74 | Título sección 6 y P74 completos; el subtítulo 6.1 no está coloreado | R09; título y resultados intactos |
| 10–11 / 8–9 | Conclusiones, A:P75 | Parte en p. 10 completa; en p. 11 desde «El módulo…» hasta fin. «resulta competitivo… [11] y [12]» al inicio de p. 11 no está marcada | R09–R11; no sustituir el diferencial 2,3 |
| 11 / 9 | Trabajo futuro, A:P77 | Párrafo completo; encabezado 6.2 no marcado | Conservar TF1–TF6: ya especifica extensiones |
| 11 / 9 | Agradecimientos, A:P79 | Primera línea hasta «Saber Pro»; «2020–2024» en siguiente línea sin marca | R12; conservar agradecimiento y período |
| 11–12 / 9–10 | Referencias, A:P81–P106 | No se observan resaltados IA en las entradas bibliográficas | Preservar todas las referencias; pendientes del DIFF independientes |

Tampoco se observan marcas IA en el bloque restante de introducción, secciones 2.1–2.4, títulos bilingües, celdas de Tabla 1 o imágenes. No se deduce de ello que estén académicamente validados. Los encabezados «D. Beltrán…» y «auditorría» son errores independientes de la detección.

### A.3 Propuestas por sección, con justificación y contraste

Las propuestas son fragmentos de revisión, no un artículo alternativo. Lo no incluido en cada reemplazo queda intacto. No cambian citas, referencias, números de secciones, tablas ni figuras. Todas permanecen **NO APLICADAS**. Cuando se ofrece una formulación de alcance distinto, se explicita esa diferencia y se requiere revisión científica; no se presenta como equivalente semántico automático.

#### R01 — Resúmenes: explicar la función del producto sin fórmulas impersonales

**Clasificación: MEJORA DE REDACCIÓN.**

- **Original A:P7:** «A deployable inference module with three empirical confidence flags is delivered.»
- **Propuesta:** «The accompanying deployable inference module provides three empirical confidence flags.»
- **Original A:P9:** «Se entrega un módulo de inferencia deployable con tres flags empíricos de confianza.»
- **Propuesta:** «El módulo de inferencia desarrollado puede desplegarse y proporciona tres flags empíricos de confianza.»
- **Justificación académica:** identificar el artefacto y su función; mantener que es desplegable sin afirmar un despliegue institucional ya realizado. Evita centrar la oración en el acto genérico de “entregar”. No toca métricas, orden de modelos ni afirmación sobre el historial.
- **Evidencia:** `src/inference.py`, funciones de inferencia y reglas de confianza; `DIFF_CAMERA_READY.md`, §4.4. «Empíricos» se conserva: no se convierten en intervalos o probabilidades.
- **Contraste DIFF:** A:P7/P9 siguen intactos en B. La propuesta no resuelve los problemas de calibración o anticipación señalados por el DIFF; estos pertenecen a R09.

#### R02 — Introducción: qué mide Saber Pro y qué permite concluir sobre calidad

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P12:** «El examen Saber Pro mide la calidad de los programas de educación superior universitaria en Colombia.»
- **Propuesta para discutir:** «Los resultados de Saber Pro se utilizan como uno de los insumos para evaluar los programas de educación superior universitaria en Colombia.»
- **Justificación académica:** distinguir un indicador del constructo completo de calidad. La nueva frase reduce una afirmación absoluta; por ello no se clasifica como simple estilo.
- **Evidencia y límite:** A:P12/P18 ya mencionan el uso institucional de resultados y [1]/[15]; `DIFF_CAMERA_READY.md`, §4.5, deja pendiente el respaldo técnico ICFES. Las citas existentes se conservan y debe verificarse que apoyen la redacción definitiva. No se añade ni elimina una referencia.
- **Contraste DIFF:** asunto de precisión/alcance independiente de la marca. No aplicar sin revisar definición técnica y respaldo documental.

#### R03 — Fuente de datos: separar tamaño, unidad de fila y estructura

**Clasificación: MEJORA DE REDACCIÓN.**

- **Original A:P27:** desde «El dataset crudo consolidado suma 1.730.805 filas…» hasta «…estructura long-format.»
- **Propuesta:** «El dataset crudo consolidado suma 1.730.805 filas distribuidas en cinco archivos anuales. Cada fila corresponde a una combinación de programa académico, prueba específica y tipo de medida estadística, no a un programa individual. Esta organización produce una estructura long-format.»
- **Justificación académica:** dividir una oración de varias funciones para que el lector distinga volumen, unidad de registro y organización de datos. Conserva literalmente los hechos y no incorpora otra clave de agrupación.
- **Evidencia:** A:P27, `src/cleaning.py` y reportes de ingesta. La oración inicial con período 2020–2024/[1] y la oración posterior con 97,3 % se mantienen. El recuento crudo conserva su carácter histórico; no se afirma haberlo reproducido desde Excel en esta fase.
- **Contraste DIFF:** P27 no cambió en B; compatible con conservación de cifras y estructura. No invade D04 sobre joins.

#### R04 — Pivot: resolver primero la discrepancia entre descripción y código

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P29:** inner join de las tres capas sobre llave de cuatro campos.
- **Propuesta de revisión:** tratar explícitamente, como corrección metodológica, la distinción entre inner join con global por año/institución/programa y left join de niveles incluyendo prueba. Mantener definiciones de las tres capas, 127.716 filas y disponibilidad del target al 100 %. No se ofrece otra versión “más natural” que disimule esta diferencia.
- **Justificación académica:** conectar la decisión de integración con el código que la ejecuta; cambiarla modifica una descripción metodológica aceptada.
- **Evidencia:** `src/cleaning.py`, KEY3/KEY4 y `_pivot_long_to_wide`; DIFF D04. D04 también recomienda recuperar definiciones explicativas suprimidas.
- **Contraste DIFF:** B:P30 ya difiere de A:P29. No dar por aprobada esa modificación por aparecer en el borrador ni replicarla silenciosamente en A:P15. Revisión conjunta con Nathalia antes de editar.

#### R05 — Catálogo, rezagos y codificación: reemplazar garantías por trazabilidad, solo tras revisión

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P15/P36:** «15 features… causalmente válidas»; A:P31 atribuye ΔR²≈0,22 al catálogo.
- **Propuesta de revisión:** separar la lista de entradas de las comprobaciones realmente realizadas. Si Nathalia lo valida, acompañar la descripción de rezagos con que `shift(1)`/`shift(2)` usan observaciones previas disponibles; identificar que la separación 2020–2023/2024 es externa. Describir TargetEncoder multiclase como configuración observada, sin cambiar el codificador ni el modelo.
- **Justificación académica:** hacer verificable qué se hizo, con qué alcance y dónde está la evidencia. No afirmar que se realizaron validación interna cronológica completa o ablaciones por fuga si el repositorio no lo demuestra.
- **Evidencia:** `src/features.py`; pipelines; DIFF D05 y §4.1–4.2/4.4: 2.022 saltos de historial mayores de un año; 15 entradas/417 columnas; revisión de splits y causalidad.
- **Contraste DIFF:** B:P37 ya incorpora parte de estas precisiones; eso no autoriza nuevas modificaciones. Preservar 15, 98.954, 28.762, los seis tipos L1–L6 y ΔR²≈0,22. No recalcular resultados ni convertir matices de metodología en ajustes de estilo.

#### R06 — Modelos: expresar directamente cómo se evaluó y explicó el modelo

**Clasificación: MEJORA DE REDACCIÓN.**

- **Original A:P38/B:P39, últimas dos oraciones:** «Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6].»
- **Propuesta:** «Evaluamos los modelos con RMSE, MAE y R². Para interpretar el modelo final, utilizamos SHAP [6].»
- **Justificación académica:** explicitar acciones de los autores y finalidad de SHAP, conservando métodos y cita. No se atribuye causalidad a SHAP ni se añade una técnica.
- **Evidencia:** funciones de evaluación y SHAP; Tabla 1; DIFF conserva estas métricas y figuras.
- **Contraste DIFF:** aplicable únicamente a esas dos oraciones. La discrepancia 500/188 árboles, DIFF D06, está en otra parte del mismo párrafo y no se toca con esta propuesta. El tramo resaltado no incluye esa cifra.

#### R07 — Resultados: separar descripción visual de garantías de validez

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **A:P41:** revisar «confirmando que… no introdujo distorsiones sistemáticas». Propuesta conceptual: describir cobertura y distribución sin presentar un recuento de filas como prueba de ausencia de distorsión. Mantener 411.946, 127.716, 28.762 y la remisión a Tabla 1.
- **A:P43:** «Para verificar que el modelo no incurre en sobreajuste» → propuesta para discutir: «Para examinar el ajuste del modelo». Mantener el resto de la descripción, 225 iteraciones y todos los resultados; la frase final y el pie A:P45 también requieren coherencia científica antes de editarse.
- **A:P46:** distinguir la concentración de puntos observada de una explicación por tamaño de cohortes/inestabilidad, que requiere respaldo adicional.
- **Justificación académica:** reducir garantías que no se derivan únicamente de una gráfica. La modificación cambiaría fuerza inferencial, no números; requiere revisión y no se aplicará como retoque estilístico.
- **Evidencia:** Figuras 1–3; DIFF §4.1/4.4. El corte de la curva de aprendizaje por año 2023 sí está documentado; no afirmar que esa curva use los folds que mezclan años.
- **Contraste DIFF:** estos pasajes permanecen en B. Se preservan pies y figuras en esta fase; una futura aprobación debe abordar juntos narrativa y pies para evitar contradicciones.

#### R08 — SHAP, áreas y discusión del historial: distinguir predicción de explicación causal

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **A:P51/P63:** conservar la dominancia de lag_1_promedio_global, +28, ranking, R² y [7]/[8]. Revisar «efectos de intercepto por área» y la explicación de volatilidad; no interpretar NBC_129.0 como código directo de una disciplina.
- **A:P56:** la formulación de B «Algunas áreas de Salud…» es parcial; el rango 4,1–6,2 sigue requiriendo revisión. No sustituirlo por cifras nuevas ni borrar grupos para que la prosa resulte más convincente.
- **Propuesta de revisión:** distinguir en el texto qué es contribución SHAP, qué es error de subgrupo y qué es una interpretación aún no contrastada. Las explicaciones causales deben someterse a revisión explícita; no se ofrecen como hallazgos nuevos.
- **Justificación académica:** asociar cada afirmación con la evidencia que realmente permite sostenerla.
- **Evidencia:** Figura 4, métricas por NBC/departamento; DIFF D05/D07, §4.2/4.4; ficha [8] pendiente.
- **Contraste DIFF:** no ampliar la matización D07 ni modificar etiquetas, imágenes o pies de Figuras 4–5. El ranking predictivo se conserva.

#### R09 — Confianza, anticipación, política y conclusiones

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **A:P7/P9/P69/P74:** revisar «habilitan intervención», «transforma… de reactiva a proactiva» y «con un año de anticipación». Propuesta conceptual: separar rendimiento retrospectivo demostrado de uso institucional potencial, condicionado a disponibilidad de entradas. No afirmar despliegue o impacto curricular medido.
- **A:P60/P75:** no reescribir «diferencial de 2,3 puntos» para hacerlo parecer una validación de incertidumbre. Los valores 84,4 %, 15,6 %, 9,1, 11,4 y 2,3 quedan congelados mientras se reconcilia su procedencia.
- **Justificación académica:** distinguir herramienta predictiva, reglas empíricas y evidencia de impacto. La reducción de alcance debe aprobarse como tal; no es una operación para bajar un indicador.
- **Evidencia:** `src/inference.py`, `src/features.py` (CANTIDADEVALUADOS); DIFF §4.3–4.4, discrepancia de errores por grupos y límite de anticipación.
- **Contraste DIFF:** no se incorporan al paper las métricas recalculadas del DIFF. No se alteran [15]/[26] ni resultados de conclusión. R01 solo mejora la frase funcional del módulo, no resuelve estos pendientes.

#### R10 — Comparación con Transformer: describir diferencias sin atribuir causas no aisladas

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P65:** «La brecha… confirma cuatro factores estructurales…».
- **Propuesta para discutir:** presentar los cuatro factores como diferencias documentadas de la configuración evaluada; distinguir esa descripción de una demostración causal mediante ablaciones. Conservar R² 0,706/0,041, ratio 3,05×, brecha 6,4, padding 51,7 %, [11]/[12] y estructura de la sección.
- **Justificación académica:** un contraste entre dos modelos con varias diferencias simultáneas no aísla cuánto aporta cada factor.
- **Evidencia:** `outputs/reports/decision_transformer.txt`, DIFF §4.4. No se ejecuta un nuevo Transformer ni se “corrige” su rendimiento.
- **Contraste DIFF:** mismo pendiente de alcance, también presente en A:P75. Debe resolverse coherentemente sin suprimir resultados.

#### R11 — Contribución metodológica y novedad

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P67/P75:** «llena un vacío», «ningún trabajo previo», «inédita» y transferibilidad a PISA.
- **Propuesta de revisión:** formular la aportación verificable —documentar el catálogo en este proyecto— separándola de exclusividad bibliográfica y generalización no verificadas. La nueva formulación debe conservar seis tipos, ΔR²≈0,22, [9]/[16]/[21]/[22] y las restantes referencias, hasta decidir académicamente su relación con cada afirmación.
- **Justificación académica:** no convertir una búsqueda bibliográfica incompleta en afirmación universal. Reducir categorización cambia el alcance aceptado y requiere revisión.
- **Evidencia:** DIFF §4.5: identificación pendiente de [16]/[21], contradicción de ficha [8], identificación de [22]. Turnitin no certifica esas referencias ni autoriza reemplazarlas.
- **Contraste DIFF:** no se cambia bibliografía en esta fase, tampoco se usa R11 para insertar o revertir [20]. La modificación existente de [20] se mantiene como decisión separada D09 del DIFF.

#### R12 — Agradecimientos: coherencia de la unidad de datos

**Clasificación: CAMBIO CIENTÍFICO — REQUIERE REVISIÓN.**

- **Original A:P79:** «microdatos agregados».
- **Propuesta para discutir:** «datos agregados», conservando ICFES, agradecimiento y 2020–2024.
- **Justificación académica:** el proyecto describe reportes agregados, no registros individuales; “microdatos” puede confundir al lector. Aunque sea una modificación mínima, se clasifica conservadoramente por afectar nomenclatura de la unidad de datos, no por el resaltado.
- **Evidencia:** sección 3.1, `src/cleaning.py`, DIFF sobre granularidad.
- **Contraste DIFF:** P79 no cambió; validar consistencia terminológica antes de aplicarlo.

**Pasajes marcados sin propuesta de cambio:** palabras clave; títulos de secciones; descripción de colores de SHAP; todos los pies de figura en esta fase; limitaciones L1–L7 y trabajo futuro TF1–TF6. Ya cumplen una función técnica concreta. La revisión científica de ciertas interpretaciones no autoriza recortar esos elementos.

## B. Informe de similitud

### B.1 Resultados y filtros

La página 2 reporta **5 % de similitud general** y señala: **«No se han detectado manipulaciones de texto sospechosas.»** No aparecen alertas de integridad que requieran examinar sustitución de caracteres, texto oculto u otras manipulaciones en este informe.

El informe enumera como filtrados **Bibliografía, Texto citado y Texto mencionado**. Esto limita la interpretación del 5 %: no es una certificación de referencias correctas ni de todas las citas contextuales. Las categorías de fuentes son Internet 4 %, publicaciones 3 % y trabajos entregados 2 %; pueden superponerse y **no se suman** para reemplazar la similitud general. Las once fuentes principales muestran cada una **<1 %** (p. 3).

### B.2 Fuentes principales y relevancia de las coincidencias visibles

Los nombres se reproducen tal como aparecen en el PDF. Las fichas 3 y 11 están truncadas en el informe; no se inventan sus títulos completos. Los trabajos de estudiantes no están disponibles íntegramente en este PDF.

| N.º | Fuente indicada por Turnitin | Peso | Lugar visible y tipo de coincidencia | Valoración académica |
|---:|---|---:|---|---|
| 1 | Fundacion Universidad de San Andres, trabajo del estudiante | <1 % | Similitud p. 5; A:P15, organización del artículo por secciones | Fórmula de navegación compartida; no demuestra apropiación de un resultado |
| 2 | Universidad Autonoma de Chile, trabajo del estudiante | <1 % | pp. 7–8; A:P41/P42, presentación y título de Tabla 1 | Expresiones comunes sobre métricas y conjunto de prueba; no se marcan como copiadas las cifras de la tabla |
| 3 | Publicación: Sergio Merino Fidalgo, Eduardo Zalama Casanova, Jaime Gómez García-Bermejo, J… | <1 % | p. 5; cierre del mapa del artículo y encabezados de marco teórico | Organización genérica; ficha truncada, sin inferir una fuente específica adicional |
| 4 | Universidad de Manizales, trabajo del estudiante | <1 % | p. 4; A:P12, frase inicial sobre Saber Pro/educación superior | Coincidencia breve; la generalización sobre calidad tiene un problema de precisión independiente (R02) |
| 5 | tesisdigitales.umich.mx | <1 % | p. 11; títulos de conclusiones y «El presente trabajo» | Encabezados y fórmula de apertura; no justifica cambiar estructura |
| 6 | www.scribd.com | <1 % | p. 4; A:P12, nombre completo del ICFES y fragmentos adyacentes | Nombre institucional obligatorio para identificación; no reemplazar por sinónimos |
| 7 | repository.poligran.edu.co | <1 % | p. 5; A:P18, «aseguramiento de calidad de la educación superior» | Terminología institucional; revisar respaldo [1]/[15] por precisión, no por porcentaje |
| 8 | www.economia.puc.cl | <1 % | p. 6; encabezados 3/3.1 y «Los datos» | Rótulos metodológicos y palabras comunes |
| 9 | www.grade.org.pe | <1 % | p. 5; A:P18, «teoría de respuesta al ítem» | Término psicométrico establecido; preservarlo |
| 10 | www2.icfes.gov.co | <1 % | p. 5; A:P18, habilidad del evaluado/dificultad del ítem | Léxico técnico pertinente; verificar exactitud y atribución del contenido psicométrico con [1]/[23], sin cambiar términos para eliminar coincidencia |
| 11 | Publicación: Diofanto Arce Tovar. «Análisis Crítico de la Reforma del Sistema Educativo Colom…» | <1 % | p. 4; A:P12, «El Ministerio de Educación Nacional (MEN)» | Nombre institucional, no evidencia de copia de argumentos de esa publicación |

### B.3 ¿Existe un problema real de similitud que deba corregirse?

**En los fragmentos visibles no se identificó un pasaje sustantivo extenso, un resultado apropiado ni una manipulación de texto que obligue a reescribir por similitud.** Las coincidencias se concentran en nombres institucionales, léxico técnico, encabezados y frases de organización. Se mantienen esos términos, la tabla y las citas.

Esto no equivale a una auditoría de originalidad contra los textos completos de las once fuentes: algunos son trabajos de estudiantes inaccesibles y dos fichas están truncadas. Si una comparación posterior de una fuente completa demostrara una cita textual no atribuida, correspondería corregir la atribución según criterio académico, no ocultar la coincidencia.

Sí existen problemas reales independientes: precisión de afirmaciones sobre Saber Pro/Rasch, identificación bibliográfica pendiente y residuos de plantilla. Están en el DIFF y en la sección C; **el 5 % no los resuelve ni los causa**. No se añaden ni eliminan citas/referencias para alterar el indicador.

## C. Problemas independientes de plantilla y edición

Se verificaron tanto la versión representada en los PDF oficiales como el DOCX base y el camera-ready actual. Los PDF oficiales no se corrigen: son evidencia histórica. Las correcciones obligatorias deben quedar resueltas en el camera-ready final; algunas ya estaban hechas antes de esta revisión y otras quedan pendientes. Ninguna se ejecutó en esta fase de informe/propuestas.

| ID / clasificación | Evidencia en versión sometida/base | Estado en camera-ready actual y acción concreta | Contraste con DIFF |
|---|---|---|---|
| C01 — **CORRECCIÓN OBLIGATORIA** | IA p. 3 / similitud p. 4; fechas «septiembre 1, 2020 / octubre 5, 2020»; A footer1.xml | Ya sustituidas por marca DRAFT. Conservar la retirada de fechas ficticias. No inventar recepción/aceptación; completar solo con datos editoriales confirmados cuando corresponda. | F10 |
| C02 — **CORRECCIÓN OBLIGATORIA** | IA pp. 5/7/9/11 y similitud pp. 6/8/10/12: «D. Beltrán et al. / Abstraction & Application 41 (2023) 3 - 16»; A header1.xml | Ya reemplazado por identificación de Saber Pro, autores y DRAFT. Conservar la corrección; no restaurar volumen/paginación ajenos. | F07 |
| C03 — **CORRECCIÓN OBLIGATORIA** | IA pp. 4/6/8/10/12 y similitud pp. 5/7/9/11/13: «auditorría», espacio doble «promedio  global» y capitalización distinta del título; A header2.xml | El encabezado breve de B ya elimina esos errores. El título principal conserva «auditoría» correcto. Conservar corrección. | F08 |
| C04 — **CORRECCIÓN OBLIGATORIA** | IA p. 10 / similitud p. 11, A:P69: «recoleción» | B:P70 ya dice «recolección». Corrección ortográfica sin cambio de significado. | D08 |
| C05 — **CORRECCIÓN OBLIGATORIA** | En A, core.creator=Francisco Alejandro Madera Ramírez; no es autor del paper. No se atribuye este campo al DOCX sometido sin disponer de sus bytes. | B.creator ya identifica a los autores, pero B.lastModifiedBy=Raul Antonio Aguilar Vera, modified=2023-03-22 y revision=30 proceden de plantilla. Retirar atribución/cronología falsas mediante edición posterior, sin inventar autores o fechas. | F12/F13 |
| C06 — **CORRECCIÓN OBLIGATORIA** | El problema se detecta en B, no se infiere de Turnitin: caché PAGE=61 y estadísticas Pages=3, Words=457, Paragraphs=5 heredadas | Actualizar campos/estadísticas en una copia editorial y verificar render; no convertir 61 en texto fijo ni usar Pages=3 como extensión real del paper. | F10/F14 |
| C07 — **CORRECCIÓN OBLIGATORIA** | A y B header3.xml: descr de docPr y cNvPr contiene `C:\Users\mramirez\Documents\2016\sem2-2016\Abstraction & Application\Template\uady.jpg` | Sustituir en futura edición esa descripción ajena por texto alternativo descriptivo del logo, sin cambiar la imagen: «Logotipo de la Universidad Autónoma de Yucatán (UADY)». No es referencia bibliográfica ni dato científico. | Detalle adicional de F11, visible en anexo XML del DIFF |
| C08 — **CORRECCIÓN OBLIGATORIA** | B sigue diciendo «Pendiente de análisis de similitud e IA» en footer1.xml y core.description | Estado desactualizado por recepción de los informes. Propuesta editorial: «DRAFT · Informes de Turnitin recibidos; revisión académica pendiente». Mantener estado borrador; no sustituirlo por “aprobado”. | F10/F12; nueva evidencia oficial |
| C09 — **CORRECCIÓN OBLIGATORIA** | Estilos rStyle=17 y tblStyle=3 usados en B sin definición; 241 referencias de carácter y una de tabla | Resolver los vínculos de estilo en una futura edición conservando apariencia, contenido y plantilla. Verificar visualmente. No es un hallazgo que Turnitin haya señalado. | F06 |

### Elementos que no deben eliminarse como supuestos placeholders

- **UADY y Abstraction & Application:** identidad gráfica/editorial de la plantilla oficial, no falsa afiliación de los autores. Conservar; retirar únicamente identificación de otro artículo y datos editoriales ficticios.
- **Portadas, logos de Turnitin, “Quick Submit”, identificador de entrega y rótulo “Engrega de integridad”:** pertenecen al informe exportado, no al manuscrito; conservar íntegros los PDF.
- **Título PDF “Microsoft Word - Document1”:** metadato genérico del exportado oficial, no prueba de que el paper carezca de título. No se edita la evidencia; B ya tiene título principal en core.
- **[20] “Anónimo” en versión sometida:** es un problema de ficha bibliográfica identificado en el DIFF, no autorización para borrar una referencia como contenido de plantilla. La versión B ya tiene D09; no se cambia en esta fase.
- **Ausencia visible del bloque de autores en los PDF:** diferencia comprobada, pero no se infiere que sea error ni se atribuye a anonimización sin evidencia. B ya contiene autores, afiliación y correos confirmados en el registro previo. No se atribuye a “D. Beltrán” autoría del paper.

## D. Contraste final con DIFF_CAMERA_READY.md

Este apartado documenta el contraste exigido antes de aplicar cambios. **Contrastar no equivale a aprobar ni aplicar.**

| Propuestas | Clasificación | Resultado del contraste | Estado |
|---|---|---|---|
| R01, R03, R06 | **MEJORA DE REDACCIÓN** | Fragmentos equivalentes en función/alcance; conservan números, citas y estructura. No resuelven ni encubren discrepancias científicas. | Propuestas para revisión, no aplicadas |
| R02, R04–R05, R07–R12 | **CAMBIO CIENTÍFICO — REQUIERE REVISIÓN** | Afectan precisión técnica o alcance; vinculados a D04–D07 y §4 del DIFF. No deben aprobarse como un lote de “humanización”. | Revisión con Nathalia; no aplicadas |
| C01–C04 | **CORRECCIÓN OBLIGATORIA** | Ya resueltas en B según F07/F08/F10/D08. | Conservar correcciones existentes |
| C05–C09 | **CORRECCIÓN OBLIGATORIA** | Residuos o estado editorial pendientes en B; acciones concretas enumeradas sin cambiar ciencia. | Pendientes de edición editorial posterior |

**Contenido congelado:** Tabla 1 y sus MAE aceptados; cinco figuras y sus pies; resultados de Ridge/Lasso/LightGBM/Transformer; diferencias de error por flags; años/recuentos; configuración metodológica; citas/referencias y orden de secciones. Las discrepancias siguen visibles en el DIFF. No se sustituyen resultados aceptados por recálculos ni se ejecutan experimentos para modificar un porcentaje.

**Prioridad académica:** (1) cerrar residuos editoriales; (2) revisar las tres mejoras de redacción equivalentes; (3) resolver por separado con Nathalia los pendientes científicos y bibliográficos. La recepción de Turnitin no demuestra que el comité haya pedido cambiar resultados, ni invalida o confirma la aceptación.

## E. Registro de conservación

Se conservaron los hashes de ambos DOCX de `DIFF_CAMERA_READY.md`:

- Base: `5657e9af580c1c555c32128930b7c98cbeb3358cbdd511cd1b7f7ab706db7bcb`.
- Camera-ready: `938bcc7b9bd0cb6e4bca89bc6052a4846edc020af933b2d7adb7aa5318d360f0`.

Se registraron hashes de los archivos preexistentes de `outputs/CONACIC2026` para verificar al cierre que no cambiaron, incluido el DIFF, presentación, guion y fuentes. Se incorporan únicamente los dos PDF, su registro de procedencia y este informe; se versiona también el DIFF previo como antecedente sin modificar su contenido. Los cambios ajenos de video ENSIU presentes al iniciar quedan fuera de esta incorporación. No se realizó envío ni publicación.
