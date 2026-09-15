- Paper aceptado sin observaciones.
- Similitud Turnitin 5 %.
- IA Turnitin 72 %.
- Resultados principales LightGBM reproducibles.
- Ninguna modificación científica aplicada después de la auditoría.

# Reunión con Nathalia — decisiones para cerrar el camera-ready

**Duración: 25 minutos:** puntos 1–6, 15 min; 7–12, 8 min; cierre, 2 min. Registrar A/B y evidencia pendiente en cada decisión. Conservar provisionalmente no equivale a validar una afirmación cuestionada. Este documento no aplica cambios ni autoriza el cierre científico.

**Fuentes exclusivas:** `DIFF_CAMERA_READY.md` (DIFF), `REVISION_TURNITIN.md` (TURNITIN) y `PLAN_REVISION_FINAL.md` (PLAN), en esta carpeta. Los C científicos se citan como PLAN; los C01–C09 editoriales finales pertenecen a TURNITIN.

## 1. Validación temporal interna

1. **TEMA:** Separación externa frente a selección interna (PLAN C02; DIFF §4.1).
2. **QUÉ DICE EL PAPER ACEPTADO:** Entrena en 2020–2023 y prueba en 2024; la brecha de la curva «confirma regularización adecuada».
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Folds y Optuna 80/20 mezclan años; preprocesamiento lineal previo al CV interno. La curva sí valida en 2023 y el holdout 2024 está separado.
4. **RIESGO REAL:** Alto: extender la garantía temporal a toda selección; no demuestra falsedad de las métricas externas.
5. **OPCIÓN A — conservar aceptado:** Mantener texto y garantía, dejando el límite pendiente.
6. **OPCIÓN B — corregir/matizar:** Explicitar el límite interno y circunscribir la curva a su partición.
7. **RECOMENDACIÓN TÉCNICA:** B, confirmando la corrida aceptada; conservar split externo y resultados.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 2. TargetEncoder multiclass y alcance de SHAP

1. **TEMA:** Qué codificación e interpretación se sostienen (PLAN C03/C04; DIFF §4.2).
2. **QUÉ DICE EL PAPER ACEPTADO:** 15 features «causalmente válidas», TargetEncoder e indicadores NBC como efectos por disciplina.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Tres PKL: multiclass, 135 valores objetivo, 417 columnas; siguen siendo regresores. NBC_129.0 codifica el objetivo 129, no una disciplina.
4. **RIESGO REAL:** Alto en interpretación; no se demostró error numérico de SHAP.
5. **OPCIÓN A — conservar aceptado:** Mantener descripción e interpretación actuales.
6. **OPCIÓN B — corregir/matizar:** Describir 15 entradas/417 columnas y limitar SHAP a contribuciones predictivas según la codificación.
7. **RECOMENDACIÓN TÉCNICA:** B tras confirmar correspondencia entre artefacto, columnas y figura; preservar ranking y valores, incluido +28.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 3. Anticipación «un año antes»

1. **TEMA:** Horizonte operativo acreditado (PLAN C03/C10; DIFF §4.4).
2. **QUÉ DICE EL PAPER ACEPTADO:** Predicción con un año de anticipación y utilidad para gestión proactiva.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** CANTIDADEVALUADOS usa el registro corriente; no consta disponibilidad un año antes. Los rezagos son observaciones previas disponibles: 2.022 saltos superan un año.
4. **RIESGO REAL:** Alto: confundir evaluación retrospectiva con disponibilidad anticipada e impacto operativo.
5. **OPCIÓN A — conservar aceptado:** Sostener el año de anticipación, pendiente de acreditar calendario de entradas.
6. **OPCIÓN B — corregir/matizar:** Describir evaluación 2024 y condicionar anticipación a disponibilidad de todas las entradas.
7. **RECOMENDACIÓN TÉCNICA:** B salvo evidencia del calendario real; precisar rezagos y mantener métricas.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 4. Flags de confianza y RMSE 9,1/11,4

