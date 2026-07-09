"""Structured content for the revised Saber Pro paper (OPUS47 version).

Consumed by ``scripts/build_paper.py`` to emit a reproducible .docx.
All prose in this module already obeys revision rules R1-R7 of the
STEP 2 rewrite (see ``outputs/reports/cambios_realizados.txt``).

The file is split into four top-level constants:

- ``METADATA``: title, authors, affiliations.
- ``SECTIONS``: an ordered list of section dicts. Each dict has a
  ``kind`` field that the builder dispatches on:
    * ``heading``   — numbered or unnumbered heading.
    * ``paragraph`` — plain prose paragraph.
    * ``bullets``   — bulleted list.
    * ``figure``    — figure placeholder with caption.
    * ``table``     — 2D table with header + rows + caption.
- ``REFERENCES``: ordered list of IEEE-formatted reference strings.
- ``APPENDICES``: reproducibility / software appendix content.

The content was produced under senior-reviewer standards for IEEE
Transactions on Learning Technologies / Computers & Education (Q1).
"""

# ---------------------------------------------------------------------------
# METADATA
# ---------------------------------------------------------------------------

METADATA = {
    "title_es": (
        "Motor Predictivo del Desempeño Académico Agregado en el Examen "
        "Saber Pro: Un Enfoque de Datos de Panel (2020–2024) con LightGBM "
        "e Ingeniería de Features Libre de Fuga"
    ),
    "author": "Edwin Santiago Paz Bedoya",
    "affiliation": (
        "Especialización en Inteligencia Artificial — Código 1071010 | "
        "Proyecto Nodo — Modalidad de Grado | 2025"
    ),
    "repo": "https://github.com/Blaister9/Sabero_Pro_ModeloPredictivo",
}

# ---------------------------------------------------------------------------
# SECTIONS
# ---------------------------------------------------------------------------

# Abstract (Spanish): ~250 words. Structure:
# (1) context + problem   (2 sentences ≤25 words)
# (2) method              (2 sentences)
# (3) results             (2 sentences)
# (4) contribution        (2 sentences)
# (5) availability        (1 sentence)
ABSTRACT_ES = (
    "El examen Saber Pro del ICFES mide la calidad de los programas "
    "universitarios en Colombia, pero el ICFES publica los resultados "
    "meses después de la aplicación. Esta asimetría temporal obliga a las "
    "instituciones a gestionar la calidad de forma reactiva. Este trabajo "
    "construye un motor predictivo del indicador agregado PROMEDIO_GLOBAL "
    "a nivel de programa, entrenado sobre datos de panel 2020–2024 "
    "(1,73 millones de filas). El pipeline pivota los datos nativos en "
    "formato long hacia un esquema wide mediante tres capas de unión, "
    "corrige seis tipos de fuga de información documentados en el paper "
    "y construye 15 features temporales causalmente válidas. El split "
    "temporal estricto entrena en 2020–2023 (n=98 954) y evalúa en 2024 "
    "(n=28 762). Cuatro modelos compiten: Ridge (RMSE=10,23; R²=0,647), "
    "Lasso (RMSE=10,07; R²=0,658), LightGBM con Optuna (RMSE=9,33; "
    "R²=0,706) y un Transformer encoder (RMSE=16,86; R²=0,041). LightGBM "
    "queda como modelo final y supera al mejor baseline en 7,4 % de RMSE. "
    "El catálogo de seis fugas temporales, con impacto conjunto medido "
    "de ΔR²≈0,22, constituye la contribución metodológica principal y es "
    "transferible a otros sistemas de evaluación en panel. El módulo de "
    "inferencia entrega predicciones con tres flags empíricos de "
    "confianza. El código y los artefactos son reproducibles en Python "
    "y residen en GitHub."
)

ABSTRACT_EN = (
    "The Saber Pro exam, administered by ICFES, grades the quality of "
    "Colombian university programs, yet ICFES releases results months "
    "after the test. This lag forces institutions to manage quality "
    "reactively. This paper builds a predictive engine for the program-"
    "level aggregate indicator PROMEDIO_GLOBAL, trained on 2020–2024 "
    "panel data (1.73 million rows). The pipeline pivots the native "
    "long-format files into a wide schema through three join layers, "
    "corrects six types of information leakage documented in the paper, "
    "and engineers 15 causally valid temporal features. A strict "
    "temporal split trains on 2020–2023 (n=98,954) and tests on 2024 "
    "(n=28,762). Four models compete: Ridge (RMSE=10.23; R²=0.647), "
    "Lasso (RMSE=10.07; R²=0.658), LightGBM with Optuna (RMSE=9.33; "
    "R²=0.706), and a Transformer encoder (RMSE=16.86; R²=0.041). "
    "LightGBM wins as the final model and improves the best baseline "
    "by 7.4 % in RMSE. The catalogue of six temporal leakages, with a "
    "measured joint impact of ΔR²≈0.22, is the main methodological "
    "contribution and transfers to other panel evaluation systems. The "
    "inference module delivers predictions with three empirical "
    "confidence flags. The code and artefacts are reproducible in "
    "Python and live on GitHub."
)

INDEX_TERMS_ES = (
    "Saber Pro, ICFES, predicción del desempeño académico, datos de "
    "panel temporales, LightGBM, fuga temporal de información, "
    "ingeniería de features, educación superior en Colombia, Gradient "
    "Boosting, Transformer."
)

# ---------------------------------------------------------------------------
# Build the SECTIONS list
# ---------------------------------------------------------------------------

SECTIONS = []


def _add(kind, **payload):
    SECTIONS.append({"kind": kind, **payload})


# ---- I. INTRODUCCIÓN ------------------------------------------------------
_add("heading", level=1, number="I", text="INTRODUCCIÓN")

_add("paragraph", text=(
    "El examen Saber Pro mide la calidad de los programas de educación "
    "superior universitaria en Colombia. El Instituto Colombiano para la "
    "Evaluación de la Educación (ICFES) lo administra y publica los "
    "resultados agregados en la variable PROMEDIO_GLOBAL. El Ministerio "
    "de Educación Nacional (MEN) usa estos resultados para acreditar "
    "programas, asignar recursos de fomento y comparar instituciones "
    "entre regiones [1], [15]."
))

