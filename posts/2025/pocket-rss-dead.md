---
date_published: 2025-06-07
description: I pulled the plug on pocket-rss.com
tags:
- RSS
- Web
title: Pocket to RSS is No More
---

As you may have heard already, Mozilla has decided to kill Pocket on July 8th 2025[^1]. This means that pocket-rss.com, my fun little way of repairing the RSS feature that Mozilla removed from Pocket will no longer work. I made the call to just wind down the service today. The truth is, I've been getting Sentry alerts telling me that Mozilla already doesn't care about API consumers like pocket-rss.com. My server's requests for user's Pocket saves would routinely fail with 503 errors since I launched the app. I had wondered if Mozilla was intentionally strangling their API's resources as a way to cut costs. I am now almost certain this was the case.

So, if you used pocket-rss.com, I hope it was of some value and I hope you've moved to [Instapaper](http://instapaper.com) or [Matter](https://hq.getmatter.com) by now.

**Stats**

- 186 users
- ~1rps
- Monolith Flask app
- $2.40 / month to operate (not including the domain)
- Used Fly, Redis and Mongo Atlas

[^1]: [Pocket is saying goodbye - What you need to know](https://support.mozilla.org/en-US/kb/future-of-pocket)
