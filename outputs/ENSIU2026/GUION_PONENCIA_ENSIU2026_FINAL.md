# Guion final ENSIU 2026

**Anticipar para Incluir: Inteligencia Artificial al Servicio de la Equidad Educativa**

Autores: Edwin Santiago Paz Bedoya y Nathalia Orozco Morales. UNIMINUTO Virtual, Bogotá, Colombia. Edwin: Especialización en Inteligencia Artificial, código 1071010.

## Uso y duración

La versión A acompaña las diez diapositivas adaptadas y sirve para ensayo o una exposición con apoyo visual autorizada por la organización. Su objetivo editorial es **9 minutos**, aproximadamente 8:30–9:30 según ritmo y pausas. No corresponde al formato general de los términos ENSIU.

Los términos oficiales establecen **5 minutos STA sin apoyo audiovisual y 1 minuto de video R**. La versión B de este archivo está preparada para ese formato. El audiovisual existente se conserva. Confirmar con Nathalia si la sesión permite proyectar el PPTX solicitado; no asumir una excepción por disponer de él.

Las cifras están transcritas de la presentación científica final. Las instrucciones entre corchetes no se pronuncian. Las duraciones son estimaciones de lectura, no mediciones de una grabación. El texto oral A contiene 1.088 palabras separadas por espacios; el STA de B, incluida su transición al video, contiene 525. Las cifras principales ya están escritas como se pronuncian. Las siglas, las pausas y los cambios de diapositiva añaden tiempo, por lo que conviene ensayar con cronómetro.

## Versión A: exposición con las diez diapositivas

| Diapositiva | Tiempo de referencia | Acumulado | STAR |
| --- | --- | --- | --- |
| 1. Portada | 0:25 | 0:25 | Presentación |
| 2. Problema y objetivo | 0:50 | 1:15 | S y T |
| 3. Datos y construcción del panel | 0:50 | 2:05 | A |
| 4. Control de fuga y evaluación | 1:00 | 3:05 | A |
| 5. Modelos evaluados | 0:45 | 3:50 | A |
| 6. Desempeño global | 1:05 | 4:55 | R |
| 7. Comparación de modelos | 0:50 | 5:45 | R |
| 8. SHAP | 1:00 | 6:45 | R |
| 9. Error y limitaciones | 1:15 | 8:00 | R |
| 10. Conclusiones | 1:00 | 9:00 | R |

### 1. Portada

**Texto oral**

Buenos días. Soy Edwin Santiago Paz Bedoya, de la Especialización en Inteligencia Artificial de UNIMINUTO Virtual. Presento el trabajo realizado con Nathalia Orozco Morales: Anticipar para Incluir. Estudiamos cómo estimar el desempeño agregado de los programas en Saber Pro y cómo examinar las diferencias del error entre territorios, en el marco de la Misión cuatro.

**Apoyo:** mantener la portada, sin leer el código del programa.

### 2. Problema y objetivo

**Texto oral**

Los resultados de Saber Pro se publican meses después de la aplicación. Ese desfase motiva el objetivo: estimar el promedio global de un programa usando su información histórica pública del ICFES.

El trabajo se vincula con Datos para la equidad y con la sistematización de información territorial. Queremos examinar dónde una estimación funciona mejor y dónde exige más cautela.

La evaluación es retrospectiva. Un uso anticipado requiere comprobar que todas las variables estén disponibles en el momento de predecir. Estudiamos resultados agregados de programas, no puntajes individuales ni una intervención educativa ya validada.

**Apoyo:** señalar problema, objetivo y línea de equidad.

### 3. Datos y construcción del panel

**Texto oral**

Utilizamos reportes públicos del ICFES de dos mil veinte a dos mil veinticuatro. Reorganizamos las medidas que venían en filas separadas para reunirlas en columnas comparables. El panel contiene ciento veintisiete mil setecientas dieciséis observaciones agregadas.

Cada fila combina institución, programa, prueba y año. El total no equivale a estudiantes ni a programas únicos. Las barras muestran la cantidad de observaciones de cada año.

