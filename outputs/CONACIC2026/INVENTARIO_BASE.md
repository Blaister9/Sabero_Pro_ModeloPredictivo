# Inventario de la base aceptada

Base: `entrega_congreso\Saber_pro_paper_CONGRESO_10P_FINAL.docx`
SHA-256: `5657e9af580c1c555c32128930b7c98cbeb3358cbdd511cd1b7f7ab706db7bcb`

Transcripción para auditoría. No constituye otro artículo.

**P0** Predicción del PROMEDIO_GLOBAL de Saber Pro mediante LightGBM y auditoría de fuga temporal: un estudio a nivel de programa académico en Colombia

**P2** Predicting Saber Pro PROMEDIO_GLOBAL with LightGBM and temporal leakage auditing: a program-level study in Colombia

**P3** Edwin Santiago Paz Bedoya

**P4** UNIMINUTO, Bogotá, Colombia.

**P6** Abstract

**P7** This paper presents a full predictive pipeline for the Saber Pro PROMEDIO_GLOBAL at the academic program level in Colombia, trained on public ICFES data for 2020–2024 (127,716 post-pivot observations). A temporal leakage catalog of six leakage types (ΔR²≈ 0.22) is documented as the primary methodological contribution. LightGBM achieves R² = 0.706 and RMSE = 9.33, outperforming Ridge, Lasso and a Transformer encoder. SHAP analysis confirms that institutional inertia (lag_1_promedio_global) is the dominant predictor. A deployable inference module with three empirical confidence flags is delivered. Results enable proactive curricular intervention before ICFES official publication.

**P8** Resumen

**P9** El presente trabajo construye un motor predictivo completo del PROMEDIO_GLOBAL de Saber Pro a nivel de programa académico en Colombia, entrenado sobre datos públicos del ICFES para el período 2020–2024 (127,716 observaciones post-pivot). Se documenta un catálogo de seis tipos de fuga de información (ΔR²≈ 0,22) como contribución metodológica principal. LightGBM alcanza R² = 0,706 y RMSE = 9,33, superando a Ridge, Lasso y un Transformer encoder. El análisis SHAP confirma que la inercia institucional (lag_1_promedio_global) es el predictor dominante. Se entrega un módulo de inferencia deployable con tres flags empíricos de confianza. Los resultados habilitan intervención curricular proactiva antes de la publicación oficial del ICFES.

**P10** Palabras clave: Saber Pro, predicción del rendimiento académico, LightGBM, fuga de información, SHAP, panel temporal, educación superior colombiana.

**P11** 1 Introducción

**P12** El examen Saber Pro mide la calidad de los programas de educación superior universitaria en Colombia. El examen evalúa cinco módulos genéricos (Lectura Crítica, Razonamiento Cuantitativo, Competencias Ciudadanas, Comunicación Escrita e Inglés) y módulos específicos según el Núcleo Básico del Conocimiento (NBC) del programa; cada módulo se califica con el modelo de Rasch [23] en una escala de 0 a 300 puntos, y el PROMEDIO_GLOBAL del estudiante es el promedio de esos módulos. El Instituto Colombiano para la Evaluación de la Educación (ICFES) lo administra y publica los resultados agregados por programa en esa misma variable. El Ministerio de Educación Nacional (MEN) usa estos resultados para acreditar programas, asignar recursos de fomento y comparar instituciones entre regiones [1], [15].

**P13** El ICFES entrega los resultados varios meses después de la aplicación del examen. Esta asimetría temporal impide que las instituciones identifiquen con antelación los programas en riesgo de obtener un PROMEDIO_GLOBAL bajo, y obliga a una gestión de calidad esencialmente reactiva.

**P14** A la fecha no existe un sistema abierto de predicción que opere sobre los datos públicos del ICFES a nivel de programa universitario. El presente trabajo llena esa brecha y construye un motor completo, desde la ingesta de los archivos crudos del ICFES hasta un módulo de inferencia deployable con cuantificación de incertidumbre. El objetivo es diseñar, entrenar y evaluar un motor predictivo del PROMEDIO_GLOBAL a nivel de programa académico, capaz de anticipar el resultado de la próxima aplicación de Saber Pro a partir de su historial de resultados, y de cuantificar la incertidumbre asociada a cada predicción mediante flags de confianza.

