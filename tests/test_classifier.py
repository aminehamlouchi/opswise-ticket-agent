from opswise.classifier import classify_ticket
from opswise.models import Ticket


def test_classifies_vpn_ticket_as_network() -> None:
    ticket = Ticket(
        id="T1",
        submitted_at="2026-05-28T08:00:00",
        requester="Test User",
        subject="VPN will not connect",
        description="VPN times out after MFA.",
        affected_asset="Laptop",
        priority="medium",
    )
    result = classify_ticket(ticket)

    assert result.category == "network"
    assert result.severity == "medium"
    assert "vpn" in result.matched_keywords
