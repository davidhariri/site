---
date_published: 2024-10-16
description: 'Exploring the Micropub spec and its integration with iA Writer, I’ve
  implemented a way to post directly to my blog from the app, embracing the #indieweb
  ethos along the way.'
tags:
- IndieWeb
- Web
- Site Updates
title: Micropub
---

I recently learned that Wordpress, [Micro.blog](https://Micro.blog) and [many others](https://indieweb.org/Micropub/Servers) follow a common spec for creating, editing and deleting posts to their respective sites. It’s called [Micropub](https://www.w3.org/TR/micropub/) and I guess it’s part of the #indieweb philosophy? movement? ethos? Also just learning about that one too.

So then I learned that [iA Writer](https://ia.net/writer) (a very nicely made MacOS and iOS markdown editor which I have been using for years) supports the spec! So, naturally, I had to [implement the spec](https://github.com/davidhariri/site/blob/ecdac38df61c39a14199990f56e3f551af2da182/app.py#L101) on my site’s Flask app.

**So, now I can post directly from ia to my blog!** What a time to be alive.

And the cherry on top was this hilarious remark from [George Mandis](https://george.mand.is/2023/05/publishing-to-11ty-with-ia-writer-and-micropub/#:~:text=My%20desire%20to%20manage%20my,CMS%20like%20one%20of%20those.) which I also stumbled upon today:

> My desire to manage my blog this way versus, say, setup a Ghost blog or even return to WordPress kind of amuses me. If it was really about the writing, I think there's a strong argument for adopting a CMS like one of those. But... what can I say? I like projects.

Same, George. Same.