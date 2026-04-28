# Spec: email triage classifier

The spec used to brief Claude Code when building this system. Kept in the repo as a reference for the kind of brief that produces a clean deploy.

## Goal

A scheduled Cloud Run Job that reads new Gmail messages, classifies each into one of `needs-reply / fyi / newsletter / receipt` using Vertex AI Gemini, and applies the matching Gmail label.

## What success looks like

- The job runs hourly via Cloud Scheduler with greater than 99% success rate
- Each new inbox message gets a `triage/<category>` label within an hour of arrival
- A human can verify it's working in under 30 seconds by checking Gmail labels or Cloud Run Job logs

## Inputs

- Gmail inbox messages from the last 24 hours, filtered by `in:inbox`
- Limit: 50 messages per run

## Outputs

- Gmail labels applied to the message (`triage/needs-reply`, etc.)
- Firestore document tracking processed message IDs (so we don't re-classify)
- Structured JSON logs to Cloud Logging

## Inference

- Model: Gemini Flash (`gemini-2.0-flash-001`)
- Prompt: classifies based on `From`, `Subject`, snippet, and presence of `List-Unsubscribe` header
- Token budget: ~200 input, 10 output (single-word category response)
- Failure mode: if the model returns an invalid category, default to `fyi` and log a warning

## Architecture

- Cloud Run Job (scheduled, batch)
- Firestore Native mode for state (key-value: message ID → category)
- Secret Manager for the Gmail OAuth token
- Region: europe-west1

## Schedule

`0 * * * *` (hourly, on the hour). Etc/UTC.

## IAM

The Cloud Run Job's service account (`email-classifier-sa`) needs:

- `roles/aiplatform.user` on the project (Vertex AI calls)
- `roles/datastore.user` on the project (Firestore read/write)
- `roles/secretmanager.secretAccessor` on the `gmail-oauth-token` secret (resource-level binding, not project-wide)

The Cloud Scheduler service account (`email-classifier-scheduler-sa`) needs:

- `roles/run.invoker` on the email-classifier Cloud Run Job

## Monitoring

- Log-based metric: count of ERROR-severity log entries from this job
- Alerting policy: fires when the metric exceeds 0 in any 5-minute window
- Notification channel: Slack webhook

## Out of scope

- Real-time classification (push notifications). The 1-hour cadence is enough.
- Sentiment or priority scoring. Just bucket categories.
- Auto-replies. Classification only.
- Multiple Gmail accounts. One inbox per deploy.

## Open questions resolved during implementation

- **Database choice.** Firestore over Cloud SQL because the workload is key-value lookups, low write rate, and Firestore's free tier covers it.
- **OAuth token refresh.** The `google-auth` library handles refresh transparently as long as the refresh token is valid. Store both access and refresh tokens in Secret Manager.
- **Label naming.** `triage/<category>` rather than separate top-level labels, so a Gmail user can collapse the parent label.