**P15** Las contribuciones son las siguientes. Se documentan seis tipos de fuga de información en datos de evaluación educativa en panel temporal, con impacto conjunto medido ΔR²≈ 0,22; este catálogo es transferible a otros sistemas de evaluación con cadencia anual. Se diseña una estrategia de pivot long→wide en tres capas para datos ICFES. Se construyen 15 features temporales causalmente válidas para paneles con cobertura desigual. Se evalúan cuatro familias de modelos bajo un split temporal estricto y se explica cuantitativamente por qué el Transformer no resulta competitivo. Se entrega un módulo de inferencia con tres flags empíricos de confianza. El resto del documento se organiza así: la Sección 2 revisa los trabajos relacionados y el marco teórico; la Sección 3 describe los datos y la metodología; la Sección 4 presenta los resultados; la Sección 5 discute los hallazgos; la Sección 6 presenta las conclusiones y trabajo futuro.

**P16** 2 Marco Teórico y Trabajos Relacionados

**P17** 2.1 El Examen Saber Pro y el Modelo de Rasch

**P18** El ICFES administra Saber Pro como instrumento de aseguramiento de calidad de la educación superior colombiana, y el MEN incorpora sus resultados en los lineamientos del SACES [1], [15]. Cada módulo se califica con el modelo de Rasch [23], un modelo psicométrico de la teoría de respuesta al ítem que estima conjuntamente la habilidad del evaluado y la dificultad del ítem sobre una escala común, lo que permite comparar resultados entre aplicaciones con cuadernillos distintos. El PROMEDIO_GLOBAL publicado por programa es un agregado de puntajes Rasch individuales, no un simple conteo de aciertos, lo que explica su comportamiento aproximadamente continuo y respalda su tratamiento como variable de regresión.

**P19** 2.2 Minería de Datos Educativa y Trabajos Relacionados

**P20** La literatura de Educational Data Mining (EDM) predice el rendimiento académico sobre todo a nivel individual [7], [8]. El boosting sobre árboles [2], [3] domina los métodos aplicados. En América Latina, Rangel-Mora y Pérez-Roa [16] revisan sistemáticamente técnicas de minería sobre pruebas Saber en Colombia; Chafla et al. [21] aplican ML con explicabilidad en educación superior ecuatoriana; Acıslı-Celik y Yesilkanat [22] predicen desempeño en PISA 2015–2018. Todos estos trabajos operan a nivel de estudiante individual o de país-año, no a nivel programa-institución, brecha que motiva el presente trabajo.

**P21** 2.3 Fuga de Información en Paneles Temporales

**P22** Ninguno de los trabajos anteriores documenta sistemáticamente los riesgos de fuga cuando el target y los features proceden de la misma publicación anual. Kaufman et al. [9] advierten que la fuga es el defecto más común y costoso en minería de datos, pero la literatura EDM rara vez la audita explícitamente en paneles multianuales.

**P23** 2.4 Modelos de Aprendizaje Supervisado para Datos Tabulares

**P24** Ridge [24] y Lasso [25] son métodos de regresión regularizada (norma L2 y L1) que controlan el sobreajuste en presencia de variables correlacionadas. LightGBM [3] implementa boosting con particionamiento por hojas y manejo nativo de variables categóricas. El Transformer [5] aplica mecanismos de atención y se ha adaptado a datos tabulares. Grinsztajn et al. [11] muestran que los árboles superan a los MLP en datasets tabulares medianos con features categóricas informativas; Shwartz-Ziv y Armon [12] y Gorishniy et al. [10] confirman el patrón en benchmarks amplios. SHAP [6] es un método de interpretabilidad basado en teoría de juegos cooperativos que descompone cada predicción en contribuciones por feature.

**P25** 3 Datos y Metodología

**P26** 3.1 Fuente de Datos

**P27** Los datos provienen de los reportes agregados Saber Pro que el ICFES publica anualmente para el período 2020–2024 [1], distribuidos como un archivo abierto independiente por cada año de aplicación. El dataset crudo consolidado suma 1.730.805 filas distribuidas en cinco archivos anuales; cada fila corresponde a una combinación de programa académico, prueba específica y tipo de medida estadística, no a un programa individual, lo que produce una estructura long-format. El 97,3 % de nulos en PROMEDIO_GLOBAL refleja esa estructura, donde el target solo aparece en filas de tipo PUNTAJE_GLOBAL.

