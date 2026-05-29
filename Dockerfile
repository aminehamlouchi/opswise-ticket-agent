FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY opswise ./opswise
COPY runbooks ./runbooks
COPY sample_data ./sample_data
RUN pip install --no-cache-dir .

RUN mkdir -p outputs
CMD ["python", "-m", "opswise", "triage", "--tickets", "sample_data/tickets.csv", "--runbooks", "runbooks", "--out", "outputs/triage-report.txt", "--json-out", "outputs/triage-report.json"]
