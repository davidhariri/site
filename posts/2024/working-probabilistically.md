---
date_published: 2024-10-17
description: Exploring the importance of thinking probabilistically when working with
  LLMs, this post highlights insights on effective eval methodologies, the quirks
  of model behavior, and practical tips for building robust evaluation processes that
  go beyond traditional testing.
tags:
- LLMs
- Evals
title: Working Probabilistically
---

Working Probabilistically

I was chatting with a co-worker today about how powerful [evals](https://medium.com/@carolzhu/all-about-llm-evals-8a155a1235c7) are for code that relies on #LLMs. How we both felt evals were still not taken as seriously as they should be. He said “we have to get engineers to think probabilistically, rather than functionally” which by I think he meant ‘deterministically’.

So, I largely agree, and was guilty in the past of the common pitfall of building on #LLMs and convincing myself that all possible states must be as good as the handful I observed locally. It’s just not the case with LLMs. I still get strange surprises from flagship models like GPT-4o:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Well, this is a new one. GPT-4o thinks the response was &quot;poetic in nature&quot; ... Hm ... <a href="https://t.co/TBCCgl1NrQ">pic.twitter.com/TBCCgl1NrQ</a></p>&mdash; David Hariri (@davehariri) <a href="https://twitter.com/davehariri/status/1846027015729590423?ref_src=twsrc%5Etfw">October 15, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

So, thinking probabilistically while building on #LLMs is, I think, the following:

1. Knowing that traditional tests of functions that rely on an LLM generation are not very useful (and slow .. and expensive .. if in CI)
2. Functions that rely on LLMs can exhibit kooky behaviour. Constrain what is a valid generation as much as possible with [structured output](https://platform.openai.com/docs/guides/structured-outputs). [`Pydantic`](https://docs.pydantic.dev/latest/) + OpenAI’s new `parse` method is great for that:

```py
class SemanticIntentEvaluation(BaseModel):
        passed: bool
        reason: Optional[str] = None
        
response = openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=SemanticIntentEvaluation,
        messages=[
            {
                "role": "system",
                "content": f"""
                Evaluate the following customer service response:

                <response>{response_content}</response>

                Does the response meet the following expectations:
                - {expectations_str}
                """
            }
        ],
        temperature=0,
        top_p=1,
    )

    evaluation_result = response.choices[0].message.parsed
```

3. More often than not, the goal state with #evals is not 100%. Unlike with a test suite, not every eval must score perfect for the system to be in a production-ready state. In fact, 100% performance might be a sign that an eval set is not comprehensive or ambitious enough. 
4. Using human preferences as ground truth is still the gold standard (as far as I know) and an enduring way to evaluate system performance. If you can’t afford that, using slow, smart LLMs like o1-preview to create evals synthetically is also a good option.
5. Comparing strings is a common need for evals. You can embed both strings and use semantic distance and a threshold or you can use another LLM to compare the generation to your eval’s ground truth and give it a score. I also sometimes want to ensure key strings are quoted from source material in generations. So, I supply a list of strings which must be present in the generation and evaluate that deterministically.
6. Building tooling to quickly create evals when bugs are found is a good investment in your teams likelihood to extend the eval set.