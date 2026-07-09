# Guía de Reproducibilidad — Motor Predictivo Saber Pro

**Versión**: 1.0.0 | **Autor**: Edwin Santiago Paz Bedoya

Esta guía permite reproducir los resultados del pipeline en una máquina limpia.
La ruta completa desde datos crudos requiere los Excel ICFES en `data/raw/`; si
solo se usan los CSVs procesados versionados, la ruta mínima validada reproduce
modelos y métricas desde `data/processed/saber_pro_features.csv`.

---

## 1. Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|---|---|---|
| Sistema operativo | Windows 10 / Ubuntu 20.04 / macOS 12 | Windows 11 / Ubuntu 22.04 |
| Python | 3.10 | 3.11 o 3.12 |
| RAM | 8 GB | 16 GB |
| Disco libre | 2 GB | 4 GB |
| CPU | 4 núcleos | 8+ núcleos (búsqueda Optuna ~2× más rápida) |
| GPU | No requerida | No requerida (CPU-only) |

> **Nota**: El Transformer se entrena en CPU. Con 4 núcleos la Fase 6 toma
> ~5–8 minutos hasta convergencia por early stopping. Con el presupuesto de
> 20 minutos siempre converge antes.

---

## 2. Instalación del Entorno

### 2.1 Clonar el repositorio

```bash
git clone https://github.com/Blaister9/Sabero_Pro_ModeloPredictivo.git
cd Sabero_Pro_ModeloPredictivo
```

### 2.2 Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

Si PyTorch no instala correctamente (entornos corporativos con proxy):

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 2.4 Verificar instalación

```bash
python -c "
import pandas, numpy, sklearn, lightgbm, shap, optuna, torch
print('pandas:     ', pandas.__version__)
print('numpy:      ', numpy.__version__)
print('sklearn:    ', sklearn.__version__)
print('lightgbm:   ', lightgbm.__version__)
print('shap:       ', shap.__version__)
print('optuna:     ', optuna.__version__)
print('torch:      ', torch.__version__)
print('Todos los modulos OK')
"
```

**Salida esperada** (versiones exactas pueden variar dentro del mismo major):
```
pandas:      2.3.3
numpy:       2.3.5
sklearn:     1.8.0
lightgbm:    4.6.0
shap:        0.51.0
optuna:      4.8.0
torch:       2.11.0+cpu
Todos los modulos OK
```

---

## 3. Descarga de Datos ICFES

Los archivos de datos crudos no están en el repositorio por su tamaño (~231 MB).
Deben descargarse manualmente del portal del ICFES.

### 3.1 URL de descarga

```
https://www.icfes.gov.co/resultados/saber-pro-resultados
```

Sección: **"Bases de datos de resultados agregados por programa académico e institución"**

### 3.2 Qué descargar

Descargar el archivo de cada año en formato **Excel (.xlsx)**:

| Año | Nombre original (puede variar) | Renombrar a |
|---|---|---|
| 2020 | `SB_PRO_2020_...xlsx` o similar | `saber_pro_2020.xlsx` |
| 2021 | `SB_PRO_2021_...xlsx` | `saber_pro_2021.xlsx` |
| 2022 | `SB_PRO_2022_...xlsx` | `saber_pro_2022.xlsx` |
| 2023 | `SB_PRO_2023_...xlsx` | `saber_pro_2023.xlsx` |
| 2024 | `SB_PRO_2024_...xlsx` | `saber_pro_2024.xlsx` |

### 3.3 Ubicar los archivos

```bash
# Crear directorio si no existe
mkdir -p data/raw

# Copiar/mover los archivos descargados
# Resultado final esperado:
ls data/raw/
# saber_pro_2020.xlsx
# saber_pro_2021.xlsx
# saber_pro_2022.xlsx
# saber_pro_2023.xlsx
# saber_pro_2024.xlsx
```

### 3.4 Verificación previa de los archivos

El script de auditoría verifica automáticamente la estructura. Para una
verificación manual rápida:

```python
import pandas as pd

for year in [2020, 2021, 2022, 2023, 2024]:
    df = pd.read_excel(f"data/raw/saber_pro_{year}.xlsx", nrows=5)
    expected_cols = ["ID_PAIS", "ID_INSTITUCION", "ID_PROGRAMA_ACAD",
                     "NOMBRE_PRUEBA", "MEDIDA_AGREGACION", "CANTIDADEVALUADOS"]
    missing = [c for c in expected_cols if c not in df.columns]
    print(f"{year}: {df.shape[1]} cols, missing={missing}")
```

