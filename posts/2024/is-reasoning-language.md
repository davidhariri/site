---
date_published: '2024-12-17'
description: Exploring the nature of reasoning in AI models, questioning if making
  LLMs express their thoughts out loud limits their potential.
tags:
- LLMs
- Philosophy
- AI Agents
title: Is Reasoning Language?
---

Sometimes when I reason about a problem, I use my inner voice to think through the steps. Sometimes I will even scratch some notes down to keep track of what I’m working through. And this is how models like o1 work today. They emit their chain of thought as “reasoning tokens” as they work through their prompt before arriving at their final completion. 

But Meta has just published[^1] an interesting paper that asks the question: should reasoning happen out loud?

> Neuroimaging studies have consistently shown that the language network – a set of brain regions responsible for language comprehension and production – remains largely inactive during various reasoning tasks 

LLMs seem to have emergent world models which may encode themselves beyond relationships derived from parts of words. These world models are where I think the cross-domain reasoning intelligence is stored. And so, perhaps by asking an LLM to speak its reasoning out loud, we are nerfing it by optimizing it for thought which can be encoded as language.

I know that I often feel the frustration of not being able to communicate a certain symbolic idea because the words escape me. Maybe the best ideas that AGI will help us discover will require totally new language just to express them. And perhaps they can only be discovered by allowing models to reason in their own _inner_ ‘language’ without forcing it to be expressed out loud.

I think as reasoning models become more widely adopted, and as that reasoning happens more often in a hidden-from-output space, great tools for mechanistic interpretability will be important for understanding a models intentions and thought processes.


[^1]: [https://arxiv.org/pdf/2412.06769](https://arxiv.org/pdf/2412.06769)