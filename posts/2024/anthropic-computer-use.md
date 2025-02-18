---
date_published: '2024-10-30'
description: Just tried out Anthropic's Computer Use demo in a Docker setup! It can
  control a virtual machine and run tasks like adding a knowledge base for our bots.
  Super impressive, but it did trip up on some commands and interactions. Excited
  to see where this tech goes!
tags:
- LLMs
- AI Agents
title: Anthropic Computer Use
---

I just tried out [Anthropic’s Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use) demo Docker image. The way it works is it spins up a virtual machine in Docker and connects it through [noVNC](https://novnc.com/info.html) to a Streamlit app, also hosted by the Docker image. To use it, you type instructions in the Chat box and then the model decides what to do. It seems to be in control of when to take screenshots as a discrete action as well as when and where to interact with the virtual machine. It knows that it has access to Firefox and bash to run shell commands. 

![](/static/media/88906220-5ccc-472a-90bc-ac2393fdcd67.png)

I wanted to see if it could add a knowledge base to one of our bots. The high-level idea being *“can this LLM agent build another LLM agent”?*

It was able to add a knowledge base for [anthropic.com](https://anthropic.com) and even evaluate the agent’s performance on a few example questions it came up with. But, when I asked it to add guidance based on its evaluations, it stumbled over the instruction and got lost in writing bash commands to launch Firefox. Here’s a list of things I saw it stumble over: 

- Understanding how to dismiss modals like our “test chat” modal by clicking outside of it
- Clearing inputs before pasting text (it just keeps pasting on top of its previous text)
- Scrolling elements with overflowing content. It seems to only be able to issue `Page_Up` and `Page_Down` commands (?)
- Handling crashes in an app (like Firefox)

So, overall, I’m pretty impressed. It’s the best demo of its kind that I have seen and one of the first I’ve been able to run on my own machine. In a few iterations, I think this could be a pretty big deal for RPA.

#LLMs #Anthropic #Claude