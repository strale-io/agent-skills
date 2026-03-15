# Validate IBANs with AI agents using Strale (free, no API key needed)
#
# This capability is part of Strale's free tier — no signup required.
# 10 free executions per day via the REST API or MCP.
#
# Strale is the trust layer for AI agents.
# https://strale.dev

import httpx

BASE_URL = "https://api.strale.io"

def validate_iban(iban: str) -> dict:
    """
    Validate an IBAN number. Returns validity, country, bank info,
    and check digit verification.
    
    Free tier: no API key needed. 10 executions/day.
    """
    response = httpx.post(
        f"{BASE_URL}/v1/do",
        json={
            "capability_slug": "iban-validate",
            "inputs": {"iban": iban},
            "max_price_cents": 10
        }
        # No Authorization header needed for free-tier capabilities
    )
    result = response.json()
    
    output = result.get("output", {})
    print(f"IBAN: {iban}")
    print(f"Valid: {output.get('valid', 'Unknown')}")
    print(f"Country: {output.get('country', 'N/A')}")
    print(f"Bank: {output.get('bank_name', 'N/A')}")
    print(f"Quality score: {result.get('sqs_score', 'N/A')}/100")
    
    return result

# --- Other free capabilities (no API key needed) ---
#
# email-validate  — Validate any email address
# dns-lookup      — DNS records for any domain
# json-repair     — Fix malformed JSON
# url-to-markdown — Convert any URL to clean markdown
# iban-validate   — Validate IBAN numbers (this script)
#
# All 5 work without signup. 10/day per IP.
# Full catalog (233+ capabilities): https://strale.dev/capabilities

# --- Using with LangChain ---
#
# from langchain_strale import StraleFallbackTool
#
# tool = StraleFallbackTool(api_key="sk_live_YOUR_KEY")
# result = tool.invoke("Validate IBAN DE89370400440532013000")

if __name__ == "__main__":
    # German IBAN example
    validate_iban("DE89370400440532013000")
    
    # Swedish IBAN example
    validate_iban("SE4550000000058398257466")
