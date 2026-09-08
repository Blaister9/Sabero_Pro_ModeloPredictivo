# Guía de montaje ENSIU 2026

El video ya está ensamblado: `AUDIOVISUAL_ENSIU2026_60s.mp4`. Es la versión de prueba utilizable de 60,000 s, Full HD, H.264, 30 fps, audio AAC en español y subtítulos opcionales. Para enviarlo sin cambios, reproducirlo con sonido y subir ese archivo al canal de la convocatoria. Conservar el PPTX y el PDF como soportes; no son el archivo audiovisual.

## Reconstruir automáticamente el mismo montaje

Requisitos locales: Python 3 y FFmpeg/FFprobe. El montaje usa únicamente archivos entregados y no necesita conexión a Internet ni volver a sintetizar la voz.

1. Abrir PowerShell en `C:\Users\santi\Documents\Sabero_Pro_ModeloPredictivo`.
2. Ejecutar:

```powershell
& 'C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.\outputs\ENSIU2026\ENSAMBLAR_VIDEO.py'
```

El script sobrescribe solo el MP4 y su comprobación técnica dentro de esta entrega. Valida 1800 fotogramas, 30 fps y 60,000 s de imagen y audio; si una comprobación falla, muestra un error. Si el runtime de Codex se mueve, sustituir únicamente la ruta inicial por el Python instalado.

## Si se modifica la presentación

1. Abrir `PRESENTACION_ENSIU2026.pptx` y editar el texto o la tabla. Las figuras del proyecto son PNG incrustados: para cambiarlas, sustituirlas por un gráfico realmente respaldado por el proyecto.
2. Conservar ocho diapositivas, formato 16:9, y la tipografía Aptos. No alterar las cifras sin volver a auditarlas.
3. Exportar las diapositivas modificadas como PNG de 1920 × 1080. Reemplazar `escenas/escena_01.png` a `escena_08.png`, conservando nombres y orden. También actualizar el PDF desde PowerPoint.
4. Ejecutar el comando anterior para reconstruir el video. Si cambia la locución, actualizar el WAV continuo, el SRT y `CRONOMETRAJE.json` antes de hacerlo.

## Montaje manual en un editor de video

Crear una secuencia 1920 × 1080, 30 fps constantes, duración 00:01:00:00. Importar los ocho PNG, `audio/VOZ_ENSIU_60s.wav` y `SUBTITULOS_ENSIU.srt`. Colocar el WAV en 00:00:00:00, volumen 0 dB: ya está normalizado. Desactivar cualquier ajuste automático que recorte silencios, cambie velocidad, añada cierre o mueva clips. Colocar las imágenes en estas marcas:

| PNG | Inicio de escena | Fin nominal | Duración nominal | Inicio en fotogramas |
|---|---|---|---|---|
| escena_01.png | 00,00 s | 06,30 s | 06,30 s | 0 |
| escena_02.png | 06,30 s | 10,00 s | 03,70 s | 189 |
| escena_03.png | 10,00 s | 17,00 s | 07,00 s | 300 |
| escena_04.png | 17,00 s | 26,00 s | 09,00 s | 510 |
| escena_05.png | 26,00 s | 40,00 s | 14,00 s | 780 |
| escena_06.png | 40,00 s | 49,30 s | 09,30 s | 1200 |
| escena_07.png | 49,30 s | 53,20 s | 03,90 s | 1479 |
| escena_08.png | 53,20 s | 60,00 s | 06,80 s | 1596 |

Para los fundidos exactos, usar dos pistas de video alternadas. Prolongar cada PNG salvo el último 0,30 s después de su fin nominal. Colocar el siguiente en su inicio nominal; animar su opacidad de 0 a 100 % durante 0,30 s, sobre el anterior. El último termina exactamente a 60 s. No dejar huecos entre imágenes. Añadir el SRT como pista opcional, no quemarlo sobre las figuras si tapa sus rótulos.

Exportar un MP4 H.264, 1920 × 1080, 30 fps constantes, calidad alta (CRF 18 si está disponible), píxel yuv420p, audio AAC 48 kHz y 192 kbps. Fijar el rango de salida de 0 a 60 s, sin cola. El reproductor puede mostrar «1:00» redondeado; verificar con FFprobe:

```powershell
& 'C:\ffmpeg\bin\ffprobe.exe' -v error -show_entries 'format=duration:stream=codec_type,duration,nb_frames,r_frame_rate' -of json '.\outputs\ENSIU2026\AUDIOVISUAL_ENSIU2026_60s.mp4'
```

Esperado: duración 60.000000, video 1800 fotogramas y 30/1 fps, audio 60.000000. Comprobar también primera escena, cambio a sustento en 10 s, cambio a cierre en 40 s y firma final. Escuchar el minuto completo antes de enviar.

## Subida

Seleccionar `AUDIOVISUAL_ENSIU2026_60s.mp4` en el formulario o carpeta oficial que haya indicado ENSIU. Esperar a que termine la carga y reproducir la vista previa del archivo subido. Si el canal solicita un enlace, comprobar que el destinatario tenga permiso de lectura. No se presupone una plataforma ni una URL que no estén en la convocatoria recibida.
