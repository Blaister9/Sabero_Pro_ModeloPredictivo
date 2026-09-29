# Plan de adaptación mínima ENSIU 2026

Fecha de auditoría: 28 de septiembre de 2026 (America/Bogota). Elaborado **antes de generar el PPTX final**.

## Alcance y estado inicial

- Worktree exclusivo: `C:\Users\santi\Documents\Sabero_Pro_ModeloPredictivo_ENSIU_FINAL`.
- Rama: `feat/ensiu-2026-presentacion-final`.
- HEAD inicial: `81c61c9f5bfd2ad753b8d1f230bd57b26f22b26e`.
- `git status --short`: sin salida; árbol limpio. Rama y últimos doce commits comprobados.
- Base visual y científica: `outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx` y su PDF, diez diapositivas de 13⅓ × 7½ pulgadas.
- Se preservan diez diapositivas, orden, gráficos, tabla, cifras, posiciones, tipografía Gill Sans MT, paneles y fondo original sin marcas. Se sustituyen únicamente las marcas del evento y tres intervenciones textuales locales.
- No se modifica ningún original científico, paper, presentación antecedente, audiovisual ni archivo de CONACIC. No se ejecutan modelos ni se recalculan métricas. No se cambia de rama, no se hace merge.

## Auditoría de las seis fuentes requeridas

Se extrajeron todos los textos, tablas y notas de los dos PPTX y los dos DOCX, y el texto completo de ambos PDF. Se renderizaron e inspeccionaron individualmente las diez páginas CONACIC y las ocho páginas ENSIU. Los PDF concuerdan con el contenido de sus PPTX. Se inspeccionaron además patrón, diseños y medios incrustados de CONACIC.

| Fuente | Narrativa y función | Diferencia relevante |
| --- | --- | --- |
| CONACIC final, PPTX y PDF | Problema, panel, control de fuga, modelos, desempeño, comparación, SHAP, error y límites, conclusiones | Fuente científica prevalente. Delimita evaluación retrospectiva, comparación de configuraciones y ausencia de causalidad. |
| Comunicación ENSIU, DOCX | Alineación institucional, resumen, STAR, referencias | Sitúa el resultado en Misión 4 y equidad territorial. Contiene formulaciones más fuertes sobre desarrollo relativo, intervención y confianza que no deben trasladarse literalmente. |
| ENSIU anterior, PPTX y PDF | Ocho escenas sincronizadas con un audiovisual de 60 s | Es un antecedente audiovisual, no la base de la ponencia larga. Resume datos y resultados, usa el gráfico departamental, carece del desarrollo metodológico completo de CONACIC. |
| Guion audiovisual ENSIU, DOCX | Informar, Atraer y Convencer, con apertura, sustento y cierre | Contiene “margen de error”, pregunta retórica e impacto expresado con excesiva certeza. No se reutilizan esas frases. |

Se consultaron también el guion final CONACIC, la auditoría y entrega ENSIU anteriores, los resultados archivados y las fuentes oficiales descritas en `REVISION_OFICIAL_ENSIU_2026.md`. Los resultados numéricos finales se transcriben de la presentación CONACIC por jerarquía, sin armonizar divergencias menores con otros reportes históricos.

## Interpretación explícita de los tres pilares

La comunicación **no enumera una sección titulada “tres pilares”**. La siguiente es una interpretación editorial sustentada en su apartado 1, no una nueva cita atribuida a Nathalia ni una confirmación de su intención exacta:

1. **IA para la equidad, como propósito institucional.** Texto exacto: “Misión de Conocimiento: Misión 4 — Inteligencia Artificial para la equidad”. Se lleva a la portada y al encuadre oral de la ponencia. LightGBM y la auditoría mantienen el sustento científico.
2. **Datos para la equidad, como línea de trabajo.** Texto exacto: “Subtema / línea de trabajo: Datos para la equidad (con conexión directa a Sistematización de información territorial)”. Se añade una línea breve en la diapositiva 2. Las diapositivas 3–8 conservan la evidencia con datos públicos, evaluación y explicación del modelo.
3. **Sistematización de información territorial, como conexión aplicada.** Respaldada por la misma frase exacta y por: “El análisis de errores por Núcleo Básico del Conocimiento y por departamento muestra que la incertidumbre del modelo no se distribuye de forma pareja”. Se explican las dos desagregaciones existentes en la diapositiva 9 y se conecta el trabajo futuro con equidad territorial en la 10.

