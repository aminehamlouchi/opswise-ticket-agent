from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Ticket:
    id: str
    submitted_at: str
    requester: str
    subject: str
    description: str
    affected_asset: str
    priority: str

    @property
    def text(self) -> str:
        return " ".join([self.subject, self.description, self.affected_asset, self.priority])


@dataclass(frozen=True)
class Classification:
    category: str
    severity: str
    confidence: float
    matched_keywords: list[str]


@dataclass(frozen=True)
class Runbook:
    id: str
    title: str
    category: str
    keywords: list[str]
    steps: list[str]
    escalation: str
    path: str


@dataclass(frozen=True)
class RunbookMatch:
    runbook: Runbook
    score: float


@dataclass(frozen=True)
class ToolTrace:
    name: str
    summary: str


@dataclass(frozen=True)
class TriagePlan:
    ticket: Ticket
    classification: Classification
    runbook: RunbookMatch
    sla_target: str
    recommended_actions: list[str]
    escalation_criteria: str
    trace: list[ToolTrace] = field(default_factory=list)

    def to_dict(self) -> dict:
        value = asdict(self)
        value["runbook"]["runbook"].pop("steps", None)
        return value
