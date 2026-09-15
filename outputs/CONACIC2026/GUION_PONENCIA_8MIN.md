# Guion de ponencia CONACIC 2026

**DRAFT para ensayo. Duración objetivo: 08:30. No es el video definitivo.**

Ritmo orientativo: 135–150 palabras por minuto durante el habla, con pausas para señalar figuras. Los tiempos son una planificación; confirmar duración con voz real. No acelerar el audio para encajar.

## Pronunciación

| Escritura | Forma hablada |
|---|---|
| LightGBM | «láit yi bi em» |
| R² | «erre al cuadrado» |
| RMSE | «erre eme ese e», o «raíz del error cuadrático medio» |
| Ridge | «rich», con sonido final suave de j |
| Lasso | «laso» |
| SHAP | «shap» |
| Transformer | «transfórmer» |

## Diapositiva 1 · 00:00–00:40

**Predicción del PROMEDIO_GLOBAL de Saber Pro mediante LightGBM y auditoría de fuga temporal: un estudio a nivel de programa académico en Colombia**

**Señalar:** Señalar el título y la unidad programa académico.

Buenas tardes. Soy Edwin Santiago Paz Bedoya y presento este trabajo realizado con Nathalia Orozco Morales, de UNIMINUTO Virtual, en Bogotá. Estudiamos la predicción del promedio global de Saber Pro a nivel de programa académico en Colombia. La pregunta es hasta dónde podemos anticipar ese resultado con los datos públicos y el historial de cada programa. Para responderla comparamos cuatro modelos y revisamos un problema central: que ninguna variable revele, de manera directa o indirecta, el resultado que estamos intentando predecir. Voy a explicar los datos, la evaluación y los límites del resultado obtenido.

Fuente de respaldo: Paper aceptado, título y §1.

## Diapositiva 2 · 00:40–01:25

**Problema y objetivo de investigación**

**Señalar:** Señalar objetivo y unidad de análisis.

El punto de partida es una necesidad de las instituciones: disponer de información para revisar el desempeño de sus programas antes de conocer el siguiente resultado oficial. Nuestro objetivo fue construir y evaluar un procedimiento que estimara ese promedio a partir de información histórica. Aquí conviene aclarar la escala del trabajo. No estamos prediciendo la nota de un estudiante. Trabajamos con resultados agregados por institución, programa y prueba. Por eso, una predicción puede orientar una revisión académica, pero no describe las circunstancias de una persona. Tampoco evaluamos todavía si una intervención basada en esas predicciones mejora el aprendizaje. Esa es una pregunta posterior.

Fuente de respaldo: Paper aceptado, §1 y §5.5.

## Diapositiva 3 · 01:25–02:25

**Datos ICFES y construcción del panel**

**Señalar:** Señalar 127.716 filas y el aumento de cobertura por año.

Usamos reportes públicos del ICFES entre dos mil veinte y dos mil veinticuatro. La consolidación histórica registra cerca de un millón setecientas treinta mil filas crudas. Ese volumen no equivale a estudiantes ni a programas distintos: una misma unidad aparece varias veces para registrar diferentes medidas. Por eso fue necesario reorganizar las estadísticas en columnas y unir los puntajes por sus identificadores. El panel resultante tiene ciento veintisiete mil setecientas dieciséis observaciones. La gráfica muestra cómo cambia su cobertura en los cinco años. Cada fila identifica una institución, un programa, una prueba y un año. Conservamos el historial disponible de cada entidad. Cuando falta un año, el rezago corresponde a la observación anterior disponible, algo que debemos tener presente al interpretar las trayectorias.

Fuente de respaldo: Paper, §3.1–3.2; data/processed/saber_pro_features.csv; src/cleaning.py.

## Diapositiva 4 · 02:25–03:25

**Fuga de información y separación temporal**

**Señalar:** Señalar entrenamiento 2020–2023 y prueba 2024, luego los ejemplos de fuga.

El riesgo aparece cuando los predictores y el resultado vienen de la misma publicación anual. Por ejemplo, incluir el puntaje de una prueba del mismo ciclo o una diferencia que contiene el promedio global puede producir una evaluación demasiado favorable. El proyecto documentó seis tipos de fuga y excluyó las variables concurrentes del modelado. Los rezagos, tendencias y medidas de variabilidad se construyen usando observaciones anteriores. Para la evaluación externa se reservaron las veintiocho mil setecientas sesenta y dos filas de dos mil veinticuatro. El entrenamiento utiliza los cuatro años previos. Esta separación externa sí está comprobada. La auditoría de preparación también encontró que las divisiones internas del código mezclan años. Por eso, debemos distinguir ese holdout externo de una validación temporal completa, que sigue pendiente de revisión.

Fuente de respaldo: Paper, §3.3–3.4; src/features.py; VERIFICACION_DATOS_MODELOS.json.

## Diapositiva 5 · 03:25–04:10

**Modelos evaluados**

**Señalar:** Señalar las cuatro familias y la diferencia entre filas y secuencias.

Comparamos dos modelos lineales regularizados, Ridge y Lasso, un modelo de árboles con boosting, LightGBM, y un Transformer encoder. Ridge y Lasso funcionan como referencias para valorar cuánto aporta una estructura más flexible. LightGBM se ajustó mediante cincuenta ensayos de búsqueda de hiperparámetros. El artefacto final conservado tiene ciento ochenta y ocho árboles. El Transformer procesa secuencias por entidad y usa una arquitectura de dos capas con cuatro cabezas de atención. Su información de entrada y su número de muestras efectivas difieren de los modelos tabulares. Esa diferencia es importante: estamos comparando las configuraciones realizadas en este proyecto, y no demostrando que una familia sea siempre superior a otra.