_add("paragraph", text=(
    "El ICFES entrega los resultados varios meses después de la "
    "aplicación del examen. Esta asimetría temporal impide que las "
    "instituciones identifiquen con antelación los programas en riesgo "
    "de obtener un PROMEDIO_GLOBAL bajo, y obliga a una gestión de "
    "calidad esencialmente reactiva. Un motor que prediga el "
    "PROMEDIO_GLOBAL un año antes habilitaría intervenciones "
    "curriculares proactivas."
))

_add("paragraph", text=(
    "A la fecha no existe un sistema abierto de predicción que opere "
    "sobre los datos públicos del ICFES a nivel de programa "
    "universitario. Este trabajo llena esa brecha y construye un motor "
    "completo, desde la ingesta de los archivos crudos del ICFES hasta "
    "un módulo de inferencia deployable con cuantificación de "
    "incertidumbre."
))

_add("heading", level=2, number="A", text="Contribuciones")
_add("bullets", items=[
    "Documentamos de forma sistemática seis tipos de fuga de información "
    "en datos de evaluación educativa en panel temporal, con impacto "
    "conjunto medido ΔR²≈0,22.",
    "Diseñamos una estrategia de pivot long→wide en tres capas para "
    "datos ICFES, reutilizable en otros reportes agregados del mismo "
    "formato.",
    "Construimos 15 features temporales causalmente válidas para paneles "
    "con cobertura desigual.",
    "Evaluamos cuatro familias de modelos bajo un split temporal "
    "estricto y explicamos cuantitativamente por qué el Transformer no "
    "resulta competitivo en este dominio.",
    "Entregamos un módulo de inferencia con tres flags empíricos de "
    "confianza que distinguen predicciones estables de predicciones "
    "inciertas.",
])


# ---- II. TRABAJOS RELACIONADOS -------------------------------------------
_add("heading", level=1, number="II", text="TRABAJOS RELACIONADOS")

_add("paragraph", text=(
    "La literatura de Educational Data Mining (EDM) predice el "
    "rendimiento académico sobre todo a nivel individual [7], [8]. "
    "El boosting sobre árboles [2], [3] domina la familia de métodos "
    "aplicados en este campo. En "
    "América Latina, varios trabajos recientes abordan exámenes "
    "estandarizados nacionales. Rangel-Mora y Pérez-Roa [16] revisan "
    "sistemáticamente la aplicación de técnicas de minería de datos "
    "sobre las pruebas Saber en Colombia. Un estudio presentado en "
    "EDM 2020 [20] analiza los factores que influyen en el desempeño "
    "de las escuelas secundarias brasileñas con técnicas de minería "
    "de datos. Chafla et al. [21] aplican modelos de machine learning "
    "con explicabilidad para apoyar la toma de decisiones en "
    "educación superior ecuatoriana. Acıslı-Celik y Yesilkanat [22] "
    "predicen el desempeño en ciencias del PISA 2015–2018 con "
    "distintos algoritmos de aprendizaje automático."
))

_add("paragraph", text=(
    "Todos estos trabajos comparten dos limitaciones para nuestro "
    "escenario. Primero, operan a nivel de estudiante individual o a "
    "nivel país-año, no a nivel programa-institución que es la unidad "
    "que toma decisiones curriculares. Segundo, ninguno documenta de "
    "forma sistemática los riesgos de fuga de información que aparecen "
    "cuando el target y los features proceden de la misma publicación "
    "anual. Kaufman et al. [9] ya advierten que la fuga es el defecto "
    "más común y más costoso en minería de datos, pero la literatura "
    "EDM rara vez la audita explícitamente en paneles multianuales. "
    "Este trabajo llena esa brecha metodológica."
))

_add("paragraph", text=(
    "La comparación entre modelos de boosting y redes neuronales sobre "
    "datos tabulares también orienta nuestras decisiones. Grinsztajn "
    "et al. [11] muestran que los árboles superan a los MLP en "
    "datasets tabulares medianos con features categóricas "
    "informativas. Shwartz-Ziv y Armon [12] y Gorishniy et al. [10] "
    "confirman el patrón en benchmarks amplios y señalan que las "
    "redes tabulares requieren millones de muestras efectivas para "
    "cerrar la brecha. Estos "
    "resultados justifican que LightGBM sea nuestro candidato principal "
    "desde el diseño, no como racionalización ex post. El Transformer "
    "se evalúa por completitud y como prueba de hipótesis."
))


# ---- III. DATOS Y METODOLOGÍA --------------------------------------------
_add("heading", level=1, number="III", text="DATOS Y METODOLOGÍA")
_add("heading", level=2, number="A", text="Fuente de Datos")
_add("paragraph", text=(
    "Los datos provienen de los reportes agregados Saber Pro que el "
    "ICFES publica anualmente para el período 2020–2024 [1]. El dataset "
    "crudo consolidado suma 1 730 805 filas distribuidas en cinco "
    "archivos anuales. La Tabla I resume su tamaño. La Fig. 1 muestra "
    "el patrón de nulidad del dataset crudo; el 97,3 % de nulos en "
    "PROMEDIO_GLOBAL refleja la estructura long-format, donde el target "
    "solo aparece en filas PUNTAJE_GLOBAL."
))

_add("table",
     number="I",
     caption="TAMAÑO DEL DATASET CRUDO POR AÑO",
     header=["Año", "Filas"],
     rows=[
         ["2020", "245 234"],
         ["2021", "353 498"],
         ["2022", "406 672"],
         ["2023", "313 455"],
         ["2024", "411 946"],
         ["Total", "1 730 805"],
     ])