El historial de cada entidad permite construir los rezagos: valores de observaciones anteriores disponibles. Como la cobertura cambia, un rezago no necesariamente corresponde al año calendario inmediatamente anterior. Esta precisión importa al interpretar el modelo.

**Apoyo:** total, barras y unidad de análisis, sin leer todas las etiquetas.

### 4. Control de fuga y esquema de evaluación

**Texto oral**

Entrenamos con los años dos mil veinte a dos mil veintitrés, que reúnen noventa y ocho mil novecientas cincuenta y cuatro observaciones. Reservamos dos mil veinticuatro como test externo, con veintiocho mil setecientas sesenta y dos.

La fuga de información ocurre cuando el modelo recibe una pista que no tendría al hacer una predicción real. Por ejemplo, usar puntajes o niveles de desempeño del mismo ciclo que queremos anticipar puede producir una evaluación demasiado favorable.

La auditoría identificó seis tipos de fuga. Se excluyeron esas variables contemporáneas y se construyeron rezagos con observaciones previas. La separación del test es temporal y externa; esto no demuestra que todos los pasos de validación interna sean completamente temporales. Ese alcance forma parte de las limitaciones.

**Apoyo:** bloques de entrenamiento y prueba, y dos controles inferiores.

### 5. Modelos evaluados

**Texto oral**

Comparamos cuatro modelos. Ridge y Lasso son regresiones lineales que restringen la complejidad para reducir el sobreajuste.

LightGBM combina árboles de decisión, de modo que los nuevos árboles corrigen errores del conjunto anterior. Ajustamos su configuración mediante cincuenta ensayos con Optuna.

El Transformer utiliza atención sobre secuencias históricas: aprende a dar distinto peso a sus componentes.

Las configuraciones comparadas tienen diferencias de entradas y de muestras efectivas. Por eso, la comparación describe lo que ocurrió en este estudio. No permite atribuir toda diferencia a la arquitectura ni afirmar que un modelo siempre será superior.

**Apoyo:** recorrer los tres bloques y la cautela inferior.

### 6. Desempeño global de LightGBM

**Texto oral**

En el test externo de dos mil veinticuatro, LightGBM obtuvo un RMSE de nueve coma treinta y tres puntos, un MAE de seis coma veintiuno y un R cuadrado de cero coma setecientos seis.

La gráfica compara el valor real, en el eje horizontal, con el predicho, en el vertical. Cuanto más cerca está un punto de la diagonal, menor es su error.

El MAE promedia las distancias absolutas entre predicción y resultado. El RMSE eleva los errores al cuadrado, los promedia y toma la raíz. Así da más peso a los errores grandes y se expresa en puntos del puntaje.

R cuadrado compara el error cuadrático del modelo con el de una referencia basada en el promedio observado. No es porcentaje de aciertos. Ninguna de estas medidas garantiza un error máximo para cada predicción.

**Apoyo:** diagonal y métricas. Pronunciar las cifras despacio.

### 7. Comparación de modelos

**Texto oral**

En la tabla, Ridge tiene un RMSE cercano a diez coma veintitrés puntos y Lasso, a diez coma cero siete. LightGBM presenta nueve coma treinta y tres, el menor valor de esta comparación.

El Transformer alcanzó dieciséis coma ochenta y seis. Su MAE figura como no disponible en la tabla científica que estamos presentando.

Un RMSE menor indica menos error bajo esta medida. LightGBM obtuvo también el mayor R cuadrado, pero esta ventaja corresponde al test de dos mil veinticuatro y a las configuraciones evaluadas. Necesitamos otros cortes temporales para examinar si el resultado se mantiene.

**Apoyo:** fila destacada y columna RMSE. No leer los cuatro decimales.

### 8. Interpretabilidad mediante SHAP

**Texto oral**

Usamos SHAP, que podemos pronunciar “shap”, para describir cuánto contribuye cada variable a una predicción del modelo, respecto de una referencia.

Los rezagos históricos concentran gran parte de la señal predictiva. Destacan el resultado global previo más reciente, el segundo rezago global y el rezago de la prueba.

En la figura, hacia la derecha aparecen contribuciones que aumentan la predicción y hacia la izquierda, contribuciones que la reducen. Los colores distinguen valores altos y bajos de la variable.

