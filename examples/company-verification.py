# Verify a company with AI agents using Strale
#
# This script shows how to use Strale as a data source for agent-driven
# company verification. One API call returns structured company data
# with an independently measured quality score (SQS).
#
# Strale is the trust layer for AI agents.
# https://strale.dev
 
import httpx
import json
 
STRALE_API_KEY = "sk_live_YOUR_KEY_HERE"  # Get yours free at https://strale.dev/signup
BASE_URL = "https://api.strale.io"
 
async def verify_company(org_number: str, country: str = "SE") -> dict:
    """
    Verify a company using Strale. Returns structured company data
    with quality score and provenance.
    
    Works for Swedish (SE), UK, German, French, Dutch, and 20+ other
    country company registries.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/v1/do",
            headers={"Authorization": f"Bearer {STRALE_API_KEY}"},
            json={
                "capability_slug": "swedish-company-data",
                "inputs": {"org_number": org_number},
                "max_price_cents": 100  # €1.00 max
            }
        )
        result = response.json()
        
        print(f"Company: {result['output'].get('name', 'Unknown')}")
        print(f"Revenue: {result['output'].get('revenue_sek', 'N/A')} SEK")
        print(f"Employees: {result['output'].get('employees', 'N/A')}")
        print(f"Quality score (SQS): {result.get('sqs_score', 'N/A')}/100")
        print(f"Price: €{result['price_cents'] / 100:.2f}")
        print(f"Data source: {result.get('provenance', {}).get('source', 'N/A')}")
        
        return result
 
# --- The fallback pattern: use Strale only when your own code fails ---
 
async def verify_company_with_fallback(org_number: str) -> dict:
    """
    Try your own data source first. Fall back to Strale if it fails.
    This is the recommended integration pattern — Strale as a safety net.
    """
    try:
        # Your existing company lookup logic
        data = your_company_lookup(org_number)
        return data
    except Exception:
        # Strale catches what your code can't handle
        return await verify_company(org_number)
 
# --- Using Strale's MCP server with Claude Code or Cursor ---
#
# No SDK needed. Add to your MCP config:
#
# {
#   "mcpServers": {
#     "strale": {
#       "type": "streamableHttp",
#       "url": "https://api.strale.io/mcp",
#       "headers": {
#         "Authorization": "Bearer sk_live_YOUR_KEY_HERE"
#       }
#     }
#   }
# }
#
# Then ask your AI assistant:
# "Use Strale to look up Swedish company 559106-8089"
 
if __name__ == "__main__":
    import asyncio
    # Example: Look up a Swedish company
    asyncio.run(verify_company("559106-8089"))
