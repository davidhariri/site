---
date_published: 2024-04-08
description: I've open sourced the code that powers this website
tags:
- Projects
- Web
title: Announcing Rook
---

Back in 2014 when I was starting to hone my PHP skills, I had the idea to make my own website publishing product. I didn't mind if no one else could use it, I just wanted it to work super well for me so that I could write on [my own wall](/) from anywhere. I called it 'Rook' and I think [Mike](https://murch.me) was actually able to get it running for himself too at one point.

10 years later, I'm still scratching my own itches. This time, I wanted to give it to everyone so more people can become indie web publishers. Here it is:

![First screenshot of Rook](/static/posts/images/rook-1-screen.webp)

**What's Rook For?**

1. Hosting your own combination website and blog (like this one!)
2. Boils web publishing down to two concepts: Pages and Posts. Pages are living and can be updated regularly (ex. /about). Posts are your blog posts and are served at /blog/post.md .
3. Runs on a server that you control on your domain. You can see and modify any of the code if you want to, or just stick to changing `config.yaml`.
4. Uses [Markdown](https://daringfireball.net/projects/markdown/) for all post and page content.
5. Uses FTP (or SSH if you prefer) and hot reloading. Just drag and drop `.md` files onto your server to publish.

You can read more and find out how to [run it yourself here](https://github.com/davidhariri/rook). Please enjoy!