_add("figure",
     number=1,
     caption=(
         "Porcentaje de valores nulos por columna en el dataset crudo "
         "2020–2024. El 97,3 % de nulos en PROMEDIO_GLOBAL refleja la "
         "estructura long-format: solo las filas de tipo PUNTAJE_GLOBAL "
         "contienen el target."
     ))

_add("heading", level=2, number="B", text="Formato Long y Estrategia de Pivot")
_add("paragraph", text=(
    "El hallazgo más crítico de la auditoría fue que los archivos del "
    "ICFES usan la columna MEDIDA_AGREGACION para discriminar el tipo "
    "de estadística de cada fila. Identificamos tres capas utilizables: "
    "(a) PUNTAJE_PRUEBA, que contiene el promedio por prueba específica; "
    "(b) PUNTAJE_GLOBAL, que contiene el target PROMEDIO_GLOBAL a nivel "
    "de programa; y (c) NIVEL_DESEMPEÑO_PRUEBA, que contiene las "
    "proporciones por nivel. Excluimos formalmente PERCENTIL_PRUEBA "
    "porque produce NaN en el 100 % de las filas al cruzar por programa "
    "académico."
))

_add("paragraph", text=(
    "Justificación (J1): el pivot aplica inner join entre las tres capas "
    "sobre la llave (AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, "
    "NOMBRE_PRUEBA). El inner join preserva únicamente las entidades con "
    "las tres capas presentes, y así evita que entidades incompletas "
    "contaminen los features temporales con valores imputados espurios. "
    "Un outer join habría inflado N de 127 716 a ~180 000 filas a costa "
    "de introducir NaN estructurales en el target. El pivot produce "
    "127 716 filas wide con el target disponible en el 100 % de las "
    "observaciones."
))

_add("figure",
     number=2,
     caption=(
         "Dataset post-pivot y limpieza. Superior izquierdo: "
         "distribución del PROMEDIO_GLOBAL (media=148,1). Superior "
         "derecho: filas limpias por año. Inferior: top 15 pruebas y "
         "NBCs por frecuencia."
     ))

_add("heading", level=2, number="C", text="Data Leakage: Identificación y Corrección")
_add("paragraph", text=(
    "Durante el desarrollo identificamos seis tipos de fuga, resumidos "
    "en la Tabla II. El baseline Lasso con fugas presentes reportaba "
    "R²≈0,88; el mismo modelo, una vez aplicadas las correcciones, "
    "reporta R²=0,658. La diferencia medida sobre el pipeline completo "
    "es por tanto ΔR²≈0,22."
))

_add("paragraph", text=(
    "El impacto individual de cada fuga no es estrictamente aditivo, "
    "porque L1…L6 comparten varianza explicada y porque aplicamos las "
    "correcciones de forma secuencial durante el diseño. Los impactos "
    "individuales de la Tabla II son estimaciones cualitativas basadas "
    "en la naturaleza de cada variable (L2 es casi una transformación "
    "lineal del target publicada en el mismo release, L5 contiene el "
    "target de forma directa), no en una ablación independiente. Un "
    "estudio de ablación controlada de cada fuga queda como trabajo "
    "metodológico futuro."
))

_add("table",
     number="II",
     caption="DATA LEAKAGE IDENTIFICADO Y CORREGIDO",
     header=["#", "Tipo", "Variable(s)", "Impacto R² (est.)", "Corrección"],
     rows=[
         ["L1", "Target encoding global",
          "te_nbc, te_prueba, te_depto",
          "Alto",
          "TargetEncoder dentro del Pipeline sklearn con cv=2"],
         ["L2", "Variable concurrente: puntaje mismo año",
          "PROMEDIO_PRUEBA (t)",
          "Alto",
          "Eliminado; reemplazado por lag_1_promedio_prueba"],
         ["L3", "Variable concurrente: desviación",
          "DESVIACION (t)",
          "Medio",
          "Excluido; renombrado concurrent_desviacion"],
         ["L4", "Variable concurrente: niveles",
          "NIVEL1–4 (t)",
          "Medio",
          "Excluidos; renombrados concurrent_prop_nivel*"],
         ["L5", "Target leak directo",
          "delta_1_global = GLOB(t)−lag_1",
          "Trivial (R²→1)",
          "Eliminado completamente"],
         ["L6", "Leakage temporal en tendencia y volatilidad",
          "tendencia, desv_hist, CV",
          "Medio",
          "Reescrito con shift(1).expanding()"],
     ])

_add("heading", level=2, number="D", text="Split de Evaluación y Métricas")
_add("paragraph", text=(
    "Justificación (J2): usamos split temporal estricto (train "
    "2020–2023, n=98 954; test 2024, n=28 762) y no validación "
    "cruzada aleatoria. El caso de uso operativo requiere predecir el "
    "año t+1 a partir de la historia t, t-1, t-2, …; un k-fold "
    "aleatorio entrenaría en el futuro y evaluaría en el pasado, lo que "
    "sobreestima la generalización."
))

_add("paragraph", text=(
    "Justificación (J3): imputamos numéricos por mediana agrupada por "
    "(AÑO, NOMBRE_PRUEBA) y no por media. La distribución del "
    "PROMEDIO_GLOBAL tiene cola izquierda pesada por programas "
    "pequeños con puntajes atípicos (ver Sec. VI); la mediana resiste "
    "mejor estos outliers y evita contaminar estadísticas agrupadas."
))

_add("paragraph", text=(
    "Las métricas primarias son RMSE, R² y MAE en el test de 2024. "
    "Reportamos métricas desagregadas por Núcleo Básico del "
    "Conocimiento (NBC) y por departamento."
))


# ---- IV. INGENIERÍA DE FEATURES ------------------------------------------
_add("heading", level=1, number="IV", text="INGENIERÍA DE FEATURES")

_add("heading", level=2, number="A", text="Cobertura Temporal del Panel")
_add("paragraph", text=(
    "La entidad del panel es E = (ID_INSTITUCION, ID_PROGRAMA_ACAD, "
    "NOMBRE_PRUEBA), con 34 319 entidades únicas. La Fig. 3 muestra la "
    "distribución de cobertura: el 48,3 % de las entidades tienen los "
    "cinco años completos y el lag_1 está disponible para el 86,3 % de "
    "las observaciones."
))

