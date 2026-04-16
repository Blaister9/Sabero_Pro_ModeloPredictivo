# Arquitectura Técnica — Motor Predictivo Saber Pro

**Versión**: 1.0.0 | **Autor**: Edwin Santiago Paz Bedoya

---

## 1. Diagrama ASCII del Pipeline Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DATOS CRUDOS (5 archivos .xlsx — ~231 MB, ~1.73M filas long-format)        │
│  data/raw/saber_pro_{2020..2024}.xlsx                                       │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ src/ingestion.load_years()
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  FASE 1 — AUDITORÍA        fase1_auditoria.py                               │
│  Entrada: 5 xlsx            Salida: nulidad*.png, auditoria_2024.txt        │
│  Checks: schema, nulidad, cobertura temporal, tipos de MEDIDA_AGREGACION    │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ src/cleaning.clean_dataset()
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  FASE 2 — LIMPIEZA + PIVOT  fase2_limpieza.py                               │
│  Entrada: raw DataFrames    Salida: saber_pro_limpio.csv (127,716 × 24)     │
│                                                                             │
│  Pivot 3 capas:                                                             │
│  ① PUNTAJE_PRUEBA @ PROGRAMA_ACAD  → base wide (PROMEDIO_PRUEBA, DESVIACION)│
│  ② ⊕ inner join PUNTAJE_GLOBAL     → agrega PROMEDIO_GLOBAL (target) ★     │
│  ③ ⊕ left join  NIVEL_DESEMPEÑO    → agrega NIVEL1-4                       │
│                                                                             │
│  Excluido: PERCENTIL_PRUEBA (no disponible a nivel PROGRAMA_ACAD)          │
│  Reglas C1-C5: nulos target, DESVIACION, NIVEL1-4, CATEGORIAPRUEBA OHE     │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ src/features.build_features()
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  FASE 3 — FEATURE ENGINEERING  fase3_features.py                            │
│  Entrada: limpio.csv        Salida: saber_pro_features.csv (127,716 × 41)  │
│                                                                             │
│  Features construidas (sin leakage):                                        │
│  • lag_1/2_promedio_global, lag_1/2_promedio_prueba  → shift(n)             │
│  • tendencia_global/prueba         → expanding OLS sobre historia t-1..t-k  │
│  • desviacion_estandar_historica   → shift(1).expanding(min=2).std()        │
│  • coeficiente_variacion           → std / mean sobre historia              │
│  • log_cantidadevaluados           → log1p(CANTIDADEVALUADOS)               │
│  • cat_prueba_1, cat_prueba_34     → OHE de CATEGORIAPRUEBA                 │
│                                                                             │
│  Columnas concurrent_* (mismo año que target — NO usadas en modelo):        │
│  PROMEDIO_PRUEBA, DESVIACION, concurrent_prop_nivel{1..4}                  │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ split temporal: train ≤ 2023 / test = 2024
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
           TRAIN (98,954)           TEST (28,762)
           2020–2023               2024
                    │
         ┌──────────┼─────────────────────┐
         │          │                     │
         ▼          ▼                     ▼
┌────────────┐ ┌──────────────────┐ ┌────────────────────────────────────────┐
│  FASE 4    │ │    FASE 5        │ │              FASE 6                    │
│  Baseline  │ │    LightGBM      │ │  Transformer Encoder                  │
│            │ │                  │ │                                        │
│  Ridge     │ │  Optuna 50 trial │ │  SaberProSequenceDataset               │
│  RMSE=10.23│ │  + SHAP          │ │  max_seq_len=5, d_model=64             │
│  R²=0.647  │ │                  │ │  nhead=4, layers=2, ffn=128            │
│            │ │  RMSE=9.33  ★    │ │  CPU budget: 20 min                   │
│  Lasso     │ │  R²=0.706   ★    │ │                                        │
│  RMSE=10.07│ │                  │ │  RMSE=16.79                            │
│  R²=0.658  │ │  lgbm_model.pkl  │ │  R²=0.048                             │
└────────────┘ └────────┬─────────┘ └────────────────────────────────────────┘
                        │ modelo final seleccionado
                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  FASE 7 — INFERENCIA  src/inference.py + demo_inference.py                  │
