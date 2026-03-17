strale-agent-skills
Skills and rules that teach AI coding agents how to use Strale — the trust layer for AI agents.
What is this?
AI coding agents (Claude Code, Cursor, GitHub Copilot, Windsurf) auto-pull skill files from repos to learn how to use tools correctly. This repo contains the skill definitions that teach these agents:

When to use Strale vs. raw APIs
How to call Strale capabilities with the correct patterns
How to interpret quality scores (SQS) and make trust decisions
How to handle errors and fallbacks
How to build for EU AI Act compliance

Quick start
For Claude Code / Cursor / Windsurf users
Add Strale to your MCP config:
json{
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
Then copy the skills/strale/ folder into your project's .cursor/skills/, .claude/skills/, or .github/skills/ directory. Your AI agent will automatically use it.
For framework users

LangChain: pip install langchain-strale
CrewAI: pip install crewai-strale
Semantic Kernel: dotnet add package Strale.SemanticKernel

Files
FilePurposeSKILL.mdMain skill file — connection, patterns, quality scores, use casesexamples/company-verification.pyPython example: verify a Swedish companyexamples/iban-validation.pyPython example: validate IBANs (free, no API key)examples/agent-with-strale.tsTypeScript example: sanctions + lead enrichment agent
Free capabilities
5 capabilities work without signup (10/day per IP):

email-validate — Validate any email address
dns-lookup — DNS records for any domain
json-repair — Fix malformed JSON
url-to-markdown — Convert any URL to markdown
iban-validate — Validate IBAN numbers

Try them now — no API key needed.
Links

Capabilities catalog — Browse 225+ capabilities
Quality methodology — How SQS scores work
API docs — Full API reference
Sign up — Free €2 credits, no card needed

Strale is the trust layer for AI agents.