_add("figure",
     number=3,
     caption=(
         "Cobertura temporal por entidad. Izquierda: distribución de "
         "entidades por número de años disponibles. Derecha: porcentaje "
         "acumulado con al menos N años de historia."
     ))

_add("heading", level=2, number="B", text="Construcción de Features")
_add("paragraph", text=(
    "El pipeline construye 15 features en cuatro grupos, todas "
    "calculadas con información estrictamente anterior al año t. El "
    "Grupo A (lags) contiene lag_1 y lag_2 de PROMEDIO_GLOBAL y "
    "PROMEDIO_PRUEBA. El Grupo B (tendencia) contiene la pendiente OLS "
    "sobre historia expandida con shift(1).expanding(). El Grupo C "
    "(volatilidad) contiene la desviación estándar histórica y el "
    "coeficiente de variación, ambos con shift(1).expanding(min_periods="
    "2). El Grupo D (contexto) contiene log_cantidadevaluados, AÑO y dos "
    "indicadores OHE (cat_prueba_1, cat_prueba_34). El pipeline codifica "
    "las categóricas de alta cardinalidad (NBC, NOMBRE_PRUEBA, "
    "ID_DEPARTAMENTO) con TargetEncoder dentro del Pipeline sklearn, "
    "con cv=2. Así el encoding se ajusta solo sobre cada fold de "
    "entrenamiento y no filtra información del target global. "
    "Alternativas como los entity embeddings [17] y la similarity "
    "encoding [18] son candidatas naturales para trabajo futuro "
    "sobre las mismas categóricas."
))

_add("paragraph", text=(
    "Transformamos CANTIDAD_EVALUADOS en log_cantidadevaluados porque la "
    "variable es fuertemente asimétrica: el rango va de 1 a varios "
    "miles y la mayoría de programas evalúa entre 10 y 50 estudiantes. "
    "La transformación log estabiliza la escala y evita que programas "
    "masivos dominen la regularización lineal."
))

_add("figure",
     number=4,
     caption=(
         "Correlación de Pearson de los 20 features con mayor "
         "correlación con PROMEDIO_GLOBAL. lag_1 y lag_2 dominan "
         "(r≈0,84). Las variables concurrent_*, excluidas del modelo "
         "por pertenecer al mismo año del target, aparecen solo como "
         "referencia."
     ))


# ---- V. MODELOS ----------------------------------------------------------
_add("heading", level=1, number="V", text="MODELOS Y ESTRATEGIA DE EVALUACIÓN")

_add("heading", level=2, number="A", text="Baselines Lineales: Ridge y Lasso")
_add("paragraph", text=(
    "Ridge y Lasso son los baselines regularizados clásicos para "
    "regresión [19]. Ambos usan el mismo Pipeline de sklearn [13]: "
    "SimpleImputer "
    "por mediana, TargetEncoder con cv=2, StandardScaler y el modelo "
    "lineal. RidgeCV y LassoCV seleccionan el parámetro de "
    "regularización α con TimeSeriesSplit(n_splits=4) interno sobre el "
    "conjunto de entrenamiento."
))

_add("heading", level=2, number="B", text="Modelo Principal: LightGBM")
_add("paragraph", text=(
    "LightGBM [3] es el candidato principal por dos razones. Primero, "
    "las referencias [11] y [12] muestran que los árboles boosting "
    "superan a redes tabulares en datasets medianos con categóricas "
    "informativas, que es exactamente nuestro caso. Segundo, LightGBM "
    "maneja variables categóricas de alta cardinalidad (NBC, "
    "NOMBRE_PRUEBA, ID_DEPARTAMENTO) de forma nativa."
))

_add("paragraph", text=(
    "Justificación (J4): el tuning usa Optuna [4] con 50 trials sobre "
    "TimeSeriesSplit(n_splits=3). Elegimos 50 trials tras verificar "
    "saturación empírica: los cinco mejores trials convergen dentro de "
    "un margen de RMSE<0,05 y el mejor trial aparece antes del "
    "trial 40. Un presupuesto mayor no ofrece ganancia detectable y "
    "duplica el tiempo CPU (~7 min por bloque de 50 trials). Los "
    "hiperparámetros óptimos son learning_rate=0,029, num_leaves=31, "
    "min_child_samples=44, subsample=0,691, colsample_bytree=0,637, "
    "reg_alpha=0,807, reg_lambda=0,637 y n_estimators=500. SHAP "
    "TreeExplainer [6] aporta la interpretabilidad."
))

_add("heading", level=2, number="C", text="Modelo Experimental: Transformer Encoder")
_add("paragraph", text=(
    "El Transformer [5] (implementado con PyTorch [14]) sirve como "
    "prueba de hipótesis, no como "
    "competidor principal. La activación está condicionada a "
    "R²_LightGBM > 0,70 y N_años ≥ 3, y ambos criterios se cumplen. "
    "La arquitectura usa d_model=64, nhead=4, num_layers=2, 70 337 "
    "parámetros y secuencias por entidad de hasta cinco timesteps. El "
    "presupuesto de entrenamiento es de 20 minutos de CPU."
))

_add("paragraph", text=(
    "Justificación (J5): anticipamos que el Transformer no sería "
    "competitivo por cuatro factores, en orden esperado de impacto. "
    "Primero, el tamaño efectivo de muestras es menor, porque el "
    "Transformer entrena sobre 32 422 secuencias frente a 98 954 filas "
    "de LightGBM. Segundo, la versión actual no incorpora features "
    "categóricas (NBC, NOMBRE_PRUEBA), que son los predictores de "
    "mayor importancia SHAP en LightGBM. Tercero, el 51,7 % de las "
    "secuencias requieren padding con ceros, que introduce ruido en el "
    "mecanismo de atención. Cuarto, las entidades nuevas o de baja "
    "frecuencia generalizan peor sin embeddings aprendibles de las "
    "categóricas. La Sec. VII-A cuantifica estos cuatro factores sobre "
    "los resultados observados."
))


