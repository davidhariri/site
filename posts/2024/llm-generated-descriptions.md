---
date_published: 2024-10-16
description: In this blog post, I share a recent enhancement to my website's intake
  endpoint that utilizes LLM technology to automatically generate short descriptions
  for my blog posts. By integrating OpenAI's API, I can now effortlessly create engaging
  summaries whenever I upload new content. I discuss the process behind this implementation,
  its effectiveness with past examples, and my plans to add features for generating
  tags based on existing ones. Dive in to learn how AI is transforming the way I present
  my ideas online!
tags:
- LLMs
- Site Updates
title: LLM-Generated Descriptions
---

I just added a bit of code to my site’s intake endpoint to create #LLM generated descriptions from my blog posts so that when I upload a thought from ia writer, it gets a description for the /blog/ index page.

```py
if not description and settings.OPENAI_API_KEY:        
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short descriptions for blog posts."
                },
                {
                    "role": "user",
                    "content": f"""Generate a short description for the following blog post content:

<content>
{content}
</content>.

For example: 'Quick notes on my interview on the Hard Part Interview podcast.' or 'I made a thing that converts your pocket saves into an rss feed'

Do not write anything else other than the description and do not wrap the description in quotes."""
                }
            ],
            model="gpt-4o-mini",
        )
        description = response.choices[0].message.content
```

Pretty simple stuff, but it works well with just a couple of past examples. When I didn’t have the examples, the descriptions didn’t sound like my voice, but with them, they’re not bad and cheap as chips.

Later, I’ll add a prompt to create tags, choosing from the ones I’ve already created.