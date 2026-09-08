# Montaje final con la grabación real

Archivo para subir a YouTube: `AUDIOVISUAL_ENSIU2026_FINAL_YOUTUBE.mp4`. Video H.264, 1920 × 1080, progresivo, 30 fps constantes, 1800 fotogramas y 60,000 s. Audio AAC estéreo de 48 kHz copiado directamente de `Grabación (14).m4a`, sin recodificar. El archivo M4A original se conserva completo dentro de `audio/`.

## Reconstrucción exacta

Desde PowerShell en el repositorio, ejecutar:

```powershell
& 'C:\Users\santi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.\outputs\ENSIU2026\ENSAMBLAR_VIDEO.py'
```

Requiere Python 3 y FFmpeg/FFprobe. Usa únicamente los ocho PNG y el M4A entregados, sin conexión ni síntesis de voz. El script sobrescribe el MP4 final y sus informes de verificación dentro de esta entrega. Conserva el audio desde t=0 hasta 53,247771 s y la imagen hasta 60 s. No usar `-shortest`, filtros de audio, `atempo`, normalización, eliminación de silencios ni conversión a WAV para el montaje final.

## Marcas visuales

| Escena | Inicio | Final | Fotograma inicial | Contenido |
|---|---|---|---|---|
| 1 | 0,000 s | 3,600 s | 0 | La pregunta |
| 2 | 3,600 s | 6,500 s | 108 | La posibilidad |
| 3 | 6,500 s | 17,000 s | 195 | Los datos |
| 4 | 17,000 s | 32,200 s | 510 | La evidencia |
| 5 | 32,200 s | 40,100 s | 966 | El territorio |
| 6 | 40,100 s | 50,267 s | 1203 | La alerta |
| 7 | 50,267 s | 53,267 s | 1508 | La equidad |
| 8 | 53,267 s | 60,000 s | 1598 | La firma |

Cada transición comienza en la marca de entrada y dura 0,30 s. Para hacer el montaje manual, usar dos pistas de imagen alternadas. Prolongar la imagen anterior 0,30 s sobre el inicio de la siguiente; animar la opacidad de la siguiente de 0 a 100 %. El último plano termina en 60 s, sin negro final ni cola adicional. La firma final entra en el fotograma 1598 (53,266667 s), inmediatamente después del final del archivo de narración.

La narración manda sobre los tiempos del montaje anterior: no se fuerza a encajar en las antiguas marcas de voz sintética. El PPTX mantiene exactamente sus composiciones y tiene los nuevos avances automáticos; el PDF no cambia. Los fundidos se añaden en el MP4. El audio no está incrustado en el PPTX: se integra desde el M4A mediante copia directa en FFmpeg.

## Comprobación y subida

El montaje verifica los 1800 fotogramas y los 60 s. También compara los hashes de cada paquete AAC y el hash PCM decodificado de origen y salida: ambos deben coincidir. `VERIFICACION_AUDIO_ORIGINAL.json` registra la comprobación. El archivo utiliza `faststart` para facilitar la reproducción mientras se descarga.

Reproducir el archivo final con sonido y subir ese MP4 a YouTube. Revisar la vista previa después de que la plataforma termine de procesarlo. No es necesario publicar el PPTX, PDF ni los archivos de montaje. El SRT auxiliar se puede cargar por separado si se desean subtítulos; el video no los lleva impresos.