# ---- VI. RESULTADOS ------------------------------------------------------
_add("heading", level=1, number="VI", text="RESULTADOS")

_add("heading", level=2, number="A", text="Comparativa Global de Modelos")
_add("paragraph", text=(
    "La Tabla III resume las métricas de los cuatro modelos sobre el "
    "conjunto de test de 2024 (n=28 762)."
))

_add("table",
     number="III",
     caption="COMPARATIVA DE MÉTRICAS EN EL CONJUNTO DE TEST 2024 (N = 28 762)",
     header=["Modelo", "RMSE", "MAE", "R²", "Configuración"],
     rows=[
         ["Ridge (baseline)", "10,2294", "7,2967", "0,6467",
          "α=auto (RidgeCV)"],
         ["Lasso (baseline)", "10,0722", "7,0622", "0,6575",
          "α=auto (LassoCV)"],
         ["LightGBM (propuesto)", "9,3293", "6,2109", "0,7062",
          "Optuna 50 trials, n_est=500"],
         ["Transformer encoder", "16,7917", "n/d", "0,0481",
          "CPU, early stop época 53/200"],
     ])

_add("paragraph", text=(
    "LightGBM supera a Lasso en ΔRMSE=−0,74 puntos (−7,4 %) y en "
    "ΔR²=+0,049, y alcanza el umbral objetivo de R²>0,70. Reportamos "
    "esta mejora sobre un único split temporal (train 2020–2023 → test "
    "2024); un intervalo de confianza sobre la diferencia requeriría "
    "múltiples splits temporales (por ejemplo, walk-forward 2022→2023, "
    "2023→2024), lo cual dejamos como limitación metodológica (ver "
    "L6 en la Sec. VII-B). La Fig. 5 compara el scatter predicho "
    "vs. real de LightGBM y Lasso; la concentración sobre la "
    "diagonal de predicción perfecta es notoriamente mayor en "
    "LightGBM."
))

_add("figure",
     number=5,
     caption=(
         "LightGBM — predicho vs. real en test 2024 (n=28 762). "
         "RMSE=9,33; MAE=6,21; R²=0,706. La línea roja discontinua "
         "marca la predicción perfecta."
     ))

_add("heading", level=2, number="B", text="Importancia de Features — SHAP")
_add("paragraph", text=(
    "La Fig. 6 presenta el análisis SHAP de LightGBM. lag_1_promedio_"
    "global es el predictor dominante: los programas con historial "
    "alto (rojo) reciben valores SHAP positivos grandes, mientras los "
    "programas con historial bajo (azul) reciben valores negativos. El "
    "segundo predictor es lag_2_promedio_global, seguido de lag_1_"
    "promedio_prueba y log_cantidadevaluados. Los indicadores "
    "categóricos (NBC_129.0, NBC_135.0, etc.) aparecen como efectos de "
    "intercepto por área del conocimiento."
))

_add("figure",
     number=6,
     caption=(
         "SHAP Beeswarm — LightGBM (test 2024). Cada punto es una "
         "predicción. El color codifica el valor del feature "
         "(rojo=alto, azul=bajo). lag_1_promedio_global domina con "
         "valores SHAP de hasta +28 puntos."
     ))

_add("heading", level=2, number="C", text="Curva de Aprendizaje y Convergencia")
_add("paragraph", text=(
    "La Fig. 7 muestra la curva de aprendizaje de LightGBM durante la "
    "búsqueda Optuna. El modelo converge en la iteración 168 (best_iter) "
    "con RMSE de validación estabilizado cerca de 9,1 puntos. La brecha "
    "entre train y validación es pequeña y estable, lo que descarta "
    "sobreajuste severo."
))

_add("figure",
     number=7,
     caption=(
         "LightGBM — curva de aprendizaje (train RMSE vs. validación "
         "RMSE por iteración). La línea gris vertical marca la mejor "
         "iteración (168)."
     ))

_add("heading", level=2, number="D", text="Análisis de Errores por Área de Conocimiento")
_add("paragraph", text=(
    "La Tabla IV y la Fig. 8 presentan el RMSE desagregado por NBC. Los "
    "programas de Salud concentran los errores más bajos (4,1 a 6,2), "
    "mientras Educación (11,71) y Sin Clasificar (17,76) concentran los "
    "más altos. La categoría Sin Clasificar agrupa programas sin "
    "clasificación oficial del MEN y funciona como bolsillo categórico "
    "heterogéneo; su alto RMSE refleja esa heterogeneidad y no un fallo "
    "intrínseco del modelo."
))

_add("table",
     number="IV",
     caption=(
         "RMSE DE LIGHTGBM POR NÚCLEO BÁSICO DEL CONOCIMIENTO "
         "(SUBGRUPOS REPRESENTATIVOS, TEST 2024)"
     ),
     header=["NBC", "n", "RMSE", "MAE"],
     rows=[
         ["Formación Militar o Policial", "35", "4,11", "3,30"],
         ["Zootecnia", "138", "4,40", "3,67"],
         ["Arquitectura", "431", "5,24", "4,22"],
         ["Psicología", "834", "5,66", "4,33"],
         ["Medicina", "516", "6,22", "4,74"],
         ["Administración", "4 383", "8,36", "5,70"],
         ["Educación", "3 899", "11,71", "7,79"],
         ["Sin Clasificar", "720", "17,76", "12,24"],
     ])

_add("figure",
     number=8,
     caption=(
         "LightGBM — RMSE por NBC (top 25). Los programas de Salud "
         "presentan los errores más bajos; Educación y Sin Clasificar "
         "concentran los más altos."
     ))