│  load_model() → predict_institution() / predict_batch()                     │
│  Flags: baja_confianza_muestra_pequeña · sin_historial · extrapolacion      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Entrada/Salida de cada bloque:**

| Fase | Entrada | Salida principal | Tamaño |
|---|---|---|---|
| 1 Auditoría | 5 xlsx raw | `auditoria_2024.txt`, 3 figuras | — |
| 2 Limpieza | Raw DataFrames | `saber_pro_limpio.csv` | 127,716 × 24 |
| 3 Features | limpio.csv | `saber_pro_features.csv` | 127,716 × 41 |
| 4 Baseline | features.csv | Ridge/Lasso `.pkl`, métricas | — |
| 5 LightGBM | features.csv | `lgbm_model.pkl`, SHAP figs | 733 KB |
| 6 Transformer | features.csv | `transformer_model.pt` | 288 KB |
| 7 Inferencia | `lgbm_model.pkl` + input row | Dict predicción + flags | — |

---

## 2. Formato de Datos en Cada Etapa

### 2.1 Datos crudos (long-format)

```
Columnas: ID_PAIS, ID_REGION, ..., ID_PROGRAMA_ACAD, NOMBRE_PRUEBA,
          MEDIDA_AGREGACION, CANTIDADEVALUADOS, PUNTAJE, NIVEL_DESEMPEÑO, PERCENTIL
Filas:    ~1.73M (una por AÑO × INSTITUCION × PROGRAMA × PRUEBA × MEDIDA)
Clave:    MEDIDA_AGREGACION ∈ {PUNTAJE_PRUEBA, PUNTAJE_GLOBAL, NIVEL_DESEMPEÑO_PRUEBA, ...}
```

### 2.2 Post-limpieza/pivot (wide-format)

```
Dimensión: 127,716 × 24
Tipos:     int64 (IDs), float64 (puntajes/niveles), object (nombres)
Target:    PROMEDIO_GLOBAL — float64, rango ≈ [80, 200], media ≈ 145
Entidades: 34,319 únicas (ID_INSTITUCION × ID_PROGRAMA_ACAD × NOMBRE_PRUEBA)
Años:      2020–2024 (5 años)
```

### 2.3 Post-features

```
Dimensión: 127,716 × 41 (= 24 originales + 17 features nuevas)
Features nuevas: lag_1/2_global, lag_1/2_prueba (4) + tendencia (2) +
                 volatilidad (2) + log_cant (1) + concurrent_prop_* (6) +
                 cat_prueba_1/34 (2)
NaN esperados:   lag_1 nulo para año 1 de cada entidad (34,319 filas)
                 lag_2 nulo para años 1-2 (63,938 filas)
```

### 2.4 Entrada al Pipeline sklearn (predicción)

```
15 columnas: 10 numéricas + 3 categóricas + 2 OHE
NaN permitido en numéricas → SimpleImputer(strategy="median") las imputa
Categóricas: NBC (str), NOMBRE_PRUEBA (str), ID_DEPARTAMENTO (int/str)
```

---

## 3. Pipeline sklearn — Descripción Técnica

```
Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler",  StandardScaler()),
        ]), NUMERIC_FEATURE_COLS),                    # 10 columnas

        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="constant",
                                      fill_value="DESCONOCIDO")),
            ("encoder", TargetEncoder(smooth="auto", cv=2,
                                      random_state=42)),
        ]), CAT_TARGET_ENCODE_COLS),                  # 3 columnas

        ("ohe", "passthrough", OHE_COLS),             # 2 columnas
    ])),
    ("model", LGBMRegressor(**best_params)),
])
```

**Por qué `TargetEncoder` DENTRO del Pipeline:**

Si se calcula el target encoding fuera del Pipeline (sobre el dataset completo
antes de cualquier split), el encoding del valor de test "ve" los targets de test
durante el fit. Esto es leakage de tipo L1.

Al colocar `TargetEncoder` dentro del Pipeline, sklearn garantiza que durante
`pipeline.fit(X_train, y_train)` el encoder solo ve los pares `(X_train, y_train)`.
El parámetro `cv=2` implementa una validación cruzada interna adicional para
calcular el encoding de las filas de entrenamiento: cada mitad del train se
codifica usando la media del target de la otra mitad. Esto reduce el overfitting
del encoding en datos de entrenamiento.

