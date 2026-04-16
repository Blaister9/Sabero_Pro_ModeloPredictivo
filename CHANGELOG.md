# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2025-04-17

First complete release of the Saber Pro Predictive Engine. Full 8-phase pipeline
from raw ICFES data to inference module, evaluated on test year 2024.

### Added

#### Phase 1 — Data Audit
- `fase1_auditoria.py`: multi-year ingestion, null-rate analysis, temporal coverage audit
- `src/ingestion.py`: `load_years()` for multi-file ICFES loading with schema validation
- Output figures: `nulidad_2024.png`, `nulidad_barplot_2024.png`, `cobertura_temporal.png`
- `outputs/reports/auditoria_2024.txt`: full audit narrative

#### Phase 2 — Cleaning & Pivot
- `fase2_limpieza.py`: long→wide pivot in three explicit join layers
- `src/cleaning.py`: `clean_dataset()` with rules C1–C5
- Discovery and formal documentation of long-format MEDIDA_AGREGACION discriminator
- Formal exclusion of `PERCENTIL_PRUEBA` (unavailable at PROGRAMA_ACÁDEMICO level)
- `data/processed/saber_pro_limpio.csv` (127,716 × 24)
- `outputs/reports/log_limpieza.txt`

#### Phase 3 — Feature Engineering
- `fase3_features.py`: temporal lag, trend, and volatility features
- `src/features.py`: `build_features()` with expanding-lag leakage-free implementation
- 15 features for the model: 10 numeric + 3 categorical (TargetEncoded in Pipeline) + 2 OHE
- `data/processed/saber_pro_features.csv` (127,716 × 41)
- `outputs/reports/feature_report.txt`

#### Phase 4 — Baseline Models
- `fase4_baseline.py`, `src/models/baseline.py`
- Ridge regression (RMSE=10.23, R²=0.647) and Lasso (RMSE=10.07, R²=0.658)
- sklearn Pipeline with `TargetEncoder(smooth="auto", cv=2)` inside the Pipeline
- Baseline metrics and per-NBC/departamento breakdown CSVs
- `outputs/reports/narrativa_baseline.txt`

#### Phase 5 — LightGBM + Optuna + SHAP
- `fase5_lightgbm.py`, `src/models/boosting.py`
- LightGBM with 50-trial Optuna search (RMSE=9.33, R²=0.706 on test 2024)
- Beats best baseline by 7.4% RMSE — R²>0.70 graduation criterion met
- SHAP TreeExplainer for global interpretability
- `outputs/lgbm_model.pkl`, `outputs/lgbm_best_params.json`
- SHAP beeswarm, feature importance, residuals, error-by-NBC figures

#### Phase 6 — Transformer Encoder + Outlier Analysis
- `fase6_transformer.py`, `src/models/transformer.py`
- `SaberProTransformer`: d_model=64, nhead=4, 2 encoder layers, ffn=128, 70,337 params
- `SaberProSequenceDataset`: left-padded temporal sequences per entity (max_seq_len=5)
- 20-minute CPU time budget with hard stop and partial-results documentation
- Transformer converged at epoch 53 (4.6 min) but underperforms: RMSE=16.79, R²=0.048
- `outputs/reports/analisis_outliers.txt`: analysis of Licenciatura UMB PROMEDIO=31.0 (N=1)
- `outputs/reports/decision_transformer.txt`: model selection justification
- `outputs/transformer_model.pt`

#### Phase 7 — Inference Module
- `src/inference.py`: `load_model()`, `predict_institution()`, `predict_batch()`,
  `build_inference_row()`, `format_prediction_report()`
- Three empirical confidence flags: `baja_confianza_muestra_pequeña`,
  `baja_confianza_sin_historial`, `baja_confianza_extrapolacion`
- `demo_inference.py`: 5 individual scenarios + full batch test verification
- `outputs/reports/demo_inferencia.txt`

