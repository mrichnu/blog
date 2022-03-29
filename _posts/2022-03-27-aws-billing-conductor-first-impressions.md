---
title: AWS Billing Conductor First Impressions
tags: weeknotes
---

AWS gives us a first-class tool to modify CURs. 

<!-- more -->

## AWS Billing Conductor

[AWS Billing
Conductor](https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html)
(ABC) is a new service that I believe is primarily intended as a way for
resellers to create "Pro-forma" CURs (Cost and Usage Reports) for their
customers that include custom AWS pricing (both markups and discounts) along
with custom line items. 

My organization is looking at it to bring (more) accurate pricing into a cost
reporting tool we're evaluating, especially for AWS accounts under the [NIH
STRIDES](https://datascience.nih.gov/strides) program, which has significant
discounts that vary by service.

The way you set it up is basically:

1. (Optional) In the organization management account, grant a principal (user or
   role) access to the ABC service via IAM policy
2. Create "pricing rules" that reflect either global or per-service
   discounts/markups
3. Create "pricing plans" that combine one or more pricing rules
4. Create a "billing group", associate accounts with the billing group, and
   assign it a pricing plan. Also you must designate a "primary account", which
   cannot be the management account. Note also accounts can only be associated
   with one billing group.
5. In the primary account, create a new CUR.

I had high hopes for this service but it feels half-baked at the moment. Namely:
- New accounts must be manually associated with a billing group. I'd like to
  designate a "default" billing group per organization that all new accounts get
  associated with automatically.
- The discounts/markups can only be applied globally or per-service. There is no
  way to go down to the per-usage-type level, which makes this pretty useless
  for our specific use case (zeroing out all data transfer out costs since they
  are waived for STRIDES accounts).
- It's basically impossible to predict how much this thing will cost you. The
  free tier seems generous (1MM "pro-forma records" free per month) but your
  organization is likely generating many more records than this and the only way
  to estimate is to generate a new CUR and count the line items.
- In the primary account's Cost and Usage Report console, there is no visual
  indication that the CUR you are generating will reflect the pro-forma pricing
  that was set up for your billing group.

Like many AWS service launches, there's the beginnings of a really useful
service here but it will take a few release cycles to sand down the rough edges. 