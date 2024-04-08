---
title: Tags!
date: 2024-04-08 00:00:00+00
tags: 
- web
- code
- site updates
description: I added tags to my blog posts. You can use them to browse my posts now.
---
When I started this blog, I had always intended to have post tagging by including `tags` in the [front matter](https://indieweb.org/frontmatter) of posts and the `Post` class. It works like this:

```
---
title: Tags
tags: 
- web
- code
description: ...
---
```

This morning, Monica woke up very early and I coudn't get back to sleep so I finally got around to implementing them. Lately, I've been putting [Cursor](https://www.cursor.sh/) to the test. It was able to do most of the work- about half of it in a single try!

Anyways, tags are now implemented on this site. You can use them to [browse my posts](/blog/). I'm still working on retroactively tagging posts from 2022. If you want to see the code, it's [on GitHub](https://github.com/davidhariri/site/pull/31/files).

