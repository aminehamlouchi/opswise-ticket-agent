from __future__ import annotations

import argparse
from pathlib import Path

from opswise.exporters import write_json, write_text_report
from opswise.loader import load_runbooks, load_tickets
from opswise.planner import TriageAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpsWise helpdesk ticket triage agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    triage = subparsers.add_parser("triage", help="Triage tickets from a CSV export")
    triage.add_argument("--tickets", required=True, type=Path)
    triage.add_argument("--runbooks", required=True, type=Path)
    triage.add_argument("--out", default=Path("outputs/triage-report.txt"), type=Path)
    triage.add_argument("--json-out", default=None, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "triage":
        runbooks = load_runbooks(args.runbooks)
        tickets = load_tickets(args.tickets)
        agent = TriageAgent(runbooks)
        plans = [agent.triage(ticket) for ticket in tickets]
        write_text_report(plans, args.out)
        if args.json_out:
            write_json(plans, args.json_out)
        print(f"Triage complete: {len(plans)} ticket(s) -> {args.out}")
