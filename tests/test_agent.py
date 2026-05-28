from pathlib import Path

from opswise.loader import load_runbooks
from opswise.models import Ticket
from opswise.planner import TriageAgent


def test_agent_returns_runbook_and_sla() -> None:
    runbooks = load_runbooks(Path("runbooks"))
    agent = TriageAgent(runbooks)
    plan = agent.triage(
        Ticket(
            id="T2",
            submitted_at="2026-05-28T09:00:00",
            requester="Test User",
            subject="Account locked",
            description="Cannot login before shift.",
            affected_asset="AD account",
            priority="high",
        )
    )

    assert plan.classification.category == "identity_access"
    assert plan.sla_target == "4h"
    assert plan.runbook.runbook.id == "identity-access"
    assert len(plan.trace) == 4
