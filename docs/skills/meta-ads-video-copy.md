# Meta Ads Video Copy

Skill local para generar copy de anuncios de Meta a partir de un video subido.

Convierte un video en:

- `5` primary texts
- `5` headlines
- `5` descriptions

El skill trabaja con tres fuentes al mismo tiempo:

- audio o transcript
- screenshots o frames extraídos
- metadata básica del video

No debe escribir copy basado solo en imágenes ni solo en audio. La salida debe salir de la intersección entre lo que se dice y lo que se ve.

## Qué resuelve

Este skill sirve cuando hay que tomar un video promocional, reel, UGC, tour de propiedad, demo o pieza hablada y convertirlo en textos listos para pegar en Meta Ads Manager.

Está pensado para:

- detectar hooks reales desde el audio
- validar claims con lo visible en pantalla
- generar ángulos distintos de prueba
- mantener límites de caracteres seguros para placements comunes

## Salida esperada

La salida final debe incluir:

- `5` primary texts de hasta `125` caracteres
- `5` headlines de hasta `40` caracteres
- `5` descriptions de hasta `25` caracteres

Cada línea debe incluir:

- el ángulo usado
- el texto final
- el conteo de caracteres

## Framework de trabajo

### 1. Analizar transcript y visuales

Primero se obtiene el transcript y luego se revisan frames o screenshots.

El transcript define:

- hook
- oferta
- objeciones
- CTA
- claims

Los visuales validan y enriquecen:

- tipo de producto o propiedad
- condición
- detalles visibles
- on-screen text
- prueba visual

Si hay conflicto entre audio y visual, el copy debe quedarse solo con lo que sí está respaldado.

### 2. Definir ángulos

Antes de escribir textos individuales, se definen entre `3` y `5` ángulos distintos.

Categorías comunes:

- pain point
- outcome
- social proof
- curiosity
- comparison
- urgency
- identity
- contrarian

### 3. Generar variaciones por ángulo

Para cada ángulo se exploran variaciones cambiando:

- word choice
- specificity
- tone
- structure

Luego se elige una versión final por ángulo para cada bloque.

## Dependencias

### Requeridas

- `ffmpeg`
- `ffprobe`

### Opcionales para transcripción

- `mlx-whisper` local
- `OpenRouter`
- `OpenAI`

## Métodos de transcripción soportados

### Opción 1: local-whisper

Soporta:

- `mlx-whisper`
- `faster-whisper`
- `openai-whisper`

En este momento el skill ya está preparado para usar `mlx-whisper` desde su propio entorno virtual local.

Ejemplo:

```bash
python3 ~/.codex/skills/meta-ads-video-copy/scripts/transcribe_media.py \
  "/ruta/al/video.mov" \
  --output-dir /tmp/meta-copy-transcript \
  --provider local-whisper \
  --local-backend mlx-whisper \
  --language es
```

### Opción 2: OpenRouter

Usa `OPENROUTER_API_KEY` y por defecto el modelo:

- `mistralai/voxtral-small-24b-2507`

Ejemplo:

```bash
python3 ~/.codex/skills/meta-ads-video-copy/scripts/transcribe_media.py \
  "/ruta/al/video.mov" \
  --output-dir /tmp/meta-copy-transcript \
  --provider openrouter \
  --language es
```

### Opción 3: OpenAI

Usa `OPENAI_API_KEY` y por defecto:

- `gpt-4o-mini-transcribe`

Esta ruta segmenta automáticamente el audio si el archivo preparado supera el límite del endpoint.

## Flujo recomendado

1. Transcribir el video.
2. Extraer frames y metadata.
3. Revisar transcript y visuales juntos.
4. Definir ángulos.
5. Redactar las variaciones finales.

## Scripts principales

### `transcribe_media.py`

Ubicación:

- `~/.codex/skills/meta-ads-video-copy/scripts/transcribe_media.py`

Qué hace:

- transcribe video o audio
- soporta OpenAI, OpenRouter y local Whisper
- guarda `transcript.txt` y `transcript.json`

### `prepare_video_context.py`

Ubicación:

- `~/.codex/skills/meta-ads-video-copy/scripts/prepare_video_context.py`

Qué hace:

- extrae frames
- extrae `audio.wav`
- guarda `metadata.json`

Ejemplo:

```bash
python3 ~/.codex/skills/meta-ads-video-copy/scripts/prepare_video_context.py \
  "/ruta/al/video.mov" \
  --output-dir /tmp/meta-video-context
```

## Reglas editoriales del skill

- priorizar audio/transcript cuando el video vende verbalmente
- validar claims con screenshots o frames
- no inventar descuentos, garantías o números no respaldados
- usar emojis con moderación y tono profesional
- devolver ángulos realmente distintos, no simples reformulaciones

## Caso de uso típico

Ejemplo de uso real dentro del flujo:

1. se sube un video corto de menos de `50MB`
2. se transcribe el audio
3. se extraen frames
4. se genera un brief interno:
   - audio insights
   - visual insights
   - confirmed claims
   - angles chosen
5. se entrega el copy final listo para Ads Manager

## Ubicación del skill

El skill vive fuera de este repo, en:

- `~/.codex/skills/meta-ads-video-copy`

Documentarlo aquí permite que el equipo entienda:

- para qué sirve
- cómo ejecutarlo
- qué esperar de la salida
