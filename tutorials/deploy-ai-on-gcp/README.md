# Deploy AI Systems on Google Cloud With Claude Code

> Everyone talks about using AI agents to write code. Almost nobody talks about using them to deploy that code. If you can't deploy your software, the code is useless. No one can run it. No one can pay for it.

This tutorial is the deployment skill nobody teaches: how to actually ship AI systems to Google Cloud, end to end, with Claude Code as your deployment partner.

You'll deploy a real AI system: an email triage classifier that reads your Gmail, classifies messages with Vertex AI Gemini, and applies labels. It runs as a Cloud Run Job on a schedule. The same stack scales from a 50-line cron job to a $10,000 client AI system.

## Why This Matters Now

I've been a software engineer for 20 years. The work in this tutorial — provisioning a GCP project from scratch, wiring minimum-scope IAM, deploying a containerised job, setting up structured logging, building a custom Cloud Monitoring dashboard, and shipping alerting — used to take a team of engineers two to three weeks to do correctly.

With Claude Code as a deployment partner, I do it in an afternoon. Not because the work got easier, but because the boring parts are now generated, the cryptic errors are now explained, and the operational discipline is now defaulted into.

That's the shift. The kind of work that used to require a DevOps team is now a single developer with a clear spec and a good agent. This tutorial is how to actually do that work.

---

## The Problem

Every AI tutorial stops at "and now your app runs locally."

That's not deployment. That's a demo.

Real deployment means you can:

- Ship code to production
- Watch it run on a schedule, with logs you can search
- Get paged when it breaks, before your customer notices
- Trust it enough to put a client's name on it

The reason almost no AI content covers deployment is that it's hard. Cloud documentation is dense. Pricing is opaque. Permissions are a nightmare. Setting up monitoring takes hours. Error messages assume you already understand the system.

This tutorial closes that gap.

---

## What You'll Learn

- How to set up a Google Cloud project for AI work, end to end
- Why Cloud Run Jobs is the right primitive for scheduled AI automation
- How to use Vertex AI for production inference (and why not the Anthropic or OpenAI SDKs directly)
- How to wire up logging, metrics, and alerting before you ship
- How to use Claude Code as a deployment partner — for IAM, Terraform, debugging, and monitoring setup
- A reference Terraform module you can fork for your own automations

By the end, you'll have a working AI automation in production and a reusable workflow for any future AI deploy.

---

## My Philosophy

Operating software is genuinely hard. So I keep things as simple as possible.

That means:

- Choosing providers I trust
- Choosing tools that scale from small to large without forcing a rewrite
- Saying no to anything that adds complexity I don't need

There are a million ways to deploy software. The spectrum runs from managing your own VMs, where you do everything yourself, all the way to fully managed PaaS like Vercel, where you give up control for convenience. Cloud providers like Google Cloud sit in the middle.

```
Self-managed VMs        Cloud providers       Fully managed PaaS
(Hetzner, DigitalOcean) (GCP, AWS, Azure)     (Vercel, Render, Railway)
   You do everything    Sweet spot for AI     Hits a ceiling fast
```

I avoid VMs because the moment you take them on, you become a DevOps operator instead of a developer. I avoid the simplest PaaS because they cap out the moment you need a non-trivial database, scheduled jobs, or production-grade inference.

Google Cloud sits in a sweet spot. Cloud Run scales infinitely without you touching a load balancer, scales down to zero when nothing's running, and costs cents per month at small scale. The same stack runs simple cron jobs and serious client systems.

That's the part to remember: **one stack, full range**.

---

## "Why not n8n?"

A reasonable objection: why not n8n, Zapier, Make, or Claude Routines? They're simpler.

Honest answer: every automation I've built that mattered grew. The ones that didn't, I deleted. The ones that did, eventually outgrew whatever no-code tool I started with, and I rewrote them in Python. After enough rewrites, I just started in Python.