**P28** 3.2 Formato Long y Estrategia de Pivot

**P29** Los archivos ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo de estadística de cada fila. Se identificaron tres capas utilizables: (a) PUNTAJE_PRUEBA, promedio por prueba; (b) PUNTAJE_GLOBAL, target PROMEDIO_GLOBAL; y (c) NIVEL_DESEMPEÑO_PRUEBA, proporciones por nivel. Se aplicó un pivot long→wide con inner join sobre la llave (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA), preservando únicamente entidades con las tres capas presentes. El resultado es 127.716 filas wide con el target disponible al 100 %.  La Figura 1 ilustra la distribución del PROMEDIO_GLOBAL resultante, el crecimiento de filas limpias por año y las pruebas y NBCs más frecuentes del panel.

**P30** 3.3 Detección y Corrección de Fuga de Información

**P31** Se identificaron seis tipos de fuga (L1–L6) con impacto conjunto ΔR² ≈ 0,22. El baseline Lasso con fugas presentes reportaba R² ≈ 0,88; tras las correcciones, R² = 0,658. Las fugas incluyen: uso de PROMEDIO_GLOBAL del año corriente como feature, fuga a través de proporciones de nivel de desempeño calculadas con el target, y uso de percentiles del mismo ciclo.

**P34** Figura 1. Dataset Saber Pro post-pivot y limpieza. Superior izquierdo: distribución del PROMEDIO_GLOBAL (media = 148,1). Superior derecho: filas limpias por año (2020–2024). Inferior: top 15 pruebas y NBCs por frecuencia.

**P35** 3.4 Ingeniería de Features

**P36** Se construyeron 15 features causalmente válidas: rezagos temporales lag_1 y lag_2 del PROMEDIO_GLOBAL y de cada prueba, tendencia histórica, desviación estándar histórica, logaritmo del número de evaluados, año, identificadores de NBC y departamento codificados con TargetEncoder. El split temporal estricto usa 2020–2023 para entrenamiento (98.954 filas) y 2024 para prueba (28.762 filas).

**P37** 3.5 Modelos Evaluados

**P38** Finalmente se evaluaron cuatro familias: (1) Ridge con α automático (RidgeCV); (2) Lasso con α automático (LassoCV); (3) LightGBM con 50 trials de búsqueda Optuna [4] y n_estimators = 500; (4) Transformer encoder con early stopping (época 53/200). Las métricas de evaluación son RMSE, MAE y R². La interpretabilidad del modelo final se obtiene con SHAP [6].

**P39** 4 Resultados

**P40** 4.1 Comparativa Global de Modelos

**P41** El crecimiento de filas crudas por año, especialmente el salto a 411.946 filas en 2024, se traduce en 127.716 filas wide tras el pivot y el split temporal (n = 28.762), confirmando que la mayor cobertura institucional reciente no introdujo distorsiones sistemáticas en la distribución del target. La Tabla 1 presenta las métricas de desempeño de los cuatro modelos evaluados sobre el conjunto de prueba 2024.

**P42** Tabla 1. Comparativa de métricas en el conjunto de prueba 2024 (n = 28.762)

**P43** LightGBM supera a Lasso en ΔRMSE = −0,74 puntos (−7,4 %) y ΔR² = +0,049, alcanzando el umbral objetivo R² > 0,70. Esta mejora se reporta sobre un único split temporal; un intervalo de confianza formal requiere múltiples splits walk-forward (trabajo futuro TF6). Para verificar que el modelo no incurre en sobreajuste, la Figura 2 muestra la evolución del RMSE de entrenamiento y validación a lo largo de las 225 iteraciones de boosting. Ambas curvas convergen en la iteración 168 con una brecha pequeña y estable, lo que confirma una regularización adecuada.

**P45** Figura 2. LightGBM — Curva de aprendizaje (RMSE de entrenamiento y validación por iteración). La línea vertical marca la mejor iteración (168). La brecha pequeña y estable confirma regularización adecuada.

**P46** El diagrama de dispersión entre los valores predichos y reales del PROMEDIO_GLOBAL (Figura 3) confirma el desempeño de LightGBM sobre el conjunto de prueba 2024 (n = 28.762): los puntos se agrupan densamente sobre la diagonal de predicción perfecta (R² = 0,706), con los errores más grandes concentrados en los extremos de la distribución, donde los programas presentan cohortes pequeñas o trayectorias históricas poco estables.