1. **TEMA:** Procedencia de errores y significado de confianza (PLAN C07/C09; DIFF §4.4).
2. **QUÉ DICE EL PAPER ACEPTADO:** MEDIA 84,4 %: RMSE≈9,1; BAJA 15,6 %: ≈11,4; diferencial 2,3 informativo; cuantificación de incertidumbre.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Mismos tamaños; artefacto actual≈6,5968/17,9802. Las cifras aceptadas implican total≈9,49, frente a 9,3293 publicado. Flags por reglas, sin calibración.
4. **RIESGO REAL:** Muy alto en trazabilidad y certeza; causa histórica sin resolver.
5. **OPCIÓN A — conservar aceptado:** Congelar cifras y texto hasta identificar su origen.
6. **OPCIÓN B — corregir/matizar:** Acordar flags como señales empíricas; cualquier corrección numérica queda condicionada a reconciliar procedencia.
7. **RECOMENDACIÓN TÉCNICA:** B para alcance; congelar números hasta identificar predicciones, reglas y corrida originales. No sustituirlos por los actuales automáticamente.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 5. ΔR²≈0,22 y catálogo de seis fugas

1. **TEMA:** Atribución del aporte (PLAN C13; DIFF §4.4).
2. **QUÉ DICE EL PAPER ACEPTADO:** Seis fugas L1–L6 con impacto conjunto≈0,22; Lasso pasa de R²≈0,88 a 0,658.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** La resta concuerda; no aísla efectos ni controla otros cambios. Percentiles citados no aparecen en las 15 entradas finales; su uso histórico sigue pendiente.
4. **RIESGO REAL:** Alto: atribuir al catálogo una diferencia sin trazabilidad suficiente.
5. **OPCIÓN A — conservar aceptado:** Mantener atribución conjunta y cifras.
6. **OPCIÓN B — corregir/matizar:** Presentar comparación histórica sin efectos individuales, solo si se identifican corridas comparables.
7. **RECOMENDACIÓN TÉCNICA:** Vincular ambas corridas y cambios L1–L6; B si esa evidencia lo permite. Congelar catálogo y cifras entretanto.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 6. Causalidad, interpretación territorial y SHAP

1. **TEMA:** Asociación predictiva frente a explicación causal (PLAN C04/C11/C18).
2. **QUÉ DICE EL PAPER ACEPTADO:** Errores explicados por heterogeneidad/desarrollo territorial; SHAP orienta intervenciones; cuatro factores explican la brecha Transformer.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Tablas y SHAP describen errores/predicciones; no estiman efectos causales. La comparación Transformer no aísla cuatro causas.
4. **RIESGO REAL:** Alto: convertir asociaciones en causas o garantías de intervención.
5. **OPCIÓN A — conservar aceptado:** Mantener explicaciones y recomendaciones actuales.
6. **OPCIÓN B — corregir/matizar:** Describir diferencias observadas; presentar causas como hipótesis y limitar recomendaciones a evidencia disponible.
7. **RECOMENDACIÓN TÉCNICA:** B, conservando cifras, figuras y citas; tampoco afirmar ausencia de sesgos por simples recuentos de cobertura.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 7. LightGBM: 500 vs. 188 árboles

1. **TEMA:** Configuración por etapa (PLAN C05; DIFF D06).
2. **QUÉ DICE EL PAPER ACEPTADO:** 50 trials, n_estimators=500; curva de 225 iteraciones, mejor iteración 168.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** PKL actual: 188=168+20; JSON guardado antes del ajuste final. 500, máximo 800, curva 225 y mejor 168 corresponden a etapas distintas.
4. **RIESGO REAL:** Medio: configuración reportada ambigua, sin discrepancia de métricas LightGBM.
5. **OPCIÓN A — conservar aceptado:** Mantener 500 mientras se confirma la corrida.
6. **OPCIÓN B — corregir/matizar:** Distinguir configuración intermedia de 188 árboles finales.
7. **RECOMENDACIÓN TÉCNICA:** B condicionada a vincular JSON/PKL con la ejecución aceptada; no reemplazar indiscriminadamente cifras de etapas.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 8. Salud y rango RMSE 4,1–6,2

