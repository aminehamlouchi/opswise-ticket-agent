from __future__ import annotations

import re

from opswise.models import Classification, Ticket

KEYWORDS = {
    "identity_access": ["password", "mfa", "login", "locked", "access", "permission", "account", "badge"],
    "network": ["wifi", "vpn", "network", "latency", "dns", "ethernet", "connection", "internet"],
    "endpoint": ["laptop", "printer", "monitor", "dock", "docking", "blue screen", "device", "keyboard"],
    "application": ["outlook", "teams", "erp", "software", "application", "app", "error", "crash"],
}

HIGH_SEVERITY = ["outage", "all users", "cannot work", "production down", "site down", "security"]
MEDIUM_SEVERITY = ["blocked", "urgent", "manager", "deadline", "multiple users"]


def classify_ticket(ticket: Ticket) -> Classification:
    text = ticket.text.lower()
    subject = ticket.subject.lower()
    category_scores: dict[str, tuple[int, list[str]]] = {}
    for category, keywords in KEYWORDS.items():
        matched = [keyword for keyword in keywords if _contains(text, keyword)]
        if matched:
            subject_boost = sum(2 for keyword in matched if _contains(subject, keyword))
            category_scores[category] = (len(matched) + subject_boost, matched)

    if category_scores:
        category, (_, matched_keywords) = max(category_scores.items(), key=lambda item: item[1][0])
    else:
        category, matched_keywords = "general", []

    severity = _severity(text, ticket.priority)
    confidence = min(0.45 + (len(matched_keywords) * 0.15), 0.95)
    return Classification(
        category=category,
        severity=severity,
        confidence=round(confidence, 2),
        matched_keywords=matched_keywords,
    )


def _contains(text: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in text
    return bool(re.search(rf"\b{re.escape(keyword)}\b", text))


def _severity(text: str, priority: str) -> str:
    if priority.lower() == "high" or any(phrase in text for phrase in HIGH_SEVERITY):
        return "high"
    if priority.lower() == "medium" or any(phrase in text for phrase in MEDIUM_SEVERITY):
        return "medium"
    return "low"
