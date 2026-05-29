from __future__ import annotations

import os

from opswise.classifier import classify_ticket
from opswise.models import Runbook, Ticket, ToolTrace, TriagePlan
from opswise.retriever import retrieve_runbook


class TriageAgent:
    def __init__(self, runbooks: list[Runbook]):
        self.runbooks = runbooks

    def triage(self, ticket: Ticket) -> TriagePlan:
        trace: list[ToolTrace] = []

        classification = classify_ticket(ticket)
        trace.append(ToolTrace("classify_ticket", f"{classification.category}/{classification.severity} at {classification.confidence} confidence"))

        runbook_match = retrieve_runbook(ticket, classification, self.runbooks)
        trace.append(ToolTrace("retrieve_runbook", f"Selected {runbook_match.runbook.id} with score {runbook_match.score}"))

        sla_target = sla_for(classification.severity)
        trace.append(ToolTrace("apply_sla_policy", f"SLA target is {sla_target}"))

        recommended_actions = [
            f"Confirm requester impact and affected asset: {ticket.affected_asset}.",
            *runbook_match.runbook.steps[:4],
            "Document resolution notes and update the requester before closing the ticket.",
        ]
        trace.append(ToolTrace("plan_actions", f"Prepared {len(recommended_actions)} actions"))

        return TriagePlan(
            ticket=ticket,
            classification=classification,
            runbook=runbook_match,
            sla_target=sla_target,
            recommended_actions=recommended_actions,
            escalation_criteria=runbook_match.runbook.escalation,
            trace=trace,
        )


def sla_for(severity: str) -> str:
    env_key = f"OPSWISE_DEFAULT_SLA_{severity.upper()}"
    defaults = {
        "high": "4h",
        "medium": "1 business day",
        "low": "3 business days",
    }
    return os.getenv(env_key, defaults.get(severity, "3 business days"))
