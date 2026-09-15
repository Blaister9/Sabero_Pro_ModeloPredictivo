# Revisión visual y técnica del paquete DRAFT

## Artículo

Se renderizó el DOCX con `render_docx.py`, usando un adaptador de conversión por Microsoft Word. El intento estándar falló porque no existe `soffice.exe` en este Windows; se conservaron los logs en el directorio temporal. Word exportó el PDF y Poppler produjo PNG a 130 dpi. Se inspeccionaron individualmente las diez páginas de la última revisión (`draft_render_v5`).

| Página | Elementos revisados | Resultado |
|---|---|---|
| 1 | Títulos bilingües, dos autores, afiliación, dos correos, abstracts, pie | Contenido legible; logo UADY preservado; DRAFT; sin fechas ficticias |
| 2 | Introducción y marco teórico, encabezado y numeración | Flujo continuo; sin cortes de texto ni encabezados huérfanos |
| 3 | Marco teórico y metodología de datos | Jerarquía de secciones legible; sin desbordes |
| 4 | Figura 1, caption, variables y modelos | Figura completa; caption unido; correcciones metodológicas visibles |
| 5 | Tabla 1 y curva de aprendizaje | Tabla ajustada a márgenes; cifras conservadas; filas completas |
| 6 | Scatter y SHAP con captions | Dos figuras completas; etiquetas originales conservadas |
| 7 | Error por NBC, confianza y discusión | Figura completa; título y caption presentes; sin texto cortado |
| 8 | Discusión y conclusiones | Continuidad legible; limitaciones y numeración presentes |
| 9 | Trabajo futuro, agradecimientos, referencias 1–11 | Jerarquía y bibliografía legibles; referencias enteras |
| 10 | Referencias 12–26 | Bibliografía completa; no existe página adicional |

Se conservan cinco figuras sin recomprimir sus archivos originales. Las etiquetas más densas de las figuras 1, 4 y 5 son pequeñas en impresión por la maquetación del artículo aceptado; pueden ampliarse en el PDF. No se declara una mejora de resolución que no se haya realizado. Los gráficos completos y su contenido relevante también se presentan en diapositivas. Esta limitación debe revisarse si el editor exige una tipografía mínima específica para figuras.

Carta 8,5 × 11 pulgadas; márgenes idénticos a plantilla: 0,984 pulgadas arriba/abajo y 1,18125 izquierda/derecha. La tabla aceptada sobresalía del ancho útil; se ajustó a 8.838 twips sin cambiar ninguna celda. Se normalizaron encabezados corridos con DRAFT y campo PAGE para impedir la pérdida de numeración. La primera página conserva el logo y el estilo oficial. Estilos, tema, numeración y medios originales de la plantilla están preservados según `VERIFICACION_PAQUETE.json`.

## Presentación

Se inspeccionaron las cinco diapositivas vacías de la plantilla: todas exportan el mismo fondo oficial. Se importó el PPTX original y se reutilizaron sus masters, layouts y cinco slides, ampliándolo a diez. No se reconstruyeron logos ni fondo. Dimensión: 12.192.000 × 6.858.000 EMU, equivalente a 16:9. Fuente de contenido: Gill Sans MT, definida en el tema oficial para títulos y cuerpo. Los paneles de contenido dejan visibles logos y franja lateral del diseño oficial.

Se abrió el PPTX generado mediante PowerPoint y se exportaron diez PNG 1920×1080 y PDF. Se inspeccionaron las diez imágenes individualmente:

| Diapositiva | Revisión |
|---|---|
| 1 | Título exacto completo, autoría y correos sin cortes |
| 2 | Objetivo y unidad de análisis legibles |
| 3 | Cinco recuentos anuales correctos, gráfica editable con libro embebido |
| 4 | Holdout externo y pendiente metodológico explícitos |
| 5 | Familias de modelos y 188 árboles finales sin sobreposición |
| 6 | Scatter original y métricas legibles |
| 7 | Tabla editable completa; MAE aceptados conservados |
| 8 | SHAP original completo y lectura principal de rezagos |
| 9 | Errores por NBC y cifras regionales con tamaños de grupo |
| 10 | Conclusiones y trabajo futuro, sin afirmaciones de despliegue |

Cada diapositiva tiene marca DRAFT, número y notas con bloque hablado, tiempo y fuente. El PDF tiene diez páginas. El finalizador verificó integridad, dimensiones, geometría y editabilidad de la tabla y gráfica. La revisión visual complementa esas pruebas; no equivale a aprobación científica.

## Guion y video

Guion: 1.162 palabras, diez bloques, 510 segundos planificados. No se ha medido duración con voz real. Escenas: diez JPG Full HD exportados de la presentación revisada. El ensamblador comprueba entradas, se limita a PREVIEW y rechaza sobreescritura o duración superior a 600 s.

Prueba técnica realizada con un clip temporal de control de 2 s, una escena y un tono de prueba: H.264, 1920×1080, 30 fps, yuv420p, AAC 48 kHz. Se verificó con ffprobe. No se generó voz sintética, preview completo ni video definitivo. La prueba corta valida codificación y marca visual; la sincronización del ensayo completo queda pendiente de diez tomas de voz.

## Límite de esta verificación

El paquete es revisable y sus archivos están preparados. Los hallazgos metodológicos/bibliográficos de `AUDITORIA_CAMERA_READY.md`, los análisis de similitud e IA y la aprobación final siguen abiertos. No hay evidencia de envío porque no se realizó ningún envío.
