# Agent Layer — Hard Compliance Constraints

From the hackathon's mandatory AI Resource & Tooling Guide (already reviewed this project). Both of the following were confirmed by direct inspection of the guide's PDF, not assumed:

## 1. No MCP

MCP (Model Context Protocol) appears **zero times** in the mandatory guide. The hackathon's tooling rules were written around a different integration approach. Do not build the agent layer on MCP — it would not comply with the rules this hackathon actually enforces, regardless of how convenient MCP is for tool-calling elsewhere.

## 2. LLM brain: Gemini 2.5 or Groq-hosted only — not Claude

The guide's permitted-LLM table does **not include Claude/Anthropic models**. If `agent/`'s decision logic (§Decide in `agent/README.md`) ends up using an LLM rather than plain threshold rules — e.g. for a more sophisticated congestion-response policy — it must be built on Gemini 2.5 or a Groq-hosted model. This constraint applies to the deployed hackathon submission; it does not apply to this development process itself (this repo and its research were produced with Claude Code, which is fine — the constraint is on what ships).

## Why this file exists

These two constraints are easy to violate by default (MCP and Claude are both the path of least resistance in most current agent tooling) and easy to lose track of once implementation starts. This file is the single place both are stated so nobody has to re-derive them from the PDF mid-build.
