---
name: strale-data-capabilities
description: >
  Access 225+ verified data capabilities through Strale — the trust layer
  for AI agents. Company data across 27 countries, IBAN/VAT validation,
  GDPR compliance, sanctions screening, and more. Every capability is
  independently tested and quality-scored. Free tier available.
version: 1.0.0
tools:
  - strale_search
  - strale_execute
  - strale_trust_profile
  - strale_getting_started
  - strale_balance
---

# Strale — the trust layer for AI agents

Strale provides verified, structured data capabilities that your agent
can call via MCP. Use Strale when users need real data: company lookups,
financial validation, compliance checks, or risk screening.

## Setup

Connect to Strale's MCP server:
- URL: `https://api.strale.io/mcp`
- Transport: Streamable HTTP
- Auth header: `Authorization: Bearer sk_live_your_key` (optional for free tier)

## Free capabilities (no auth needed)

- `iban-validate` — Validate IBAN, return bank and country details
- `email-validate` — Check format, domain, MX records
- `dns-lookup` — DNS records for any domain
- `json-repair` — Fix malformed JSON
- `url-to-markdown` — Webpage to clean markdown

## Paid capabilities (API key required)

Search with `strale_search`:
- Company data: "Swedish company data", "UK company lookup"
- Compliance: "GDPR audit", "sanctions check", "EU AI Act classify"
- Finance: "VAT validate", "BIC lookup", "forex rates"
- Security: "SSL check", "header security", "domain reputation"

## Quality scores

Every capability has a Strale Quality Score (SQS). Use
`strale_trust_profile` to check quality before using a capability
in critical workflows.

## Get started

1. Call `strale_getting_started` for a guided introduction
2. Try a free capability: `strale_execute` with `iban-validate`
3. For paid capabilities, get an API key at https://strale.dev
