---
title: "Weeknotes: Week of January 16, 2022"
tags: weeknotes
---

AWS CloudFormation example templates, CloudShell and Cloud9, and a GitHub
Actions surprise. 

<!-- more -->

## AWS CloudFormation Examples

GitHub user [Thomas Step](https://github.com/thomasstep) has created an
enormously useful
[repository](https://github.com/thomasstep/aws-cloudformation-reference) of
example sample CloudFormation templates for different AWS resources. Most useful
for me recently was the [Fargate
example](https://github.com/thomasstep/aws-cloudformation-reference/tree/main/fargate),
as I just needed to set up a simple Fargate/ECS cluster in order to test some
deployment stuff, but I'm not familiar enough with ECS to quickly set up an
example on my own. Nor do I have access to any existing ones that I can mess
around with. Being able to quickly launch a resource from these templates
without having to learn the ins and outs of the service was a HUGE time saver.
Thanks Thomas!

## AWS CloudShell and Cloud9

I want to like CloudShell as a way to quickly run CLI commands without having to
mess around with CLI authentication and role assumption. I know the coolest
possible version of me would just be in the terminal all the time, but being
realistic I spend at least 80% of my time in the browser and am quite often
using the AWS web console. CloudShell is promising but has one huge glaring
flaw: **it forgets my bash history each time I start a new session**. If there's
a way around this I can't find it.

Cloud9 is a little better, but it's a much heavier service since it requires
spinning up an "environment" which is an EC2 instance, so I can't easily just
hop into a random account I don't often use and run a CLI command. But today I
used it to demo some stuff for my team and it has some big advantages for team
use:

- AWS CLI authentication is handled automagically - you are the same user in the
    Cloud9 terminal as you are in the web console.
- Most tools you would need are already installed and available for everyone.
  Great for newer team members or folks coming from non-Linux backgrounds.

Downsides/annoyances of Cloud9:
- Not a great IDE experience. VS Code is really much better.
- When used in conjunction with AWS SSO, if you have a short session length you
  get timed out of your IDE session annoyingly often, regardless of your
  activity.
- When created via an IAM role environments seem to be tied to the role that
  created them. So if for example I usually stick to a federated role with
  `PowerUserAccess` permissions in an account but sometimes use a role with
  `AdministratorAccess` for specific things, even though both roles are being
  assumed by the same federated principal (me), there's no way to share the
  Cloud9 environment across them. Looks like they can be shared to IAM users,
  but at my work we try to avoid IAM users for anything but service accounts.

## GitHub Actions

Started playing with this this week. One minor thing that surprised me:
Workflows cannot be triggered manually unless they explicitly allow for
triggering via the `workflow_dispatch` event. Documentation here:
[https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)