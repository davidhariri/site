---
date_published: 2023-07-30
description: A quick update on this site's performance (it should be a lot faster
  from now on!)
tags:
- Site Updates
title: Site Performance
---

Well, I'm incredibly dumb. In my last post, I complained about my site's performance. I noticed that my P50 load time was around 900ms which is inexcusably slow. I had thought it was because of Flycast or Supabase, but it turned out it was user error.

I profiled the application locally today with [werkzeug's `ApplicationProfiler` module](https://werkzeug.palletsprojects.com/en/2.3.x/middleware/profiler/) and found that my page speed was around 70ms on my machine. So, not Supabase and not something about my application's configuration. I then checked Fly's own metrics and confirmed that HTTP resolution was taking around 1000 ms on average. Up to a 3s P95!

So, I reasoned that it was something about my DNS resolution. I then checked Fly and to my surprise my application was being served from Sydney!

```bash
fly machines list

dhariri-com
ID            	NAME               	STATE  	REGION	IMAGE                                            	IP ADDRESS                      	VOLUME	CREATED             	LAST UPDATED        	APP PLATFORM	PROCESS GROUP	SIZE
3d8d9902f22408	throbbing-bush-9724	started	syd   	dhariri-com:deployment-01GPS1NYBDWFM0Y1TA5ETVF4JA	fdaa:0:5fa8:a7b:f1:74b8:3b78:2  	      	2023-05-26T05:46:02Z	2023-07-30T16:14:53Z	v2          	app          	shared-cpu-1x:256MB
```

Every request to my site (most are from the US or Canada) was making a round-the-world trip to Sydney and back. I'm not sure how this happened, but I'm glad I figured it out. I'm now serving from Seattle, Toronto and my P50 load time is around 100ms so far. Much better!

When I set up this site, I must have done it from Sydney when I was travelling there and so Fly must have defaulted to that region. I am glad I figured this out and didn't have to do anything more drastic. I'm also glad that I didn't have to move to a different platform. I really like Fly (for hobby projects) and I'm glad I can continue to use it.