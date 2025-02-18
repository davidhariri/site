---
date_published: '2024-05-18'
description: My answer to the question 'What is the most important yet often overlooked
  aspect of scaling software?'
tags:
- Startups
- Code
title: Scaling Software
---

A third year CS student applying to a role at [Ada](https://ada.cx) asked me:

> I'm curious to know, in your experience, what is the most important yet often overlooked aspect of scaling software, and how can it be done correctly?

What a great question...

In my experience, the most important yet often overlooked aspect of scaling software is maintaining simplicity. As systems grow, there's a tendency to add layers of complexity that can bog down development. The time that it takes to change a system (and the rate at which changes cause regressions) is the key to scaling it. The introduction of complexity most often arises from the people involved. And so, the root answer to your question is really _‘people'_.
 
It’s counter-intuitive, but maintaining a smaller, high-quality team of developers is more efficient at scaling software than having many less skilled individuals. Every person introduces mistakes and complexity- some much more than others. Less experienced or less caring developers create more bugs and more complicated code. The best developers guard simplicity with every change. The best teams have these great developers supervise the learning of less experienced, but eager to learn ones.
 
_"How can it be done correctly"_ is hard to answer in one email, but I like [this idea](https://www.adamtal.me/2019/05/first-make-the-change-easy-then-make-the-easy-change) from Kent Beck:

> “First make the change easy, then make the easy change”.

The idea is to always make your next code change easy to make. This requires refactoring your code to maintain simplicity as you work. As you do this, you’ll find sometimes that you might over-abstract things or go down blind alleys. This is when growth happens. Each of these moments make you a better developer.