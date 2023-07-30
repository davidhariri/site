---
title: Recently
date: 2023-07-30 15:46:59+00
tags: 
description: Sharing reflections on a great summer so far in Toronto, embracing AI tools like ChatGPT, evolving in my role at Ada, exploring new coding practices and dabbling in music.
---
Monica and I have been enjoying the summer here in Toronto. It was our 9th anniversary last week and we celebrated it at our family cottage. We had a game of Molky on the lawn, some painting, saunas, swims, running and we tried to recreate one of our all-time favourite meals: Cacio e Pepe and Branzino. It was the best weekend of my summer so far.

<img src="https://guzchhprwtwnbpvtcnhj.supabase.co/storage/v1/object/public/web-images/cottage%20lake.jpeg" style="max-width: 240px" title="Our boat and lake at sunset"/>
<img src="https://guzchhprwtwnbpvtcnhj.supabase.co/storage/v1/object/public/web-images/monica%20painting.jpeg" style="max-width: 240px" title="Monica painting at our cottage"/>

One of the biggest changes in my life is that I find that I now use ChatGPT for work and personal interests every day. Monica also uses it for researching topics for her book and has become a big fan. I think the integration into daily life has only just begun...

## Work

After our restructuring in February, I took on a new role as Ada's "Product Architect", reporting to [Mike Gozzo](https://twitter.com/gozmike), our CPTO. I now spend a lot of my time documenting our system, charting the path forward for the overall development of our platform, prototyping new projects and working with our teams to implement new functionality. I've been enjoying this role a lot, but I still have a lot to learn about doing it well. It's a good mix of technical and strategic work. In past roles I have been too far removed from the strategic direction of the company. This is a better balance.

More recently I have been working closely with our teams to integrate LLMs into Ada's platform. We have been prototyping different approaches to this and we think we have found one that takes full advantage of the reasoning capabilities of the largest LLMs, while controlling for trust. I'm excited to see how this will work in practice. That's all I can share at this time.

Since 2016, I've built my web applications with two codebases: A React-based front-end and a Flask-based back-end. This works, but as I have gotten more into detailed type hinting I have found the level of effort to keep both codebases in sync no longer makes this separation desirable. For my most recent prototype application, I decided to break out of this way of building and develop a single codebase with just Flask, WTForms, Jinja and htmx for partial rendering and form submission. I was pleasantly surprised. This is a hugely efficient way to build a web application. For what it's worth, DHH has been [trying to convince us all about this set up for years](https://www.youtube.com/watch?v=IFUPG9KCJ4E) (but in Ruby-land, of course). I'm not sure I'll ever go back to a React-based front-end for my own projects. Most of the time, I don't need the complexity of a React-based front-end. I just need a simple way to render partials, submit forms and handle user input. I'm going to write a blog post about this soon about the trade-offs of this approach.

Our voice product, which [Chris Erwin](https://twitter.com/chriserwin) and I built together, is gaining traction. We have had over 130,000 calls through it so far. One customer is using the full breadth of capability of our platform to do some really impressive personalization and back-of-house automation. I'm excited to see how this will grow over the next year.

## Reading
I finished [Brick by Brick](https://www.amazon.ca/Brick-Rewrote-Innovation-Conquered-Industry/dp/0307951618) by David C Robertson. I thought it was a terrific book for anyone interested in running innovative teams. It outlines the importance of constraints in a successful product development process and how Lego had to re-find these to pull out of a near bankruptcy. I also enjoyed the stories of the Lego designers and how they work because Lego has been a big inspiration for my own work.

I've started to read [The Fabric of Reality](https://www.amazon.ca/Fabric-Reality-Parallel-Universes-Implications/dp/014027541X/ref=sr_1_1?gclid=CjwKCAjwlJimBhAsEiwA1hrp5voIEocKfzhOdlyidcDmct_bTQC8XJo6w-PGG0badVe8EeJvwyE3RRoCJVYQAvD_BwE&hvadid=647419034071&hvdev=c&hvlocphy=9000935&hvnetw=g&hvqmt=e&hvrand=7241683292199767522&hvtargid=kwd-314768216536&hydadcr=27622_14550630&keywords=david+deutsch+fabric+of+reality&qid=1690731812&sr=8-1) by David Deutsch. I'm only a few pages in so far so I have no comment other than it's going to be a slow read for an already slow reader.

## Hobbies

I've been getting slowly into the world of music creation. So far, I have a few pedals and a synth (loaned to me by Binod). I haven't made a song yet, but just playing around with the sounds is a lot of fun. Companies like Teenage Engineering, Elektron and Chase Bliss have very inspiring graphic identities and product experiences.

## Running

I had been on a good streak of running 5-6 times a week for months until this week when a bout of Sciatica and some tough work days have kept me from running. I'm hoping to get back out there next week. I'm still well ahead of my goal to run 1000km this year so I'm trying not to be too hard on myself about having a down week.

## Site

It's now been a little over a year since I rewrote this site. I haven't finished the total scope of what I want to do with it, but now that the dust has settled it's clear that two things are important to get better:

1. It's too hard to post so I post less than I used to on Twitter / Medium. I'm thinking I can solve this by introducing an API
2. The performance (average latency) is too slow, despite caching the blog pages with Redis. I think it has to do with the hosting tier I'm on on Fly and using Supabase for the database (when the cache is missed). I'm going to take more control over this and see if I can get most page load times down to under 100ms in the US and Canada.
