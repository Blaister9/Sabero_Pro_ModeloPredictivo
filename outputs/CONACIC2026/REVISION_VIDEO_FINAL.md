# Revisión final del video CONACIC 2026

## Fuentes y criterio

Fuente principal: `CONAC202617_CANDIDATE.docx`, versión enviada. Base exclusiva: `PRESENTACION_CONACIC2026_V3_ACADEMICA.pptx`, archivo actual de 10 diapositivas. Este contraste se redactó antes de editar la presentación final.

Se cotejaron el texto completo y la tabla del DOCX, sus figuras incrustadas y las diez diapositivas de la V3 renderizadas con PowerPoint. Las referencias P001–P109 identifican, desde uno e incluyendo párrafos vacíos, los párrafos directos del cuerpo del DOCX. Las tablas se identifican por su título, sin contarlas como párrafos. Se incluyen además sección, figura y fragmento para localizar la evidencia sin depender de esta numeración.

No se modifica el artículo ni se revisan sus decisiones metodológicas. La edición se limita a discrepancias y detalles no respaldados por la fuente principal. No se usan la V2 ni resultados recalculados.

SHA-256 inicial del paper: `341025eca3f3c1037cede7b3a75daf972ff3c8d9cab58072e16d35137d19e060`.

SHA-256 inicial de la V3: `416b9c0c7a2633d297f5818777db2170f736525c1e1d05a29d07289f406800b1`.

## Diapositiva 1 — Título y autoría

- **Contenido actual:** título completo del trabajo, Edwin Santiago Paz Bedoya, UNIMINUTO Virtual – Bogotá, Colombia y CONACIC 2026.
- **Coincidencia:** título y afiliación coinciden. La autoría está incompleta.
- **Discrepancia:** falta Nathalia Orozco Morales en la V3 actual. Se verificó directamente el archivo, sin asumir que la revisión histórica describe su estado presente.
- **Cambio mínimo:** añadir Nathalia Orozco Morales debajo de Edwin Santiago Paz Bedoya en el cuadro de autoría existente. Conservar título y afiliación.
- **Evidencia:** P001, P004–P005. P004: «Edwin Santiago Paz Bedoya¹, Nathalia Orozco Morales¹».
- **Modificación visual:** sí, solo el cuadro de autoría; ampliar su altura dentro del espacio disponible si lo exige la segunda línea.

## Diapositiva 2 — Problema y objetivo

- **Contenido actual:** publicación de resultados meses después del examen; estimación del PROMEDIO_GLOBAL por programa con información histórica pública del ICFES.
- **Coincidencia:** sí.
- **Discrepancia:** ninguna. No promete una anticipación operativa garantizada.
- **Cambio mínimo:** ninguno. En el guion, delimitar el estudio como evaluación retrospectiva y mencionar que el uso anticipado depende de la disponibilidad de entradas.
- **Evidencia:** §1, P015–P017; resumen, P011, «según la disponibilidad de las entradas»; §6.1, P077, «en una evaluación retrospectiva».
- **Modificación visual:** no.

## Diapositiva 3 — Datos y construcción del panel

- **Contenido actual:** 127.716 observaciones procesadas, reportes ICFES 2020–2024, unidad institución/programa/prueba/año y gráfico anual con 19.135, 24.233, 27.722, 27.864 y 28.762 filas.
- **Coincidencia:** sí. El total corresponde al panel post-pivot, no a estudiantes ni a programas únicos. Los cinco recuentos coinciden con la Figura 1 incrustada en el paper.
- **Discrepancia:** ninguna. «Procesadas» es compatible con «post-pivot» y no justifica por sí solo una reescritura.
- **Cambio mínimo:** ninguno; explicar oralmente la reorganización de filas a columnas y el carácter agregado de las observaciones.
- **Evidencia:** §§3.1–3.2, P029–P031; Figura 1, panel «Filas limpias por año» y P036.
- **Modificación visual:** no. Se conserva el gráfico editable y su libro incrustado.