---

## 4. Decisiones de Diseño Críticas

### 4a. Inner join vs left join para PUNTAJE_GLOBAL

```python
# DECISIÓN: inner join
df_wide = df_prueba.merge(df_global, on=[...], how="inner")
```

**Justificación**: `PUNTAJE_GLOBAL` contiene el `PROMEDIO_GLOBAL` que es la
variable objetivo. Si una fila de `df_prueba` no tiene correspondencia en
`df_global`, el target es Nulo. La regla R1 del pipeline prohíbe imputar el
target. Un left join generaría filas sin target que luego serían eliminadas de
todos modos — el inner join hace esta selección de forma explícita y eficiente.

### 4b. `shift(1).expanding()` vs `expanding()` directo

```python
# INCORRECTO — incluye el valor del año actual t en la std
df["desviacion"] = grp.transform(lambda x: x.expanding(min_periods=2).std())

# CORRECTO — solo usa historia hasta t-1
df["desviacion"] = grp.transform(
    lambda x: x.shift(1).expanding(min_periods=2).std()
)
```

**Justificación**: La métrica de desviación estándar para el año t es un feature
que el modelo usa para predecir `PROMEDIO_GLOBAL(t)`. Si incluye `PROMEDIO_GLOBAL(t)`
en su cálculo, hay leakage directo (leakage L6). `shift(1)` desplaza la serie
una posición hacia adelante, de modo que la fila del año t solo ve historia hasta
t-1. El resultado es idéntico conceptualmente a calcular la std sobre
{t-1, t-2, ...}, pero más eficiente en pandas.

### 4c. Split temporal único vs TimeSeriesSplit completo

```python
# Para evaluación final: split único
df_train = df[df["AÑO"] <= 2023]  # n=98,954
df_test  = df[df["AÑO"] == 2024]  # n=28,762

# TimeSeriesSplit usado SOLO para RidgeCV/LassoCV (búsqueda interna de alpha)
tscv = TimeSeriesSplit(n_splits=4)
```

**Justificación**: El objetivo del paper es evaluar el desempeño en el escenario
de producción real: predecir el año 2024 usando toda la historia disponible
(2020–2023). Un TimeSeriesSplit con 4 folds sacrificaría datos de entrenamiento
valiosos. Se usa solo para la selección de hiperparámetros del Lasso/Ridge dentro
de la función de pérdida, no para la evaluación final.

Para la búsqueda de hiperparámetros de LightGBM se usa un split 80/20
cronológico único (más rápido: ~8s/trial en lugar de ~40s/trial con 4-fold CV).

### 4d. CPU-first en el Transformer

El Transformer se implementó sin llamadas a `.cuda()`. Razón:
1. El entorno de desarrollo es Windows sin GPU compatible.
2. El dataset de secuencias tiene 32,422 muestras — tamaño que no justifica GPU.
3. La restricción de 20 minutos de presupuesto es representativa del costo
   real de producción CPU (el modelo debería ser deployable en cualquier
   máquina estándar del ICFES/MEN).

### 4e. Imputación por mediana agrupada NBC+PRUEBA vs mediana global

```python
# DECISIÓN: mediana agrupada
df[col] = df.groupby(["NBC", "NOMBRE_PRUEBA"])[col].transform(
    lambda x: x.fillna(x.median())
)
# fallback: mediana global si el grupo completo tiene nulos
df[col].fillna(df[col].median(), inplace=True)
```

**Justificación**: Las variables `DESVIACION` y `NIVEL1-4` tienen distribuciones
distintas por área del conocimiento (NBC) y por tipo de prueba. La mediana global
mezcla distribuciones heterogéneas. La mediana agrupada por `NBC + NOMBRE_PRUEBA`
produce una imputación más representativa del contexto del programa.

---

## 5. Catálogo Técnico de los 6 Leakages

### L1 — Target Encoding Global

**Código incorrecto** (computa encoding sobre todo el dataset):
```python
# En features.py — INCORRECTO
from sklearn.preprocessing import TargetEncoder
te = TargetEncoder(smooth="auto")
df["te_nbc"] = te.fit_transform(df[["NBC"]], df["PROMEDIO_GLOBAL"])
# ↑ usa PROMEDIO_GLOBAL del test para calcular el encoding del test
```

