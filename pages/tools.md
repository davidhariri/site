---
title: "Tools"
description: "The tools that I use day to day to build software"
date_published: 2022-11-14
date_last_updated: 2024-11-09
---

The following are most of the tools that I use day to day to build software. They are the tools I most understand, most rely on and the tools that I am most fond of. I think people might be surprised at how vanilla my set up is. I am typically the last person to adopt a new tool because I favour the things I know how to use productively.

### Qualities of Good Tools

Over the years, I've tried lots of tools. The ones that have stuck around for me share some mix of these qualities:

- Simple
- Fast
- Approachable
- Composable

### Client-Side

**[HTMX](https://htmx.org)**

Most of the time, I just need a little bit of extra interactivity. HTMX is the tool I now turn to for this first.

**[Typescript](https://www.typescriptlang.org)**

I'll be honest, when I first tried TS, I really didn't like it. I wasn't used to type-safe programming and thought having to declare the type of everything was unneesary. Now, having seen so many problems arise from type-unsafe projects, I sware by type safety.

**[React](https://reactjs.org)**

There are times where a lot of interactivity is needed. When that happens, I will build a server-side API and use React to interface with it. React is still really good. I find that I can go very far with its STL and [`swr`](https://swr.vercel.app).

**[Tailwind](https://tailwindcss.com)**

I resisted Tailwind for a long time, but as I started doing a lot more prototyping, I came to appreciate its utility. Now that I use an LLM to generate a lot of my client-side code, I find that I'm more productive asking for inline tailwind classes rather than writing lots of my own CSS boiler plate.

**[Parcel](https://parceljs.org)**

I have used other tools for bundling like Webpack, Babel, Gulp and Grunt in the past. I find them all to ask the developer to learn and configure far too much. Parcel is the tool I turn to to make compiling my JS and CSS a non-event.

### Server-Side

**[Python 3.12](https://www.python.org)**

Before 2013 I wrote server-side code in PHP. I credit [Brendan Lynch](https://brendanlynch.com) with introducing me to Python and the basic tools. The language has come a long way since 2.7. It's my favourite programming lanuage and the one I recommend without hesitation to anyone.

**[Flask 2](https://flask.palletsprojects.com/en/2.0.x/)**

More often than not, I use Flask to create web apps. I find that it's just the right amount of abstraction for most of my projects.

**[FastAPI](https://fastapi.tiangolo.com)**

When I need to build an API, I turn to FastAPI. It's the fastest way to get a basic API off the ground and I love using Pydantic to handle my data and generate OpenAPI schemas.

**[Redis](https://redis.io)**

Redis is the database I turn to for caching, session storage and pub/sub. It's fast, elegant and the integration with Python is seamless.

**[MongoDB](https://www.mongodb.com)**

Mongo gets a lot of criticism, but it's scaled very well for Ada and I appreciate not having to declare a schema before saving data.

**[Fly](https://fly.io)**

Infra has never been of much interest to me. I can run `kubectl` and have deployed to AWS in the past, but I have always favored paying PaaS' like Fly to worry about my infrastructure whenever possible. I also usually work at the early stages of projects where costs are not as important to tune.

Before 2021, I used Heroku to deploy applications to the internet. I moved away from Heroku because the platform began showing a lack of maintenance from their acquirers.

Before 2016 I would use Digital Ocean droplets and run and update applications. If I wanted to trade a bit of value for complexity, I would move a project off Heroku to Digital Ocean.

### Computer Hardware

**Mac Studio**

This computer is terrific value. It's very fast, virtually silent and has all of the ports I need. My configuration has tons of RAM and a GPU for running [ollama](https://ollama.com) locally for experimentation with open source models.

**Apple Pro Display XDR**

I use this display for most of my work. It's bright, has great color and the size is perfect for my needs.
