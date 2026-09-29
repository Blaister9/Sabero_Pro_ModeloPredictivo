# Adaptación mínima y verificación ENSIU final

Estos archivos documentan la edición puntual del paquete PowerPoint original. No contienen entrenamiento, inferencia ni nuevos cálculos de métricas.

## Herramientas utilizadas

- Node.js 24 del runtime incluido en Codex, con `@oai/artifact-tool` y `jszip`.
- Python incluido en Codex, con `lxml`, `Pillow`, `PyMuPDF` y `pywin32`.
- Microsoft PowerPoint 16.0 instalado en el equipo, para exportar el PDF y los PNG.
- Validadores de integridad, geometría y gráfico nativo del skill Presentations.

`adaptar_presentacion.mjs` importa e inspecciona con Artifact Tool, luego realiza cambios locales en OOXML. Esta decisión conserva exactamente la tabla, el gráfico editable y su libro incrustado, las imágenes y las coordenadas del resto de objetos. No se convierte cada diapositiva en una imagen ni se reconstruye una plantilla equivalente. `validar_presentacion.mjs` aplica los validadores al candidato y copia el archivo aprobado al destino final.

## Entradas preservadas

Base: `outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx`. Su SHA-256 es `2bff0a2a7b0f4562ed2940ea51dea1024ae266cf5f55e47de0f6972eeabecf6a`.

Logos: `docs/ENSIU2026/fuentes_oficiales/`, con origen en su manifiesto. Textos de notas: versión A del guion final. `ORIGINALES_SHA256.json` registra los 182 archivos versionados del HEAD inicial para detectar modificaciones no autorizadas.

## Ejecución desde la raíz del worktree

Las rutas del runtime y del skill en `validar_presentacion.mjs` corresponden a este equipo. Si cambia su instalación, resolverlas primero con el inventario de dependencias de Codex. No instalar ni modificar las dependencias para reproducir este paquete.

```powershell
$env:RUNTIME_NODE_MODULES='C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
$env:PYTHONIOENCODING='utf-8'
& 'C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' outputs/ENSIU2026/fuentes_final/adaptar_presentacion.mjs
& 'C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' outputs/ENSIU2026/fuentes_final/validar_presentacion.mjs
& 'C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' outputs/ENSIU2026/fuentes_final/exportar_y_verificar.py
```

El candidato y los renders van a `build/ensiu2026/`, ignorado por Git. El finalizador **rechaza sobrescribir** el PPTX final existente: para una revisión posterior, elegir un nuevo nombre de salida en el script y ajustar el exportador. No borrar originales para eludir esta protección. El exportador abre las presentaciones en modo de solo lectura y cierra exclusivamente las que abrió.

El PDF puede tener metadatos de exportación distintos en otra ejecución. Los hashes archivados describen la entrega inspeccionada, no prometen exportación binaria idéntica en cualquier versión de Office.

## Qué comprueban los controles

`exportar_y_verificar.py` valida hashes originales, cambios textuales permitidos, eliminación de medios de marca anterior, identidad binaria de las partes científicas, tabla y libro originales, contenido esperado del PDF y equivalencia de las áreas de contenido de D3–D9 en renders PowerPoint. El script genera `build/ensiu2026/verificacion.json` y `text_geometry.json`. `VERIFICACION_FINAL.json` es la evidencia archivada de la entrega actual.

La revisión visual individual y las cautelas de interpretación están documentadas en `REVISION_PRESENTACION_ENSIU2026_FINAL.md`. Los controles estructurales no sustituyen esa revisión ni comprueban aceptación de la organización. El permiso de proyectar las diapositivas y el turno individual siguen sujetos a confirmación con Nathalia.