## Diapositiva 4 — Control de fuga y esquema de evaluación

- **Contenido actual:** entrenamiento 2020–2023, 98.954 filas; test externo 2024, 28.762 filas; exclusión de puntajes y niveles del mismo ciclo; rezagos de observaciones anteriores disponibles.
- **Coincidencia:** sí, con el alcance de split temporal externo.
- **Discrepancia:** ninguna. No afirma que toda la validación interna haya sido temporalmente estricta.
- **Cambio mínimo:** ninguno. El guion menciona los seis tipos de fuga y el cambio conjunto reportado de ΔR²≈0,22, vinculado a Lasso, sin presentarlo como ganancia de LightGBM ni como efecto causal aislado.
- **Evidencia:** §3.3, P033, Lasso R²≈0,88 frente a 0,658; §3.4, P038, «El split externo respeta el orden temporal» y tamaños 98.954/28.762; §1, P017.
- **Modificación visual:** no.

## Diapositiva 5 — Modelos evaluados

- **Contenido actual:** Ridge/Lasso con penalización L2/L1; LightGBM con 50 trials de Optuna; Transformer encoder sobre secuencias históricas; comparación de configuraciones con diferencias en sus entradas.
- **Coincidencia:** sí. Se presentan cuatro modelos en tres bloques.
- **Discrepancia:** ninguna. Omitir detalles de árboles o épocas no cambia los resultados del paper.
- **Cambio mínimo:** ninguno. Mantener la delimitación a las configuraciones evaluadas.
- **Evidencia:** §2.4, P026; §3.5, P040; §5.2, P068, diferencias de muestras efectivas, entradas y secuencias.
- **Modificación visual:** no.

## Diapositiva 6 — Desempeño global de LightGBM

- **Contenido actual:** dispersión predicho/real, RMSE 9,33, MAE 6,21, R² 0,706; test externo 2024, n=28.762.
- **Coincidencia:** sí. Son los redondeos de 9,3293; 6,2109; 0,7062.
- **Discrepancia:** ninguna. La imagen científica corresponde a la Figura 3 del artículo, conservada en la V3 con mayor resolución.
- **Cambio mínimo:** ninguno. Explicar los ejes y la diagonal sin interpretar R² como porcentaje de aciertos ni RMSE como margen fijo para cada predicción.
- **Evidencia:** Tabla 1; §4.1, P048; Figura 3 y P051, con esas métricas y el conjunto de prueba.
- **Modificación visual:** no.

## Diapositiva 7 — Comparación de modelos

- **Contenido actual:** tabla Modelo/RMSE/MAE/R² con Ridge 10,2294/7,2967/0,6467; Lasso 10,0722/7,0622/0,6575; LightGBM 9,3293/6,2109/0,7062; Transformer 16,8588/n/d/0,0405. Comentario limitado al test 2024.
- **Coincidencia:** sí, todas las celdas coinciden con la Tabla 1.
- **Discrepancia:** ninguna. Se conserva «n/d» en el MAE del Transformer.
- **Cambio mínimo:** ninguno. La comparación oral queda limitada a 2024 y a las configuraciones estudiadas, sin superioridad universal o significancia estadística no reportada.
- **Evidencia:** §4.1, P043–P045 y Tabla 1; §5.2, P068.
- **Modificación visual:** no. Se conserva íntegra la tabla editable.

## Diapositiva 8 — Interpretabilidad mediante SHAP

- **Contenido actual:** beeswarm original; rezago reciente del PROMEDIO_GLOBAL, segundo rezago global y rezago de la prueba; precisión explícita de ausencia de causalidad.
- **Coincidencia:** sí. `lag_1_promedio_global` tiene la mayor contribución predictiva observada.
- **Discrepancia:** ninguna. No se usa «inercia institucional» como explicación causal.
- **Cambio mínimo:** ninguno. Señalar oralmente la primera fila y explicar el eje SHAP y el color. No interpretar las etiquetas codificadas NBC como efectos de disciplinas concretas.
- **Evidencia:** §4.2, P053 y Figura 4/P055; §3.4, P038, para la codificación multiclase.
- **Modificación visual:** no. Se conserva la figura completa.

