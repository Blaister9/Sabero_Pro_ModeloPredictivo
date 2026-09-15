# Guía de ensayo y grabación CONACIC 2026

**DRAFT. No se ha generado el video definitivo.** La presentación de investigación es independiente del audiovisual ENSIU. No usa su narración, su estructura de 60 segundos ni sus escenas.

## Ensayo

1. Abrir `PRESENTACION_CONACIC2026.pptx` en modo presentación y `GUION_PONENCIA_8MIN.md` en otra pantalla o impreso.
2. Ensayar una vez sin grabar. Usar los puntos de señalamiento del guion, sin leer cifras completas de cuatro decimales.
3. Grabar una toma de ensayo y anotar inicio y fin de cada bloque. El plan suma 08:30, con 1.162 palabras. A 145 palabras por minuto el habla ocupa unos 8 minutos, dejando unos 30 segundos para pausas. La duración real aún no está medida.
4. Objetivo: entre 08:00 y 09:00. Reservar margen antes del máximo de 10 minutos, incluyendo saludo, cambios de diapositiva y agradecimiento.
5. Si un bloque excede su tiempo, simplificar la explicación con la asesora o ajustar el cronometraje. No acelerar la voz ni cortar el final de una frase.

## Voz real intercambiable

Grabar un archivo por diapositiva: `01.wav` a `10.wav`. WAV PCM, mono, 48 kHz, 16 o 24 bits. Conservar una toma original. Dejar alrededor de 0,3 s antes de comenzar y 0,5 s al terminar. Micrófono a unos 15–20 cm, habitación silenciosa, nivel sin saturación. Escuchar con audífonos antes de montar.

Guardar voz definitiva de Santiago en `audio/voz_real/`. Una narración preliminar, si se decide producirla, iría en otra carpeta con la misma numeración. El ensamblador recibe `--audio-dir`: cambiar esa ruta sustituye toda la voz; reemplazar `06.wav` sustituye solo la sección 6. No hay que modificar las imágenes. La participación de Nathalia se integra con la misma numeración después de acordarla.

## Montaje preparado

`escenas/01.jpg` a `10.jpg` son exportaciones Full HD de las diapositivas revisadas. `CRONOMETRAJE.json` es la fuente de tiempos y narración. `STORYBOARD_Y_TRANSICIONES.md` indica el punto visual que acompaña cada bloque. Todas las escenas conservan la marca DRAFT.

Desde la raíz del repositorio, con Python y FFmpeg disponibles:

```powershell
python outputs/CONACIC2026/fuentes/ensamblar_preview.py --check
python outputs/CONACIC2026/fuentes/ensamblar_preview.py --audio-dir outputs/CONACIC2026/audio/voz_real --dry-run
python outputs/CONACIC2026/fuentes/ensamblar_preview.py --audio-dir outputs/CONACIC2026/audio/voz_real --output outputs/CONACIC2026/PREVIEW_RITMO.mp4
```

El script solo genera PREVIEW, lo marca visualmente, rechaza sobreescrituras y exige diez audios. Extiende cada escena si la voz dura más que el tiempo previsto, añade margen final y rechaza un total superior a 600 s. No recorta frases, ni acelera audio, ni sube archivos. La validación final con ffprobe comprueba formato, resolución y duración. Si el ritmo es correcto, conservar el reporte de duración y escuchar todo el archivo.

Las tomas de audio y futuros MP4 quedan ignorados en Git. No se ha producido voz sintética ni un preview de duración completa en esta fase. Solo se prueba técnicamente el ensamblador con un clip de control en el directorio temporal.

## Configuración MP4 recomendada

| Parámetro | Valor preparado |
|---|---|
| Contenedor | MP4, faststart |
| Video | H.264 / libx264, 1920 × 1080, 30 fps, yuv420p |
| Calidad | CRF 18, preset medium, imagen estática sin animaciones |
| Audio | AAC, 48 kHz, 192 kb/s, normalización de escucha |
| Transición | Corte simple entre diapositivas; sin fundidos que cambien tiempos |
| Duración objetivo | 510 s; confirmar con voz real |
| Máximo informado | 600 s, incluida portada y cierre |

Si se graba cámara, colocarla sin tapar gráficas, tabla, autores ni logos. Definir primero con Nathalia si se requiere aparición en pantalla; no consta exigencia verificada del comité.

## Paso al definitivo

Solo después de revisión con Nathalia, revisión de similitud e IA y aprobación del contenido: incorporar correcciones, regenerar y revisar PPTX/PDF, volver a exportar escenas, grabar las tomas aprobadas y ensayar. Retirar las marcas DRAFT/PREVIEW únicamente en esa nueva fase. El ensamblador actual está limitado deliberadamente a previews. La plataforma, visibilidad y enlace se decidirán con las instrucciones finales del comité. No existe todavía enlace de video ni evidencia de envío.
