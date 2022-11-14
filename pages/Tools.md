_Updated November 14 2022_

The following are most of the tools that I use day to day to build software for the web. They are the tools I most understand, most rely on and the tools that I am most fond of. I think people might be surprised at how vanilla my set up is. I am typically the last person to adopt a new tool because I favour the things I know how to use productively.

### Qualities of Good Tools

Over the years, I've tried lots of tools. The ones that have stuck around for me share some mix of these qualities:

- Simple
- Fast
- Approachable
- Composable

### Client-Side

**[Typescript](https://www.typescriptlang.org)**

I'll be honest, when I first tried TS, I really didn't like it. I wasn't used to type-safe programming and thought having to declare the type of everything was unneesary. Now, having seen so many problems arise from type-unsafe projects, I sware by type safety.

Before 2020 I just wrote JS in ES6 syntax and transpiled it to ES5.

Before 2014 I tried out [Coffeescript](https://coffeescript.org) and liked it. I can't recall why I didn't stick to it. Perhaps this primed me to love Python's syntax?

**[React](https://reactjs.org)**

Before 2014, I used JQuery for most of my client-side JavaScript. _React was a rare case where I threw myself head first in to a comparitively new technology. Something about its design struck me immediately as "right". I have been using React since 0.12 (2014)._

**[SASS](https://sass-lang.com)**

Before 2014 I just wrote a lot of poorly organized and sprawling CSS files.

**[Parcel](https://parceljs.org)**

I have used other tools for bundling like Webpack, Babel, Gulp and Grunt in the past. I find them all to ask the developer to learn and configure far too much.

### Server-Side

**[Python 3.11](https://www.python.org)**

Before 2013 I wrote server-side code in PHP. I credit [Brendan Lynch](https://brendanlynch.com) with introducing me to Python and the basic tools. The language has come a long way since 2.7. It's my favourite programming lanuage and the one I recommend without hesitation to anyone.

**[Flask 2](https://flask.palletsprojects.com/en/2.0.x/)**

**[Redis](https://redis.io)**

**[PostgreSQL](https://www.postgresql.org)**

**[Fly](https://fly.io)**

Infra has never been of much interest to me. I have run `kubectl` and deployed to AWS in the past, but I have always favored paying Heroku to worry about my infrastructure whenever possible. I also usually work at the early stages of projects where costs are not as important to tune.

Before 2021, I used Heroku to deploy applications to the internet. I moved away from Heroku because the platform began showing a lack of maintenance from their acquirers.

Before 2016 I would use Digital Ocean droplets and run and update applications. If I wanted to trade a bit of value for complexity, I would move a project off Heroku to Digital Ocean.

**[Docker](https://www.docker.com)**

Before 2021 I would just use virtualenv, .env files and detailed instructions to set up local development. Docker makes this more scalable for teams, but I don't use it for personal projects unless they require specific versions of databases.

### Computer Hardware

**Mac Mini M1**

This computer is terrific value. It's very fast, silent and has the ports I need. If I end up doing more ML work locally, I will replace it with the rumored Mac Pro with Apple Silica.

**Apple Pro Display XDR**

I wouldn't recommend this display. Here's why:

1. Poor value. The price point makes it pretty hard to recommend. You pay more for the _how did they do that?_ hardware.
2. The matrix of backlighting is visible as darker vertical bands in certain situations. For example, when I swipe from one virtual desktop to another. My guess is that the refresh rate of the backlighting is lower than the LCD.
3. There is a ghosting / halo effect in high-contrast, on-black conditions. For example, when the Apple TV logo appears before "Swan Song (2021)"
