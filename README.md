# OpsWise Ticket Agent

OpsWise Ticket Agent is a helpdesk automation agent for entry-level IT and infrastructure teams. It ingests raw support tickets, classifies the issue, retrieves a matching runbook, assigns an SLA target, and exports a triage report.

The project is CLI-first so it can run as a local batch job, scheduled script, or future service integration.

## Quickstart

Run the sample:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m opswise triage --tickets sample_data/tickets.csv --runbooks runbooks --out outputs/triage-report.txt --json-out outputs/triage-report.json
```

## Architecture

```mermaid
flowchart LR
    A["CSV tickets"] --> B["Classification tool"]
    B --> C["Runbook retrieval tool"]
    C --> D["SLA policy tool"]
    D --> E["Triage planning tool"]
    E --> F["Text and JSON reports"]
```

## Triage Workflow

The agent runs a multi-step workflow:

1. Normalize ticket text.
2. Classify category and severity with confidence.
3. Retrieve the best runbook for the category and keywords.
4. Apply an SLA policy.
5. Produce next actions and escalation criteria.
6. Export both human-readable and machine-readable reports.

The current workflow is deterministic and testable. A future version can swap in a model-backed classifier or planner while keeping the same tool boundaries.

## Ticket CSV Schema

```csv
id,submitted_at,requester,subject,description,affected_asset,priority
```

## Local Setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m opswise triage --tickets sample_data/tickets.csv --runbooks runbooks --out outputs/report.txt
```

## Docker

```bash
docker build -t opswise-ticket-agent .
docker run --rm -v "$PWD/outputs:/app/outputs" opswise-ticket-agent
```

## Deployment Ideas

- Scheduled GitHub Action that triages a CSV export daily.
- Containerized cron job on a small VM.
- Future FastAPI service with Jira, GitHub Issues, or Slack integrations.

## Testing

```bash
pytest
python -m opswise triage --tickets sample_data/tickets.csv --runbooks runbooks --out outputs/triage-report.txt --json-out outputs/triage-report.json
```
