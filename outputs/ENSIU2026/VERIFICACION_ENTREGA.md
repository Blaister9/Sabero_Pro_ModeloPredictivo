# Verificación de la entrega

- Ocho escenas exportadas mediante PowerPoint y revisadas individualmente. PDF de ocho páginas renderizado y revisado, con inspección ampliada de las páginas de resultados.
- PPTX con texto y tabla comparativa nativos editables; figuras originales incrustadas. Avances automáticos suman 60 s. Paquete y geometría validados después del guardado final en PowerPoint.
- Video final H.264: 1920 × 1080, 30 fps, 1800 fotogramas y 60,000 s. Audio AAC de 60,000 s. Subtítulos opcionales actualizados; datos técnicos en VERIFICACION_VIDEO.json.
- Inspección de fotogramas decodificados del MP4, incluidos resultados y último fotograma. No se detectaron cortes de texto, elementos fuera del lienzo ni pérdida de las cifras destacadas.
- Pista WAV: 2.880.000 muestras a 48 kHz, 60,000 s. Fragmentos suman 50,745 s. Guion final 122 palabras. El audio conserva al menos 0,11 s después de la última actividad de cada fragmento medida con umbral RMS de −42 dBFS. No se recortan finales de voz detectables a ese umbral.
- Sonoridad medida del MP4: −16,7 LUFS integrada, pico verdadero −1,4 dBFS. Las marcas de palabras son del sintetizador; se recomienda la revisión auditiva humana previa al envío.
- Conteos, métricas LightGBM y jerarquía SHAP contrastados con los artefactos; diferencias narrativas documentadas en AUDITORIA_CONSISTENCIA.md. Los hashes de todas las fuentes verificadas permanecen iguales.
- Storyboard con 60 filas de segundos, guion por escena y guía de transiciones coherentes con CRONOMETRAJE.json. El script de montaje se ejecutó correctamente.

El validador geométrico produjo una advertencia preventiva de altura estimada en la tabla de la escena 4. La exportación real de PowerPoint y el PDF muestran la tabla completa, separada de la nota inferior, sin solapamiento.
