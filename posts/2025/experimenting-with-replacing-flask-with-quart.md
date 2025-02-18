---
date_published: '2025-01-10'
description: Exploring the benefits of switching from Flask to Quart for improved
  performance and asynchronous capabilities in Ada's application.
tags:
- Ada
- Code
title: Experimenting with Replacing Flask with Quart
---

Tonight I kicked off experimenting with replacing Ada’s monolith application with [Quart](https://quart.palletsprojects.com/en/latest/). The reason I’m interested in Quart is it’s basically a replacement for Flask, but served as a true ASGI application which allows for using an asynchronous event loop to process incoming requests. I say “true” because Flask has asyncio support, but doesn’t fully leverage asyncio’s capabilities, such as cooperative multitasking and non-blocking I/O, resulting in less interesting at-scale performance. My hope with all of this is that Quart and hypercorn dramatically improve our applications throughput per instance and reduce overall latency.

You might be wondering ‘why not FastAPI’? FastAPI is great for API development from scratch, but for an existing Flask application it would be much more work for only incremental improvement in developer experience to migrate it to FastAPI.

So far, the experiment is going pretty well. The application boots up and returns requests quickly, with a few routes purposely disabled for now. I’ve been able to swap `flask-cors` and `flask-limiter` with Quart equivalents. The only snag I ran into so far is some of the advanced features of `flask-limiter` such as creating custom decorators, specifying error messages, and providing breach handlers seem to be missing.