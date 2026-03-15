# Exportar conversaciones de bots en GHL

Script para exportar conversaciones del ultimo mes desde Go High Level y generar un `.txt` por bot para analisis o reentrenamiento en otra IA.

## Variables de ambiente

Crear un `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Variables requeridas:

- `GHL_INTEGRATION_TOKEN`: private integration token del sub-account.
- `GHL_LOCATION_ID`: `locationId` de la cuenta donde viven las conversaciones.

Alias soportado:

- `GHL_ORGANIZATION_ID`: el script lo acepta como alias de `GHL_LOCATION_ID`.

Opcional:

- `GHL_API_BASE`: por default usa `https://services.leadconnectorhq.com`.
- `GHL_API_VERSION`: por default usa `2021-07-28`.
- `GHL_USER_AGENT`: por default usa un user agent propio del script para evitar bloqueos por el user agent por defecto de `urllib`.

## Ejecutar

```bash
python3 scripts/export_ghl_bot_conversations.py
```

Opciones utiles:

```bash
python3 scripts/export_ghl_bot_conversations.py --days 30 --output-dir exports/ghl-bot-conversations
python3 scripts/export_ghl_bot_conversations.py --stdout-summary
```

## Salida

El script genera:

- un archivo `.txt` por bot detectado;
- un `sin-asignar.txt` para conversaciones donde la API no expone metadata suficiente para ligar la conversacion con un bot concreto;
- un `summary.json` con conteos y metadatos de la corrida.

## Como agrupa por bot

El script:

1. descubre agentes publicados usando endpoints de `Conversation AI` y `AI Agent Studio`;
2. busca conversaciones recientes;
3. descarga detalle + mensajes de cada conversacion;
4. intenta asignar cada conversacion al bot correcto usando `conversation-ai/generations` y leyendo `employeeId` por cada mensaje AI generado.

Si en tu cuenta ciertas conversaciones terminan en `sin-asignar`, normalmente significa una de estas dos cosas:

- los mensajes salientes no tienen una generacion AI recuperable en `conversation-ai/generations`.
- la conversacion no tiene respuestas AI generadas por los agentes consultables desde ese endpoint.

En ese caso, el script no fuerza una inferencia por texto.

## Scopes recomendados

En la integracion privada de GHL, asegurate de incluir al menos permisos de lectura sobre conversaciones y mensajes. Si usas Conversation AI / AI Agent Studio, agrega tambien los scopes de lectura necesarios para esos modulos.

## Si aparece "Access denied" de Cloudflare

El script ya envia:

- header `Version: 2021-07-28`, que HighLevel muestra en sus ejemplos de Private Integrations;
- un `User-Agent` explicito, para evitar el bloqueo comun al user agent por defecto de `urllib`.

Si aun falla:

- confirma que el token sea de tipo `Sub-Account` o una Private Integration creada dentro del sub-account correcto;
- confirma que `GHL_LOCATION_ID` sea el `locationId` del mismo sub-account;
- prueba sobre una red sin VPN o proxy corporativo;
- si tu cuenta tiene reglas de seguridad adicionales delante de Cloudflare, puede ser necesario allowlist por `User-Agent`.