_add("heading", level=2, number="E", text="Análisis Geográfico de Errores")
_add("paragraph", text=(
    "La Fig. 9 presenta el RMSE de LightGBM desagregado por "
    "departamento. Sucre (RMSE≈13), Chocó (≈12) y Putumayo (≈11) "
    "concentran los mayores errores; Huila y Casanare presentan los "
    "menores (≈6). Estos departamentos de mayor error coinciden con "
    "regiones de menor desarrollo económico y mayor heterogeneidad "
    "institucional. Evitamos la interpretación causal: la correlación "
    "observada no prueba causalidad, pero sugiere que incorporar "
    "variables socioeconómicas externas (trabajo futuro TF1) podría "
    "mejorar la predicción en estas regiones."
))

_add("figure",
     number=9,
     caption=(
         "LightGBM — RMSE por departamento (top 25). Los departamentos "
         "con mayor error coinciden con regiones de menor desarrollo "
         "económico y mayor heterogeneidad institucional."
     ))

_add("heading", level=2, number="F", text="Resultados del Transformer Encoder")
_add("paragraph", text=(
    "El Transformer convergió en 53 épocas (≈4,6 min de CPU). La "
    "Fig. 10 compara su comportamiento con el de LightGBM. La curva de "
    "aprendizaje del Transformer (arriba) muestra una brecha de 6,4 "
    "puntos de RMSE entre validación (≈10,4) y test (16,79), que "
    "indica sobreajuste a entidades de validación. El scatter (abajo) "
    "muestra cómo el Transformer colapsa las predicciones hacia la "
    "media (≈150 puntos) y no captura la variabilidad de los "
    "programas con PROMEDIO_GLOBAL bajo o alto."
))

_add("figure",
     number=10,
     caption=(
         "Transformer encoder. Arriba: curva de aprendizaje; la brecha "
         "val (≈10,4) vs. test (16,79) indica generalización "
         "deficiente. Abajo: scatter predicho vs. real en test 2024; "
         "el modelo colapsa predicciones hacia ≈150 puntos."
     ))

_add("heading", level=2, number="G", text="Módulo de Inferencia y Confianza")
_add("paragraph", text=(
    "La Tabla V resume la distribución de flags de confianza sobre las "
    "28 762 predicciones del test de 2024. Las predicciones de "
    "confianza MEDIA (84,4 %) obtienen RMSE≈9,1 frente a RMSE≈11,4 de "
    "confianza BAJA (15,6 %). El diferencial observado de 2,3 puntos "
    "indica que los flags son informativos; no reportamos un intervalo "
    "de confianza formal por la misma razón expuesta para la "
    "comparativa global (único split temporal)."
))

_add("table",
     number="V",
     caption="DISTRIBUCIÓN DE FLAGS DE CONFIANZA EN EL TEST 2024 (N = 28 762)",
     header=["Flag / Categoría", "n", "%"],
     rows=[
         ["baja_confianza_muestra_pequeña (N < 5)", "3 406", "11,84 %"],
         ["baja_confianza_sin_historial (lag_1 = NaN)", "1 897", "6,60 %"],
         ["baja_confianza_extrapolacion (AÑO > max train)",
          "28 762", "100,00 %"],
         ["Confianza MEDIA (solo flag extrapolación)", "24 288", "84,44 %"],
         ["Confianza BAJA (≥ 2 flags)", "4 474", "15,56 %"],
     ])


# ---- VII. DISCUSIÓN ------------------------------------------------------
_add("heading", level=1, number="VII", text="DISCUSIÓN")

_add("heading", level=2, number="A", text="Por Qué LightGBM Supera al Transformer")
_add("paragraph", text=(
    "La brecha observada (R²=0,706 vs. R²=0,048) confirma los cuatro "
    "factores anticipados en la Sec. V-C. Primero, la asimetría de "
    "muestras efectivas: LightGBM entrena sobre 98 954 filas y el "
    "Transformer sobre 32 422 secuencias (ratio 3,05×). Segundo, la "
    "ausencia de features categóricas en el Transformer: NBC y "
    "NOMBRE_PRUEBA son los predictores de mayor importancia SHAP en "
    "LightGBM, y no están disponibles en el Transformer actual sin "
    "embeddings aprendibles adicionales. Tercero, la brecha de 6,4 "
    "puntos de RMSE entre validación y test indica sobreajuste a "
    "entidades de validación. Cuarto, el 51,7 % de secuencias con "
    "padding en ceros degrada el mecanismo de atención, porque el "
    "modelo debe aprender a ignorar tokens nulos sin ayuda de una "
    "máscara categórica rica."
))

_add("paragraph", text=(
    "Estas condiciones replican con precisión el régimen descrito por "
    "Grinsztajn et al. [11] (datasets tabulares medianos, <100 k "
    "muestras, categóricas informativas) y por Shwartz-Ziv y Armon [12] "
    "(MLPs y Transformers requieren millones de muestras efectivas "
    "para cerrar la brecha frente a GBDTs). Nuestros hallazgos son, "
    "por tanto, consistentes con la evidencia previa."
))

_add("heading", level=2, number="B", text="Limitaciones")
_add("bullets", items=[
    "L1 — El período 2020–2024 incluye años atípicos de pandemia "
    "COVID-19, que pueden introducir sesgos irrepetibles en cohortes "
    "futuras.",
    "L2 — La granularidad es agregada a nivel programa-institución; no "
    "se dispone de información individual por estudiante o por sede.",
    "L3 — No se incluyen variables externas socioeconómicas ni "
    "indicadores de calidad docente.",
    "L4 — El catálogo de pruebas cambia entre años, lo que dificulta "
    "la comparación longitudinal estricta.",
    "L5 — La validación cubre solo un horizonte de un año (t→t+1).",
    "L6 — Los intervalos de confianza sobre las diferencias entre "
    "modelos y entre categorías de confianza no se reportan, porque "
    "requieren múltiples splits temporales (walk-forward). Esta "
    "validación queda como trabajo futuro.",
    "L7 — La categoría Sin Clasificar funciona como bolsillo "
    "heterogéneo y requiere un reclasificador previo para ser tratada "
    "como NBC regular.",
])

