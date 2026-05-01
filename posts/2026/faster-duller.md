---
title: I am getting faster (and duller)
description: Reflecting on a month of shipping a lot, but with a noticable trade off to understanding.
date_published: 2026-05-01
tags:
  - LLMs
  - Claude
  - Programming
  - AI
---

> You can outsource your thinking to a computer
> But not your understanding
> — [@yacineMTB](https://x.com/yacineMTB/status/2042207940690502134)

Been feeling like this a lot lately. I shipped 76 PRs in April. On the surface, this is impressive[^1] (to me, at least). But as I reflect on April, I feel estranged from my code in a way I think I rightfully should be worried about.

```
⏺ For April 2026 in this repo (••••••):

  - PRs shipped: 76
  - Median line count (additions + deletions): 242

  (Mean was ~656, skewed by a few large PRs like the -12,849 line cleanup and the iOS app addition.)
```

In May, I'm going to stop Claude maxxing everything and try to add some nuance to my development process to see if I gain back some intuition for the system. I'm thinking something like this:

- For improvements, write them in Cursor or Zed, using tab complete and the Ask mode in the AI chat window.
- For refactoring, similar to above, but grunt out code removal operations once I'm finished planning.
- For bug fixes, grunt out tracing with logfire, sentry and railway logs, but plan the fix myself in Cursor afterwards. Again, using Ask mode along the way in there to get help as I work.
- For research, find primary sources using AI + Firecrawl, but do more of the reading myself again and rely less on summaries.

I spent today doing this and it felt slow. Like when you start Zone 2 training for the first time. We'll see if it has the same gains on the other side.

---

[^1]: My friend Josh [merged 164](https://x.com/joshuakelly/status/2049943718816285018?s=20) proving that a 10x eng's multiplier moves with their use of AI.
