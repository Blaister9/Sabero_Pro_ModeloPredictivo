# Reproducir los artefactos de preparación

Ejecutar desde la raíz del repositorio. Los scripts no envían ni publican nada. No ejecutar las fases generales del proyecto para reconstruir esta entrega: esas fases sobrescriben reportes históricos.

## Runtime usado

- Python: `C:/Users/santi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
- Node: `C:/Users/santi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`.
- Paquetes Node: `C:/Users/santi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`.
- Microsoft Word y PowerPoint instalados en Windows, mediante COM, solo para conversión de copias a PDF y PNG.
- FFmpeg y ffprobe disponibles en PATH.

## Fuentes y pasos

1. Conservar las plantillas descargadas y verificar sus hashes en `plantillas_oficiales/PROCEDENCIA.json`.
2. Ejecutar `fuentes/contenido_ponencia.py` para regenerar `CRONOMETRAJE.json`, guion y storyboard.
3. Ejecutar `fuentes/build_camera_ready.py` para regenerar el DOCX DRAFT a partir de la plantilla retenida y la base aceptada. Sus correcciones de párrafo son explícitas, sin reescritura del original. Guarda `CAMBIOS_CAMERA_READY.json`.
4. Para el DOCX, invocar `fuentes/render_word.py` con cuatro argumentos: ruta DOCX, carpeta nueva de render, carpeta de habilidad `documents`, carpeta `native/poppler/Library/bin` del runtime. Usa `render_docx.py` y cambia únicamente el convertidor a PDF por Word, tras diagnóstico de falta de LibreOffice. Copiar el PDF resultante al nombre de entrega y revisar todas sus páginas.
5. Copiar `fuentes/build_deck.mjs` a `tmp/conacic2026/`, con un enlace `node_modules` hacia los paquetes del runtime. Definir `RUNTIME_NODE_MODULES`, `CONACIC_RUNTIME_PYTHON` y `CONACIC_PRESENTATIONS_SKILL` con las rutas del runtime y habilidad instalada. Definir `CONACIC_FINAL_PPTX` con una ruta nueva y `CONACIC_RECEIPT` con otra ruta nueva fuera de la carpeta del PPTX. Ejecutar con Node del runtime. El finalizador no sobrescribe el PPTX ni el recibo existentes: conservar las versiones anteriores y usar rutas nuevas para cada revisión, luego copiar la versión elegida a los nombres de entrega. El recibo verifica el hash de esos mismos bytes aunque registre la ruta temporal de generación.
6. Exportar el PPTX final desde PowerPoint a PDF y PNG 1920×1080. Revisar las diez diapositivas. Las escenas JPG se generan de esos PNG, calidad 95, conservando 1920×1080, sin recortes de los gráficos.
7. Para recalcular la auditoría con modelos locales, ejecutar `fuentes/verificar_modelos.py`. Requiere los tres PKL y el CSV procesado. No entrena modelos. Los PKL no se incluyen en Git y no deben descargarse de fuentes desconocidas para ejecutarlos.
8. Ejecutar `fuentes/verificar_paquete.py` para comprobar consistencia y hashes de conservación, y `fuentes/ensamblar_preview.py --check` para comprobar preparación audiovisual. La generación completa del preview requiere diez WAV. Nunca se confunde este preview con el video definitivo.

La gráfica editable de cobertura anual contiene una copia de sus cinco recuentos comprobados en CSV, con un libro de datos embebido. No representa una nueva ejecución de entrenamiento. Las otras gráficas son las imágenes originales del proyecto, embebidas sin regenerar resultados. Los masters, fondos, logos y dimensiones proceden del PPTX oficial importado.

La tabla del artículo se ajustó al ancho útil de 8.838 twips para respetar los márgenes. Se normalizó el texto de los encabezados corridos y el campo PAGE, conservando el logo de primera página y la geometría de sección. Estas son correcciones de formato registradas, no cambios de resultados.