Los tres componentes tienen distinta jerarquía: misión, línea y conexión temática. No son tres misiones independientes. Tampoco son las cuatro etapas STAR. El guion técnico audiovisual y el anexo oficial sí contienen otra tríada explícita: “Informar (Datos y Pertinencia)”, “Atraer (Gancho y Estética)” y “Convencer (Valor e Impacto Social)”. Esa tríada organiza el clip R; no se adopta como estructura conceptual nueva del PPTX, porque Nathalia remitió específicamente la comunicación y Santiago pidió conservar CONACIC. La ambigüedad se deja registrada para confirmación con la asesora sin bloquear la adaptación.

STAR se mantiene en el guion, sin reordenar: S y T en diapositiva 2; A en 3–5; R en 6–10. La portada identifica el trabajo.

## Matriz previa a la edición

Las referencias D1–D10 significan las diapositivas de la presentación CONACIC final, acompañadas de su PDF. Son las fuentes científicas prevalentes. Las referencias complementarias solo documentan procedencia, sin nuevos cálculos.

| Slide CONACIC | Contenido actual | Fuente científica | Relación con ENSIU | Conservar / adaptar / omitir | Motivo |
| --- | --- | --- | --- | --- | --- |
| 1 | Título científico, dos autores, afiliación | D1; comunicación ENSIU, encabezado y §1 | Título registrado y Misión 4 | Adaptar identidad y título; conservar autores, afiliación, panel y posición | Presentar la misma investigación bajo la inscripción ENSIU |
| 2 | Problema de disponibilidad de resultados y objetivo de estimación | D2; comunicación, S y T | Datos para la equidad | Conservar ambos textos; añadir en el cuadro vacío “Datos para la equidad: información pública con lectura territorial.” | Explicitar la línea sin sustituir el problema ni el objetivo |
| 3 | 127.716 filas; distribución 2020–2024; unidad institución/programa/prueba/año | D3; gráfico nativo y libro incrustado | Datos abiertos del ICFES | Conservar contenido y gráfico; adaptar solo identidad | Ya responde a la comunicación |
| 4 | 98.954 filas train 2020–2023; 28.762 test 2024; exclusión de información contemporánea; rezagos | D4; guion científico final | IA evaluada con control metodológico | Conservar contenido y formas; adaptar solo identidad | Preservar las cautelas y cifras |
| 5 | Ridge, Lasso, LightGBM, Transformer y diferencias de entradas | D5 | IA aplicada | Conservar contenido; adaptar solo identidad | Evitar superioridad universal o comparación no matizada |
| 6 | Dispersión LightGBM; RMSE 9,33; MAE 6,21; R² 0,706; n = 28.762 | D6 y su imagen original | Resultado predictivo | Conservar íntegro; adaptar solo identidad | No cambiar métricas ni gráfico |
| 7 | Tabla editable de los cuatro modelos y conclusión para el test 2024 | D7; valores de la tabla original | Comparación evaluada | Conservar íntegro; adaptar solo identidad | Mantener todos los decimales, incluido n/d del MAE Transformer |
| 8 | SHAP, tres rezagos y advertencia no causal | D8 y su imagen original | Interpretabilidad responsable | Conservar íntegro; adaptar solo identidad | La cautela ya está correctamente expresada |
| 9 | Gráfico de RMSE por NBC; cifras departamentales; límites | D9; imagen original NBC; comunicación §1 y R | Sistematización territorial y error heterogéneo | Conservar íntegro; adaptar solo identidad | El gráfico izquierdo es por NBC; los números derechos son por departamento. Se aclara oralmente, sin sustituir figuras |
| 10 | Tres conclusiones y frase de trabajo futuro | D10; comunicación §1 y R | Uso futuro con enfoque de equidad | Conservar las tres conclusiones; adaptar únicamente la última frase | Hacer explícita la equidad como evaluación pendiente |

Texto nuevo de la frase final de D10: “Trabajo futuro: validación walk-forward, mejores datos y evaluación institucional con enfoque de equidad territorial.” Se admite dos líneas dentro del espacio inferior existente si es necesario. No se altera ninguna conclusión científica.

