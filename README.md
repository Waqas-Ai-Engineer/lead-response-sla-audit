# ⚡ lead-response-sla-audit

![python](https://img.shields.io/badge/python-3.8%2B-blue) ![deps](https://img.shields.io/badge/dependencies-zero-brightgreen) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

**How fast does your business actually answer new leads?** Drop in a CSV export from any CRM, form tool or call log and get a speed-to-lead report: % answered within your SLA, median/P90 response, leads never answered, after-hours gaps, per-source breakdown and an *illustrative* revenue-leak estimate. Built for roofing, HVAC, clinics, salons and real-estate teams, and for freelancers who want a data-backed pitch for lead-response automation.

## Quickstart (under 2 minutes, offline)

```bash
git clone https://github.com/Waqas-Ai-Engineer/lead-response-sla-audit && cd lead-response-sla-audit
python -m leadsla examples/sample_leads.csv --job-value 6500 --html report.html
python -m unittest discover tests
```

No installs, no API keys, no network. Your data never leaves your machine.

## Input format

`lead_id,source,created_at,first_response_at,won` — timestamps like `2026-09-01 14:05:00`; leave `first_response_at` empty if nobody replied; `won` is 1/0.

## Options

| Flag | Meaning |
|---|---|
| `--sla 15` | SLA in minutes |
| `--job-value 6500` | average job value; enables the leak scenario |
| `--html out.html` | shareable HTML report with an inline chart |

## Sample output

See [`examples/sample_output.md`](examples/sample_output.md). **The sample data is synthetic** (seeded generator in `examples/make_sample.py`), not real client data; the dollar figure is a scenario computed from whatever data you feed it, not a promise.

## Architecture

```
CSV -> core.load -> core.audit -> report.to_markdown / report.to_html
```

## Ideas to extend

Business-hours-aware SLAs, Google Sheets input, a webhook that alerts when a lead breaches SLA (n8n friendly).

## Need this built? Hire me

I'm **Muhammad Waqas, AI Agents & Business Automation**. I build lead-response automations (instant WhatsApp/SMS/email replies, CRM sync, AI receptionists, reporting) for service businesses. Reach me via my [GitHub profile](https://github.com/Waqas-Ai-Engineer).

If this was useful, a ⭐ helps others find it.