Esta lectura explica cómo el modelo utiliza la información. No demuestra que una variable cause el resultado educativo, ni que modificarla produzca una mejora. La utilidad de SHAP aquí es describir el comportamiento predictivo y sus límites.

**Apoyo:** primeras tres filas, eje horizontal y advertencia no causal.

### 9. Análisis de error y limitaciones

**Texto oral**

Esta diapositiva reúne dos desagregaciones. La figura izquierda muestra el error por Núcleo Básico del Conocimiento, es decir, por áreas de formación. Las cifras de la derecha corresponden a departamentos. Son análisis distintos.

En Sucre el RMSE es de aproximadamente trece puntos; en Chocó, doce; y en Putumayo, once. El error territorial resume las diferencias entre predicciones y resultados dentro de cada grupo.

Estas diferencias son descriptivas. No demuestran que el desarrollo económico cause más error ni que el modelo haya probado brechas socioeconómicas. Tampoco bastan para decidir por sí solas qué programa necesita una intervención.

Su relación con la equidad consiste en reconocer que la calidad predictiva no es uniforme y que debe revisarse antes de apoyar decisiones. Tenemos un solo año de prueba externa y datos agregados sin covariables socioeconómicas. Hace falta mejorar la información y contrastar cualquier uso con el contexto de cada territorio.

**Apoyo:** distinguir expresamente gráfico NBC y cifras departamentales.

### 10. Conclusiones

**Texto oral**

LightGBM alcanzó un RMSE de nueve coma treinta y tres y un R cuadrado de cero coma setecientos seis en el test de dos mil veinticuatro. Los rezagos históricos aportaron la mayor señal predictiva observada.

El trabajo incluye un módulo de inferencia con indicadores empíricos de confianza, llamados flags. Son señales de cautela sobre la información disponible. No son intervalos de confianza calibrados.

Antes de un uso institucional necesitamos evaluar otros períodos y revisar las diferencias entre grupos. La validación walk-forward significa repetir la evaluación avanzando el corte temporal. También se requieren mejores datos y una evaluación institucional con enfoque de equidad territorial.

El aporte actual es una base predictiva evaluada y una descripción de sus límites. El impacto del acompañamiento o de una intervención curricular sigue pendiente de comprobación. Muchas gracias.

**Apoyo:** las tres conclusiones y la frase de trabajo futuro.

## Versión B: formato oficial STA oral y video R

**Objetivo:** terminar la exposición oral en 4:40–5:00, a un ritmo conversado de aproximadamente 125–135 palabras por minuto, con pausas breves. Después, reproducir el audiovisual R de 60 segundos. No proyectar el deck durante STA salvo instrucción específica de la organización que modifique los términos publicados.

### S. Situación, referencia 0:00–1:05

**Texto oral STA**

Buenos días. Soy Edwin Santiago Paz Bedoya, de UNIMINUTO Virtual. Presento, junto con Nathalia Orozco Morales, el trabajo Anticipar para Incluir, sobre inteligencia artificial y equidad educativa.

Los resultados de Saber Pro se publican meses después de su aplicación. Ese desfase motivó el estudio de una estimación basada en el historial público de los programas. La pregunta de investigación es hasta dónde esa información permite anticipar su desempeño agregado.

El trabajo se inscribe en la Misión cuatro, Inteligencia Artificial para la equidad, en la línea Datos para la equidad y su conexión con la sistematización de información territorial. Esta orientación exige revisar si una estimación tiene la misma calidad en distintos grupos antes de utilizarla para apoyar decisiones.

### T. Tarea, referencia 1:05–1:50

**Texto oral STA**

Nos propusimos construir y evaluar un modelo del promedio global de Saber Pro a nivel de programa académico, usando los reportes abiertos del ICFES. La hipótesis fue que el historial contiene información útil para estimar un resultado posterior.

La evaluación es retrospectiva. No estimamos puntajes individuales ni probamos una intervención curricular. Un uso antes de la publicación oficial requiere verificar que las variables necesarias estén disponibles en ese momento. También planteamos examinar qué variables utiliza el modelo y cómo cambia su error entre áreas de formación y departamentos.

