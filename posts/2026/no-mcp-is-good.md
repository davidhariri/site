---
title: MCP is not for you
date_published: 2026-03-24
tags:
    - AI
    - LLMs
    - MCP
description: The one in which I refute the recent arguments against MCP and where I think it's coming from.
---

Lately, I've been reading that MCP is "dead".

> "MCP provides no real-world benefit, and that we'd be better off without it."

— [MCP is dead; long live the CLI](https://ejholmes.github.io/2026/02/28/mcp-is-dead-long-live-the-cli.html)

> "If you want the agent to do something that it doesn't do yet, you don't go and download an extension or a skill or something like this. You ask the agent to extend itself."

— [Pi: The Minimal Agent Within OpenClaw](https://lucumr.pocoo.org/2026/1/31/pi/)

> "The reason I think MCP may be a one-year wonder is the stratospheric growth of coding agents."

— [2025: The year in LLMs](https://simonwillison.net/2025/Dec/31/the-year-in-llms/)

If you're a developer sitting in a terminal with a self-assembling coding agent like pi, openclaw or Claude Code, CLIs and an open network work great. Your agent can shell out to anything. Why would we need anything more? Let's think about this as a system developer instead of as a hacker.

## Where Does the CLI Run?

If you've never deployed sandboxes at scale, giving agents CLIs sounds easy. It is not. Keeping a warm pool alive, persisting disk changes between agent loops, managing cold starts, injecting authentication without risk of exfiltration, sticky sessions through reverse proxies — there's [a whole industry](https://e2b.dev/) of companies that exist solely to manage this for you (for a toll).

An MCP tool call is a single, standardized network round-trip. Depending on the server, the lower bound is 20ms. That's at least an order of magnitude faster than the lower bound on a warm sandbox's start up. The server does whatever orchestration it needs internally and returns a result straight to the client without any need for intermediation.

## CLIs Were Not Made for Agents

CLIs were barely made for humans.

MCP schemas carry affordance hints — `readOnlyHint`, `destructiveHint`, `idempotentHint` — that tell the client how dangerous a tool is. Claude uses these to auto-allow safe read-only tools while prompting for approval on destructive ones. CLIs have nothing like this. The client has no way to know that `rm` is scarier than `ls` without someone hardcoding that. My mom might think `rm` means "remember" or "remind". 

MCP servers also act as a policy boundary. You expose `query_database` without exposing `drop_table`. With a CLI, the agent gets whatever the binary gives it.

## MCP Servers Burn Tokens

> "[MCP] demands too much context. You must supply significant upfront input, and every tool invocation consumes even more context than simply writing and running code."

— [Tools: Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/)

True. Or at least, it was. Claude Code now [defers tool loading](https://www.atcyrus.com/stories/mcp-tool-search-claude-code-context-pollution-guide) on demand (85% reduction). Cloudflare's [Code Mode](https://blog.cloudflare.com/code-mode-mcp/) collapses entire APIs into two tools (99.9% reduction).

More broadly, using the sub-agent pattern for scoped task execution is a terrific way to manage main thread context bloat.

## End Users Don't Have API Tokens

Most CLIs need an API token. If you're a B2B SaaS deploying agents on behalf of your customers, you cannot have a userbase sharing a single API token and its priveleges. You need OAuth flows where the end user authenticates through your existing system and the agent gets scoped access on their behalf.

I fail to see how this can be done as neatly and securely as MCP provides.

But I do concede that the MCP auth story is _still cooking_. It's a hell of a lot better than it was in 2025. The [2026 roadmap](https://workos.com/blog/2026-mcp-roadmap-enterprise-readiness) is still working on SSO flows and gateway patterns. But at least MCP is trying to solve this. CLIs don't even acknowledge this problem exists because they were built for developers, not systems.

MCP is not for you, the developer in a terminal. It's for systems and end-users who have never, and will never think about code.
