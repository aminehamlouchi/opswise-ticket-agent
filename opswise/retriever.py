from __future__ import annotations

import re

from opswise.models import Classification, Runbook, RunbookMatch, Ticket

TOKEN_RE = re.compile(r"[a-zA-Z0-9']+")


def retrieve_runbook(ticket: Ticket, classification: Classification, runbooks: list[Runbook]) -> RunbookMatch:
    query_tokens = set(TOKEN_RE.findall(ticket.text.lower()))
    scored: list[tuple[float, Runbook]] = []
    for runbook in runbooks:
        keyword_overlap = query_tokens & {keyword.lower() for keyword in runbook.keywords}
        category_boost = 4 if runbook.category == classification.category else 0
        keyword_boost = len(set(classification.matched_keywords) & set(runbook.keywords))
        score = category_boost + len(keyword_overlap) + keyword_boost
        scored.append((score, runbook))

    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        raise ValueError("No runbooks loaded")
    score, runbook = scored[0]
    return RunbookMatch(runbook=runbook, score=round(score, 2))