## Diapositiva 9 — Análisis de error y limitaciones

- **Contenido actual:** Figura 5 de RMSE por NBC; Sucre 13,29 (n=366), Chocó 12,03 (n=243), Putumayo 11,18 (n=54); único año de prueba, datos agregados, ausencia de variables socioeconómicas y heterogeneidad del error.
- **Coincidencia:** figura, departamentos y limitaciones coinciden. La precisión numérica regional excede lo reportado en el paper final.
- **Discrepancia:** §4.3 informa Sucre ≈13, Chocó ≈12 y Putumayo ≈11. El DOCX no publica esos decimales ni los n departamentales. No se afirma que sean erróneos, pero no se trasladan a la versión pública cuando la fuente principal no los documenta.
- **Cambio mínimo:** sustituir solo las tres líneas por «Sucre ≈13 puntos», «Chocó ≈12 puntos» y «Putumayo ≈11 puntos». Retirar los n. Conservar figura, título y limitaciones.
- **Evidencia:** §4.3, P058; Figura 5 y P060; §5.5, P074. La figura muestra desagregación por NBC y el texto derecho, por departamento: no se confunden ambas.
- **Modificación visual:** sí, únicamente el cuadro de cifras regionales. Sin nueva gráfica ni cambio de posiciones.

## Diapositiva 10 — Conclusiones

- **Contenido actual:** desempeño LightGBM en 2024; señal predictiva de rezagos; ampliación de validación temporal y revisión de heterogeneidad antes del uso institucional; walk-forward como trabajo futuro.
- **Coincidencia:** sí.
- **Discrepancia:** ninguna. Las conclusiones preservan el alcance empírico del estudio.
- **Cambio mínimo:** ninguno. El guion complementa con los flags empíricos del módulo de inferencia y aclara que no constituyen intervalos ni incertidumbre calibrada. Mantener walk-forward y evaluación institucional como trabajo futuro.
- **Evidencia:** §4.2, P053; §4.4, P062; §5.5, P074, «sin intervalos de confianza formales»; §6.1, P077–P078; §6.2, P080.
- **Modificación visual:** no.

## Decisión de edición

Cambios visibles autorizados por el contraste: diapositivas **1 y 9**. Las otras ocho se conservan, incluido su texto. La exposición oral cubre el catálogo de fugas y los flags empíricos sin añadir diapositivas ni sobrecargar la V3.

El archivo actual no contiene notas de orador. Las fuentes se documentan en esta revisión y el guion se entrega por separado. No se incorporan auditorías internas, etiquetas DRAFT ni comentarios de producción al material público.

## Verificación final

Verificación completada el 21 de septiembre de 2026.