---

## 4. Verificación: Dimensiones Esperadas por Año

Después de ejecutar **Fase 2** (limpieza), verificar contra estas dimensiones:

| Año | Filas post-pivot (aprox.) | Entidades únicas (aprox.) |
|---|---|---|
| 2020 | 17,100 | 17,100 |
| 2021 | 18,200 | 18,200 |
| 2022 | 19,800 | 19,800 |
| 2023 | 20,900 | 20,900 |
| 2024 | 28,762 | 28,762 |
| **Total** | **~127,716** | **34,319 entidades** |

> Las dimensiones son aproximadas; pueden variar ±5% si el ICFES publica
> versiones revisadas de los datos.

**Verificación rápida del CSV procesado:**

```python
import pandas as pd
df = pd.read_csv("data/processed/saber_pro_limpio.csv", low_memory=False)
assert len(df) > 120_000, f"Filas esperadas >120k, encontradas: {len(df)}"
assert "PROMEDIO_GLOBAL" in df.columns, "Falta columna target"
assert df["PROMEDIO_GLOBAL"].isna().sum() == 0, "Target tiene nulos — revisar Fase 2"
print(f"OK: {len(df):,} filas, {df.shape[1]} columnas")
print(f"Años: {sorted(df['AÑO'].unique())}")
```

---

## 5. Ejecución con Tiempos Esperados por Fase

Tiempos medidos en CPU de 8 núcleos / 16 GB RAM. En máquinas más lentas
multiplicar por 1.5–2×.

```bash
# Fase 1: Auditoría de datos
python fase1_auditoria.py
# Tiempo esperado: ~2-4 min (lectura 5 xlsx de ~230 MB total)
# Salida: outputs/reports/auditoria_2024.txt, 3 figuras PNG

# Fase 2: Limpieza y pivot
python fase2_limpieza.py
# Tiempo esperado: ~3-5 min
# Salida: data/processed/saber_pro_limpio.csv (~25 MB)

# Fase 3: Feature engineering
python fase3_features.py
# Tiempo esperado: ~2-3 min
# Salida: data/processed/saber_pro_features.csv (~40 MB)

# Fase 4: Baseline Ridge/Lasso
python fase4_baseline.py
# Tiempo esperado: ~5-8 min (LassoCV con TimeSeriesSplit 4 folds)
# Salida: outputs/ridge_model.pkl, outputs/lasso_model.pkl

# Fase 5: LightGBM + Optuna
python fase5_lightgbm.py
# Tiempo esperado: ~10-15 min (50 trials × ~8-12s/trial)
# Salida: outputs/lgbm_model.pkl, SHAP figures, métricas CSV

# Fase 6: Transformer + Outliers
python fase6_transformer.py
# Tiempo esperado: ~5-20 min (early stopping típico: ~5 min)
# Salida: outputs/transformer_model.pt, reports/decision_transformer.txt

# Demo de inferencia
python demo_inference.py
# Tiempo esperado: ~1 min
# Salida: 5 predicciones individuales + batch test completo
```

**Ejecución completa secuencial (estimado total: ~25-45 min)**:

```bash
for fase in fase1_auditoria fase2_limpieza fase3_features fase4_baseline fase5_lightgbm fase6_transformer demo_inference; do
    echo "=== Ejecutando $fase.py ==="
    python ${fase}.py
done
```

---

## 6. Verificación de Resultados

Después de ejecutar la Fase 5, verificar las métricas contra los valores de referencia:

```python
import pandas as pd

metrics = pd.read_csv("outputs/metrics/baseline_metrics.csv")
print(metrics)
```

**Salida esperada (tolerancia ±0.05 en RMSE, ±0.005 en R²)**:

```
    modelo     RMSE      MAE       R2
0    Ridge   10.2294   7.2967   0.6467
1    Lasso   10.0722   7.0622   0.6575
2  LightGBM   9.3293   6.2109   0.7062
```

**Verificación automatizada de criterios de grado:**

