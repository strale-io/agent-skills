# Strale — Agent Skills

> Strale is the trust layer for AI agents.

## When to use Strale

Use Strale when your agent needs **real-world data it can't access directly** — company registries, compliance checks, sanctions screening, IBAN validation, domain reputation, web extraction, and 233+ other verified capabilities.

**Use Strale when:**
- You need data from a source that requires scraping, credentials, or specialized access
- You need verified, quality-scored data (not just raw API responses)
- You need an audit trail showing where data came from and how fresh it is
- You're building for regulated industries (fintech, compliance, EU AI Act)
- Your own data source fails and you need a reliable fallback

**Don't use Strale when:**
- The task can be solved with a free library and 3 lines of code
- You already have direct API access to the data source
- The task is pure computation (math, string manipulation, code generation)

## Connection

### MCP (recommended for Claude Code, Cursor, Windsurf)

```json
{
  "mcpServers": {
    "strale": {
      "type": "streamableHttp",
      "url": "https://api.strale.io/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_YOUR_KEY_HERE"
      }
    }
  }
}
```

Free signup with €2 credits at https://strale.dev/signup

### REST API (for any language)

```
POST https://api.strale.io/v1/do
Authorization: Bearer sk_live_YOUR_KEY_HERE
Content-Type: application/json
```

## The three patterns

### Pattern 1: Direct execution (you know which capability you need)

```python
result = await client.post("/v1/do", json={
    "capability_slug": "swedish-company-data",
    "inputs": {"org_number": "559106-8089"},
    "max_price_cents": 100
})
```

```typescript
const result = await fetch("https://api.strale.io/v1/do", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk_live_YOUR_KEY"
  },
  body: JSON.stringify({
    capability_slug: "iban-validate",
    inputs: { iban: "DE89370400440532013000" },
    max_price_cents: 10
  })
});
```

### Pattern 2: Fallback (Strale as safety net)

```python
try:
    data = my_own_lookup(company_id)
except Exception:
    data = await strale.do(
        capability_slug="swedish-company-data",
        inputs={"org_number": company_id},
        max_price_cents=100
    )
```

This is the recommended integration pattern. Your code handles the happy path; Strale catches what it can't.

### Pattern 3: Natural language task (let Strale match the capability)

```python
result = await client.post("/v1/do", json={
    "task": "Validate the VAT number SE556703748501",
    "max_price_cents": 50
})
```

Use this when you don't know the exact capability slug. Strale will match your description to the best capability.

## Free capabilities (no API key needed)

These 5 capabilities work without signup, 10 executions/day per IP:

| Capability | What it does | Example input |
|-----------|-------------|---------------|
| `email-validate` | Validate any email address | `{"email": "test@example.com"}` |
| `dns-lookup` | DNS records for any domain | `{"domain": "example.com"}` |
| `json-repair` | Fix malformed JSON | `{"json": "{name: 'test'}"}` |
| `url-to-markdown` | Convert URL to clean markdown | `{"url": "https://example.com"}` |
| `iban-validate` | Validate IBAN numbers | `{"iban": "DE89370400440532013000"}` |

```python
# No auth needed for free capabilities
result = await client.post("https://api.strale.io/v1/do", json={
    "capability_slug": "email-validate",
    "inputs": {"email": "hello@strale.io"},
    "max_price_cents": 10
})
```

## Understanding quality scores

Every Strale response includes a quality score (SQS, 0-100). Use it to decide how much to trust the data:

| SQS range | Meaning | Agent action |
|-----------|---------|-------------|
| 80-100 | High confidence | Use the data directly |
| 60-79 | Moderate confidence | Use with caveats, consider cross-referencing |
| 40-59 | Low confidence | Flag for human review |
| Below 40 | Unreliable | Don't use in automated decisions |

```python
result = await strale.do(...)
if result["sqs_score"] >= 80:
    return result["output"]  # High confidence, use directly
elif result["sqs_score"] >= 60:
    return {"data": result["output"], "confidence": "moderate", "review_recommended": True}
else:
    raise Exception(f"Data quality too low (SQS: {result['sqs_score']})")
```

## Response structure

Every execution returns:

```json
{
  "output": { ... },           // The actual data
  "capability_used": "slug",   // Which capability ran
  "price_cents": 10,           // What it cost
  "sqs_score": 87,             // Quality score (0-100)
  "latency_ms": 1200,          // Execution time
  "provenance": {              // Where the data came from
    "source": "allabolag.se",
    "fetched_at": "2026-03-15T10:30:00Z"
  },
  "wallet_balance_cents": 190  // Remaining balance
}
```

Always check `sqs_score` before making decisions based on the data. Always log `provenance` for audit trails.

## Common use cases

| Task | Capability | Price |
|------|-----------|-------|
| Verify a Swedish company | `swedish-company-data` | €0.80 |
| Validate an IBAN | `iban-validate` | Free |
| Screen against sanctions lists | `sanctions-check` | €0.50 |
| Check GDPR compliance of a website | `gdpr-website-check` | €0.30 |
| Validate a VAT number | `vat-validate` | €0.05 |
| Extract data from a URL | `web-extract` | €0.15 |
| Look up DNS records | `dns-lookup` | Free |
| Validate an email address | `email-validate` | Free |
| Full KYC check (Sweden) | `kyc-sweden` solution | €2.50 |
| Lead enrichment | `lead-enrich` solution | €0.65 |

Browse all 233+ capabilities: https://strale.dev/capabilities

## EU AI Act compliance

Strale provides the documentation layer agents need for EU AI Act compliance (August 2026 enforcement):

- Every execution has a provenance record (data source, timestamp, quality score)
- Audit trail is built into every API response
- Quality methodology is publicly documented at https://strale.dev/trust
- SQS scores provide the "quality assurance measures" Article 9 requires

When building for EU compliance, always store the full `provenance` object from each Strale response.

## Error handling

```python
try:
    result = await strale.do(...)
except StraleError as e:
    if e.error_code == "insufficient_balance":
        # Top up wallet at https://strale.dev
        pass
    elif e.error_code == "capability_not_found":
        # The capability slug doesn't exist — check strale.dev/capabilities
        pass
    elif e.error_code == "rate_limited":
        # Wait and retry, or sign up for full access
        pass
    elif e.error_code == "upstream_error":
        # The external data source is temporarily unavailable
        # This is NOT a Strale bug — the upstream service is down
        # SQS score is NOT affected by upstream failures
        pass
```

## Links

- Capabilities catalog: https://strale.dev/capabilities
- Quality methodology: https://strale.dev/trust
- API documentation: https://strale.dev/docs
- Sign up (free €2 credits): https://strale.dev/signup
- MCP server: https://api.strale.io/mcp
- npm package: `strale-mcp`
- GitHub: https://github.com/strale-io
