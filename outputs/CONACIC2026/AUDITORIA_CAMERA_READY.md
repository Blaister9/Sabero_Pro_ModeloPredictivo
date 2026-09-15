# Auditoría previa al camera ready de CONACIC 2026

Estado: **DRAFT, revisión abierta**. Auditoría realizada el 14 de septiembre de 2026, antes de editar la copia del artículo. Paper 17 aceptado sin observaciones según comunicación aportada por Santiago. Los informes de similitud e IA siguen pendientes.

## Base y trazabilidad

Se adopta `entrega_congreso/Saber_pro_paper_CONGRESO_10P_FINAL.docx`, incorporado en `dea64f7897cf6bbcf75796215faf1aa078679db1` (`docs: add final congress delivery package`). Santiago confirmó esta base en la conversación. No se dispone de descarga o recibo de EasyChair que permita certificar por hash el archivo sometido. Los archivos sin `_FINAL` no tienen evidencia de envío y no sustituyen esta base.

SHA-256 DOCX: `5657e9af580c1c555c32128930b7c98cbeb3358cbdd511cd1b7f7ab706db7bcb`.

Título exacto: **Predicción del PROMEDIO_GLOBAL de Saber Pro mediante LightGBM y auditoría de fuga temporal: un estudio a nivel de programa académico en Colombia**.

La base contiene título en español e inglés, 107 párrafos, una tabla, cinco figuras y 26 referencias. El PDF conservado tiene 10 páginas. Procede de la V4 de la asesora, reducida al límite del congreso. Los documentos OPUS47 y el paper extenso son antecedentes, no la base final.

Autor visible en la base: Edwin Santiago Paz Bedoya. Incorporación requerida y confirmada por Santiago: **Edwin Santiago Paz Bedoya y Nathalia Orozco Morales**, ambos **UNIMINUTO Virtual – Bogotá, Colombia**. Correos confirmados: `edwin.paz@uniminuto.edu` y `nathalia.orozco@uniminuto.edu`.

La rama `feat/conacic-2026-camera-ready` parte de `a5c831e`, estado más reciente del proyecto que incluye `origin/main` (`92ee758`). Se ejecutó `git fetch origin`. El stash `b58a7d0` se conserva. Los cambios locales en los dos MP4 de ENSIU se dejan intactos y fuera de este commit.

## Contenido científico aceptado

- Datos: reportes agregados ICFES 2020–2024, 1.730.805 filas crudas según el informe histórico, 127.716 filas procesadas. Unidad: institución-programa-prueba-año, no estudiante. Recuento comprobado en CSV: 19.135, 24.233, 27.722, 27.864 y 28.762 filas por año.
- Metodología: transformación long a wide, historial por entidad, catálogo L1–L6 de fuga, entrenamiento 2020–2023 (98.954 filas), prueba 2024 (28.762), modelos Ridge, Lasso, LightGBM y Transformer.
- Tabla 1: comparación de los cuatro modelos. Figuras: 1 distribución del dataset; 2 curva LightGBM; 3 predicho frente a real; 4 SHAP; 5 error por NBC. Se conservan las cinco figuras, con su contenido original.
- Conclusiones: LightGBM como modelo seleccionado, utilidad predictiva del historial, control de fuga, alertas empíricas y límites de un único año de prueba. Trabajo futuro: covariables externas, horizontes adicionales, embeddings del Transformer, actualización anual, equidad y walk-forward.

## Contraste cuantitativo

Se cargaron los tres modelos locales y se recalcularon predicciones sobre el CSV 2024, sin entrenar ni sobrescribir artefactos. Evidencia y hashes en `VERIFICACION_DATOS_MODELOS.json`. No se afirma reproducción integral desde los Excel crudos.

| Modelo | RMSE paper / recalculado | MAE paper / recalculado | R² paper / recalculado |
|---|---|---|---|
| Ridge | 10,2294 / 10,2294 | 7,2967 / 7,2964 | 0,6467 / 0,6467 |
| Lasso | 10,0722 / 10,0722 | 7,0622 / 7,0589 | 0,6575 / 0,6575 |
| LightGBM | 9,3293 / 9,3293 | 6,2109 / 6,2109 | 0,7062 / 0,7062 |
| Transformer | 16,8588 / reporte histórico | n/d | 0,0405 / reporte histórico |

Las pequeñas diferencias MAE de los baselines requieren reconciliar reporte y serialización antes del cierre. **Se mantienen las cifras aceptadas**. Transformer se verifica contra `decision_transformer.txt`, sin nueva ejecución. Mejora LightGBM frente a Lasso: 7,375 % de RMSE, redondeada a 7,4 %.

## Inconsistencias reales y tratamiento

