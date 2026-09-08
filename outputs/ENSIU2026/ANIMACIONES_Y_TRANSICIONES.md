# Transiciones de la versión con voz real

Las composiciones originales permanecen intactas. Cada cambio del MP4 es un fundido cruzado de 0,30 s (9 fotogramas), sin zoom, paneo ni animaciones sobre los datos. Los nuevos tiempos siguen la grabación real.

| Cambio | Inicio | Final | Fotogramas (base cero) |
|---|---|---|---|
| E1 a E2 | 3,600 s | 3,900 s | 108–116 |
| E2 a E3 | 6,500 s | 6,800 s | 195–203 |
| E3 a E4 | 17,000 s | 17,300 s | 510–518 |
| E4 a E5 | 32,200 s | 32,500 s | 966–974 |
| E5 a E6 | 40,100 s | 40,400 s | 1203–1211 |
| E6 a E7 | 50,267 s | 50,567 s | 1508–1516 |
| E7 a E8 | 53,267 s | 53,567 s | 1598–1606 |

Mantener la última escena hasta el fotograma 1799 inclusive. La grabación termina en 53,247771 s; la firma entra en 53,266667 s y queda completamente asentada después del fundido de 0,30 s. El resto del cierre permanece silencioso y fijo. No añadir música, efectos sonoros, voz sintética ni salida a negro.

Los avances automáticos del PPTX coinciden con las duraciones nominales del storyboard. La reproducción final debe generarse con `ENSAMBLAR_VIDEO.py`, que añade los fundidos sin incrementar la duración total. La pista M4A se integra tal cual con `-c:a copy`.
