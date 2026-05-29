from __future__ import annotations

import csv
from pathlib import Path

from opswise.models import Runbook, Ticket


def load_tickets(path: Path) -> list[Ticket]:
    with path.open(newline="", encoding="utf-8") as file:
        return [Ticket(**row) for row in csv.DictReader(file)]


def load_runbooks(directory: Path) -> list[Runbook]:
    runbook_paths = sorted([*directory.glob("*.txt"), *directory.glob("*.md")])
    return [_parse_runbook(path) for path in runbook_paths]


def _parse_runbook(path: Path) -> Runbook:
    lines = path.read_text(encoding="utf-8").splitlines()
    metadata: dict[str, str] = {}
    body_start = 0
    for index, line in enumerate(lines):
        if not line.strip():
            body_start = index + 1
            break
        if ":" not in line:
            break
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    steps: list[str] = []
    escalation = "Escalate if the issue remains unresolved after standard troubleshooting."
    section = ""
    for line in lines[body_start:]:
        stripped = line.strip()
        lower = stripped.lower()
        if lower in {"steps:", "first pass:"}:
            section = "steps"
            continue
        if lower == "escalation:":
            section = "escalation"
            continue
        if lower.startswith("escalation:"):
            escalation = stripped.split(":", 1)[1].strip()
            section = "escalation"
        elif stripped.startswith("- "):
            steps.append(stripped[2:])
        elif stripped and section == "escalation":
            escalation = stripped

    return Runbook(
        id=metadata.get("runbook", metadata.get("id", path.stem)),
        title=metadata.get("title", path.stem.replace("-", " ").title()),
        category=metadata.get("category", "general"),
        keywords=[item.strip() for item in metadata.get("keywords", "").split(",") if item.strip()],
        steps=steps,
        escalation=escalation,
        path=str(path),
    )