**P49** Figura 3. LightGBM — Predicho vs. Real en el conjunto de prueba 2024 (n = 28.762). RMSE = 9,33; MAE = 6,21; R² = 0,706. Los errores más grandes se concentran en los extremos de la distribución.

**P50** 4.2 Importancia de Features — SHAP

**P51** El análisis SHAP (Figura 4) revela que lag_1_promedio_global es el predictor dominante, con valores SHAP de hasta +28 puntos. Le siguen lag_2_promedio_global, lag_1_promedio_prueba y log_cantidadevaluados. Los indicadores NBC aparecen como efectos de intercepto por área disciplinar. La variable log_cantidadevaluados muestra que programas con cohortes pequeñas tienen SHAP negativo, reflejando mayor volatilidad en el promedio histórico.

**P53** Figura 4. LightGBM — SHAP Beeswarm (test 2024). lag_1_promedio_global domina con valores SHAP de hasta +28 puntos. El color codifica el valor del feature (rojo = alto, azul = bajo). Los rezagos temporales del PROMEDIO_GLOBAL dominan ampliamente sobre el resto de predictores.

**P55** 4.3 Análisis de Errores por Área y Región

**P56** La Figura 5 desagrega el RMSE de LightGBM por Núcleo Básico del Conocimiento (top 25), revelando diferencias sustanciales entre áreas disciplinares. Los programas de Salud concentran los errores más bajos (RMSE entre 4,1 y 6,2 puntos), mientras que Educación (RMSE = 11,71) y Sin Clasificar (RMSE = 17,76) concentran los más altos, explicados por la alta heterogeneidad interna de esas categorías. El análisis geográfico complementario muestra que Sucre (≈ 13), Chocó (≈ 12) y Putumayo (≈ 11) presentan los mayores errores, coincidiendo con regiones de menor desarrollo económico relativo.

**P58** Figura 5. LightGBM — RMSE por Núcleo Básico del Conocimiento (top 25). Sin Clasificar y Artes Representativas concentran los errores más altos por alta heterogeneidad interna.

**P59** 4.4 Módulo de Inferencia y Confianza

**P60** Las predicciones de confianza MEDIA (84,4 %) obtienen RMSE aprox. 9,1 frente a RMSE aprox. 11,4 de confianza BAJA (15,6 %). El diferencial de 2,3 puntos confirma que los tres flags empíricos son informativos y permiten priorizar alertas institucionales según nivel de certeza. Para contrastar con LightGBM, el Transformer encoder exhibe una brecha considerable entre validación (aprox. 10,4 puntos RMSE) y test (16,86), lo que evidencia sobreajuste y generalización deficiente al conjunto de prueba 2024.

**P61** 5 Discusión

**P62** 5.1 Inercia Institucional como Predictor Dominante

**P63** El patrón SHAP es consistente con la inercia institucional documentada en EDM: Romero y Ventura [7] identifican que el desempeño académico pasado es el predictor más robusto del desempeño futuro, y Behr et al. [8] confirman este hallazgo en predicción de abandono universitario. Los programas tienden a mantener su nivel relativo de desempeño entre ciclos, lo que justifica que el historial de PROMEDIO_GLOBAL sea suficiente para alcanzar R² = 0,706 sin variables de proceso internas.

**P64** 5.2 Por Qué LightGBM Supera al Transformer

**P65** La brecha (R² = 0,706 vs. 0,041) confirma cuatro factores estructurales: asimetría de muestras efectivas (ratio 3,05×), ausencia de features categóricas aprendibles en el Transformer, brecha val/test de 6,4 puntos por sobreajuste, y 51,7 % de secuencias con padding. Estas condiciones replican el régimen descrito por Grinsztajn et al. [11] y Shwartz-Ziv y Armon [12].

**P66** 5.3 Contribución Metodológica: Catálogo de Fugas

**P67** La documentación de seis tipos de fuga con ΔR² ≈ 0,22 llena un vacío metodológico identificado por Kaufman et al. [9]. La revisión de Rangel-Mora y Pérez-Roa [16], Chafla et al. [21] y Acıslı-Celik y Yesilkanat [22] confirma que ningún trabajo previo audita sistemáticamente fugas en paneles con publicación anual. El catálogo es transferible a PISA y otros exámenes de estado latinoamericanos.

