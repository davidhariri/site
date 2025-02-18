---
date_published: 2024-04-07
description: My list of qualities that resilient, highly availabile services should
  have.
tags:
- Web
- Ada
- Startups
- Code
title: Service Health
---

We had [a full outage](https://status.ada.support/incidents/3n5rs1zqzmkh) last week that was deeply rattling for our team. Before this, we hadn't had any major disruption to our services since the prior year. I think it caught most of us by surprise which is never what you want. It ate majorly into our SLA budget for the year and it was a reminder of two very important perennial truths for our business:

1. We are a critical service for our customers. Like a utility, they expect us to be up and running all the time. Owning pipes is a blessing and a curse.
2. There is always a bottle-neck lurking in the shadows that we haven't yet discovered. We need to find it before it finds us.

In response to last week, we've been combing through our services and double checking our monitors, alerts, bottle-necks, and failure modes. I'll use this space to collect my list of things a high quality, high availability service should have:

<blockquote class="callout note">
This list is only really useful for those deploying Python WSGI services on <a href="https://kubernetes.io/">Kubernetes</a>.
</blockquote>

1. Automated Integration Tests: We make use of [`pytest`](https://docs.pytest.org/en/8.0.x/), [dependency injection](https://www.youtube.com/watch?v=2ejbLVkCndI) and [`mocking`](https://pypi.org/project/requests-mock/) to test the _functionality_ of our code. We strive to not write ["change detection tests"](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html).
2. Synthetic End-to-end Testing: We use [DataDog Synthetics](https://www.datadoghq.com/product/synthetics/) for this. It's a great way to test the _availability_ of our services from multiple locations around the world.
3. Fast CI/CD with [GitHub Actions](https://github.com/features/actions), [Docker](https://www.docker.com/), [Kubernetes](https://kubernetes.io/) and [ArgoCD](https://argoproj.github.io/argo-cd/)
4. Basic Observability (we use DataDog for most of this)
    - Logs
    - Request Tracing
    - Exception Tracking (we use Sentry for this)
    - Memory, CPU, Disk, Network metrics
5. SLO(s): We're in the process of defining these for our services. We're using [DataDog](https://www.datadoghq.com/) for this.
6. Health Monitors, Alerts, Escalation Policies and Runbooks: We use [PagerDuty](https://www.pagerduty.com/) for this.
7. Load Testing: In the past I've used [Locust](https://locust.io/) for this, but it's only useful for local testing. I'm looking for a cloud-based solution that can simulate real-world traffic patterns. I've heard good things about [k6](https://k6.io/) and [Artillery](https://artillery.io/).
8. Rate Limiting: We use [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) and Redis for this.
9. Load Balancing: We use [NGINX](https://www.nginx.com/) and [Gunicorn](https://gunicorn.org/) for this.
10. Automatic Scaling Policies: We use [HPA](https://kubernetes.io/docs/tasks/run-application/scale-app/#horizontal-pod-autoscaler) for this.