**Código correcto** (encoding dentro del Pipeline, solo sobre train):
```python
# En models/baseline.py y models/boosting.py
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import TargetEncoder

te_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
    ("encoder", TargetEncoder(smooth="auto", cv=2, random_state=42)),
])
# pipeline.fit(X_train, y_train) → te_pipe solo ve y_train
```

---

### L2 — Variable Concurrente: PROMEDIO_PRUEBA año t

**Código incorrecto**:
```python
# Feature directa del mismo año que el target
feature_cols = [..., "PROMEDIO_PRUEBA", ...]  # valor del año t — INCORRECTO
```

**Código correcto**:
```python
# Solo el lag del año anterior
feature_cols = [..., "lag_1_promedio_prueba", ...]  # valor del año t-1
# PROMEDIO_PRUEBA del año t se renombra a "concurrent_PROMEDIO_PRUEBA" (no entra al modelo)
```

---

### L3 — Variable Concurrente: DESVIACION año t

**Código incorrecto**:
```python
feature_cols = [..., "DESVIACION", ...]  # std de PUNTAJE_PRUEBA del mismo año — INCORRECTO
```

**Código correcto**:
```python
# Excluida del modelo; renombrada en el CSV como referencia
# df.rename(columns={"DESVIACION": "concurrent_DESVIACION"}, ...)
```

---

### L4 — Variables Concurrentes: NIVEL1-4 año t

**Código incorrecto**:
```python
feature_cols = [..., "NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4", ...]  # INCORRECTO
```

**Código correcto**:
```python
# Renombradas como concurrent_prop_nivel1..4, no incluidas en feature_cols
# Disponibles en el CSV para análisis exploratorio post-hoc
```

---

### L5 — Target Leak Directo: delta_1_global

**Código incorrecto**:
```python
df["delta_1_global"] = df["PROMEDIO_GLOBAL"] - df["lag_1_promedio_global"]
# ↑ PROMEDIO_GLOBAL(t) − lag_1(t-1) = target(t) − constante → contiene el target directamente
feature_cols = [..., "delta_1_global", ...]  # INCORRECTO — leak directo
```

**Código correcto**:
```python
# delta_1_global eliminada completamente
# Si se quiere capturar cambio reciente: usar tendencia_global (expanding OLS sin año t)
```

---

### L6 — Leakage Temporal en Tendencia y Volatilidad

**Código incorrecto** (expanding window incluye año t):
```python
df["tendencia_global"] = (
    df.groupby(ENTITY_COLS)["PROMEDIO_GLOBAL"]
    .transform(lambda x: x.expanding(min_periods=2).apply(_ols_slope))
)
# ↑ para año t, usa historia t, t-1, t-2, ... → incluye target del año t
```

**Código correcto** (shift antes de expanding):
```python
def expanding_slope(group):
    group = group.sort_values("AÑO").reset_index(drop=False)
    slopes = []
    for i in range(len(group)):
        hist = group["PROMEDIO_GLOBAL"].iloc[:i].dropna().values  # solo t-1, t-2...
        slopes.append(_ols_slope(pd.Series(hist)))
    return pd.Series(slopes, index=group.index)

# Volatilidad:
df["desviacion_estandar_historica"] = grp.transform(
    lambda x: x.shift(1).expanding(min_periods=2).std()  # shift(1) excluye año t
)
```

---

## 6. Guía de Extensibilidad

### 6.1 Agregar un Nuevo Año

```
Paso 1: Descargar datos
  → data/raw/saber_pro_2025.xlsx  (estructura idéntica a años previos)

Paso 2: Actualizar main.py
  YEARS = [2020, 2021, 2022, 2023, 2024, 2025]
  TRAIN_YEARS = [2020, 2021, 2022, 2023, 2024]
  TEST_YEAR = 2025

Paso 3: Ejecutar pipeline completo
  python main.py --years 2020 2021 2022 2023 2024 2025
```

El pipeline es automáticamente compatible porque:
- `load_years()` concatena dinámicamente todos los xlsx disponibles
- Los lags y expanding windows se recalculan para el nuevo año
- El TargetEncoder dentro del Pipeline se refit sobre el nuevo train

### 6.2 Agregar un Nuevo Feature — Checklist Anti-Leakage