- **Cantidad:** 10 diapositivas en el PPTX y 10 páginas en el PDF.
- **Render:** exportación nativa con Microsoft PowerPoint a 1920 × 1080. Se inspeccionaron individualmente las diez imágenes finales y, por separado, las diez páginas rasterizadas del PDF.
- **Revisión visual:** sin desbordamientos, cortes, solapamientos involuntarios ni glifos ausentes observados. La comprobación de límites de texto en PowerPoint tampoco detectó cuadros excedidos.
- **Material público:** sin DRAFT, instrucciones internas, marcadores pendientes o comentarios de producción en las diapositivas. Los nombres internos de objetos no forman parte del contenido visible.
- **Autoría:** ambos autores completos y afiliación correcta en portada.
- **Cifras:** total post-pivot, partición externa y métricas contrastados con el DOCX. Las doce celdas de métricas de la tabla coinciden exactamente con la Tabla 1 del paper. Las cifras regionales quedan en la precisión aproximada publicada.
- **Legibilidad:** títulos, mensajes principales y métricas legibles a 1920 × 1080. Las figuras de SHAP y NBC mantienen sus etiquetas originales; el guion indica dónde señalar y evita exigir la lectura de todas sus etiquetas durante la grabación.
- **Preservación:** solo cambian `ppt/slides/slide1.xml` y `ppt/slides/slide9.xml`. Las otras 85 partes del archivo son idénticas a la V3. Esto incluye 36 partes de patrones, diseños, temas, imágenes, gráfico y libro incrustado. Se conservan fuentes, posiciones, dimensiones y estructura de 10 diapositivas. No hizo falta ampliar el cuadro de autoría.
- **Comparación visual reproducible:** las diapositivas 2, 3, 4, 5, 6, 7, 8 y 10 son idénticas píxel por píxel a los renders de la V3 actual. En 1 y 9 se revisaron los cambios frente a sus originales.
- **Editabilidad:** tabla de la diapositiva 7 y gráfico anual con libro incrustado de la diapositiva 3 preservados.
- **Fuentes intactas:** SHA-256 del paper y de la V3 sin cambios respecto a los valores iniciales consignados arriba. Los cambios locales preexistentes del repositorio permanecen intactos. No se modificaron datos, resultados ni modelos; no hubo reentrenamiento ni merge.
- **Alcance audiovisual:** no se generaron MP4 ni voces sintéticas.

### Duración estimada del guion

El texto que se dice, incluidas las transiciones, contiene **1.030 palabras escritas**. Al expandir las cifras y la pronunciación de siglas y nombres técnicos, equivale aproximadamente a **1.157 palabras orales**. El conteo excluye títulos, instrucciones de señalamiento, explicaciones para el presentador y pausas entre corchetes.

La estimación reserva **40 segundos** para pausas, señalamientos, cambios de diapositiva y cierre. A 140–145 palabras orales por minuto, la duración resulta entre **8:39 y 8:56**. El objetivo de **8:45** corresponde aproximadamente a 143 palabras por minuto durante el habla. La distribución admite variaciones locales de ritmo al explicar cifras y figuras.

| Diapositiva | Objetivo | Acumulado |
| --- | --- | --- |
| 1 | 25 s | 0:25 |
| 2 | 48 s | 1:13 |
| 3 | 52 s | 2:05 |
| 4 | 60 s | 3:05 |
| 5 | 48 s | 3:53 |
| 6 | 62 s | 4:55 |
| 7 | 58 s | 5:53 |
| 8 | 62 s | 6:55 |
| 9 | 58 s | 7:53 |
| 10 | 52 s | 8:45 |

Es una estimación editorial, no una medición de audio. La duración real se confirma con el ensayo de Santiago. Incluso a 130 palabras orales por minuto y con las mismas pausas, el cálculo es aproximadamente 9:34, por debajo del máximo de diez minutos.

### Archivos producidos

- `REVISION_VIDEO_FINAL.md`: contraste de las diez diapositivas, evidencia y verificación.
- `PRESENTACION_CONACIC2026_FINAL.pptx`: presentación editable final.
- `PRESENTACION_CONACIC2026_FINAL.pdf`: exportación de las diez diapositivas.
- `GUION_VIDEO_CONACIC2026_FINAL.md`: explicación oral, tiempos, señalamientos y transiciones.
- `TARJETA_GRABACION_CONACIC.md`: cifras críticas e ideas breves por diapositiva.
- `RENDER_FINAL/Diapositiva1.png` a `Diapositiva10.png`: diez imágenes de verificación a 1920 × 1080.

SHA-256 PPTX final: `2bff0a2a7b0f4562ed2940ea51dea1024ae266cf5f55e47de0f6972eeabecf6a`.

SHA-256 PDF final: `af0447f6eaf21ce40e703697a4b33b4f096bc4a0fe2f776c302f9f4ca32f094b`.