Portada: “Anticipar para Incluir: Inteligencia Artificial al Servicio de la Equidad Educativa”. Se reutiliza el cuadro inferior vacío para “Misión 4 — Inteligencia Artificial para la equidad” y la identificación del programa de Edwin: Especialización en Inteligencia Artificial, código 1071010. El programa se atribuye solo a Edwin.

**Clasificación solicitada antes de generar:** cero diapositivas literalmente idénticas (todas requieren retirar identidad); siete con contenido idéntico y cambios visuales únicamente (3, 4, 5, 6, 7, 8, 9); tres con cambios locales de texto (1, 2, 10). Cero omitidas o reordenadas. Esta matriz se mostró al usuario en el chat antes de la generación.

## Cambios compartidos del patrón

- Retirar físicamente logos CONACIC, UADY y SiMCise, así como el texto vertical SIMULTÁNEA y los medios exclusivos del evento anterior; no ocultarlos bajo rectángulos.
- Sustituirlos por archivos oficiales ENSIU y UNIMINUTO sin deformarlos.
- Conservar fondo genérico de IA, barras, paneles, tipografía y posiciones. El fondo original no contiene logos ni palabras del evento.
- Cambiar pies a ENSIU 2026 y conservar numeración. Añadir notas de ponente con explicación y procedencia; estas notas no añaden contenido proyectado.
- Mantener íntegros los tres gráficos científicos incrustados, el gráfico nativo anual y la tabla editable.

## Control de lenguaje

RMSE se explica como raíz del promedio de errores al cuadrado y una medida que penaliza más los errores grandes, nunca como margen garantizado. MAE es el promedio de las distancias absolutas. R² compara el error cuadrático con una referencia basada en el promedio observado, no es porcentaje de aciertos. SHAP describe contribuciones predictivas, no causalidad. Rezagos son observaciones previas disponibles, no necesariamente el año calendario inmediatamente anterior.

Sucre ≈13, Chocó ≈12 y Putumayo ≈11 son errores descriptivos. No prueban una causa económica, brechas socioeconómicas ni necesidad de intervención por sí solos. No se presentan flags empíricos como intervalos calibrados. La intervención curricular y el impacto institucional continúan pendientes de validación.

## Duración y conflicto con las reglas oficiales

Los TDR oficiales, §5 (p. 5), establecen seis minutos: cinco STA orales **sin diapositivas** y uno de video R. La adenda del 3 de septiembre mantiene las modalidades y sitúa Misión 4 el 2 de octubre, 100% virtual. Por tanto, el deck solicitado se conserva como material completo para preparación o para uso si el organizador/asesora confirma una excepción. No se reduce arbitrariamente a partir del tiempo oficial, porque ese formato no prevé proyectar slides.

Se entregará un guion principal por las diez diapositivas, con duración estimada cercana a nueve minutos, y dentro del mismo archivo una versión oral STA de hasta cinco minutos, enlazada al audiovisual R existente de 60 s. Ambos usos se distinguen claramente. No se modifica el clip existente.

La programación incluye a Nathalia Orozco Morales y el semillero coincidente el 2/10/2026, bloque 4 ENSIU, 11:10 a. m.–12:00 m., virtual. No aparece Edwin ni el título y no hay hora individual. No se atribuye automáticamente esa fila al trabajo: corresponde confirmar la inscripción y quién presenta.

## Entrega y QA

Crear los seis entregables solicitados (plan, revisión oficial, PPTX, PDF, guion, revisión final), archivar fuentes oficiales consultadas con URLs y SHA-256, y conservar código de adaptación y comprobación dentro de ENSIU. Renders y pruebas privadas bajo `build/ensiu2026/` (ya ignorado por Git).

Exportar PDF directamente del PPTX final. Renderizar todas las diapositivas, inspeccionar cada una y comparar con CONACIC. Comprobar ausencia de marcas en texto, patrón y medios; cifras, autoría, equivalencia, gráficos sin cambios y límites científicos. Verificar por hashes que todos los originales siguen intactos.

Antes del commit: mostrar `git status`, `git diff --stat` y `git diff --name-status`, con la lista exacta de archivos nuevos. Commit solicitado: `feat(ensiu): prepare final 2026 presentation`. Push únicamente a `origin/feat/ensiu-2026-presentacion-final`.
