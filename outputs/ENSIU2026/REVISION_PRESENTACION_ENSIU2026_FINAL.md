# Revisión final de la adaptación ENSIU 2026

Fecha: 28 de septiembre de 2026, America/Bogota.

## Resultado

Adaptación mínima completada: **10 diapositivas, mismo orden que CONACIC final**. Las diapositivas 3–9 conservan íntegro su contenido. Solo 1, 2 y 10 tienen ajustes textuales locales según el plan mostrado previamente. El cambio del patrón retira logos CONACIC, UADY y SiMCise y el texto SIMULTÁNEA. Se insertan los originales oficiales ENSIU/UNIMINUTO, sin deformación.

No se generaron gráficos nuevos. El fondo genérico de IA, los paneles, la franja verde, la tipografía, la tabla y todos los gráficos científicos se conservan. La franja lateral queda sin el rótulo del evento anterior. El logo ENSIU tiene un fondo blanco propio del JPG oficial; no se recortó ni se inventó una versión transparente.

Los 182 archivos versionados existentes al inicio conservan sus SHA-256. No cambió la presentación CONACIC, su PDF, el paper, los antecedentes ENSIU, los datos, modelos, código científico ni las métricas. No se ejecutaron experimentos ni se recalcularon resultados.

## Revisión por diapositiva

Se abrió el PPTX final con Microsoft PowerPoint 16.0 mediante automatización, se exportaron las diez diapositivas a PNG de 1920 × 1080 y el PDF directamente desde ese mismo archivo. Se renderizaron las diez páginas del PDF y se inspeccionaron visualmente **una por una**, además de comparar la estructura y los renders con la base. No se usó solo una hoja de contacto para aprobar el diseño.

| Slide | Contenido y cambio | QA visual y científico | Resultado |
| --- | --- | --- | --- |
| 1 | Título ENSIU completo, autores y afiliación originales; Misión 4; programa/código atribuido a Edwin | Título en dos líneas dentro del panel, autores legibles, misión y código sin cortes; dos logos correctos y proporcionados; pie ENSIU | Conforme |
| 2 | Problema y objetivo intactos; nueva línea Datos para la equidad | Nueva línea separada del objetivo y dentro del panel; no tapa texto; estructura y separación original conservadas | Conforme |
| 3 | Panel, 127.716 y recuentos anuales originales | Gráfico nativo editable con libro original; etiquetas 19.135, 24.233, 27.722, 27.864, 28.762 preservadas; unidad de análisis legible | Conforme; contenido visual idéntico |
| 4 | Train 2020–2023, 98.954; test 2024, 28.762; controles | Cajas y frases sin cortes; cifras correctas; guion distingue evaluación externa de validación interna | Conforme; contenido visual idéntico |
| 5 | Ridge/Lasso, LightGBM y Transformer | Textos y advertencia de diferencias de entradas intactos; no se promete superioridad universal | Conforme; contenido visual idéntico |
| 6 | Dispersión y RMSE 9,33, MAE 6,21, R² 0,706 | Ejes, diagonal, nube y cifras legibles; test 2024 y n correctos; guion explica las tres métricas sin confundir R² con aciertos | Conforme; contenido visual idéntico |
| 7 | Tabla científica completa sin cambios | Tabla sigue editable; todos los decimales preservados y n/d Transformer intacto; fila LightGBM destacada; texto referido al test 2024 | Conforme; contenido visual idéntico |
| 8 | Imagen SHAP y tres rezagos originales | Primeras variables y eje legibles; advertencia de ausencia de causalidad conservada; sin recortes del gráfico | Conforme; contenido visual idéntico |
| 9 | Gráfico NBC, cifras departamentales y límites originales | Se conserva el gráfico por áreas, no se lo etiqueta como departamental; Sucre ≈13, Chocó ≈12, Putumayo ≈11; límites visibles; guion explica ambas desagregaciones | Conforme; contenido visual idéntico |
| 10 | Tres conclusiones intactas; frase final adaptada a equidad territorial | La frase nueva ocupa dos líneas dentro del espacio inferior; no se superpone al pie; mantiene validación e impacto institucional como trabajo pendiente | Conforme |

En todas: ausencia visual de marcas anteriores; pie ENSIU y numeración correctos; tipografía Gill Sans MT; ningún texto cortado, ningún desbordamiento ni superposición no prevista. Los gráficos conservan su tamaño y resolución originales: las etiquetas densas requieren visualización a pantalla completa, como en la base, y no deben leerse una a una durante la exposición.