| | No-code (n8n, Zapier) | Cloud Run Job |
|---|---|---|
| Time to ship v1 | Faster | A bit slower |
| Logs and observability | Vendor UI | Cloud Logging, structured |
| Cost at automation volume | Per-task pricing adds up | Cents per month |
| Version control | None | Git |
| Tests | Limited | pytest, full Python |
| Migration when it grows | Forced rewrite | None — same stack |
| Lock-in | High | Low |

If your automation will never grow, sure, use n8n. But mine always do.

---

## The Stack

Two stacks. One philosophy. Same primitives.

### Stack 1: Scheduled automation (this tutorial)

```
Cloud Scheduler (cron)
        ↓
Cloud Run Job (your Python code)
        ↓
Vertex AI (Gemini)
        ↓
Firestore (state)
        ↓
Cloud Logging → log-based metric → Alerting policy → Slack
        ↑
Secret Manager (credentials)
```

### Stack 2: Full app (same primitives, more parts)

```
Cloud CDN
   ↓
Cloud Run (Next.js frontend)
   ↓
Cloud Run (Python backend)
   ↓
Cloud SQL (Postgres) + Vertex AI (Gemini)
   ↓
Same logging, monitoring, alerting, secrets
```

You don't change tools when your project grows. You add more of them.

---

## The Five Things You Have to Think About in Production

Skip any of these and you're shipping a toy.

### 1. Cost

Cloud Run scales to zero. You pay for runtime, not provisioned capacity. A daily 30-second job costs cents per month. Don't pre-pay for infrastructure you don't use.

### 2. Logs

Cloud Logging captures stdout for free, time-indexed, queryable. Every print statement is searchable. This is your debugger in production.

Use structured JSON logging. One event per line.

```python
print(json.dumps({"event": "message_classified", "category": "needs-reply", "message_id": msg_id}))
```

### 3. Metrics

Logs tell you what happened. Metrics tell you trends.

Use log-based metrics for cheap custom signals (count of messages classified, count of errors). Use Cloud Monitoring for the rest (CPU, memory, latency).

### 4. Alerting and dashboards

If your customer is the first to know something's broken, you've already lost.

Set up notification channels (Slack webhook, email, PagerDuty) before you ship. Wire alerting policies to log-based metrics. Test the alert by deliberately failing the job once.

Then build a dashboard. Cloud Monitoring dashboards are JSON. You define them once and check them in. The reference Terraform module in this repo creates one automatically: executions, errors, duration, recent logs, all in a single view.

This is one of the parts of the workflow that genuinely changed how I work. A custom monitoring dashboard for a production system used to be one to two days of a junior engineer's time. With Claude Code drafting the JSON from a description of what I want to see, it takes 15 minutes. The dashboard in this tutorial was generated this way.

### 5. Production inference

Don't call Anthropic or OpenAI APIs directly from production. Use Vertex AI.

The strongest argument is the SLA. Going direct to Anthropic or OpenAI as a standard API customer, you get no contractual uptime commitment. Both have status pages and best-effort uptime, but when they go down, you have no recourse. Vertex AI carries a published SLA tied to your GCP agreement, with service credits if Google misses it. Claude on Vertex sits under that same SLA — Google takes responsibility for the serving infrastructure even though the model weights come from Anthropic.

The reliability picture is real too. Both Anthropic and OpenAI have had outages and capacity exhaustion incidents during peak load. Vertex has issues sometimes, but the failure modes are different: when Vertex breaks, it's usually a regional GCP problem that affects a lot of services and you can route around it. When the direct APIs break, your specific inference path fails, often without ETA, and your only option is to wait.

Other reasons:

- **Unified billing.** Inference cost shows up on your GCP invoice. One bill, not three. Easier for clients, easier for accounting.
- **IAM and VPC.** Inference traffic stays inside your GCP project. Same auth surface as the rest of your stack. No separate API keys floating around in Secret Manager.
- **Observability.** Vertex calls show up in Cloud Logging and Cloud Monitoring like any other GCP service. One pane of glass.
- **Multi-model.** Gemini, Claude on Vertex, Llama, all under one auth model. Swap a string when models change.