Fuente de respaldo: Paper, §3.5 y §5.2; outputs/reports/decision_transformer.txt.

## Diapositiva 6 · 04:10–05:05

**Resultado principal de LightGBM**

**Señalar:** Señalar diagonal, nube central y valores RMSE y R².

Este es el resultado principal sobre el año reservado. En el eje horizontal está el promedio observado y en el vertical, el predicho. La diagonal representa una predicción exacta. La mayor parte de los puntos se concentra cerca de esa línea, aunque aparecen errores mayores hacia los extremos. LightGBM obtuvo un error cuadrático medio, expresado como raíz, de nueve coma treinta y tres puntos. Lo abreviamos como erre eme ese e. El erre al cuadrado fue cero coma setecientos seis. Este último valor compara el error con una predicción constante basada en la media del conjunto evaluado. No significa que acertemos el setenta por ciento de las predicciones. El error absoluto medio fue seis coma veintiún puntos. Los tres valores de LightGBM se verificaron con el modelo guardado.

Fuente de respaldo: Paper, figura 3; outputs/figures/lgbm_predicho_vs_real.png; outputs/metrics/baseline_metrics.csv.

## Diapositiva 7 · 05:05–06:00

**Comparación en el conjunto de prueba 2024**

**Señalar:** Señalar Lasso y LightGBM, luego la fila Transformer.

La tabla conserva los resultados del artículo aceptado. Ridge obtuvo un error de diez coma veintitrés puntos y Lasso, diez coma cero siete. LightGBM reduce ese error a nueve coma treinta y tres. Frente a Lasso, la reducción relativa es de aproximadamente siete coma cuatro por ciento. El Transformer quedó en dieciséis coma ochenta y seis puntos, con un erre al cuadrado cercano a cero coma cero cuatro. En esta configuración no fue competitivo. El reporte registra menos muestras efectivas y ausencia de las variables categóricas que sí reciben los modelos tabulares. Esas diferencias son limitaciones de la comparación y posibles explicaciones, no efectos aislados experimentalmente. Como tenemos un solo año de prueba, tampoco presentamos intervalos de confianza ni una conclusión de superioridad universal.

Fuente de respaldo: Paper, tabla 1; baseline_metrics.csv; decision_transformer.txt. Se conservan MAE aceptados; discrepancias pequeñas en auditoría.

## Diapositiva 8 · 06:00–06:55

**Interpretabilidad mediante SHAP**

**Señalar:** Señalar primera fila SHAP y colores de los rezagos. No interpretar sufijos NBC como códigos disciplinares.

Para entender el comportamiento del modelo usamos SHAP, que podemos pronunciar shap. La figura resume cuánto contribuyen las variables a las predicciones de una muestra del conjunto de prueba. A la derecha están las contribuciones que elevan la predicción y a la izquierda, las que la reducen. El color representa el valor de la variable. La primera fila corresponde al promedio global de la observación anterior disponible y es la de mayor influencia en este resumen. Le siguen el segundo rezago global y el primer rezago de la prueba. Esto muestra que el modelo aprovecha con fuerza el historial. Hay que separar interpretación predictiva de causalidad: la gráfica explica cómo responde el modelo a sus entradas. No demuestra que cambiar una característica produzca por sí solo un cambio en el desempeño académico.

Fuente de respaldo: Paper, figura 4; outputs/figures/lgbm_shap_beeswarm.png; narrativa_lgbm.txt.

## Diapositiva 9 · 06:55–07:45

**Errores y límites de generalización**

**Señalar:** Señalar Sin Clasificar y Educación; acompañar los datos regionales con sus tamaños.

El promedio de error oculta diferencias entre grupos. En el análisis por área, Sin Clasificar presenta un error de diecisiete coma setenta y seis puntos y Educación, de once coma setenta y uno. El análisis regional también muestra variación. Sucre registra trece coma veintinueve puntos, Chocó doce coma cero tres y Putumayo once coma dieciocho. Los tamaños de esos grupos son distintos, de modo que no debemos leer estas cifras como una clasificación de la calidad educativa. Son errores del modelo. Además, el panel solo cubre cinco años, incluye el período de pandemia y no incorpora variables socioeconómicas externas. Estas condiciones limitan la generalización y justifican revisar con cuidado cualquier uso institucional.

Fuente de respaldo: Paper, §4.3 y §5.5; metricas_lgbm_por_nbc.csv; metricas_lgbm_por_depto.csv.

## Diapositiva 10 · 07:45–08:30

**Conclusiones y trabajo futuro**

**Señalar:** Señalar resultado, alcance y validación futura.

En síntesis, LightGBM fue la mejor de las configuraciones evaluadas para predecir el promedio global de Saber Pro en dos mil veinticuatro. El historial contiene señal predictiva útil, y revisar las fugas de información es parte del resultado metodológico. También identificamos los límites de la evidencia: trabajamos con datos agregados, un único año de prueba y diferencias entre las entradas de los modelos. El siguiente paso es evaluar varios cortes temporales, revisar la codificación y la disponibilidad de cada variable, e incorporar información externa cuando esté justificada. Cualquier uso para acompañamiento académico debe validarse con las instituciones. Ese es el alcance que podemos defender con este trabajo. Muchas gracias.

Fuente de respaldo: Paper, §6; auditoría de preparación. No hay despliegue ni estudio causal demostrado.

## Control del ensayo

Texto hablado: 1162 palabras. Duración planificada: 08:30. Grabar una toma completa y anotar desvíos por diapositiva. Objetivo aceptable: 08:00–09:00; máximo comunicado: 10:00, incluyendo portada y cierre.

La frase sobre revisión de validaciones internas debe actualizarse únicamente después de resolver el hallazgo metodológico con evidencia. No ocultar ese pendiente durante la revisión con Nathalia.