Antes de agregar cualquier feature nueva, responder **todas** estas preguntas:

```
[ ] 1. ¿La variable usa información del año t (el año que se predice)?
       Si SÍ → es concurrente → no puede usarse como feature del modelo.
       Renombrarla como "concurrent_*" y mantenerla solo en el CSV.

[ ] 2. ¿La variable es una función del target PROMEDIO_GLOBAL del año t?
       Si SÍ → es target leak directo → eliminar completamente.

[ ] 3. Si la variable usa historia expandida (expanding window),
       ¿está usando shift(1) antes del expanding?
       Si NO → agregar shift(1) o usar iloc[:i] en el loop.

[ ] 4. Si la variable es categórica y se va a target-encodear,
       ¿el encoding se calcula dentro del Pipeline?
       Si NO → mover el TargetEncoder al interior del Pipeline.

[ ] 5. ¿Se verificó que el RMSE del baseline (Lasso) no sube más de 0.5
       al quitar la nueva feature del modelo?
       Si el RMSE cae mucho al incluirla → inspeccionar por posible leakage.
```

### 6.3 Cambiar el Modelo Principal

```python
# En src/models/boosting.py o nuevo src/models/mi_modelo.py
def build_mi_modelo_pipeline(params, num_cols, cat_cols, ohe_cols):
    preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)
    return Pipeline([
        ("preprocessor", preprocessor),  # MISMO preprocesador → sin leakage
        ("model", MiModelo(**params)),
    ])

# En fase5_lightgbm.py → reemplazar train_lgbm(...) por train_mi_modelo(...)
```

**Importante**: el `ColumnTransformer` con `TargetEncoder` DEBE mantenerse para
las columnas categóricas, independientemente del modelo que se use en el último
paso.

---

## 7. Vulnerabilidades y Consideraciones de Seguridad

### 7.1 Pickle Injection (severidad: ALTA en producción)

`outputs/lgbm_model.pkl` está serializado con `joblib` (internamente usa pickle).
Cargar un archivo `.pkl` malicioso puede ejecutar código arbitrario.

**Mitigaciones implementadas**:
- El archivo `.pkl` está en `.gitignore` — no se distribuye en el repositorio.
- Distribución recomendada: GitHub Releases con hash SHA256 publicado.
- Verificación recomendada antes de cargar:

```python
import hashlib, joblib

EXPECTED_SHA256 = "abc123..."  # hash del modelo validado

with open("outputs/lgbm_model.pkl", "rb") as f:
    content = f.read()

assert hashlib.sha256(content).hexdigest() == EXPECTED_SHA256, \
    "Model integrity check FAILED — file may be tampered"

model = joblib.load("outputs/lgbm_model.pkl")
```

### 7.2 Datos Personales (GDPR / Ley 1581)

El dataset opera sobre **datos agregados a nivel de programa**, no datos
individuales de estudiantes. Los archivos ICFES no contienen nombres, cédulas
ni ningún identificador personal directo. No aplica tratamiento especial de
datos personales.

### 7.3 Sesgo Geográfico

El modelo tiene mayor error (RMSE > 12) en departamentos con menor
representación en el dataset histórico (ej. Vichada, Guainía). Usar el modelo
para tomar decisiones de acreditación en estos departamentos requiere revisión
manual y considerar los flags de baja confianza.

---

## 8. Limitaciones con Implicaciones Técnicas

| # | Limitación | Implicación técnica | Mitigación posible |
|---|---|---|---|
| L1 | 5 años (incluye COVID 2020-2021) | Distribución train ≠ distribución sin pandemia | Monitoreo de drift anual; re-entrenamiento si MAE > 11 |
| L2 | Granularidad programa-institución | No detecta variabilidad intra-programa | Enriquecer con datos individuales anonimizados si disponibles |
| L3 | Sin variables externas | NBC=EDUCACIÓN tiene RMSE=11.7 (el más alto) | Incorporar índice socioeconómico municipal (DANE Sisbén) |
| L4 | Catálogo de pruebas no estable | Entidades con historial incompleto no por ser nuevas | Trazabilidad de IDs de prueba entre años ICFES |
| L5 | Extrapolación >1 año no validada | R² degrada con horizonte > 1 año | Implementar predicción multi-paso con cuantificación de incertidumbre |