_add("heading", level=2, number="C", text="Implicaciones para Política Educativa")
_add("paragraph", text=(
    "Con R²=0,706, el sistema explica el 70,6 % de la varianza del "
    "PROMEDIO_GLOBAL un año antes de la publicación del ICFES. Como "
    "referencia trivial, un modelo que siempre predice la media "
    "entrenada alcanza R²=0 por construcción sobre el test; una mejora "
    "de 0,706 sobre ese baseline trivial representa una ganancia "
    "sustancial. Los programas con lag_1 bajo y tendencia negativa se "
    "pueden identificar como de alto riesgo para intervención "
    "curricular anticipada. El análisis de RMSE por departamento "
    "(Fig. 9) indica dónde concentrar la recolección de variables "
    "socioeconómicas externas (trabajo futuro TF1)."
))


# ---- VIII. CONCLUSIONES --------------------------------------------------
_add("heading", level=1, number="VIII", text="CONCLUSIONES Y TRABAJO FUTURO")

_add("heading", level=2, number="A", text="Conclusiones")
_add("paragraph", text=(
    "Este trabajo aporta cinco conclusiones, ordenadas por "
    "transferibilidad metodológica. La contribución principal es C1: "
    "documentar de forma sistemática la fuga de información en paneles "
    "temporales de evaluación educativa."
))

_add("bullets", items=[
    "C1 — La fuga de información en panel temporal es sistémica en "
    "datos de evaluación educativa: seis tipos identificados con "
    "impacto conjunto medido ΔR²≈0,22 sobre un pipeline baseline. "
    "Este catálogo es la contribución metodológica primaria del "
    "trabajo y es transferible a cualquier sistema de evaluación con "
    "cadencia anual y estructura long-format.",
    "C2 — El formato long nativo del ICFES exige una estrategia de "
    "pivot en tres capas (PUNTAJE_PRUEBA, PUNTAJE_GLOBAL, "
    "NIVEL_DESEMPEÑO_PRUEBA) para producir un dataset wide "
    "causalmente limpio.",
    "C3 — LightGBM supera a los baselines lineales en 7,4 % de RMSE. "
    "Los features temporales (lag_1, lag_2) y las categóricas "
    "codificadas con TargetEncoder son los predictores más "
    "importantes por SHAP.",
    "C4 — El Transformer encoder no es competitivo (R²=0,048 frente a "
    "R²=0,706 de LightGBM). Cuatro factores anticipados desde el "
    "diseño explican la brecha: asimetría de muestras efectivas, "
    "ausencia de features categóricas, padding dominante y "
    "sobreajuste a validación.",
    "C5 — Los flags empíricos de confianza son informativos: "
    "RMSE≈9,1 en confianza MEDIA frente a RMSE≈11,4 en confianza "
    "BAJA. Los flags permiten que el módulo de inferencia acompañe "
    "cada predicción con una señal interpretable de incertidumbre.",
])

_add("heading", level=2, number="B", text="Trabajo Futuro")
_add("bullets", items=[
    "TF1 — Incorporar variables externas: Sisbén, gasto por estudiante, "
    "calidad docente e IDH municipal.",
    "TF2 — Extender a predicción multi-horizonte (t+1 y t+2) con lags "
    "recursivos.",
    "TF3 — Dotar al Transformer de embeddings aprendibles para NBC, "
    "NOMBRE_PRUEBA e ID_DEPARTAMENTO, y repetir el experimento.",
    "TF4 — Habilitar fine-tuning anual incremental sin reentrenamiento "
    "completo.",
    "TF5 — Realizar análisis de equidad por región y por modalidad "
    "(presencial / virtual).",
    "TF6 — Ejecutar validación walk-forward multi-split (2022→2023, "
    "2023→2024, …) para reportar intervalos de confianza formales "
    "sobre las diferencias entre modelos y entre categorías de "
    "confianza.",
    "TF7 — Desplegar un API REST (FastAPI + Docker) con batch "
    "prediction y monitoreo de data drift.",
])


# ---- ACKNOWLEDGMENTS -----------------------------------------------------
_add("heading", level=1, number="IX", text="AGRADECIMIENTOS")
_add("paragraph", text=(
    "El autor agradece al ICFES por la publicación abierta de los "
    "microdatos agregados de Saber Pro 2020–2024, y a los revisores "
    "anónimos por los comentarios constructivos sobre el manejo de "
    "fuga de información en panel temporal."
))


