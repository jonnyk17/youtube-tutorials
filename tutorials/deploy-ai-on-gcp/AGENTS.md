# AGENTS.md

Reference for Claude Code working in this repo.

## Project

Email triage classifier. Reads new Gmail messages, classifies each into one of `needs-reply / fyi / newsletter / receipt` using Vertex AI Gemini, applies a Gmail label.

Runs as a Cloud Run Job. Triggered hourly by Cloud Scheduler. State in Firestore. Secrets in Secret Manager.

## Stack

- Runtime: Python 3.12 on Cloud Run Jobs
- Inference: Vertex AI Gemini Flash
- Storage: Firestore (state only)
- Secrets: Secret Manager
- Scheduling: Cloud Scheduler
- Observability: Cloud Logging + log-based metrics + Cloud Monitoring alerting
- IaC: Terraform, modules in `terraform/`

## Region

`europe-west1`. Pin a region. Don't multi-region without explicit reason.

## Conventions

### Inference

- All inference goes through Vertex AI. Never call Anthropic or OpenAI SDKs directly.
- Default model: Gemini Flash. Step up to Pro only when measurably needed.
- Set explicit max_output_tokens on every call.
- Log model name, prompt tokens, completion tokens, and latency for every inference.

### IAM

- Minimal scope, every time. No `roles/owner`, no `roles/editor`.
- Per-service service accounts. Naming: `<service>-sa`.
- Grant roles at the resource level when possible (specific secret, specific job), not project level.
- All IAM lives in Terraform, not console clicks.

### Secrets

- All secrets in Secret Manager. Mount via env vars at runtime.
- Never commit, never log, never hardcode.
- Rotate quarterly minimum.

### Logging

- Structured JSON logging, one event per line.
- Standard fields: `event`, `service`, `timestamp` (auto), plus event-specific data.
- Print stdout. Cloud Run captures it.
- Severity via the `severity` field for ERROR/WARNING.
- No PII unless reviewed.

### Monitoring and alerting

- Every Cloud Run Job needs:
  - A log-based metric for ERROR-severity entries
  - An alerting policy on that metric
  - A notification channel
  - A Cloud Monitoring dashboard (JSON, checked into Terraform)
- Set monitoring up in the same Terraform apply as the job. Not after.
- Dashboards are JSON. Generate them from a description of what should be visible, then review and check in.

### Cost

- Cloud Run Jobs scale to zero. Default to that.
- Avoid persistent VMs unless workload genuinely justifies.
- Add `labels = { service = "<name>", environment = "<env>" }` for billing breakdowns.

### Deployment

- Build with Cloud Build, not local Docker.
- Tag images with git SHA, not `latest` (in production).
- Use Terraform to deploy production. `gcloud run jobs deploy` is fine for development iteration.

### Testing

- Local: pytest, run with `DRY_RUN=true` against a test inbox.
- Pre-deploy: run once with `LIMIT=5` to verify auth and connectivity.
- Post-deploy: tail logs for the first scheduled run.

## Out of scope (for the agent)

- Don't suggest GKE, Compute Engine, or App Engine.
- Don't suggest serverless functions for jobs that need >9 minutes.
- Don't draft Kubernetes YAML.
- Don't recommend third-party SaaS over GCP-native services without prompting.

## Starting a new feature

1. Read this file in full.
2. Read the relevant Terraform under `terraform/`.
3. Ask clarifying questions about scope before writing code.
4. Write a spec under `docs/<feature>/spec.md` if the technical approach isn't obvious.
5. Implement, then update Terraform.
6. Add or update monitoring before declaring done.
