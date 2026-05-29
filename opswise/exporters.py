from __future__ import annotations

import json
from pathlib import Path

from opswise.models import TriagePlan


def write_json(plans: list[TriagePlan], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([plan.to_dict() for plan in plans], indent=2), encoding="utf-8")


def write_text_report(plans: list[TriagePlan], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["OpsWise Triage Report", "=====================", ""]
    for plan in plans:
        lines.extend(
            [
                f"Ticket {plan.ticket.id}: {plan.ticket.subject}",
                "-" * (len(plan.ticket.id) + len(plan.ticket.subject) + 9),
                "",
                f"Requester: {plan.ticket.requester}",
                f"Category: {plan.classification.category}",
                f"Severity: {plan.classification.severity}",
                f"Confidence: {plan.classification.confidence}",
                f"SLA target: {plan.sla_target}",
                f"Runbook: {plan.runbook.runbook.title}",
                "",
                "Recommended actions:",
                "",
            ]
        )
        lines.extend(f"{index}. {action}" for index, action in enumerate(plan.recommended_actions, start=1))
        lines.extend(
            [
                "",
                "Escalation criteria:",
                "",
                plan.escalation_criteria,
                "",
                "Processing notes:",
                "",
            ]
        )
        lines.extend(f"- {trace.name}: {trace.summary}" for trace in plan.trace)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