1. **TEMA:** Categorías que respaldan la generalización (PLAN C08; DIFF D07).
2. **QUÉ DICE EL PAPER ACEPTADO:** Salud concentra los menores errores, RMSE 4,1–6,2.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Salud Pública≈11,7652; Medicina≈6,2174; Optometría≈4,687. El ≈4,1089 corresponde a formación militar/policial.
4. **RIESGO REAL:** Medio: generalización y extremo inferior sin respaldo como Salud.
5. **OPCIÓN A — conservar aceptado:** Mantener frase y rango pendientes de trazabilidad.
6. **OPCIÓN B — corregir/matizar:** Describir variación entre NBC y comportamiento no uniforme de Salud.
7. **RECOMENDACIÓN TÉCNICA:** B tras conciliar categorías/figura/CSV; «algunas áreas» no resuelve por sí solo el rango. No proponer uno nuevo ahora.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 9. MAE Ridge/Lasso

1. **TEMA:** Correspondencia entre tabla, CSV y PKL (PLAN C06; DIFF §4.3).
2. **QUÉ DICE EL PAPER ACEPTADO:** Ridge 7,2967; Lasso 7,0622.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** CSV histórico coincide; PKL actuales redondean a 7,2964/7,0589. RMSE/R² concuerdan; causa histórica desconocida.
4. **RIESGO REAL:** Medio en trazabilidad; no es solo redondeo ni evidencia de cambio de ranking.
5. **OPCIÓN A — conservar aceptado:** Mantener celdas del CSV histórico.
6. **OPCIÓN B — corregir/matizar:** Corregir solo tras identificar predicciones, muestra, commit y cálculo de origen.
7. **RECOMENDACIÓN TÉCNICA:** A provisional; aprobar B únicamente con procedencia reconciliada. No atribuir la discrepancia a serialización sin evidencia.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 10. Referencias [8], [16], [21], [22]

1. **TEMA:** Identidad y respaldo argumental, por referencia (PLAN C14–C16; DIFF §4.5).
2. **QUÉ DICE EL PAPER ACEPTADO:** [8] Behr, 2022; [16] Rangel-Mora/Pérez-Roa, 2021; [21] Chafla/Morocho/Ortega, 2025; [22] Acıslı-Celik/Yesilkanat, 2023; apoyan discusión y novedad.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** [8]: contradicción de autor/revista/año; [16]/[21]: sin identidad exacta; [22]: identificada, ficha incompleta y exclusividad no demostrada.
4. **RIESGO REAL:** Alto en respaldo; búsqueda negativa no demuestra inexistencia.
5. **OPCIÓN A — conservar aceptado:** Mantener fichas y usos pendientes de resolver.
6. **OPCIÓN B — corregir/matizar:** Verificar obra/pasaje individualmente; completar [22] y revisar pertinencia de cada cita.
7. **RECOMENDACIÓN TÉCNICA:** B con cuatro resoluciones separadas; obtener DOI/PDF de [8]/[16]/[21]. No sustituir por títulos parecidos ni eliminar citas automáticamente.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 11. Novedad y exclusividad

1. **TEMA:** Alcance defendible de la contribución (PLAN C12).
2. **QUÉ DICE EL PAPER ACEPTADO:** «No existe», «ningún trabajo previo», «inédita» y catálogo transferible a PISA.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** Referencias inciertas y búsqueda insuficiente para ausencia universal; no consta aplicación a PISA.
4. **RIESGO REAL:** Alto: novedad y transferencia más amplias que la evidencia.
5. **OPCIÓN A — conservar aceptado:** Mantener exclusividad y transferencia afirmadas.
6. **OPCIÓN B — corregir/matizar:** Delimitar aporte al catálogo/procedimiento documentados en este panel; condicionar transferencia a otros datos y calendarios.
7. **RECOMENDACIÓN TÉCNICA:** B; resolver conjuntamente respaldo bibliográfico y ΔR², sin borrar cifras o referencias por estilo.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## 12. Tratamiento del 72 % de Turnitin

