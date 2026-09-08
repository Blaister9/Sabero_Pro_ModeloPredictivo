# Animaciones y transiciones exactas

El MP4 utiliza un fundido cruzado lineal de 0,30 s (9 fotogramas) en cada cambio de escena. Los gráficos originales permanecen completos y fijos: no se dibujan puntos ficticios ni se modifican valores. El video no requiere música ni tomas de campus. La voz se mantiene continua mediante la pista de 60 segundos.

| Cambio | Inicio del fundido | Fin del fundido | Fotogramas de transición (base cero) |
|---|---|---|---|
| E1 a E2 | 06,30 s | 06,60 s | 189–197 |
| E2 a E3 | 10,00 s | 10,30 s | 300–308 |
| E3 a E4 | 17,00 s | 17,30 s | 510–518 |
| E4 a E5 | 26,00 s | 26,30 s | 780–788 |
| E5 a E6 | 40,00 s | 40,30 s | 1200–1208 |
| E6 a E7 | 49,30 s | 49,60 s | 1479–1487 |
| E7 a E8 | 53,20 s | 53,50 s | 1596–1604 |

Entre cambios, mantener la composición sin zoom ni paneo. La primera imagen está visible desde el fotograma 0. No añadir entrada desde negro ni salida a negro. La última escena permanece hasta el fotograma 1799; el archivo termina en 60,000 s.

En el PPTX, cada diapositiva tiene avance automático con la duración nominal indicada en el storyboard y sin transición interna. Los fundidos del MP4 se aplican durante el montaje para controlar exactamente su duración. Los PNG de `escenas/` son las composiciones asentadas exportadas por PowerPoint. La voz se entrega como WAV externo; no está incrustada en el PPTX.

Para replicar el MP4, no sumar siete fundidos al minuto. Cada escena anterior conserva 0,30 s de margen sobre el cambio, y la siguiente se superpone durante esos mismos 0,30 s. El script `ENSAMBLAR_VIDEO.py` implementa ese solapamiento y corta el resultado a 1800 fotogramas. Si se trabaja en un editor con fundidos centrados, mover cada transición para que empiece en la marca de la tabla, no en la mitad de ella.
