#!/usr/bin/env python3
"""Exporta conversaciones recientes de GHL y genera un TXT por bot."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_API_BASE = "https://services.leadconnectorhq.com"
DEFAULT_API_VERSION = "2021-07-28"
DEFAULT_OUTPUT_DIR = Path("exports/ghl-bot-conversations")
DEFAULT_DAYS = 30
PAGE_SIZE = 100
MAX_RETRIES = 4
DEFAULT_USER_AGENT = "svrdocs-ghl-export/1.0 (+https://services.leadconnectorhq.com)"
CONVERSATION_SORT_BY = "last_message_date"
GENERATION_SOURCES = ("conversation", "workflow")


class ApiError(RuntimeError):
    """Raised when the GHL API returns an error."""


@dataclass(frozen=True)
class Agent:
    agent_id: str
    name: str
    source: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class DetectionResult:
    agent_ids: set[str]
    strategy: str
    evidence: list[str]


@dataclass(frozen=True)
class ProcessedConversation:
    conversation_id: str
    sort_at: datetime
    detection: DetectionResult
    block: str


def extract_disallowed_properties(error_text: str) -> set[str]:
    return set(re.findall(r"property ([A-Za-z0-9_]+) should not exist", error_text))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Exporta conversaciones de GHL del ultimo mes y genera un archivo TXT por bot."
        )
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Cantidad de dias hacia atras a exportar. Default: {DEFAULT_DAYS}.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directorio destino. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path(".env"),
        help="Archivo .env opcional para cargar variables de ambiente. Default: .env",
    )
    parser.add_argument(
        "--stdout-summary",
        action="store_true",
        help="Imprime tambien el resumen final en stdout.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Cantidad de workers paralelos para exportar conversaciones. Default: 6.",
    )
    return parser.parse_args()


def load_env_file(env_file: Path) -> None:
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def require_env(name: str, aliases: Iterable[str] | None = None) -> str:
    aliases = list(aliases or [])
    for candidate in [name, *aliases]:
        value = os.getenv(candidate)
        if value:
            return value
    alias_text = f" (aliases: {', '.join(aliases)})" if aliases else ""
    raise SystemExit(f"Falta la variable de ambiente requerida: {name}{alias_text}")


def build_headers(
    token: str,
    location_id: str,
    api_version: str,
    user_agent: str,
) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": api_version,
        "locationId": location_id,
        "User-Agent": user_agent,
    }


def make_request(
    method: str,
    url: str,
    headers: dict[str, str],
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    query = urlencode({k: v for k, v in (params or {}).items() if v is not None}, doseq=True)
    full_url = f"{url}?{query}" if query else url
    payload = None if body is None else json.dumps(body).encode("utf-8")
    request = Request(full_url, headers=headers, method=method.upper(), data=payload)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(request, timeout=60) as response:
                content = response.read()
            if not content:
                return {}
            return json.loads(content.decode("utf-8"))
        except HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < MAX_RETRIES:
                time.sleep(attempt * 2)
                continue
            raise ApiError(
                f"HTTP {exc.code} en {full_url}\nRespuesta: {response_body}"
            ) from exc
        except URLError as exc:
            if attempt < MAX_RETRIES:
                time.sleep(attempt * 2)
                continue
            raise ApiError(f"Error de red contra {full_url}: {exc}") from exc


def parse_timestamp(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    if isinstance(value, (int, float)):
        if value > 10_000_000_000:
            value = value / 1000
        return datetime.fromtimestamp(value, tz=UTC)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.isdigit():
            return parse_timestamp(int(text))
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    return None


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "sin-nombre"


def first_non_empty(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def find_first_list(payload: Any, preferred_keys: tuple[str, ...]) -> list[dict[str, Any]]:
    queue = [payload]
    while queue:
        current = queue.pop(0)
        if isinstance(current, dict):
            for key in preferred_keys:
                value = current.get(key)
                if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                    return value
            queue.extend(current.values())
        elif isinstance(current, list):
            if current and all(isinstance(item, dict) for item in current):
                return current
            queue.extend(current)
    return []

def extract_agent_candidates(payload: dict[str, Any], source: str) -> list[Agent]:
    items = find_first_list(payload, ("agents", "data", "items"))
    candidates: list[Agent] = []
    for item in items:
        agent_id = first_non_empty(item, "id", "_id", "agentId")
        name = first_non_empty(item, "name", "agentName", "title")
        if not agent_id or not name:
            continue
        candidates.append(
            Agent(
                agent_id=str(agent_id),
                name=str(name),
                source=source,
                raw=item,
            )
        )
    return candidates


def discover_agents(api_base: str, headers: dict[str, str], location_id: str) -> dict[str, Agent]:
    discovered: dict[str, Agent] = {}

    conversation_ai_params: dict[str, Any] = {"limit": PAGE_SIZE}
    try:
        payload = make_request(
            "GET",
            f"{api_base}/conversation-ai/agents/search",
            headers,
            params=conversation_ai_params,
        )
    except ApiError as exc:
        disallowed = extract_disallowed_properties(str(exc))
        if disallowed:
            payload = make_request(
                "GET",
                f"{api_base}/conversation-ai/agents/search",
                headers,
                params={
                    key: value
                    for key, value in conversation_ai_params.items()
                    if key not in disallowed
                },
            )
        else:
            raise

    agents = extract_agent_candidates(payload, "conversation-ai")
    for agent in agents:
        discovered.setdefault(agent.agent_id, agent)

    agent_studio_paths = (
        "/agent-studio/agent",
        "/agent-studio/public-api/agents",
    )
    for agent_path in agent_studio_paths:
        offset = 0
        found_on_this_path = False
        while True:
            try:
                payload = make_request(
                    "GET",
                    f"{api_base}{agent_path}",
                    headers,
                    params={
                        "locationId": location_id,
                        "limit": PAGE_SIZE,
                        "offset": offset,
                        "isPublished": "true",
                    },
                )
            except ApiError as exc:
                if "HTTP 404" in str(exc) or "HTTP 422" in str(exc):
                    break
                raise
            agents = extract_agent_candidates(payload, "agent-studio")
            if not agents:
                break
            found_on_this_path = True
            for agent in agents:
                discovered.setdefault(agent.agent_id, agent)
            if len(agents) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
        if found_on_this_path:
            break

    return discovered


def extract_conversations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return find_first_list(payload, ("conversations", "data", "items"))


def conversation_timestamp(conversation: dict[str, Any]) -> datetime | None:
    for key in (
        "lastMessageDate",
        "lastMessageAt",
        "updatedAt",
        "dateUpdated",
        "createdAt",
        "dateAdded",
    ):
        parsed = parse_timestamp(conversation.get(key))
        if parsed:
            return parsed
    return None


def search_recent_conversations(
    api_base: str,
    headers: dict[str, str],
    location_id: str,
    cutoff: datetime,
) -> list[dict[str, Any]]:
    conversations: list[dict[str, Any]] = []
    start_after_date: Any = None
    seen_ids: set[str] = set()
    stagnant_cursor = None

    while True:
        params = {
            "locationId": location_id,
            "limit": PAGE_SIZE,
            "status": "all",
            "sort": "desc",
            "sortBy": CONVERSATION_SORT_BY,
            "startAfterDate": start_after_date,
        }
        payload = make_request(
            "GET",
            f"{api_base}/conversations/search",
            headers,
            params=params,
        )
        batch = extract_conversations(payload)
        if not batch:
            break

        oldest_in_batch = None
        for conversation in batch:
            conversation_id = first_non_empty(conversation, "id", "_id", "conversationId")
            if not conversation_id:
                continue
            conversation_id = str(conversation_id)
            if conversation_id in seen_ids:
                continue
            seen_ids.add(conversation_id)
            ts = conversation_timestamp(conversation)
            if ts:
                oldest_in_batch = ts
            if ts and ts < cutoff:
                continue
            conversations.append(conversation)

        last_cursor = first_non_empty(batch[-1], "lastMessageDate", "lastMessageAt", "updatedAt")
        if not last_cursor:
            break
        if last_cursor == stagnant_cursor:
            break
        stagnant_cursor = last_cursor
        start_after_date = last_cursor
        if oldest_in_batch and oldest_in_batch < cutoff:
            break

    return conversations


def get_conversation_messages(
    api_base: str,
    headers: dict[str, str],
    conversation_id: str,
) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    last_message_id: str | None = None
    seen_ids: set[str] = set()

    while True:
        payload = make_request(
            "GET",
            f"{api_base}/conversations/{conversation_id}/messages",
            headers,
            params={"limit": PAGE_SIZE, "lastMessageId": last_message_id},
        )
        batch = find_first_list(payload, ("messages", "data", "items"))
        if not batch:
            break
        for message in batch:
            message_id = first_non_empty(message, "id", "_id", "messageId")
            if message_id:
                message_id = str(message_id)
                if message_id in seen_ids:
                    continue
                seen_ids.add(message_id)
            messages.append(message)
        last_seen = first_non_empty(batch[-1], "id", "_id", "messageId")
        if not last_seen or len(batch) < PAGE_SIZE:
            break
        last_message_id = str(last_seen)

    messages.sort(
        key=lambda item: parse_timestamp(
            first_non_empty(
                item,
                "dateAdded",
                "createdAt",
                "updatedAt",
                "timestamp",
                "messageTimestamp",
            )
        )
        or datetime.fromtimestamp(0, tz=UTC)
    )
    return messages

def get_generation_details(
    api_base: str,
    headers: dict[str, str],
    message_id: str,
    source: str,
) -> dict[str, Any]:
    return make_request(
        "GET",
        f"{api_base}/conversation-ai/generations",
        headers,
        params={"messageId": message_id, "source": source},
    )


def detect_agents_by_generation(
    api_base: str,
    headers: dict[str, str],
    messages: list[dict[str, Any]],
    agents: dict[str, Agent],
) -> DetectionResult:
    outbound_messages = [
        message for message in messages if str(first_non_empty(message, "direction") or "").lower() == "outbound"
    ]
    outbound_messages.sort(
        key=lambda message: (
            bool(str(message.get("userId") or "").strip()),
            parse_timestamp(first_non_empty(message, "dateAdded", "createdAt")) or datetime.max.replace(tzinfo=UTC),
        )
    )

    detected_agent_ids: set[str] = set()
    evidence: list[str] = []

    for message in outbound_messages:
        message_id = first_non_empty(message, "id", "_id", "messageId")
        if not message_id:
            continue
        message_id = str(message_id)
        for source in GENERATION_SOURCES:
            try:
                generation = get_generation_details(api_base, headers, message_id, source)
            except ApiError as exc:
                if "No Ai suggestion Found" in str(exc):
                    continue
                raise
            employee_id = first_non_empty(generation, "employeeId")
            if not employee_id:
                continue
            employee_id = str(employee_id)
            if employee_id in agents:
                detected_agent_ids.add(employee_id)
                if len(evidence) < 8:
                    evidence.append(f"messageId:{message_id}|source:{source}|employeeId:{employee_id}")
                break
            if not detected_agent_ids:
                return DetectionResult(
                    agent_ids=set(),
                    strategy="ghl_generation_unknown_employeeId",
                    evidence=[
                        f"messageId:{message_id}",
                        f"source:{source}",
                        f"employeeId:{employee_id}",
                    ],
                )

    if detected_agent_ids:
        return DetectionResult(
            agent_ids=detected_agent_ids,
            strategy="ghl_generation_employeeId",
            evidence=evidence,
        )

    return DetectionResult(agent_ids=set(), strategy="unassigned", evidence=[])


def get_contact_label(detail: dict[str, Any]) -> str:
    contact = detail.get("contact")
    if isinstance(contact, dict):
        name = first_non_empty(contact, "name", "fullName")
        contact_id = first_non_empty(contact, "id", "_id", "contactId")
        if name and contact_id:
            return f"{name} ({contact_id})"
        if name:
            return str(name)
        if contact_id:
            return str(contact_id)

    name = first_non_empty(detail, "fullName", "contactName")
    contact_id = first_non_empty(detail, "contactId")
    if name and contact_id:
        return f"{name} ({contact_id})"
    if name:
        return str(name)
    if contact_id:
        return str(contact_id)
    return "Sin contacto"


def get_channel_label(detail: dict[str, Any]) -> str:
    return str(first_non_empty(detail, "channel", "type", "conversationType") or "Desconocido")


def speaker_label(message: dict[str, Any], matched_agents: set[str], agents: dict[str, Agent]) -> str:
    direction = str(first_non_empty(message, "direction") or "").lower()
    if direction == "inbound":
        return "LEAD"
    if matched_agents and not str(message.get("userId") or "").strip():
        first_agent = agents[sorted(matched_agents)[0]]
        return f"BOT:{first_agent.name}"

    if direction == "outbound":
        return "STAFF"
    return "DESCONOCIDO"


def message_body(message: dict[str, Any]) -> str:
    body = first_non_empty(message, "body", "message", "html", "content", "text")
    parts: list[str] = []
    if body:
        parts.append(str(body).strip())

    attachments = message.get("attachments")
    if isinstance(attachments, list) and attachments:
        urls = []
        for attachment in attachments:
            if isinstance(attachment, dict):
                url = first_non_empty(attachment, "url", "link")
                if url:
                    urls.append(str(url))
            elif attachment:
                urls.append(str(attachment))
        if urls:
            parts.append("Adjuntos: " + ", ".join(urls))

    return "\n".join(part for part in parts if part).strip() or "[sin contenido]"


def render_conversation_block(
    conversation_id: str,
    conversation: dict[str, Any],
    messages: list[dict[str, Any]],
    detection: DetectionResult,
    agents: dict[str, Agent],
) -> str:
    created_at = parse_timestamp(
        first_non_empty(conversation, "dateAdded", "createdAt", "startDate")
    )
    updated_at = parse_timestamp(
        first_non_empty(conversation, "dateUpdated", "updatedAt", "lastMessageDate")
    )
    matched_labels = ", ".join(agents[agent_id].name for agent_id in sorted(detection.agent_ids))
    header = [
        "=" * 100,
        f"CONVERSATION_ID: {conversation_id}",
        f"CONTACTO: {get_contact_label(conversation)}",
        f"CANAL: {get_channel_label(conversation)}",
        f"BOT_ASIGNADO: {matched_labels or 'SIN_ASIGNAR'}",
        f"BOT_ASSIGNMENT_SOURCE: {detection.strategy}",
        f"BOT_ASSIGNMENT_EVIDENCE: {', '.join(detection.evidence) if detection.evidence else 'N/D'}",
        f"CREADA_EN: {created_at.isoformat() if created_at else 'N/D'}",
        f"ACTUALIZADA_EN: {updated_at.isoformat() if updated_at else 'N/D'}",
        "-" * 100,
    ]

    rendered_messages: list[str] = []
    for message in messages:
        timestamp = parse_timestamp(
            first_non_empty(
                message,
                "dateAdded",
                "createdAt",
                "updatedAt",
                "timestamp",
                "messageTimestamp",
            )
        )
        channel = first_non_empty(message, "type", "messageType", "channel") or "Desconocido"
        rendered_messages.append(
            "\n".join(
                [
                    f"[{timestamp.isoformat() if timestamp else 'N/D'}] "
                    f"{speaker_label(message, detection.agent_ids, agents)} | {channel}",
                    message_body(message),
                ]
            )
        )

    return "\n".join(header + rendered_messages + [""])


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_exports(
    output_dir: Path,
    grouped_conversations: dict[str, list[ProcessedConversation]],
    agents: dict[str, Agent],
    summary: dict[str, Any],
) -> None:
    ensure_output_dir(output_dir)
    for bucket, items in grouped_conversations.items():
        if bucket == "_sin_asignar":
            file_name = "sin-asignar.txt"
            label = "Sin asignar"
        else:
            agent = agents[bucket]
            file_name = f"{slugify(agent.name)}__{slugify(agent.agent_id)}.txt"
            label = agent.name

        ordered_blocks = [
            item.block
            for item in sorted(items, key=lambda item: item.sort_at, reverse=True)
        ]

        content = [
            f"Bot: {label}",
            f"Exportado en: {datetime.now(UTC).isoformat()}",
            f"Rango: ultimos {summary['days']} dias",
            f"Conversaciones incluidas: {len(ordered_blocks)}",
            "",
            "\n".join(ordered_blocks),
        ]
        (output_dir / file_name).write_text("\n".join(content), encoding="utf-8")

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def process_conversation(
    api_base: str,
    headers: dict[str, str],
    conversation: dict[str, Any],
    agents: dict[str, Agent],
) -> ProcessedConversation | None:
    conversation_id = first_non_empty(conversation, "id", "_id", "conversationId")
    if not conversation_id:
        return None
    conversation_id = str(conversation_id)
    messages = get_conversation_messages(api_base, headers, conversation_id)
    detection = detect_agents_by_generation(api_base, headers, messages, agents)
    block = render_conversation_block(conversation_id, conversation, messages, detection, agents)
    sort_at = conversation_timestamp(conversation) or datetime.fromtimestamp(0, tz=UTC)
    return ProcessedConversation(
        conversation_id=conversation_id,
        sort_at=sort_at,
        detection=detection,
        block=block,
    )


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)

    token = require_env("GHL_INTEGRATION_TOKEN", aliases=["GHL_API_TOKEN"])
    location_id = require_env("GHL_LOCATION_ID", aliases=["GHL_ORGANIZATION_ID"])
    api_base = os.getenv("GHL_API_BASE", DEFAULT_API_BASE).rstrip("/")
    api_version = os.getenv("GHL_API_VERSION", DEFAULT_API_VERSION)
    user_agent = os.getenv("GHL_USER_AGENT", DEFAULT_USER_AGENT)
    cutoff = datetime.now(UTC) - timedelta(days=args.days)

    headers = build_headers(token, location_id, api_version, user_agent)

    print("Descubriendo bots/agentes en GHL...", file=sys.stderr)
    agents = discover_agents(api_base, headers, location_id)
    print(f"Agentes detectados: {len(agents)}", file=sys.stderr)

    print(f"Buscando conversaciones desde {cutoff.isoformat()}...", file=sys.stderr)
    recent_conversations = search_recent_conversations(api_base, headers, location_id, cutoff)
    print(f"Conversaciones encontradas: {len(recent_conversations)}", file=sys.stderr)

    grouped_conversations: dict[str, list[ProcessedConversation]] = defaultdict(list)
    assigned_count_by_agent: dict[str, int] = defaultdict(int)
    worker_count = max(1, args.workers)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {
            executor.submit(process_conversation, api_base, headers, conversation, agents): conversation
            for conversation in recent_conversations
        }
        for index, future in enumerate(as_completed(future_map), start=1):
            processed = future.result()
            if processed is None:
                continue
            print(
                f"[{index}/{len(recent_conversations)}] Exportando conversacion {processed.conversation_id}...",
                file=sys.stderr,
            )
            if not processed.detection.agent_ids:
                grouped_conversations["_sin_asignar"].append(processed)
                continue

            for agent_id in sorted(processed.detection.agent_ids):
                grouped_conversations[agent_id].append(processed)
                assigned_count_by_agent[agent_id] += 1

    summary = {
        "generatedAt": datetime.now(UTC).isoformat(),
        "days": args.days,
        "locationId": location_id,
        "apiBase": api_base,
        "apiVersion": api_version,
        "userAgent": user_agent,
        "workers": worker_count,
        "detectedAgents": [
            {
                "id": agent.agent_id,
                "name": agent.name,
                "source": agent.source,
            }
            for agent in sorted(agents.values(), key=lambda item: item.name.lower())
        ],
        "conversationCount": len(recent_conversations),
        "exportedFiles": len(grouped_conversations),
        "assignedConversationCountByAgent": {
            agents[agent_id].name: count
            for agent_id, count in sorted(assigned_count_by_agent.items())
        },
        "unassignedConversationCount": len(grouped_conversations.get("_sin_asignar", [])),
    }

    write_exports(args.output_dir, grouped_conversations, agents, summary)
    print(f"Export terminado en: {args.output_dir}", file=sys.stderr)

    if args.stdout_summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ApiError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