1. **TEMA:** Respuesta académica al indicador (TURNITIN §A.1; PLAN §1.3/§5).
2. **QUÉ DICE EL PAPER ACEPTADO:** Es el texto evaluado; no contiene el 72 %, que pertenece al informe posterior.
3. **QUÉ ENCONTRÓ LA AUDITORÍA:** 72 % del texto calificado señalado como probable IA; similitud 5 %. El informe advierte posibles errores y exige juicio humano.
4. **RIESGO REAL:** Confundir indicadores con prueba de autoría, plagio o validez científica; reescribir sin razón académica.
5. **OPCIÓN A — conservar aceptado:** Mantener redacción correcta aunque esté marcada y conservar informes íntegros.
6. **OPCIÓN B — corregir/matizar:** Incorporar únicamente R01/R03/R06 por claridad equivalente; resolver cambios de alcance en sus decisiones científicas.
7. **RECOMENDACIÓN TÉCNICA:** B limitada a esas mejoras; conservar los demás pasajes correctos. Sin porcentaje objetivo, promesas de reducción ni manipulación del detector.
8. **DECISIÓN DE NATHALIA: [PENDIENTE]**

## CAMBIOS QUE PODEMOS HACER SIN DISCUSIÓN

- **TURNITIN C01:** Retirar/conservar retirada de fechas editoriales ficticias; usar solo datos confirmados.
- **TURNITIN C02:** Retirar/conservar retirada del encabezado de otro artículo.
- **TURNITIN C03:** Corregir errata «auditorría», espacio doble y capitalización del encabezado.
- **TURNITIN C04:** «recoleción» → «recolección».
- **TURNITIN C05:** Corregir atribuciones y cronología heredadas de plantilla, sin inventar datos.
- **TURNITIN C06:** Actualizar campos PAGE y estadísticas; verificar render en la futura edición.
- **TURNITIN C07:** Sustituir ruta ajena del logo por texto alternativo descriptivo, sin cambiar imagen.
- **TURNITIN C08:** Actualizar estado a informes recibidos/revisión pendiente, conservando DRAFT.
- **TURNITIN C09:** Resolver referencias de estilo huérfanas, preservando contenido/apariencia y verificando visualmente.
- **R01:** Explicitar función del módulo en ambos resúmenes, sin ampliar alcance.
- **R03:** Separar tamaño, unidad de fila y estructura en frases; conservar hechos y cifras.
- **R06:** Expresar directamente evaluación e interpretación; conservar RMSE, MAE, R² y SHAP [6].

## CAMBIOS BLOQUEADOS HASTA DECISIÓN

- **PLAN C01:** Joins, claves, capas y criterio de inclusión.
- **PLAN C02–C04:** Validación interna, garantías de la curva, codificación, rezagos, validez de variables, SHAP y suficiencia del historial.
- **PLAN C05–C09:** Árboles, MAE, RMSE por confianza/diferencial, generalización/rango de Salud y significado de incertidumbre.
- **PLAN C10–C13:** Anticipación, uso curricular/impacto, causalidad territorial y Transformer, novedad, transferencia y atribución ΔR² al catálogo.
- **PLAN C14–C16:** Fichas y usos de [8], [16], [21], [22], incluida la compleción de [22] reservada a Nathalia.
- **PLAN C17–C19:** Definición Rasch/global/calidad, respaldo [1]/[15]/[23]/[26], unidad de datos en agradecimientos, inferencias de cobertura/sesgo, límites y efectos esperados del trabajo futuro.
- **Cualquier otro cambio científico:** Texto, cifras, tablas, figuras, citas, conclusiones o alcance; una reformulación por Turnitin tampoco lo desbloquea. Sin decisión y evidencia suficiente, queda pendiente; esta agenda no autoriza su aplicación.
