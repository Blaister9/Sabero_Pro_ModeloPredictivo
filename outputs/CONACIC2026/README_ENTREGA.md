# Preparación de entrega CONACIC 2026

**Paper 17 — ACEPTADO SIN OBSERVACIONES. Paquete DRAFT de revisión. No enviado.**

El cierre está condicionado a recibir y revisar los análisis de similitud e IA, resolver los hallazgos de auditoría y aprobar el contenido con Nathalia. No se ha generado el video definitivo.

## Archivos para revisar

| Archivo | Propósito |
|---|---|
| [AUDITORIA_CAMERA_READY.md](AUDITORIA_CAMERA_READY.md) | Base aceptada, contraste reproducible y pendientes reales |
| [CAMERA_READY_DRAFT.docx](CAMERA_READY_DRAFT.docx) | Copia editable en plantilla A&A, con autoría y correos |
| [CAMERA_READY_DRAFT.pdf](CAMERA_READY_DRAFT.pdf) | Exportación Word para revisión de las 10 páginas |
| [PRESENTACION_CONACIC2026.pptx](PRESENTACION_CONACIC2026.pptx) | Diez diapositivas en plantilla oficial, con notas |
| [PRESENTACION_CONACIC2026.pdf](PRESENTACION_CONACIC2026.pdf) | Revisión de diapositivas exportadas desde PowerPoint |
| [GUION_PONENCIA_8MIN.md](GUION_PONENCIA_8MIN.md) | 1.162 palabras, 08:30 planificados, puntos de señalamiento |
| [STORYBOARD_Y_TRANSICIONES.md](STORYBOARD_Y_TRANSICIONES.md) | Sincronización de las diez escenas |
| [GUIA_GRABACION_MP4.md](GUIA_GRABACION_MP4.md) | Ensayo, voz reemplazable y montaje Full HD |
| [REUNION_ASESORA.md](REUNION_ASESORA.md) | Decisiones abiertas y preguntas técnicas del congreso |
| [VERIFICACION_VISUAL.md](VERIFICACION_VISUAL.md) | Revisión por página/diapositiva y límites de verificación |

## Checklist de cierre

- [x] Base aceptada identificada y confirmada por Santiago: archivo `_FINAL` de `entrega_congreso`.
- [x] Auditoría realizada antes de modificar la copia.
- [x] Original aceptado preservado, con SHA-256 registrado.
- [x] Autores: Edwin Santiago Paz Bedoya y Nathalia Orozco Morales.
- [x] Institución para ambos: UNIMINUTO Virtual – Bogotá, Colombia, confirmada por Santiago.
- [x] Correos confirmados e incorporados: edwin.paz@uniminuto.edu y nathalia.orozco@uniminuto.edu.
- [x] Plantilla oficial A&A descargada del enlace actual del congreso.
- [x] DOCX y PDF DRAFT con 10 páginas, cinco figuras y una tabla.
- [ ] Conformidad final de Nathalia sobre ficha institucional y título.
- [ ] Camera ready aprobado para envío, retirando DRAFT solo después de resolver todos los pendientes.
- [ ] Análisis de similitud recibido, revisado y con acciones documentadas.
- [ ] Análisis de IA recibido, revisado y con acciones documentadas.
- [ ] Hallazgos de validación interna, codificación, MAE, alcance y bibliografía resueltos (ver auditoría).
- [ ] Requisito de clasificación MSC y metadatos editoriales confirmado si aplica.
- [x] Presentación construida con el PPTX oficial de Ponencias Simultáneas enlazado actualmente.
- [x] Guion académico por diapositiva; duración planificada de 08:30.
- [ ] Ensayo cronometrado con voz real completado.
- [ ] Participación de Nathalia en voz/cámara y orden final acordados.
- [x] Storyboard, escenas Full HD y ensamblador de PREVIEW preparados.
- [ ] Video MP4 definitivo, máximo 10 minutos, aprobado y revisado de principio a fin.
- [ ] Modalidad, plataforma y visibilidad del video confirmadas.
- [ ] Enlace de video generado y accesibilidad comprobada.
- [ ] Requisitos institucionales UNIMINUTO revisados.
- [ ] Zona horaria y canal de entrega comprobados en la comunicación final.
- [ ] DOCX final entregado antes del **20 de septiembre de 2026, 23:59**, según correo aportado.
- [ ] Video/enlace entregado antes del **23 de septiembre de 2026, 23:59**, según correo aportado.
- [ ] Evidencia de envío guardada (recibo/acuse y fecha). Actualmente **no existe**.

## Fechas y fuentes

Los plazos del 20 y 23 de septiembre provienen del correo transcrito por el usuario. No se infiere su zona horaria. La [convocatoria pública](https://conacic.siycise.org/convocatoria) conserva una fecha general distinta (31 de agosto), y especifica un máximo de diez páginas. Se toma el correo particular como instrucción operativa, dejando visible la diferencia.

Las plantillas se descargaron el 14 de septiembre de 2026 (Bogotá) desde [Recursos y Plantillas de CONACIC](https://conacic.siycise.org/). Se conserva el PPTX cuyo nombre incluye 2024, porque es el archivo enlazado actualmente. URLs y hashes en `plantillas_oficiales/PROCEDENCIA.json`.

## Alcance y conservación

Rama: `feat/conacic-2026-camera-ready`, desde `a5c831e`. Sin merge a main, sin push, sin correos, sin cargas web. Stash existente conservado. Los entregables ENSIU y los cambios locales en sus MP4 no forman parte del commit de esta fase.

Se preservan las cifras científicas aceptadas. El resultado LightGBM se reprodujo con el modelo local. Las diferencias detectadas están explícitas y no se ocultaron con reentrenamiento. El contenido del DOCX conserva pendientes científicos para revisión; su marca DRAFT es sustantiva, no una formalidad.

## Reproducción de esta preparación

Los scripts de `fuentes/` documentan la generación y no reescriben las fuentes aceptadas. `build_camera_ready.py` usa OOXML de la plantilla oficial; `render_word.py` usa el rasterizador de la habilidad de documentos con conversión Word nativa, porque no está instalado LibreOffice. `build_deck.mjs` importa el PPTX oficial con Artifact Tool y pasa validación de estructura, geometría, tabla y gráfica editables. `contenido_ponencia.py` regenera guion y tiempos. Para reconstruir slides, proporcionar las rutas de runtime y habilidad indicadas en `fuentes/REPRODUCIR.md`.
