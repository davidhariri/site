---
date_published: '2024-11-02'
description: Just found an incredible guide on building LLMs as a judge by Hamel Husain!
  Super insightful, especially since we’re using a similar system at Ada to evaluate
  transcript resolutions. Excited about how smartly it's avoiding blind spots in test
  coverage!
tags:
- LLMs
- Evals
title: Creating an LLM-as-a-Judge
---

[This guide](https://hamel.dev/blog/posts/llm-judge/#the-problem-ai-teams-are-drowning-in-data) to creating #LLMs-as-a-judge systems by Hamel Husain is the best I’ve ever seen.

[Ada](https://ada.cx) uses one of these in production to evaluate whether transcripts resolved or not (and the reasons for why they don’t). We used domain experts to ensure it works, but we didn’t use scenario, feature and persona dimensions. This is a very clever way to try to avoid blind spots in test coverage.