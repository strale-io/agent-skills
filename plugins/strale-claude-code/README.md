# Strale — Claude Code Plugin

Strale is the trust layer for AI agents. This plugin gives Claude Code
access to 225+ verified data capabilities via MCP.

## Install

From a Claude Code plugin marketplace that includes this repo:
```
/plugin marketplace add strale-io/agent-skills
/plugin install strale@strale-agent-skills
```

## What's included

- **MCP server**: Connects to `api.strale.io/mcp` for live data access
- **Strale skill**: Teaches Claude Code when and how to use Strale's
  data capabilities (validation, company data, compliance, finance)

## Free tier

5 capabilities work without signup or API key:
`iban-validate`, `email-validate`, `dns-lookup`, `json-repair`, `url-to-markdown`

## Full access

Set `STRALE_API_KEY` for 225+ paid capabilities.
Get a key at https://strale.dev (free trial credits).

## Links

- [Strale website](https://strale.dev)
- [MCP server docs](https://strale.dev/docs)
- [Trust methodology](https://strale.dev/trust)
