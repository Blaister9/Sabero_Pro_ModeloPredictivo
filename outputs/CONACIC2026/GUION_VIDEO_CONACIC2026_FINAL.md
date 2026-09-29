# Guion oral final CONACIC 2026

**Presenta:** Edwin Santiago Paz Bedoya. **Coautora:** Nathalia Orozco Morales. UNIMINUTO Virtual – Bogotá, Colombia.

**Duración objetivo: 8:45.** Los tiempos incluyen la transición, pausas breves y cambio de diapositiva. Hablar con ritmo conversado y sin leer títulos, etiquetas o tablas completos. Cada párrafo es una unidad corta de explicación. Las indicaciones entre corchetes no se dicen en voz alta.

Fuente de contenido: `CONAC202617_CANDIDATE.docx`. Presentación: `PRESENTACION_CONACIC2026_FINAL.pptx`.

| Diapositiva | Tiempo | Acumulado |
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

### Diapositiva 1 — Título y autoría

**Tiempo objetivo:** 25 segundos. Acumulado: 0:25.

**Qué debe entender la audiencia:** quién presenta, quiénes realizaron el trabajo y qué se estudió.

**Guion:**

Buenos días. Soy Edwin Santiago Paz Bedoya. Presento este trabajo realizado con Nathalia Orozco Morales, de UNIMINUTO Virtual, en Bogotá.

Estudiamos la predicción del promedio global de Saber Pro a nivel de programa académico, con LightGBM y una auditoría de fuga de información temporal.

**Apoyo visual / dónde señalar:** mantener la portada. No leer el título completo ni señalar cada nombre.

**Transición breve:** Comienzo con el objetivo del estudio.

### Diapositiva 2 — Problema y objetivo

**Tiempo objetivo:** 48 segundos. Acumulado: 1:13.

**Qué debe entender la audiencia:** el objetivo de estimación y la diferencia entre evaluación retrospectiva y uso anticipado.

**Guion:**

Los resultados de Saber Pro se publican varios meses después de la aplicación del examen. Ese desfase motivó el objetivo del trabajo: estimar el promedio global de los programas a partir de la información histórica pública del ICFES.

Trabajamos con resultados agregados. El interés está en el desempeño del programa, no en predecir el puntaje de cada estudiante.

[Pausa breve.]

La evaluación que presentamos es retrospectiva. Un posible uso antes de la publicación oficial depende de que las variables necesarias estén disponibles en ese momento. Por eso, el resultado del estudio debe leerse dentro de ese alcance.

**Apoyo visual / dónde señalar:** primero el bloque «Problema» y después «Objetivo». Mantener el puntero quieto durante la explicación del alcance.

**Transición breve:** Para esta evaluación construimos el siguiente panel de datos.

### Diapositiva 3 — Datos y construcción del panel

**Tiempo objetivo:** 52 segundos. Acumulado: 2:05.

**Qué debe entender la audiencia:** de dónde salen las observaciones y cuál es su unidad de análisis.

**Guion:**

Utilizamos los reportes públicos del ICFES de 2020 a 2024. En los archivos originales, distintas medidas de un programa y una prueba aparecen en filas separadas.

Reorganizamos esas medidas en columnas mediante un pivot. El panel resultante contiene 127.716 observaciones. Cada fila corresponde a una combinación de institución, programa, prueba y año. Ese total no representa estudiantes ni programas únicos.

[Señalar las barras.]

La gráfica muestra cuántas filas hay en cada año. El historial disponible por entidad permite construir los rezagos que usa el modelo. Es información de observaciones anteriores, dentro de un panel cuya cobertura cambia entre años.

**Apoyo visual / dónde señalar:** total superior, bloque de unidad de análisis y barras de 2020 a 2024. No leer los cinco recuentos.

**Transición breve:** Con esos datos pasamos al control de fuga y a la evaluación.

### Diapositiva 4 — Control de fuga y esquema de evaluación

**Tiempo objetivo:** 60 segundos. Acumulado: 3:05.

**Qué debe entender la audiencia:** qué se separó temporalmente y por qué importa la auditoría de fuga.

**Guion:**

Entrenamos con 2020 a 2023: 98.954 filas. Reservamos 2024 como test temporal externo, con 28.762 filas. La separación temporal es externa. Esto no implica una validación interna completamente temporal.

