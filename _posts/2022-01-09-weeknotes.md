---
title: "Weeknotes: Week of January 9, 2022"
tags: weeknotes
---

AWS IAM Access Analyzer vs. IAM Access Advisor

<!-- more -->

## IAM Access Analyzer

Tried this out for the first time this week and it turns out I totally misunderstood its purpose. Access
Analyzer helps you find instances where a resource in your "zone of trust" (which can be an AWS account or
organization) is accessed by a principal from *outside* the zone of trust (e.g. an IAM user or role in a
different AWS account, an AWS service, or god forbid an anonymous/un-authenticated user).

I had thought an Access Analyzer was needed to create an IAM policy based on a user's actions, but it turns
out that is something you only need CloudTrail for, as the "generate policy" action just searches CloudTrail
events.

## IAM Access Advisor

This is the thing you want to look at what services and actions an IAM principal has used during a time frame.
However, listing management actions is only supported for EC2, IAM, S3, and Lambda. For other services it just
lists that the service itself was accessed.