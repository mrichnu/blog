---
title: A Middle Ground with Docker
tags: docker
---
Get the benefits of Docker without upending your existing development workflow.

<!-- more -->

## My Moment Of Docker Clarity
I was, for a long time, a [Docker](http://docs.docker.com/) skeptic. I was in
the audience for the now-famous lightning talk at PyCon 2013 where it was first
introduced, and I was puzzled. I had my development and deployment workflows
worked out and because I had full control over my production environment,
Docker seemed of little use to me. Why learn yet another new deployment tool
when [Fabric](http://docs.fabfile.org/) and a bit of manual fiddling with
servers works perfectly fine?

I continued to be even more mystified by one of the supposed great benefits of
Docker: having my development environment exactly match my production
environment. Again, all my tests were passing in both so I didn't see the need
for an extra layer of tooling.

What ended up partially changing my mind about Docker was, of all things, a
great blog post about [making maps with Python](http://maxberggren.se/2015/08/04/basemap/).
You see, getting all of the necessary libraries needed for that blog post
(IPython, Numpy, Basemap, etc.) installed and updated on a Mac is surprisingly
difficult and I was getting increasingly frustrated trying to install them with
pip, and then while reading the [miniconda documentation](http://docs.continuum.io/anaconda/images)
I saw these magic words:

```
docker run -t -i continuumio/miniconda /bin/bash
```

And then, I was enlightened.

Docker was not just for deploying my apps, I saw, but was a general purpose
software packaging, distribution, and deployment solution that was far easier
to use and more approachable than it seemed at first glance.

## Finding My Docker Path

I am still not ready to dive in 100%. I believe Docker, useful as it is, is
optimized for **horizontal scaling of stateless microservices**. I understand
that there are technology companies out there that benefit greatly from this,
but for what I do (highly tailored, bespoke web applications for a small-ish
group of users at a research university) I don't need scaling. Moreover, my
apps tend to be highly stateful and I love few things more than a beautifully
normalized Postgres schema. Docker and databases don't play well together.

(You of course *can* run your database in a Docker container, and many
quickstarts have you doing just this, but I believe it is a Bad Idea that
diminishes some of the benefits of Dockerizing your app in the first place.)

Furthermore, I believe that what is important about my app is the behavior of
the app, not the deployment method I choose to use at any given time. I may use
Docker now, but I may switch to a pure push-to-deploy PaaS in the future, so I
don't want to have to restructure my repository just to accommodate the
[limitations of Dockerfiles](http://docs.docker.com/reference/builder/#copy).

So, my current approach is to write very simple shell scripts to build docker
images for the stateless parts of my app (namely, the nginx frontend and the
app code running in gunicorn), wire them together and deploy them with
`docker-compose`, and have them use databases that I manage "out of band" with
Ansible.

This approach gives me 

- the benefits of being able to redeploy my app anywhere, insulating me from the shifting infrastructure landscape
- an easy way to distribute my application
- the benefits of packaging my dependencies with my code.

While allowing me to avoid

- having to fight Docker to containerize an inherently stateful service
- disrupting my preferred local development workflow, using `virtualenv`, `pip`, and Django's `runserver` command.
- having Docker infect my repository layout by forcing all app code to live in the context of a Dockerfile.

No doubt my approach will continue to evolve and my build scripts can be
refined, but this method is a useful and effective middle ground.