## Evidencia de conservación y equivalencia

- Se compararon los objetos OOXML por slide contra la base, descontando el cambio literal del pie. Solo cambiaron los cuadros previstos: portada (título y cuadro inferior), D2 (cuadro inferior antes vacío) y D10 (frase de trabajo futuro). El número de objetos por diapositiva permanece igual.
- Se comparó píxel por píxel el área de contenido de D3–D9, renderizada por la misma versión de PowerPoint a 1920 × 1080. Las siete áreas resultaron **idénticas**. La región excluye el patrón de logos y el pie que deben cambiar.
- Se verificaron bytes idénticos para las tres imágenes científicas, el fondo genérico, el gráfico anual, sus relaciones y su libro Excel incrustado. La tabla D7 conserva exactamente su XML original.
- Se eliminaron del paquete los tres medios de marca antigua, sus relaciones y la miniatura heredada. Se buscaron nombres de marcas en XML, notas, metadatos y texto PDF, incluyendo la concatenación de las letras verticales de SIMULTÁNEA. No quedaron coincidencias.
- El validador de integridad, el de geometría, la política de fuentes, la importación Artifact Tool y la validación del gráfico/libro nativo pasaron sin hallazgos. La tabla conserva todos sus valores originales, no una tabla reconstruida.
- Los límites de texto medidos por PowerPoint quedan dentro de sus cajas. Se inspeccionaron además visualmente gráficos, márgenes y logos.
- El PDF se generó del PPTX entregado, no de una composición paralela. Tiene diez páginas y el mismo contenido. Se compararon los renders: la diferencia media por canal entre PNG PowerPoint y PDF rasterizado está entre 1,8830 y 2,7605 sobre 255, atribuible a los distintos renderizadores. La equivalencia es de contenido y composición, no identidad binaria de píxeles entre formatos.

Evidencia reproducible: `fuentes_final/VERIFICACION_FINAL.json` y `fuentes_final/ORIGINALES_SHA256.json`. Renders y diagnósticos completos permanecen en `build/ensiu2026/`, ignorado por Git. Se utilizó PowerPoint como exportador nativo, no se afirma una revisión manual en su interfaz.

## Control científico

| Elemento | Comprobación |
| --- | --- |
| Dataset | 127.716 observaciones agregadas; no estudiantes ni programas únicos |
| Entrenamiento | 2020–2023, 98.954 observaciones |
| Prueba externa | 2024, 28.762 observaciones |
| LightGBM | RMSE ≈9,33; MAE ≈6,21; R² ≈0,706 |
| Comparadores | Ridge RMSE 10,2294; Lasso 10,0722; Transformer 16,8588, preservados de D7 |
| SHAP | Rezagos como contribuciones predictivas; sin causalidad |
| Territorio | Diferencias descriptivas; sin causa económica ni prueba de brechas socioeconómicas |
| Intervención | Uso institucional y efectos curriculares pendientes de validación |
| Flags | Solo señales empíricas; no intervalos calibrados |

La comunicación ENSIU original usa expresiones más fuertes sobre desarrollo relativo, certeza e intervención. El guion conserva el sentido de equidad como orientación del uso y la evaluación futura, pero no adopta esas afirmaciones como resultados comprobados. No se añadió el ΔR² al deck ni se ejecutó una nueva auditoría del modelo. Los reportes históricos muestran pequeñas diferencias de MAE en baselines; se preserva la tabla CONACIC final conforme a la jerarquía instruida, sin corregir ni recalcular cifras.

## Tres pilares, tiempos y programación

La interpretación documentada es **Misión 4 / Datos para la equidad / Sistematización de información territorial**, con citas exactas del apartado 1 de la comunicación. Es una inferencia editorial explícita; el DOCX no los enumera bajo la etiqueta “tres pilares”. La otra tríada del guion audiovisual (Informar, Atraer, Convencer) y las cuatro etapas STAR se distinguen en el plan.

El guion A por diapositivas contiene 1.088 palabras de texto oral. Con cifras principales ya expresadas en palabras, pronunciación de siglas y pausas, se estima **8:30–9:30**, con referencia de ensayo de **9:00**. La versión B STA tiene 525 palabras y se estima en **4:40–5:00**, seguida del clip R de **60 s**. No se grabó ni midió audio nuevo. El cronometraje es editorial y requiere ensayo de Santiago.