#### Phase 8 — Paper Draft
- `paper/draft/01_titulo_y_abstract.txt` — Bilingual title and abstract
- `paper/draft/02_introduccion.txt` — Introduction and contributions
- `paper/draft/03_datos_y_metodologia.txt` — Data, pivot strategy, 6-leakage table
- `paper/draft/04_feature_engineering.txt` — 15 features, expanding lag, corrections
- `paper/draft/05_resultados.txt` — Full 4-model comparison tables
- `paper/draft/06_discusion.txt` — LightGBM vs Transformer quantitative analysis
- `paper/draft/07_conclusiones.txt` — Conclusions and future work
- `paper/draft/08_referencias.txt` — 18 references

#### Documentation
- `README.md`: complete professional documentation (15 sections)
- `requirements.txt`: pinned versions of all 23 dependencies
- `docs/ARQUITECTURA_TECNICA.md`: ASCII pipeline diagram, design decisions, leakage catalog
- `docs/GUIA_REPRODUCIBILIDAD.md`: step-by-step reproducibility guide
- `outputs/CHECKLIST_FINAL.txt`: 73/73 files verified on disk

### Fixed — Data Leakage Corrections

All six leakage types were discovered and corrected during development.
Total measured impact: ΔR² = +0.22 (from honest R²=0.658 to inflated R²≈0.88).

- **[L1] Target encoding over full dataset** — `te_nbc`, `te_nombre_prueba`,
  `te_id_departamento` were computed over the full dataset in `features.py`.
  Fix: removed from `features.py`; moved `TargetEncoder(cv=2)` inside sklearn
  `Pipeline` so encoding is computed only on train data in each fold.

- **[L2] Concurrent variable: same-year PROMEDIO_PRUEBA** — `PROMEDIO_PRUEBA`
  at year t belongs to the same ICFES annual release as the target `PROMEDIO_GLOBAL`.
  Fix: removed as a direct feature; replaced only with `lag_1_promedio_prueba` (year t−1).

- **[L3] Concurrent variable: same-year DESVIACION** — standard deviation of
  test scores from the same evaluation year as the target.
  Fix: excluded from model features; renamed to `concurrent_*` prefix in CSV.

- **[L4] Concurrent variables: same-year NIVEL1-4** — performance level
  proportions from the same evaluation year.
  Fix: excluded from model; renamed to `concurrent_prop_nivel*` in CSV.

- **[L5] Direct target leak in delta feature** — `delta_1_global` was defined
  as `PROMEDIO_GLOBAL(t) − lag_1_global(t−1)`, directly containing the target.
  Fix: deleted entirely.

- **[L6] Temporal leakage in trend and volatility features** — `tendencia_global`,
  `tendencia_prueba`, `desviacion_estandar_historica`, and `coeficiente_variacion`
  included the value at year t in their expanding-window calculations.
  Fix: rewrote all four features using `shift(1).expanding()` pattern:
  for year t, only history from t−1, t−2, ... is used.

### Security

- **Pickle deserialization risk**: `outputs/lgbm_model.pkl` is serialized with
  `joblib`. Loading pickle files from untrusted sources can execute arbitrary code.
  Mitigation: the model file is excluded from the git repository (`.gitignore`)
  and should be distributed only through authenticated channels (GitHub Releases,
  internal artifact registries). Always verify the SHA256 hash of the `.pkl` file
  before loading in production environments.
  Recommended hash verification before loading:
  ```python
  import hashlib, joblib
  with open("outputs/lgbm_model.pkl", "rb") as f:
      digest = hashlib.sha256(f.read()).hexdigest()
  assert digest == "<known_good_hash>", "Model file integrity check failed"
  model = joblib.load("outputs/lgbm_model.pkl")
  ```

---

## [Unreleased]

### Planned
- `main.py`: master orchestration script for the complete 8-phase pipeline
- `tests/`: unit tests for leakage detection and feature integrity checks
- Incremental model update mechanism (annual fine-tuning)
- FastAPI REST endpoint for production inference
- Docker container for reproducible deployment