### A. Acción, referencia 1:50–4:45

**Texto oral STA**

Consolidamos los reportes de dos mil veinte a dos mil veinticuatro en un panel de ciento veintisiete mil setecientas dieciséis observaciones agregadas. Cada fila corresponde a institución, programa, prueba y año. No representa a un estudiante ni a un programa único.

Separamos el entrenamiento, de dos mil veinte a dos mil veintitrés, de la prueba externa de dos mil veinticuatro. Así examinamos el desempeño en un período posterior. Esta separación externa no equivale a una validación interna totalmente temporal.

Auditamos la fuga de información. Una fuga aparece cuando el modelo recibe una pista que no tendría al predecir, como un puntaje del mismo ciclo que pretende anticipar. Excluimos información contemporánea del objetivo y construimos rezagos, que son valores de observaciones anteriores disponibles.

Comparamos Ridge y Lasso, dos modelos lineales que restringen su complejidad; LightGBM, que combina árboles de decisión; y un Transformer, que utiliza atención sobre secuencias históricas. La comparación reconoce diferencias en las entradas y las muestras efectivas de las configuraciones.

Evaluamos el error con tres medidas. El MAE promedia la distancia absoluta entre predicción y resultado. El RMSE da más peso a los errores grandes y se expresa en puntos del puntaje. R cuadrado compara el error cuadrático con una referencia basada en el promedio observado. No es un porcentaje de aciertos.

Además, usamos SHAP para describir la contribución de las variables a las predicciones. Esta explicación del modelo no demuestra causalidad. Desagregamos el error por áreas de formación y por departamento para revisar diferencias que un promedio nacional puede ocultar.

La lectura territorial se mantiene descriptiva. No atribuye el error al desarrollo económico ni demuestra por sí sola una brecha socioeconómica. Antes de orientar una decisión institucional se necesitan otros períodos de evaluación, mejores datos y revisión del contexto local.

### Transición a R, referencia 4:45–5:00

**Texto oral STA**

El siguiente audiovisual resume los resultados de esta evaluación y su posible relación con el acompañamiento institucional. Esa aplicación es una posibilidad que todavía necesita validación.

### R. Resultado, 5:00–6:00

Reproducir **`AUDIOVISUAL_ENSIU2026_FINAL_YOUTUBE.mp4`**, ya existente en esta carpeta, de 60,000 s según su verificación archivada. No narrar encima. No sustituir el clip por las diez diapositivas. La voz definitiva existente dura 53,247771 s y el cierre visual completa el minuto, según `README_ENTREGA.md` y los archivos de verificación previos. Esos archivos no se editaron.

## Pronunciación y respuestas breves para preguntas

- **RMSE:** “erre, eme, ese, e”, o “raíz del error cuadrático medio”. No decir “margen de error”.
- **MAE:** “eme, a, e”, o “error absoluto medio”.
- **R²:** “erre al cuadrado”. Cero coma setecientos seis no significa setenta coma seis por ciento de aciertos.
- **Rezago:** valor de una observación anterior disponible; puede haber huecos entre años.
- **SHAP:** “shap”. Describe contribuciones del modelo, sin demostrar causas educativas.
- **Error territorial:** error de predicción calculado dentro de un departamento. Es distinto del puntaje educativo del territorio y de una medición de desigualdad socioeconómica.
- **Equidad:** aquí orienta la revisión del desempeño por grupos y el diseño de una evaluación futura. No es un efecto de intervención ya medido.
- **Flags:** señales empíricas de cautela, no intervalos calibrados ni probabilidades garantizadas.

## Confirmaciones pendientes para el ensayo definitivo

La agenda pública sitúa a Nathalia y el semillero coincidente en el bloque 4, el 2 de octubre, 11:10 a. m.–12:00 m., virtual. No identifica el título ni a Edwin. Confirmar con Nathalia la correspondencia de esa fila, quién presenta, el turno individual y si se autoriza el apoyo visual. La adaptación de diez slides queda disponible sin afirmar que ese formato sustituya los términos oficiales.