```python
import pandas as pd

metrics = pd.read_csv("outputs/metrics/baseline_metrics.csv")
lgbm = metrics[metrics["modelo"] == "LightGBM"].iloc[0]

RMSE_REF = 9.3293
R2_REF   = 0.7062
TOL_RMSE = 0.05
TOL_R2   = 0.005

assert abs(lgbm["RMSE"] - RMSE_REF) <= TOL_RMSE, \
    f"RMSE fuera de tolerancia: {lgbm['RMSE']:.4f} vs {RMSE_REF} ± {TOL_RMSE}"
assert abs(lgbm["R2"] - R2_REF) <= TOL_R2, \
    f"R² fuera de tolerancia: {lgbm['R2']:.4f} vs {R2_REF} ± {TOL_R2}"
assert lgbm["R2"] > 0.70, \
    f"Criterio de grado NO cumplido: R²={lgbm['R2']:.4f} < 0.70"

print("VERIFICACION PASADA")
print(f"  LightGBM RMSE = {lgbm['RMSE']:.4f}  (ref {RMSE_REF} ± {TOL_RMSE})")
print(f"  LightGBM R²   = {lgbm['R2']:.4f}  (ref {R2_REF} ± {TOL_R2})")
print(f"  Criterio R² > 0.70: CUMPLIDO")
```

---

## 7. Errores Comunes y Soluciones

### Error: `ModuleNotFoundError: No module named 'torch'`

```bash
# Solución: instalar PyTorch CPU-only explícitamente
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Error: `FileNotFoundError: data/raw/saber_pro_2020.xlsx`

```
Causa: Los archivos ICFES no están en el repositorio (son muy grandes).
Solución: Descargar manualmente del portal ICFES (ver Sección 3).
```

### Error: `UnicodeEncodeError: 'charmap' codec can't encode character`

```bash
# Solución: ejecutar con encoding UTF-8 explícito
# Windows
set PYTHONIOENCODING=utf-8 && python fase5_lightgbm.py

# Linux/macOS
PYTHONIOENCODING=utf-8 python fase5_lightgbm.py
```

### Error: `_pickle.UnpicklingError: STACK_GLOBAL requires str`

```
Causa: El archivo .pkl fue guardado con pickle nativo; este proyecto usa joblib.
Solución: Regenerar el modelo ejecutando fase5_lightgbm.py.
          No usar pickle.load() — siempre usar joblib.load().
```

### Error: `InvalidParameterError: TargetEncoder ... cv must be >= 2`

```
Causa: Versión de scikit-learn >= 1.3 requiere cv >= 2 (entero).
       cv=None no es válido en scikit-learn 1.3+.
Solución: Usar cv=2 (ya configurado en el código). Verificar versión:
          python -c "import sklearn; print(sklearn.__version__)"
          # debe ser >= 1.3.0
```

### Error: `git push` falla con `Could not resolve host: github.com`

```bash
# Causa: proxy corporativo intercepta SSL
# Solución temporal para el push:
git -c http.sslVerify=false -c http.proxy="" push -u origin main

# Solución permanente para el repositorio:
git config http.sslVerify false
```

### Resultados ligeramente distintos a los de referencia

**Causa**: Las métricas pueden variar muy ligeramente (±0.02 RMSE) entre
ejecuciones debido a:
- `random_state` en `TargetEncoder` y `LGBMRegressor`
- Orden de resolución de ties en Optuna
- Versión exacta de numpy/scipy

**Solución**: Los `random_state=42` están fijados en todo el código. Si la
variación es > 0.05 en RMSE o > 0.005 en R², verificar versiones de
dependencias con `pip freeze` y comparar contra `requirements.txt`.

---

## Apéndice — Checksum de Archivos Procesados

Para verificar integridad de los CSVs procesados:

```python
import hashlib, pandas as pd

def md5_csv(path, nrows=1000):
    """Checksum rápido sobre las primeras 1000 filas."""
    df = pd.read_csv(path, nrows=nrows, low_memory=False)
    return hashlib.md5(df.to_csv(index=False).encode()).hexdigest()

print("limpio.csv   (primeras 1000 filas):", md5_csv("data/processed/saber_pro_limpio.csv"))
print("features.csv (primeras 1000 filas):", md5_csv("data/processed/saber_pro_features.csv"))
```

> Los hashes exactos dependen del año de publicación del ICFES. Los valores de
> referencia se actualizan en cada release en la sección
> [Releases del repositorio](https://github.com/Blaister9/Sabero_Pro_ModeloPredictivo/releases).