La auditoría documentó seis tipos de fuga. Entre ellos están usar información del puntaje objetivo o de los niveles de desempeño del mismo ciclo. Para la predicción se construyeron rezagos con observaciones anteriores disponibles.

[Pausa breve.]

El artículo reporta que Lasso pasó de un R cuadrado cercano a 0,88 a aproximadamente 0,658 después de las correcciones, una diferencia cercana a 0,22. Es el cambio conjunto reportado en esa comparación, no una mejora de LightGBM.

**Apoyo visual / dónde señalar:** bloque azul de entrenamiento, bloque verde del test y las dos líneas inferiores. El ΔR² se explica oralmente; no aparece como una cifra nueva en pantalla.

**Transición breve:** Con ese esquema evaluamos cuatro modelos.

### Diapositiva 5 — Modelos evaluados

**Tiempo objetivo:** 48 segundos. Acumulado: 3:53.

**Qué debe entender la audiencia:** qué modelos se compararon y el alcance de esa comparación.

**Guion:**

Ridge y Lasso son las referencias lineales. Los dos incorporan regularización: Ridge con penalización L dos y Lasso con L uno.

LightGBM combina árboles mediante boosting. Para su ajuste usamos una búsqueda de cincuenta ensayos con Optuna.

También evaluamos un Transformer encoder, que utiliza atención sobre secuencias históricas por entidad.

[Pausa breve.]

Comparamos las configuraciones del estudio, con diferencias en entradas y muestras efectivas. Por eso, no atribuimos toda la diferencia de desempeño a la arquitectura. Evaluamos cómo se comportó cada configuración en el test de 2024.

**Apoyo visual / dónde señalar:** recorrer los tres bloques. Al final, señalar la línea inferior que delimita la comparación.

**Transición breve:** Primero presento el resultado global de LightGBM.

### Diapositiva 6 — Desempeño global de LightGBM

**Tiempo objetivo:** 62 segundos. Acumulado: 4:55.

**Qué debe entender la audiencia:** cómo leer la dispersión y qué significan las tres métricas del test externo.

**Guion:**

En el test externo de 2024, LightGBM obtuvo un RMSE de 9,33 puntos, un MAE de 6,21 y un R cuadrado de 0,706.

[Señalar los ejes y la diagonal.]

En el eje horizontal está el promedio global real y en el vertical, el predicho. La línea diagonal indica coincidencia perfecta. La distancia a esa línea permite reconocer los errores.

El MAE resume la magnitud media del error absoluto. El RMSE da más peso a los errores grandes. El R cuadrado no es un porcentaje de aciertos.

Según el artículo, los errores más grandes se concentran en los extremos de la distribución. Las métricas resumen el conjunto, con errores diferentes para cada observación.

**Apoyo visual / dónde señalar:** métricas de la derecha, diagonal roja y extremos de la nube. Dejar unos segundos para que la audiencia lea la figura.

**Transición breve:** La siguiente tabla compara ese resultado con los otros modelos.

### Diapositiva 7 — Comparación de modelos

**Tiempo objetivo:** 58 segundos. Acumulado: 5:53.

**Qué debe entender la audiencia:** LightGBM obtuvo el mejor resultado de esta comparación concreta.

**Guion:**

Esta es la comparación en 2024. Ridge y Lasso tuvieron RMSE cercanos a diez puntos. LightGBM obtuvo el menor RMSE y el mayor R cuadrado.

Frente a Lasso, el artículo reporta una reducción del RMSE de 7,4 por ciento.

[Señalar la última fila.]

El Transformer encoder alcanzó un RMSE de 16,86 y un R cuadrado cercano a 0,041. Su MAE aparece como no disponible en la tabla del artículo.

LightGBM fue mejor en este test y con estas configuraciones. El resultado no establece una superioridad universal sobre los Transformers. Para evaluar su estabilidad necesitamos más cortes temporales.

**Apoyo visual / dónde señalar:** fila verde de LightGBM, Lasso como referencia y última fila del Transformer. No leer la tabla celda por celda.

**Transición breve:** Después examinamos qué variables contribuyeron a las predicciones de LightGBM.

### Diapositiva 8 — Interpretabilidad mediante SHAP

**Tiempo objetivo:** 62 segundos. Acumulado: 6:55.

