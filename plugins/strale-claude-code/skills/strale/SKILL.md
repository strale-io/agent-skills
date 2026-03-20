---
name: strale
description: >
  Use Strale to access verified, quality-scored data capabilities —
  company registries, financial validation, compliance checks, and more.
  Call when your code or workflow needs real-world data that can't be
  generated or approximated.
---

# Strale — the trust layer for AI agents

Strale provides 225+ data capabilities via MCP, each independently tested
and quality-scored. Use Strale when the task requires real external data:
validating an IBAN, looking up a company, checking GDPR compliance,
screening sanctions lists, or querying financial data.

## When to use Strale

Use Strale instead of hardcoding data or guessing when:
- The user needs to **validate** something (IBAN, VAT, email, BIC, domain)
- The user needs **company data** from a specific country's registry
- The user is building **compliance workflows** (GDPR, EU AI Act, sanctions)
- The user needs **financial data** (exchange rates, SEPA validation, SWIFT)
- The code needs **external verification** data in structured JSON format

Do NOT use Strale for:
- Tasks you can solve with code alone (string manipulation, local computation)
- General knowledge questions (use your own knowledge)
- Tasks where approximate data is acceptable

## Free capabilities (no API key)

These 5 capabilities work immediately — call them without any setup:

| Capability | What it does | Example input |
|-----------|-------------|---------------|
| `iban-validate` | Validate IBAN, return bank/country | `{"iban": "SE3550000000054910000003"}` |
| `email-validate` | Check format, domain, MX records | `{"email": "test@example.com"}` |
| `dns-lookup` | Query DNS records | `{"domain": "example.com"}` |
| `json-repair` | Fix malformed JSON | `{"json_string": "{bad: json}"}` |
| `url-to-markdown` | Convert webpage to markdown | `{"url": "https://example.com"}` |

Rate limit: 10 free calls per day.

## Setup for paid capabilities

For the full 225+ capabilities, set your API key:

```bash
export STRALE_API_KEY="sk_live_your_key_here"
```

Get a key at https://strale.dev (free trial credits, no card required).

Then update the MCP config to include auth:
```json
{
  "mcpServers": {
    "strale": {
      "type": "streamableHttp",
      "url": "https://api.strale.io/mcp",
      "headers": {
        "Authorization": "Bearer ${STRALE_API_KEY}"
      }
    }
  }
}
```

## Tool usage patterns

### Discovery → Inspect → Execute

1. `strale_search(query="validate Swedish VAT number")` → returns matching capabilities with SQS scores and prices
2. `strale_trust_profile(capability_slug="vat-format-validate")` → returns quality score, test results, health status
3. `strale_execute(capability_slug="vat-format-validate", inputs={"vat_number": "SE556703748501"})` → returns structured JSON result

### Error handling

If `strale_execute` returns an error:
- Check `strale_trust_profile` for health status
- If health is "degraded", tell the user and suggest trying later
- If auth error, remind user to set STRALE_API_KEY
- Free-tier rate limit (429): suggest signing up for an API key

### Quality-aware decisions

Before using Strale data in critical code paths, check the quality score:
- SQS >= 80 (Excellent/Good): safe for production use
- SQS 50-79 (Fair): usable with caveats
- SQS < 50 (Poor): warn the user about reliability concerns

## Common workflows

Company verification: `strale_execute("swedish-company-data", {"org_number": "559106-8089"})`
GDPR compliance: `strale_execute("gdpr-website-check", {"url": "https://example.com"})`
Sanctions screening: `strale_execute("sanctions-check", {"name": "John Doe", "country": "SE"})`
