# Auditoría de consistencia ENSIU 2026

Se verificaron las dos fuentes oficiales de `docs/ENSIU2026/` contra datos, código, modelo serializado y resultados locales. No se modificaron las fuentes oficiales. Esta revisión sirve a la entrega audiovisual; no modifica ni incorpora la entrega de congreso.

| Afirmación | Resultado y evidencia |
|---|---|
| 127.716 registros | Confirmado contando filas de `data/processed/saber_pro_limpio.csv` y `saber_pro_features.csv`. Son observaciones agregadas institución-programa-prueba-año, no estudiantes ni programas únicos. El objetivo es PROMEDIO_GLOBAL. |
| 2020–2024 | Confirmado: 19.135; 24.233; 27.722; 27.864; 28.762 observaciones por año, respectivamente. Total 127.716. |
| LightGBM | Confirmado: `outputs/lgbm_model.pkl` contiene un Pipeline con LGBMRegressor. `fase5_lightgbm.py:56` define prueba 2024 y entrenamiento anterior. No se reentrenó. |
| R² = 0,706 | Confirmado. `outputs/metrics/baseline_metrics.csv` registra 0,7062. Recalculado con las 28.762 filas de 2024 y el modelo guardado: 0,7061747115974841. |
| RMSE = 9,33 | Confirmado. CSV: 9,3293. Recalculado: 9,329341949418497 puntos. MAE recalculado: 6,21093744100961. RMSE no es margen máximo, intervalo de confianza ni garantía individual de ±9,33 puntos. Se corrige la frase «acierta con un margen de error de apenas 9 puntos sobre 300». |
| Ridge, Lasso, Transformer | Confirmado en `baseline_metrics.csv` y `outputs/reports/decision_transformer.txt`, sección 3. RMSE: Ridge 10,2294; Lasso 10,0722; LightGBM 9,3293; Transformer 16,8588. El Transformer tiene entradas y unidad de entrenamiento distintas; el resultado se limita a los experimentos reportados y no prueba superioridad universal. |
| Seis fugas de información | Catálogo documentado en `README.md:287` y `docs/ARQUITECTURA_TECNICA.md:263`: codificación del objetivo global, puntaje concurrente, desviación concurrente, niveles concurrentes, delta del objetivo y tendencia/volatilidad con año actual. El código excluye las variables concurrentes y usa historia previa. Es una comprobación de catálogo e implementación, no certificación exhaustiva de ausencia de toda fuga. No se utiliza ΔR² ≈ 0,22 en el video porque no se reprodujo una ablación. |
| 15 features temporales | Corrección necesaria: `src/models/baseline.py:97` y `src/inference.py:102` definen 15 variables de entrada: 10 numéricas, 3 categóricas y 2 indicadoras. Hay 8 variables históricas (4 rezagos, 2 tendencias y 2 de variabilidad), además del año y tamaño de cohorte. No son 15 variables temporales. `feature_report.txt` cuenta 17 columnas nuevas en el CSV, que es un concepto distinto. No se usa la formulación incorrecta en pantalla ni en voz. |
| SHAP | Confirmado por código (`src/models/boosting.py:479` y `fase5_lightgbm.py:216`) y gráficos existentes. Recalculado con el modelo guardado, 5.000 filas de prueba y RandomState(42): mean abs SHAP de lag_1_promedio_global = 6,2389602; lag_2_promedio_global = 2,3781396; lag_1_promedio_prueba = 1,1711287. La historia previa domina. El análisis está respaldado por gráficos originales del proyecto; no se fuerza este gráfico en el minuto. |
| Sucre, Chocó y Putumayo | Confirmado como los tres RMSE más altos de los 26 departamentos reportados en `metricas_lgbm_por_depto.csv`: 13,2927 (n=366), 12,0347 (n=243), 11,1818 (n=54). El gráfico original muestra los primeros 25. El repositorio no incorpora un indicador económico para probar la asociación con «menor desarrollo relativo». Tampoco el mayor error demuestra por sí solo mayor necesidad social. Se elimina esa atribución y se formula reforzar datos y acompañamiento como orientación. |
| Aproximadamente un año antes | Respaldo parcial: hay prueba retrospectiva 2024 con entrenamiento 2020–2023 y rezagos de observaciones anteriores. `src/features.py:200` aclara que shift(1) usa la observación anterior disponible, que puede estar a más de un año. `log_cantidadevaluados` usa la cohorte del año objetivo; no hay auditoría de su disponibilidad doce meses antes. No hay validación prospectiva con fechas de publicación. Se sustituye «saber, un año antes» por «estimar, con su historial» y se muestra «evaluación retrospectiva del siguiente año». |
| Misión 4 | Alineación declarada explícitamente en ambos DOCX oficiales: «Inteligencia Artificial para la equidad». Se presenta como alineación institucional del trabajo, no como resultado empírico. |

## Ajustes mínimos del guion

El gancho conserva su pregunta y afirmación final, cambiando solo el verbo y la garantía temporal no validada. El sustento conserva el orden datos, precisión, territorio e impacto. Se sustituye el margen garantizado por el nombre correcto de RMSE y su valor 9,33, y la atribución económica no probada por el hallazgo territorial verificable. El cierre conserva el texto oficial; el guion separa su última frase en dos oraciones y escribe 2026 en palabras para pronunciación.

Se mantienen UNIMINUTO, ENSIU 2026 y los autores de las fuentes oficiales. La propuesta de acompañamiento e intervención proactiva es una aplicación potencial: no se afirma que ya redujo brechas ni que se haya medido su impacto. La secuencia usa tipografía y evidencia real, sin campus inventados ni un dashboard inexistente. UNIMINUTO aparece como firma tipográfica, sin fabricar un logotipo.

## Alcance de la comprobación

Auditoría rápida local, sin usar el paper de congreso como autoridad y sin reentrenamiento. La comparación del Transformer se verifica en el reporte existente. Las predicciones LightGBM y la jerarquía SHAP sí se recalcularon. Las fechas de publicación, el desarrollo económico y el impacto de intervenciones no están validados por estos artefactos. El resultado validado es retrospectivo sobre 2024.

## Actualización con narración real definitiva

Por instrucción posterior del usuario, `Grabación (14).m4a` sustituye el texto hablado y la voz de la primera versión. El audio se incorpora completo, con su duración real de 53,247771 s y sin edición. Las ocho composiciones y sus métricas permanecen iguales. Se ajustan únicamente los tiempos para seguir la narración real; los últimos 6,752229 s del video quedan sin audio y concluyen con la firma institucional. La transcripción auxiliar normaliza la grafía de los nombres de los modelos y de las cifras, sin intervenir en la grabación. La grabación es la fuente definitiva de la voz.