**P68** 5.4 Implicaciones para Política Educativa

**P69** El SACES colombiano incorpora Saber Pro como insumo central para registro calificado y acreditación [15]. Un sistema que anticipe el PROMEDIO_GLOBAL un año antes transforma la gestión de calidad de reactiva a proactiva. Esta lógica es análoga a la propuesta por López-García et al. [26] para detección de fracaso estudiantil en la Universidad Industrial de Santander, aunque el presente trabajo opera a nivel programa-institución, complementándola. Los NBC con SHAP negativo y los departamentos con mayor RMSE señalan prioridades concretas de intervención y de recoleción de datos socioeconómicos externos.

**P70** 5.5 Limitaciones

**P71** L1: el período 2020–2024 incluye años atípicos de pandemia. L2: granularidad agregada a nivel programa-institución, sin datos individuales [7], [8]. L3: no se incluyen variables socioeconómicas externas [26]. L4: el catálogo de pruebas cambia entre años. L5: validación de un único horizonte (t→t+1). L6: sin intervalos de confianza formales por ausencia de walk-forward [9]. L7: la categoría Sin Clasificar requiere reclasificador previo.

**P72** 6 Conclusiones y Trabajo Futuro

**P73** 6.1 Conclusiones

**P74** El presente trabajo demuestra que es posible predecir el PROMEDIO_GLOBAL de Saber Pro a nivel de programa académico con un año de anticipación, alcanzando R² = 0,706 y RMSE = 9,33 puntos sobre el conjunto de prueba 2024, a partir exclusivamente de datos públicos del ICFES. Este resultado valida que la inercia institucional capturada por los rezagos temporales contiene suficiente señal para habilitar una gestión curricular proactiva.

**P75** La contribución metodológica más relevante es la documentación sistemática de seis tipos de fuga de información con impacto conjunto ΔR² ≈ 0,22, inédita en la literatura EDM para datos de exámenes de estado con estructura long-format y publicación anual. La comparación entre modelos confirma que LightGBM supera a los baselines lineales en 7,4 % de RMSE, y que el Transformer no resulta competitivo por cuatro factores estructurales consistentes con la evidencia de [11] y [12]. El módulo de inferencia entrega flags de confianza informativos con un diferencial de 2,3 puntos de RMSE entre categorías. Para reproducibilidad, el repositorio documenta la ejecución desde los CSVs procesados y los artefactos regenerables.

**P76** 6.2 Trabajo Futuro

**P77** Seis líneas de extensión se identifican como prioritarias. TF1: incorporar variables socioeconómicas externas (Sisbén, IDH municipal, gasto por estudiante) para reducir el error en departamentos como Sucre, Chocó y Putumayo. TF2: extender a predicción multi-horizonte (t+1 y t+2) para ampliar la ventana de intervención curricular. TF3: dotar al Transformer de embeddings aprendibles para NBC y NOMBRE_PRUEBA y repetir el experimento bajo las mismas condiciones. TF4: habilitar fine-tuning anual incremental sin reentrenamiento completo. TF5: realizar análisis formal de equidad por región y modalidad antes de cualquier despliegue institucional. TF6: ejecutar validación walk-forward multi-split para reportar intervalos de confianza formales sobre las diferencias entre modelos.

**P78** Agradecimientos

**P79** Los autores agradecen al ICFES por la publicación abierta de los microdatos agregados de Saber Pro 2020–2024.

**P80** Referencias

**P81** [1] ICFES, “Resultados Saber Pro 2020–2024,” Instituto Colombiano para la Evaluación de la Educación, Bogotá, Colombia, 2024.

**P82** [2] T. Chen y C. Guestrin, “XGBoost: A scalable tree boosting system,” en Proc. 22nd ACM SIGKDD, 2016, pp. 785–794.

**P83** [3] G. Ke et al., “LightGBM: A highly efficient gradient boosting decision tree,” en Adv. Neural Inf. Process. Syst., vol. 30, 2017.

**P84** [4] T. Akiba et al., “Optuna: A next-generation hyperparameter optimization framework,” en Proc. 25th ACM SIGKDD, 2019.

