---
title: On Testing
date_published: 2025-03-10
tags:
  - Code
  - Startups
  - Learnings
---

When we were just getting started on [Ada](https://ada.cx), we didn't write any tests. I came from an agency background where we concentrated on the first release of the product. As far as I remember, our clients didn't want us to "waste time" writing tests. The codebase that became Ada as it is today was the third full rewrite of the product so we were still in a mode of writing code quickly, testing it out with customers, and then iterating or throwing it away. Given how likely we were to throw the code away, there was no point in writing tests.

But in hindsight, there was a moment where we knew we were on to something and we should have switched modes from "throwaway code" to "production code". By the time we on-boarded our third engineer, we should have had established patterns for how to write tests and how to write code in our codebase. Instead, I had to figure this out on the fly while on-boarding engineers and doing my own product development tasks.

Knowing nothing about testing code and learning as much as I could, we decided to follow TDD[^1]. It was really hard. We were used to working quickly and experimentally, but TDD required us to understand the solution we needed before we could write the tests. It didn't support our workflow so we quickly abandoned it. The problem was that the resources on TDD we followed encouraged writing _unit tests_. Not knowing any better, we kept writing unit tests even after we abandoned TDD.

The result was thousands of little tests that tested the contracts between the parts of our system, but not the behaviour of the system as a user would feel it. This made changing the system hard (changes would often break the tests) and it made the test suite take a super long time to run.

The other mistake we made was writing tests that expected the production database to be available. Each test would read, write, and delete data. If you didn't know this, you could get some really confusing side-effects in your queries as we only reset the database at the end of each full suite run to save on time.

Now, we're a much more mature team and we've learned a lot about testing. Our test suite still has some of those unit tests kicking around, but we've since added lots of integration tests that test the behaviour of the system as a user experiences it. These give us much more confidence in the system and are less likely to have to be changed even as the system underneath is refactored significantly.

## Learnings

1. TDD didn't work for us and still wouldn't work for us. I'm not sure when it's the right methodology.
2. The most valuable tests we have are _integration tests_ that test the behaviour of the system as a user experiences it. These tests rare have to be changed even as the system underneath is refactored. This principle applies to good LLM evals too.
3. You might not need as many tests as you think. I'd trade 1,000 unit tests for 100 integration tests any day.
4. Use mocking and dependency injection to remove dependencies on external services like databases and APIs.
5. Use unit tests **sparingly** to test functions that have thorny logic.
6. Keep your test suite fast to run, especially in CI.

[^1]: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html) is a software development process that emphasizes writing tests before writing code.