| Hallazgo | Evidencia | Tratamiento en esta fase |
|---|---|---|
| LightGBM se describe con 500 árboles | Modelo local: 188; narrativa: mejor iteración 168 + 20. JSON de parámetros conserva 500 | Corrección objetiva en la copia: 188 árboles finales; no cambiar métricas |
| El texto afirma inner join de las tres capas | `src/cleaning.py`: inner con global por año-institución-programa y left con niveles por llave de cuatro campos | Corregir descripción de uniones en la copia |
| Codificación categórica no descrita completamente | TargetEncoder en modo automático infirió multiclase (135 valores del objetivo) en los tres modelos; 15 entradas se transforman en 417 columnas. NBC_129.0 representa el componente para la clase objetivo 129, no un código de área | Precisar implementación en copia. Revisar interpretación de componentes categóricos SHAP antes del cierre. No cambiar a target_type=continuous ni reentrenar en esta fase |
| Validaciones internas denominadas cronológicas | CSV ordenado por entidad. Los cuatro folds y el corte Optuna 80/20 mezclan 2020–2023 en ambos lados. Preprocesamiento anterior a RidgeCV/LassoCV no se reajusta en cada fold interno | Advertencia metodológica pendiente de revisión. El holdout externo 2024 sí está separado. No afirmar validación interna temporal completa ni recalcular resultados silenciosamente |
| Rezagos llamados anuales en panel incompleto | 2.022 filas tienen más de un año respecto de la observación previa. `shift(1)` coincide exactamente con el CSV | Precisar “observaciones anteriores disponibles” en la copia |
| SHAP parece contradictorio con README | Figura y narrativa histórica sitúan `lag_1_promedio_global` primero; README dice NBC primero | Conservar resultado del paper y figura. La discrepancia está en README, no justifica cambiar el hallazgo |
| Resumen histórico confunde MAE y RMSE de Sin Clasificar | CSV: RMSE 17,755; MAE 12,2368; narrativa llama RMSE a 12,237 | Paper usa RMSE correcto, conservarlo |
| Salud no presenta universalmente RMSE 4,1–6,2 | CSV incluye Salud Pública 11,7652 | Matizar en copia: “Algunas áreas de Salud” |
| Fechas y metadatos ficticios heredados de plantilla | Pie de primera página: recepción/aceptación 2020; volumen 41 (2023) en la plantilla | Sustituir por DRAFT y pendientes, sin inventar volumen, páginas editoriales ni fecha oficial de aceptación |
| Referencia [20] dice Anónimo | PDF oficial EDM 2020 identifica Adeodato y Silva Filho, pp. 545–549 | Corregir autoría bibliográfica objetiva |

Persisten asuntos que no se resuelven alterando cifras: la diferencia de error por flags necesita respaldo recalculado; la corrección del catálogo L1–L6 debe distinguir variables efectivamente usadas de ejemplos genéricos como percentiles; los flags son reglas empíricas y no intervalos probabilísticos; la disponibilidad anticipada de `CANTIDADEVALUADOS` debe justificarse; la disminución histórica ΔR²≈0,22 no equivale a una ablación por cada fuga; SHAP y errores regionales no prueban causalidad. Las afirmaciones amplias de novedad y de impacto curricular requieren moderación/revisión antes de cerrar.

## Referencias y límites de la verificación

Se inventariaron las 26 referencias en `INVENTARIO_BASE.md`, conservando numeración. [20] se contrastó con el [artículo oficial de EDM 2020](https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_55.pdf). [26] está identificado en el [repositorio institucional de la Universitat de València](https://producciocientifica.uv.es/documentos/6574e34dc27a3a35855955ee?lang=eu), DOI 10.1016/j.orp.2023.100292. [8] presenta datos bibliográficos incompatibles con el [manuscrito institucional de Behr y colaboradores](https://duepublico2.uni-due.de/servlets/MCRFileNodeServlet/duepublico_derivate_00074078/Diss_Giese.pdf); requiere completar ficha. No se localizó coincidencia exacta de [16] en la búsqueda realizada: esto no prueba inexistencia. [21] y [22], así como los detalles psicométricos de [1]/[23], quedan para comprobación bibliográfica específica. **No se certifica toda la bibliografía como validada**.

## Plantillas y decisión de cierre

Se descargaron los archivos enlazados por [CONACIC 2026](https://conacic.siycise.org/), sin reconstruirlos. La plantilla PPTX conserva “2024” en el nombre, pero es el enlace actual del recurso Ponencias Simultáneas. El límite público es [hasta 10 páginas](https://conacic.siycise.org/convocatoria). La web muestra 31 de agosto para camera ready; se usan operativamente los plazos particulares del correo aportado: 20 y 23 de septiembre, 23:59. Falta precisar zona horaria, no se infiere Bogotá ni México.

**La aceptación sin observaciones no elimina estos pendientes internos.** La copia DRAFT aplica solo cambios objetivos enumerados y autoría confirmada. El resto se conserva para revisión trazable. No enviar ni cerrar hasta revisar similitud, IA, inconsistencias y aprobación de la asesora.