**P85** [5] A. Vaswani et al., “Attention is all you need,” en Adv. Neural Inf. Process. Syst., vol. 30, 2017.

**P86** [6] S. M. Lundberg y S.-I. Lee, “A unified approach to interpreting model predictions,” en Adv. Neural Inf. Process. Syst., vol. 30, 2017.

**P87** [7] C. Romero y S. Ventura, “Educational data mining: A review of the state of the art,” IEEE Trans. Syst., Man, Cybern. C, vol. 40, n.º 6, pp. 601–618, 2010.

**P88** [8] J. Behr et al., “Early prediction of university dropouts — A random forest approach,” J. Educ. Comput. Res., vol. 60, n.º 5, pp. 1109–1148, 2022.

**P89** [9] S. Kaufman, S. Rosset y C. Perlich, “Leakage in data mining: Formulation, detection, and avoidance,” ACM Trans. Knowl. Discov. Data, vol. 6, n.º 4, 2012.

**P90** [10] Y. Gorishniy et al., “Revisiting deep learning models for tabular data,” en Adv. Neural Inf. Process. Syst., vol. 34, 2021.

**P91** [11] L. Grinsztajn, E. Oyallon y G. Varoquaux, “Why do tree-based models still outperform deep learning on typical tabular data?,” en Adv. Neural Inf. Process. Syst., vol. 35, 2022.

**P92** [12] R. Shwartz-Ziv y A. Armon, “Tabular data: Deep learning is not all you need,” Inf. Fusion, vol. 81, pp. 84–90, 2022.

**P93** [13] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.

**P94** [14] A. Paszke et al., “PyTorch: An imperative style, high-performance deep learning library,” en Adv. Neural Inf. Process. Syst., vol. 32, 2019.

**P95** [15] Ministerio de Educación Nacional, “Lineamientos SACES,” MEN, Bogotá, Colombia, 2023.

**P96** [16] J. C. Rangel-Mora y A. Pérez-Roa, “Predicción del rendimiento en pruebas Saber mediante minería de datos: revisión sistemática,” Rev. Colomb. Educ., n.º 82, 2021.

**P97** [17] C. Guo y F. Berkhahn, “Entity embeddings of categorical variables,” arXiv:1604.06737, 2016.

**P98** [18] P. Cerda, G. Varoquaux y B. Kégl, “Similarity encoding for learning with dirty categorical variables,” Mach. Learn., vol. 107, 2018.

**P99** [19] T. Hastie, R. Tibshirani y J. Friedman, The Elements of Statistical Learning, 2.ª ed. Springer, 2009.

**P100** [20] Anónimo, “Where to aim? Factors that influence the performance of Brazilian secondary schools,” en Proc. EDM, 2020.

**P101** [21] D. Chafla, M. Morocho y J. Ortega, “Machine learning models for academic performance prediction with explainability,” Frontiers in Education, vol. 10, 2025.

**P102** [22] S. Acıslı-Celik y C. M. Yesilkanat, “Predicting science achievement scores with ML: PISA 2015–2018,” Neural Comput. Appl., vol. 35, 2023.

**P103** [23] G. Rasch, “An item analysis which takes individual differences into account,” British J. Math. Stat. Psychol., vol. 19, n.º 1, pp. 49–57, 1966.

**P104** [24] A. E. Hoerl y R. W. Kennard, “Ridge regression: Biased estimation for nonorthogonal problems,” Technometrics, vol. 12, n.º 1, pp. 55–67, 1970.

**P105** [25] R. Tibshirani, “Regression shrinkage and selection via the lasso,” J. Royal Stat. Soc. B, vol. 58, n.º 1, pp. 267–288, 1996.

**P106** [26] A. López-García et al., “Early detection of students’ failure using machine learning techniques,” Operations Research Perspectives, vol. 11, 2023.

## Tabla 1
Modelo | RMSE | MAE | R² | Config.
Ridge (ref.) | 10,2294 | 7,2967 | 0,6467 | RidgeCV
Lasso (ref.) | 10,0722 | 7,0622 | 0,6575 | LassoCV
LightGBM (prop.) | 9,3293 | 6,2109 | 0,7062 | Optuna 50t
Transformer enc. | 16,8588 | n/d | 0,0405 | early stop ép.53
