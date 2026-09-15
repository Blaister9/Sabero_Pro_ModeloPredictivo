# Reunión con Nathalia Orozco Morales

Objetivo: resolver las decisiones abiertas de la versión CONACIC. La aceptación del paper 17 es sin observaciones; el cierre sigue condicionado a los análisis de similitud e IA anunciados por el comité.

## Decisiones necesarias

1. **Título y base.** Ratificar el título completo de `CAMERA_READY_DRAFT.docx`, idéntico al de la base `_FINAL`. Santiago confirmó esa base; no hay evidencia de otro archivo sometido. Evitar abreviar el título en el artículo sin contrastarlo con el registro del paper 17.
2. **Ficha institucional.** Revisar la escritura final ya incorporada para ambos: UNIMINUTO Virtual – Bogotá, Colombia; Edwin Santiago Paz Bedoya, `edwin.paz@uniminuto.edu`; Nathalia Orozco Morales, `nathalia.orozco@uniminuto.edu`. Los datos están confirmados por Santiago, por lo que solo hace falta conformidad editorial/institucional, no volver a buscarlos.
3. **Participación de Nathalia.** Definir si aparece en cámara o narra alguna sección. Propuesta disponible: Santiago narra todo. Si Nathalia participa, los bloques de motivación o conclusiones pueden grabarse por separado sin rehacer las demás diapositivas.
4. **Orden y énfasis.** Revisar el orden de las diez diapositivas y decidir si se desea dar más tiempo al catálogo de fuga o a las limitaciones. Mantener el resultado LightGBM, la comparación entre modelos y SHAP. El guion base dura 8:30 planificados.
5. **Resolución de la auditoría.** Acordar cómo documentar las pequeñas diferencias MAE de los baselines, las divisiones internas que mezclan años y `TargetEncoder` en modo multiclase (135 clases; 417 columnas). El holdout externo 2024 se conserva y las métricas principales se reproducen. No se han reentrenado modelos. Revisar los alcances causales/novedad, las afirmaciones de confianza y las referencias pendientes [8], [16], [21], [22]. Esta decisión es necesaria por evidencia del repositorio, no por observaciones del comité.
6. **Requisitos UNIMINUTO.** Confirmar forma institucional de afiliación, uso de logo si se exige, mención del programa de especialización, autorizaciones internas y cualquier revisión institucional. No se han supuesto requisitos adicionales.
7. **Formato editorial restante.** Determinar si A&A exige clasificación MSC para esta contribución. La plantilla trae el código de un artículo de ejemplo y no se copió. Volumen, paginación editorial y fechas de recepción/aceptación quedan por asignar, sin datos inventados.
8. **Video y entrega.** Si el comité no especifica plataforma o visibilidad, decidir modalidad de aparición y si el futuro enlace será público o no listado. No consta un requisito público verificable de plataforma/visibilidad en las fuentes consultadas. Confirmar también la zona horaria de los cierres 20 y 23 de septiembre a las 23:59. No se enviará nada desde esta preparación.

## Posibles preguntas del congreso

| Pregunta | Respuesta breve basada en el trabajo |
|---|---|
| ¿Predicen notas individuales? | No. La fila representa institución-programa-prueba-año. El objetivo es el promedio global agregado. |
| ¿Cuántos estudiantes hay? | El panel tiene 127.716 filas agregadas. Ese número no equivale a estudiantes distintos. |
| ¿Qué significa R² = 0,706? | La reducción relativa del error cuadrático respecto de la referencia basada en la media del conjunto evaluado es aproximadamente 70,6 %. No es porcentaje de predicciones acertadas. |
| ¿Cuál es la mejora sobre Lasso? | El RMSE pasa de 10,0722 a 9,3293, una reducción de 0,7429 puntos, aproximadamente 7,4 %. |
| ¿Cómo evitaron usar el futuro? | El test externo es 2024; los rezagos y resúmenes usan observaciones anteriores y se excluyen medidas concurrentes. La auditoría del cierre detectó que las divisiones internas mezclan años, por lo que no debemos afirmar validación temporal interna completa. |
| ¿Son 15 o 417 variables? | Son 15 entradas originales. En los modelos guardados, TargetEncoder automático infirió 135 clases del objetivo y expandió las categóricas: el modelo recibe 417 columnas transformadas. Esta configuración debe quedar descrita y revisada. |
| ¿NBC_129.0 identifica un área específica? | No debe interpretarse así. Es un componente generado por TargetEncoder para el valor objetivo 129; no un código disciplinar. El hallazgo SHAP más claro es la influencia de los rezagos globales. |
| ¿Lag 1 siempre es el año inmediatamente anterior? | No. `shift(1)` toma la observación previa disponible de la entidad. Hay 2.022 filas con separación superior a un año. |
| ¿Por qué no funcionó el Transformer? | La configuración evaluada usó secuencias más cortas y menos muestras efectivas, sin las categóricas de los modelos tabulares. Son limitaciones documentadas; no se aisló causalmente cada factor. |
| ¿SHAP demuestra inercia institucional causal? | SHAP explica las contribuciones a la predicción. La influencia del historial es predictiva; no constituye identificación causal. |
| ¿Las banderas de confianza son probabilidades? | No. Son reglas empíricas por muestra pequeña, falta de historial y extrapolación. No entregan intervalos calibrados. |
| ¿Los departamentos con mayor error tienen menor calidad educativa? | El error mide precisión del modelo, no calidad educativa. Los tamaños de grupo difieren y no se incluyeron covariables socioeconómicas. |
| ¿Se puede anticipar un año completo? | La evaluación usa 2024 tras entrenar con años anteriores. Para una anticipación operativa real debe verificarse la disponibilidad de todas las entradas, especialmente el número de evaluados. |
| ¿La superioridad es estadísticamente significativa? | No se reportaron intervalos ni múltiples cortes externos. Se afirma mejor desempeño en la configuración y año evaluados. |
| ¿Qué se pudo reproducir en esta fase? | Se recalcularon predicciones de tres modelos guardados sobre el CSV de test, sin reentrenar. LightGBM reproduce las tres métricas. Los MAE de Ridge/Lasso presentan diferencias pequeñas. Transformer se contrastó con su reporte histórico. |
| ¿Se desplegó y se midió impacto curricular? | Existe un módulo de inferencia. El trabajo no demuestra despliegue institucional ni impacto de intervenciones. |

## Acuerdos por registrar durante la reunión

Fecha: pendiente. Participantes: pendiente. Decisiones sobre los puntos 1–8: pendiente. Responsable y fecha de cada ajuste: pendiente. Este espacio no registra una aprobación anticipada.