**When direct APIs make sense:**

- You need day-zero access to a new model. Vertex usually trails Anthropic and OpenAI's direct APIs by days to weeks. If your business depends on the latest release, you go direct.
- You're not on GCP. The same argument transfers to Bedrock on AWS or Azure OpenAI Service.

For production systems on GCP with paying customers, Vertex is the default. Direct APIs are the exception.

---

## The Example: Email Triage Classifier

A Cloud Run Job that runs hourly, reads new Gmail messages, classifies each one with Gemini Flash, and applies a Gmail label.

Categories: `needs-reply`, `fyi`, `newsletter`, `receipt`.

Source code in [`email-classifier/`](email-classifier/). Deployed via the Terraform module in [`terraform/`](terraform/).

### Architecture

```
Cloud Scheduler (every 1h)
        ↓
Cloud Run Job: email-classifier
        ↓
1. Read Gmail messages (Gmail API)
2. Look up which IDs we've seen (Firestore)
3. Classify new ones (Vertex AI Gemini Flash)
4. Apply Gmail label (Gmail API)
5. Record processed ID (Firestore)
        ↓
Cloud Logging captures everything
```

Total cost at hourly cadence: under $1/month.

---

## Setup

### 1. Create a fresh GCP project

```bash
PROJECT_ID="email-triage-prod"

gcloud projects create $PROJECT_ID \
  --name="Email Triage" \
  --labels=service=email-triage,environment=prod

gcloud billing projects link $PROJECT_ID \
  --billing-account=$BILLING_ACCOUNT_ID

gcloud config set project $PROJECT_ID
```

### 2. Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com
```

### 3. Initialise Firestore

```bash
gcloud firestore databases create \
  --location=europe-west1 \
  --type=firestore-native
```

### 4. Mint a Gmail OAuth token

You need a refresh token with the `https://www.googleapis.com/auth/gmail.modify` scope. Use Google's [OAuth 2.0 quickstart](https://developers.google.com/gmail/api/quickstart/python) to mint one.

Store the JSON in Secret Manager:

```bash
gcloud secrets create gmail-oauth-token \
  --data-file=token.json \
  --replication-policy=automatic
```

### 5. Create a notification channel

In the Cloud Console: **Monitoring → Alerting → Notification channels → Add new**. Pick Slack (webhook) or email. Copy the resource ID once created.

### 6. Build and push the image

```bash
cd email-classifier
gcloud builds submit \
  --tag europe-west1-docker.pkg.dev/$PROJECT_ID/email-classifier/email-classifier:latest
```

### 7. Apply the Terraform

```bash
cd ../terraform
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars with your project ID, image URI, and notification channel
terraform init
terraform apply
```

This creates the Cloud Run Job, the Cloud Scheduler trigger, the IAM bindings, the log-based metric, and the alerting policy. One command.

### 8. Verify

```bash
gcloud run jobs execute email-classifier --region=europe-west1 --wait
```

Tail the logs:

```bash
gcloud run jobs executions list --job=email-classifier --region=europe-west1 --limit=1 --format=json | jq -r '.[0].metadata.name' | xargs -I {} gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=email-classifier" --limit=20 --format="value(textPayload)"
```

Or open the Cloud Run console and click into the latest execution.

---

## How Claude Code Helps With Each Step

Six things Claude Code does well in this workflow that would otherwise take hours:

### 1. Minimal-scope IAM

Most tutorials grant `roles/owner` and pray. Claude Code reads the actual API requirements and gives you only what's needed. For this project:

- `roles/aiplatform.user` (Vertex AI calls)
- `roles/datastore.user` (Firestore read/write)
- `roles/secretmanager.secretAccessor` on the specific secret (not project-wide)
- `roles/run.invoker` for the scheduler service account

That's the entire IAM surface for this system. No more.

### 2. Terraform from intent

Describe what you want. Claude Code drafts the Terraform. You review.

The module in [`terraform/`](terraform/) was generated this way: I described "Cloud Run Job + Scheduler + minimum-scope IAM + log-based metric + alert policy" and reviewed the output. About 5 minutes versus an hour from scratch.