Las fuentes oficiales consultadas fueron página ENSIU, programación de diez páginas, TDR de catorce páginas, Adenda 001, Anexo 1 y logos publicados, archivadas con sus URL y hashes en `docs/ENSIU2026/fuentes_oficiales/`. La revisión oficial detalla la evidencia y la prevalencia de la adenda sobre las fechas antiguas de la página.

- Misión 4: **2 de octubre de 2026, virtual**.
- Nathalia y el semillero coincidente: **bloque 4 ENSIU, 11:10 a. m.–12:00 m.**, programación p. 6.
- Edwin, título y turno individual: **PENDIENTES de confirmación**; no constan nominalmente.
- Formato oficial: **5 minutos STA sin diapositivas + 1 minuto R audiovisual**. Debe confirmarse el uso proyectado del PPTX con Nathalia/organización. La presentación está terminada y sirve como material de apoyo y preparación, pero no acredita una excepción.
- Plantilla PPTX oficial: no encontrada. Los logos oficiales sí se descargaron.

## Git y alcance de la entrega

Rama única: `feat/ensiu-2026-presentacion-final`. HEAD inicial: `81c61c9f5bfd2ad753b8d1f230bd57b26f22b26e`.

Todos los archivos incorporados son **nuevos**, bajo `docs/ENSIU2026/` y `outputs/ENSIU2026/`. Se conservaron el paper, CONACIC y todos los antecedentes. No se hizo merge ni se modificaron otras ramas. Los temporales y renders quedan dentro de este worktree en `build/ensiu2026/` y no entran al commit.

Mensaje previsto y solicitado: `feat(ensiu): prepare final 2026 presentation`. El identificador definitivo y la confirmación remota se reportan en el cierre del chat una vez ejecutados el commit y el push, para no declarar operaciones aún no realizadas dentro de este informe previo al commit.

## Pendientes de Santiago

Confirmar con Nathalia la fila de agenda, el expositor y turno individual; el permiso de apoyo visual frente a los TDR; y la intención precisa de “tres pilares”. Ensayar el guion correspondiente al formato confirmado. Estas cuestiones no alteraron ni bloquearon la adaptación mínima pedida.

## Lista exacta de archivos nuevos antes del commit

`git diff --name-status` registra únicamente altas (A), sin modificaciones ni eliminaciones:

- `docs/ENSIU2026/PLAN_PRESENTACION_FINAL_ENSIU2026.md`
- `docs/ENSIU2026/REVISION_OFICIAL_ENSIU_2026.md`
- `docs/ENSIU2026/fuentes_oficiales/Adenda_001.pdf`
- `docs/ENSIU2026/fuentes_oficiales/Anexo_Audiovisuales.docx`
- `docs/ENSIU2026/fuentes_oficiales/Logo-Ensiu-2026-web.jpg`
- `docs/ENSIU2026/fuentes_oficiales/PROCEDENCIA.json`
- `docs/ENSIU2026/fuentes_oficiales/Programacion_Resultados_2026.pdf`
- `docs/ENSIU2026/fuentes_oficiales/TDR_ENSIU_2026.pdf`
- `docs/ENSIU2026/fuentes_oficiales/ensiu_2026.html`
- `docs/ENSIU2026/fuentes_oficiales/logo-uniminuto.png`
- `outputs/ENSIU2026/GUION_PONENCIA_ENSIU2026_FINAL.md`
- `outputs/ENSIU2026/PRESENTACION_ENSIU2026_FINAL.pdf`
- `outputs/ENSIU2026/PRESENTACION_ENSIU2026_FINAL.pptx`
- `outputs/ENSIU2026/REVISION_PRESENTACION_ENSIU2026_FINAL.md`
- `outputs/ENSIU2026/fuentes_final/ORIGINALES_SHA256.json`
- `outputs/ENSIU2026/fuentes_final/REPRODUCIR.md`
- `outputs/ENSIU2026/fuentes_final/VERIFICACION_FINAL.json`
- `outputs/ENSIU2026/fuentes_final/adaptar_presentacion.mjs`
- `outputs/ENSIU2026/fuentes_final/exportar_y_verificar.py`
- `outputs/ENSIU2026/fuentes_final/validar_presentacion.mjs`
