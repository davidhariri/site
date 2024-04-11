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

I was having a conversation over email with [Louie Mantia](https://lmnt.me) on the weekend about how to get more people writing on their own domain. He had [envisioned](https://lmnt.me/blog/sketchbook/punk.html) a combination RSS reader and publisher a while back which I thought looked so great (no surprise there).

Most self-hosted publishing products have a fritcion problem when compared to writing on blogging products like Medium or X. For example, when I want to write a new post on this blog, I have to pull out my code editor, create a new Markdown file, write the post, and then push it to the repository. This is a lot of "not writing" when the goal is to write, not to mention that I have to know about Github and use `git` for it all to work.

[Rook](github.com/davidhariri/rook) so far is a good solution for people who already understand web applications, blogging and markdown. It's not great for people who just want to write. I think what I need to do now is take a step back and work backwards from the workflow I want to have. I want to, whether I'm on the go or at home, wip out an editor and publish a thought. It should be as easy as posting on Twitter to update my blog, but I want to be able to have the full expressiveness Markdown offers and use a great editor like iA Writer on my iPhone.

I think there's an opportunity to build (or adopt..?) a standard protocol that any blog server could implement which would define how a client can list, edit and create posts. We have this for making web requests to APIs, why not for publishing? Perhaps it could define a common standard for commenting and re-sharing?

```yaml
openapi: 3.0.0
info:
  title: Blog API
  description: API for managing blog posts
  version: "1.0"
servers:
  - url: https://example.com/api
paths:
  /posts/:
    get:
      summary: List posts with pagination
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
          description: Page number
        - in: query
          name: size
          schema:
            type: integer
            default: 10
          description: Number of items per page
      responses:
        '200':
          description: A paginated list of posts
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPosts'
    post:
      summary: Create a new post
      security:
        - basicAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Post'
      responses:
        '201':
          description: Post created
  /posts/{canonical_id}:
    patch:
      summary: Update a post
      security:
        - basicAuth: []
      parameters:
        - in: path
          name: canonical_id
          required: true
          schema:
            type: string
          description: Canonical ID of the post to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Post'
      responses:
        '200':
          description: Post updated
  /feed/:
    get:
      summary: Get RSS feed
      responses:
        '200':
          description: RSS XML feed
          content:
            application/rss+xml:
              schema:
                type: string
components:
  securitySchemes:
    basicAuth:
      type: http
      scheme: basic
  schemas:
    PaginatedPosts:
      type: object
      properties:
        total:
          type: integer
        pages:
          type: integer
        page:
          type: integer
        size:
          type: integer
        items:
          type: array
          items:
            $ref: '#/components/schemas/Post'
    Post:
      type: object
      properties:
        canonical_id:
          type: string
        title:
          type: string
        content:
          type: string
        date:
          type: string
          format: date-time
        tags:
          type: array
          items:
            type: string


```

I looked into [ActivityPub](https://activitypub.rocks/), but it seems to be more focused on social media and it defines more of how a federated network can be used to share content rather than individual blogs on single tenant domains. Another interesting protocol is [WebMention](https://indieweb.org/Webmention), but it seems like there is a high degree of variability in [people's implementations](https://indieweb.org/Webmention#IndieWeb_Examples) and it only solves the comment box problem, not publishing. Another solutions I saw was [what Hey is doing](https://www.hey.com/features/email-the-web/). On Hey you can email `world@hey.com` from your own address and it publishes the email as a blog post on your Hey blog. That's a cool idea because it will work from nearly anywhere and it you get drafts for free. 

I will keep digging to find what to do for Rook to make it dead easy to post to it.