### 3. Permissions debugging

When you see this:

```
googleapiclient.errors.HttpError: <HttpError 403 ... "iam.permissions.denied">
```

You hand it to Claude Code. It reads the missing role from the error and tells you which IAM binding to add. Used to take me 20 minutes per error.

### 4. Monitoring in one prompt

> "Create a log-based metric that counts ERROR-severity logs from this Cloud Run Job, and an alerting policy that fires when the metric exceeds zero in 5 minutes."

Claude Code writes the Terraform for both in one go. Setting up monitoring used to be the most annoying part of any deploy.

### 5. Custom monitoring dashboards

Cloud Monitoring dashboards are JSON. Describe what you want to see ("executions per hour, errors per 5 min, duration trend, recent log stream") and Claude Code drafts the dashboard JSON. Apply it via Terraform. Done.

This used to be a junior engineer's full week. The `terraform/dashboard.json.tftpl` in this repo was generated this way and reviewed in 5 minutes.

### 6. Cost-aware decisions

When you ask Claude Code "should I use Cloud SQL or Firestore here?" it actually reasons about workload. For this project, Firestore made sense (key-value lookups, low write rate). Claude Code recommended it and explained why. That's architectural thinking, not just code generation.

---

## Honest Limits

Three things to know before you trust this workflow.

### Claude Code sometimes picks the wrong service

It loves Cloud Functions for things that should be Cloud Run Jobs. It will sometimes suggest GKE for a workload that doesn't need it. Read what it suggests. Push back when it's wrong.

### It doesn't always handle compliance constraints unless you tell it

If you have data residency requirements, multi-region needs, or specific security policies, write them into your `AGENTS.md` or your spec. Every time. Claude Code defaults to "the simple thing" which might not be the compliant thing.

### It doesn't replace you understanding the systems

The people who get the most out of Claude Code for deployment are senior engineers who can verify what it does. If you're a vibe coder shipping to production without reading the diff, you'll have a bad time.

The agent is a partner. You're still the engineer.

---

## What's in This Repo

```
deploy-ai-on-gcp/
├── README.md                  # this file
├── AGENTS.md                  # reference AGENTS.md for Claude Code
├── spec.md                    # the spec used to brief Claude Code on this build
├── checklist.md               # 10-step opinionated GCP project setup
├── email-classifier/          # the working Python app
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
└── terraform/                 # reference Terraform module
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── dashboard.json.tftpl   # Cloud Monitoring dashboard, generated by Claude Code
    ├── terraform.tfvars.example
    └── README.md
```

Fork it. Modify it. Ship it.

---

## Customising For Your Own Automations

The shape of this tutorial generalises to almost any scheduled AI automation on GCP. To adapt:

1. **Replace the classification logic.** Swap the Gemini prompt and category list in `email-classifier/main.py` for whatever your task is.
2. **Replace the I/O.** Gmail in / Gmail out becomes whatever your system needs (Linear, Slack, Notion, Stripe, your own database).
3. **Adjust the schedule.** Change the cron expression in `terraform.tfvars`. Hourly, daily, weekly, every-five-minutes — Cloud Scheduler doesn't care.
4. **Swap the model.** `gemini-2.0-flash-001` is cheap and fast. For harder reasoning, switch to `gemini-2.0-pro-001` or `claude-sonnet-4@gcp` (Claude on Vertex).

The Terraform module, the AGENTS.md, the spec template, and the project setup checklist all stay the same. That's the point: one operational discipline, full range of automations.

---

## Going Deeper

If you want to learn this discipline directly:

- **AI Engineer Skool** — [aiengineer.co](https://aiengineer.co). $79/month community where I teach this kind of work in depth.
- **Gradient Work** — [gradientwork.com](https://gradientwork.com). The agency where I build $10k+ AI systems for clients. If you'd rather have this built for you than learn it.

---

## License

MIT. Fork it, ship it, modify it. Credit appreciated but not required.
