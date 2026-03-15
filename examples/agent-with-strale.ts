// Build an AI agent with verified data using Strale
//
// This example shows how to call Strale from a TypeScript agent.
// Every response includes a quality score (SQS) so your agent
// knows how much to trust the data.
//
// Strale is the trust layer for AI agents.
// https://strale.dev

const STRALE_API_KEY = "sk_live_YOUR_KEY_HERE"; // Free signup: https://strale.dev/signup
const BASE_URL = "https://api.strale.io";

// --- Direct API call ---

async function straleExecute(slug: string, inputs: Record<string, any>) {
  const response = await fetch(`${BASE_URL}/v1/do`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${STRALE_API_KEY}`,
    },
    body: JSON.stringify({
      capability_slug: slug,
      inputs,
      max_price_cents: 100,
    }),
  });
  return response.json();
}

// --- Example: Sanctions screening agent ---

async function screenForSanctions(name: string, country?: string) {
  const result = await straleExecute("sanctions-check", {
    name,
    country: country ?? "SE",
  });

  const output = result.output;
  console.log(`Screening: ${name}`);
  console.log(`Match found: ${output?.match_found ?? "unknown"}`);
  console.log(`Lists checked: ${output?.lists_checked?.join(", ") ?? "N/A"}`);
  console.log(`Quality score: ${result.sqs_score ?? "N/A"}/100`);
  console.log(`Price: €${(result.price_cents / 100).toFixed(2)}`);

  return result;
}

// --- Example: Lead enrichment agent ---

async function enrichLead(email: string) {
  // Use a Strale solution (multi-step workflow) for full enrichment
  const result = await straleExecute("lead-enrich", { email });

  console.log(`Lead: ${email}`);
  console.log(`Valid email: ${result.output?.valid}`);
  console.log(`Domain reputation: ${result.output?.reputation_score}/100`);
  console.log(`Tech stack: ${JSON.stringify(result.output?.tech_stack)}`);
  console.log(`Quality score: ${result.sqs_score ?? "N/A"}/100`);

  return result;
}

// --- The fallback pattern ---

async function getDataWithFallback(task: string) {
  try {
    // Your primary data source
    return await yourPrimarySource(task);
  } catch {
    // Strale as safety net — describe what you need in plain language
    const result = await fetch(`${BASE_URL}/v1/do`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${STRALE_API_KEY}`,
      },
      body: JSON.stringify({
        task, // Natural language task description
        max_price_cents: 200,
      }),
    });
    return result.json();
  }
}

// --- MCP config for Claude Code / Cursor / Windsurf ---
//
// Add to your MCP settings (no npm install needed):
//
// {
//   "mcpServers": {
//     "strale": {
//       "type": "streamableHttp",
//       "url": "https://api.strale.io/mcp",
//       "headers": {
//         "Authorization": "Bearer sk_live_YOUR_KEY_HERE"
//       }
//     }
//   }
// }

// --- Run examples ---

async function main() {
  await screenForSanctions("Acme Corporation", "US");
  await enrichLead("jane@acme.com");
}

main().catch(console.error);
