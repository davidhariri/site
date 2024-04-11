---
title: Friction to Publish
description: It's too hard to publish a blog post on this site.
date: 2024-04-09 20:46:00-0400
tags:
- rook
- code
- design
- RSS
---

I was having a conversation over email with [Louie Mantia](https://lmnt.me) on the weekend about how to get more people writing on their own domain. He had [envisioned](https://lmnt.me/blog/sketchbook/punk.html) a combination RSS reader and publisher a while back which I thought looked so great (no surprise there). He thinks [hand-making your own website](https://lmnt.me/blog/why-by-hand.html) is the best way for people to publish themselves on the web. He even wrote up an [awesome guide](https://lmnt.me/blog/how-to-make-a-damn-website.html) on how to do it for people with no prior experience. I think people should own their writing (as in files) and that writing should be on their own domain, but I don't think that should mean that people have to learn how to code and understand FTP. While I obviously think html is charming and a great, expressive, language, I know most people are intimidated by the thought of writing code, even it's just markup and CSS.

Most self-hosted publishing products have a fritcion problem when compared to writing on blogging products like Medium or X. For example, when I want to write a new post on this blog, I have to pull out my code editor, create a new Markdown file, write the post, and then push it to the repository. This is a lot of "not writing" when the goal is to write, not to mention that I have to know about Github and use `git` for it all to work.

[Rook](https://github.com/davidhariri/rook) so far is a good solution for people who already understand web applications, blogging and markdown. It's not great for people who just want to write. I think what I need to do now is take a step back and work backwards from the workflow I want to have. I want to, whether I'm on the go or at home, whip out an editor and publish a thought. It should be as easy as posting on Twitter to update my blog, but I want to be able to have the full expressiveness Markdown offers and use a great editor like iA Writer on my iPhone.

I think there's an opportunity to build (or adopt..?) a standard protocol that any blog server could implement which would define how a client can list, edit and create posts. We have this for making web requests to APIs, why not for publishing? Perhaps it could define a common standard for commenting and re-sharing?

```yaml
# Scaffold blog site protocol:

# Public endpoints
- GET /posts/
- GET /posts/{canonical_id}
- GET /feed/ # RSS feed

# Private (Requires Basic HTTP Auth headers)
- POST /posts/
- PATCH /posts/{canonical_id} # edit a post
- DELETE /posts/{canonical_id}
```

A client could be written in Swift for MacOS, React, etc. and could simply implement the protocol and work with anyones choice of blogging service (home made, open source, or totally centralized).

I was curious about prior art and so I looked into [ActivityPub](https://activitypub.rocks/), but it seems to be more focused on social media and it defines more of how a federated network can be used to share content rather than individual blogs on single-tenant domains. Another interesting protocol is [WebMention](https://indieweb.org/Webmention), but it seems like there is a high degree of variability in [people's implementations](https://indieweb.org/Webmention#IndieWeb_Examples) and it only solves the comment box problem, not publishing. Another solution I saw was [what Hey is doing](https://www.hey.com/features/email-the-web/). On Hey you can email `world@hey.com` from your own address and it publishes the email as a blog post on your Hey blog. That's a neat idea because it will work from nearly anywhere and you get drafts for free.

I will keep digging to find what to do for [Rook](https://github.com/davidhariri/rook) to make it dead easy to at least post to it...