# ---------------------------------------------------------------------------
# REFERENCES (IEEE format, [1] to [22])
# ---------------------------------------------------------------------------
REFERENCES = [
    # [1]
    "ICFES, “Resultados Saber Pro 2020–2024,” Instituto Colombiano para "
    "la Evaluación de la Educación, Bogotá, Colombia, 2024. [Online]. "
    "Available: https://www.icfes.gov.co/resultados/saber-pro-resultados",
    # [2]
    "T. Chen and C. Guestrin, “XGBoost: A scalable tree boosting "
    "system,” in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data "
    "Min., 2016, pp. 785–794, doi: 10.1145/2939672.2939785.",
    # [3]
    "G. Ke et al., “LightGBM: A highly efficient gradient boosting "
    "decision tree,” in Adv. Neural Inf. Process. Syst., vol. 30, "
    "2017, pp. 3146–3154.",
    # [4]
    "T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, “Optuna: A "
    "next-generation hyperparameter optimization framework,” in Proc. "
    "25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min., 2019, "
    "pp. 2623–2631, doi: 10.1145/3292500.3330701.",
    # [5]
    "A. Vaswani et al., “Attention is all you need,” in Adv. Neural "
    "Inf. Process. Syst., vol. 30, 2017, pp. 5998–6008.",
    # [6]
    "S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting "
    "model predictions,” in Adv. Neural Inf. Process. Syst., vol. 30, "
    "2017, pp. 4765–4774.",
    # [7]
    "C. Romero and S. Ventura, “Educational data mining: A review of "
    "the state of the art,” IEEE Trans. Syst., Man, Cybern. C, "
    "Appl. Rev., vol. 40, no. 6, pp. 601–618, Nov. 2010, "
    "doi: 10.1109/TSMCC.2010.2053532.",
    # [8]
    "J. Behr, M. Giese, H. K. Teguim Kamdjou, and K. Theiler, "
    "“Early prediction of university dropouts — A random forest "
    "approach,” J. Educ. Comput. Res., vol. 60, no. 5, "
    "pp. 1109–1148, 2022.",
    # [9]
    "S. Kaufman, S. Rosset, and C. Perlich, “Leakage in data mining: "
    "Formulation, detection, and avoidance,” ACM Trans. Knowl. "
    "Discov. Data, vol. 6, no. 4, pp. 1–21, Dec. 2012, "
    "doi: 10.1145/2382577.2382579.",
    # [10]
    "Y. Gorishniy, I. Rubachev, V. Khrulkov, and A. Babenko, "
    "“Revisiting deep learning models for tabular data,” in Adv. "
    "Neural Inf. Process. Syst., vol. 34, 2021, pp. 18932–18943.",
    # [11]
    "L. Grinsztajn, E. Oyallon, and G. Varoquaux, “Why do tree-based "
    "models still outperform deep learning on typical tabular data?,” "
    "in Adv. Neural Inf. Process. Syst., vol. 35, 2022, pp. 507–520.",
    # [12]
    "R. Shwartz-Ziv and A. Armon, “Tabular data: Deep learning is not "
    "all you need,” Inf. Fusion, vol. 81, pp. 84–90, May 2022, "
    "doi: 10.1016/j.inffus.2021.11.011.",
    # [13]
    "F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” "
    "J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.",
    # [14]
    "A. Paszke et al., “PyTorch: An imperative style, high-performance "
    "deep learning library,” in Adv. Neural Inf. Process. Syst., "
    "vol. 32, 2019, pp. 8024–8035.",
    # [15]
    "Ministerio de Educación Nacional de Colombia, “Lineamientos "
    "SACES — Sistema de Aseguramiento de la Calidad de la Educación "
    "Superior,” MEN, Bogotá, Colombia, 2023.",
    # [16]
    "J. C. Rangel-Mora and A. Pérez-Roa, “Predicción del rendimiento "
    "en pruebas Saber mediante minería de datos,” Rev. Colomb. Educ., "
    "no. 82, pp. 1–24, 2021.",
    # [17]
    "C. Guo and F. Berkhahn, “Entity embeddings of categorical "
    "variables,” 2016, arXiv:1604.06737.",
    # [18]
    "P. Cerda, G. Varoquaux, and B. Kégl, “Similarity encoding for "
    "learning with dirty categorical variables,” Mach. Learn., "
    "vol. 107, no. 8–10, pp. 1477–1494, 2018.",
    # [19]
    "T. Hastie, R. Tibshirani, and J. Friedman, The Elements of "
    "Statistical Learning, 2nd ed. New York, NY, USA: Springer, 2009.",
    # [20]
    "Anonymous, “Where to aim? Factors that influence the performance "
    "of Brazilian secondary schools,” in Proc. 13th Int. Conf. "
    "Educational Data Mining (EDM), A. N. Rafferty, J. Whitehill, "
    "V. Cavalli-Sforza, and C. Romero, Eds., 2020, pp. 545–549. "
    "[Online]. Available: https://educationaldatamining.org/files/"
    "conferences/EDM2020/papers/paper_55.pdf",
    # [21]
    "D. Chafla, M. Morocho, and J. Ortega, “Machine learning models "
    "for academic performance prediction with explainability for "
    "enhanced decision-making in Ecuadorian higher education,” "
    "Frontiers in Education, vol. 10, 2025, "
    "doi: 10.3389/feduc.2025.1632315.",
    # [22]
    "S. Acıslı-Celik and C. M. Yesilkanat, “Predicting science "
    "achievement scores with machine learning algorithms: a case "
    "study of OECD PISA 2015–2018 data,” Neural Computing and "
    "Applications, vol. 35, pp. 21201–21228, 2023, "
    "doi: 10.1007/s00521-023-08901-6.",
]


# ---------------------------------------------------------------------------
# APPENDIX A — Reproducibility (moved from old Sec. VIII)
# ---------------------------------------------------------------------------
APPENDICES = [
    {
        "title": "APÉNDICE A — ARQUITECTURA Y REPRODUCIBILIDAD",
        "paragraphs": [
            (
                "El motor predictivo es un sistema modular en Python "
                "3.10+ organizado en ocho módulos funcionales. Cuatro "
                "módulos cubren datos: src/ingestion.py (carga "
                "multianual), src/cleaning.py (pivot de tres capas y "
                "reglas C1–C5), src/features.py (15 features sin "
                "fugas) y src/evaluation.py (métricas y figuras). "
                "Tres módulos cubren modelos: src/models/baseline.py "
                "(Ridge y Lasso), src/models/boosting.py (LightGBM + "
                "Optuna + SHAP) y src/models/transformer.py "
                "(Transformer condicional). El octavo módulo, "
                "src/inference.py, expone predict_institution, "
                "predict_batch y los flags de confianza. Los módulos "
                "intercambian archivos CSV intermedios en "
                "data/processed/, lo que garantiza reproducibilidad "
                "parcial por fase."
            ),
            (
                "El pipeline completo se reproduce con "
                "`python main.py --years 2020 2021 2022 2023 2024`. El "
                "tiempo total es de aproximadamente 15 minutos en un CPU "
                "de referencia (Intel i7-12700H, 32 GB RAM, sin GPU). El "
                "código fuente, la documentación y los artefactos están "
                "disponibles en "
                "https://github.com/Blaister9/Sabero_Pro_ModeloPredictivo. "
                "Los datos raw y los modelos serializados no se versionan "
                "por tamaño y seguridad; se regeneran desde las fases "
                "documentadas. Para agregar datos de un nuevo año (p. ej., "
                "2025) se debe parametrizar el split temporal y los scripts "
                "de fase antes de publicar nuevas métricas."
            ),
        ],
    },
]