**Qué debe entender la audiencia:** el predominio predictivo del rezago reciente y el alcance no causal de SHAP.

**Guion:**

Usamos SHAP para describir la contribución de las variables a las predicciones del modelo. La primera fila corresponde a lag uno del promedio global, es decir, el rezago más reciente disponible de ese resultado.

[Señalar la primera fila.]

Es la variable con mayor contribución predictiva. Después aparecen el segundo rezago global y el rezago de la prueba.

En el eje horizontal, los valores positivos indican aportes que aumentan la predicción y los negativos, aportes que la disminuyen. El rojo representa valores altos de la variable y el azul, valores bajos.

Esto describe cómo el modelo utiliza la información. No demuestra que el desempeño pasado cause el resultado futuro, ni que modificar una variable produzca un cambio educativo. La lectura es predictiva, no causal.

**Apoyo visual / dónde señalar:** primera fila, dos filas siguientes, eje horizontal y barra de color. No recorrer todas las etiquetas codificadas del gráfico.

**Transición breve:** También revisamos cómo varía el error entre áreas y regiones.

### Diapositiva 9 — Análisis de error y limitaciones

**Tiempo objetivo:** 58 segundos. Acumulado: 7:53.

**Qué debe entender la audiencia:** el error es heterogéneo y existen límites de datos y evaluación.

**Guion:**

A la izquierda está el RMSE por Núcleo Básico del Conocimiento. La longitud de las barras muestra que el error varía entre áreas. Sin Clasificar y Artes Representativas aparecen entre los valores más altos de esta figura.

A la derecha hay otra desagregación, por departamento. El artículo reporta errores aproximados de trece puntos en Sucre, doce en Chocó y once en Putumayo. Son diferencias observadas de error; no permiten concluir que el desarrollo económico sea su causa.

[Pausa breve.]

La evaluación tiene un único año de prueba externo. Además, los datos son agregados y no incluyen variables socioeconómicas externas. Estos límites impiden trasladar automáticamente el desempeño global a cada grupo o a otros años.

**Apoyo visual / dónde señalar:** primeras barras del gráfico, cifras departamentales y bloque de limitaciones. Evitar confundir NBC con departamentos.

**Transición breve:** Con esos resultados y limitaciones cierro las conclusiones.

### Diapositiva 10 — Conclusiones

**Tiempo objetivo:** 52 segundos. Acumulado: 8:45.

**Qué debe entender la audiencia:** resultado principal, precaución en el uso y siguiente paso de validación.

**Guion:**

En esta evaluación retrospectiva, LightGBM alcanzó un RMSE de 9,33 puntos y un R cuadrado de 0,706. El historial del promedio global tuvo la mayor contribución predictiva observada.

El trabajo incluye un módulo de inferencia con flags empíricos de confianza. Son señales sobre las limitaciones de la información disponible para cada predicción. No son intervalos de confianza ni medidas de incertidumbre calibrada.

[Pausa breve.]

Antes de un uso institucional se requiere ampliar la validación temporal y revisar las diferencias entre grupos. El trabajo futuro incluye validación walk-forward con varios cortes, incorporación de variables socioeconómicas y evaluación de equidad.

Muchas gracias por su atención.

**Apoyo visual / dónde señalar:** primera conclusión al mencionar las métricas y línea de trabajo futuro al cerrar. La aclaración de flags es oral; no hace falta añadir texto a la diapositiva.

**Transición breve:** ninguna; mantener la diapositiva final dos segundos después del agradecimiento.

## Control de duración para la grabación

El objetivo de 8:45 deja 1:15 de margen frente al límite de diez minutos. El guion y sus transiciones suman 1.030 palabras escritas, equivalentes aproximadamente a 1.157 al pronunciar cifras y siglas. A 140–145 palabras por minuto, más 40 segundos de pausas y cambios, se estima una duración de **8:39–8:56**. La duración es una estimación editorial, no una medición de audio. El detalle está en `REVISION_VIDEO_FINAL.md`.

Ensayar una vez con cronómetro y la tarjeta de apoyo. Usar como referencias 3:05 al terminar la diapositiva 4 y 6:55 al terminar la 8. Las cifras y nombres técnicos necesitan una dicción tranquila. Las pausas incluyen señalar figuras y cambiar diapositivas.
