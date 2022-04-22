---
title: AWS Needs More (Permissions) Containers
tags: aws cloud azure
---

Did you know that AWS and Azure both have something called "Resource Groups",
and they mean completely different things?

And that only one of them is useful?

<!-- more -->

Azure's resource groups are logical containers where you can deploy and manage
Azure resources. Resource groups live within a subscription in the [Azure
resource
hierarchy](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/organize-resources)
and offer an extra layer to apply permissions boundaries. Each Azure resource
(e.g. a VM or storage account) must be deployed to a single resource group, and
each each resource group exists in a subscription (the cost/financial boundary).
Permissions are generally assigned in Azure at the resource group level.

TL;DR: In Azure, multiple teams can share a single subscription (IE, share a
single monthly bill) *and* have hard permissions boundaries between their
resources that are easily managed via resource groups.

AWS on the other hand also has [resource
groups](https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html)!
AWS calls their resource groups "the service that lets you manage and automate
tasks on large numbers of resources at one time". Charitably, that statement is
only partially true. AWS resource groups really only make sense in the context
of fleet management via Systems Manager. Systems Manager is truly terrific, but
I'd argue that it's a service with one foot in the past, as much of AWS's
development has clearly been towards higher-level managed services, including
"serverless" developer tools. If you're using Lambda and DynamoDB, do you have
any use at all for AWS resource groups? No!

Most crucially, AWS resource groups offer no permissions boundary. The [AWS docs
explicitly
say](https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html#how-resourcegroups-works)
"Resource Groups feature permissions are at the account level. As long as users
who are sharing your account have the correct IAM permissions, they can work
with resource groups that you create."

But wait, doesn't AWS have something called "permissions boundaries"? It does!
But [AWS IAM permissions
boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
are sets of service-level permissions controls applied to the IAM principal
(user, group, or role). They are *not* at all the same thing as a permissions
boundary at the resource level! And trying to use them as such by explicitly
adding resource ARNs to an IAM policy is a hellish experience I would wish on no
one.

So in this case at least, Azure clearly has the right of it and AWS has a giant
missing feature. (Note GCP's
[projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
fit somewhere in between an AWS account and an Azure resource group, but are
lightweight and closer to the latter.)

So what AWS needs is an extra layer of permissions boundaries at the *resource*
level. A
[container](https://www.lastweekinaws.com/blog/the-17-ways-to-run-containers-on-aws/),
if you will, for resources that principals can be assigned access to. As a cloud
architect in higher ed, I see use cases for this all the time, especially in a
classroom setting. Granting students exclusive access to create and modify only
their own resources in a shared AWS account is essentially impossible in AWS,
but easily done in Azure. 

That is, I think AWS should deprecate what it currently calls resource groups,
or just announce a new, improved version, and re-implement them to work more
like Azure's.

When AWS first started, making accounts the billing *and* permissions boundaries
likely made perfect sense, but I believe it was a fundamental architectural
flaw. But Azure and GCP had the benefit of going second, seeing where AWS had
mis-stepped, and refining their permissions models. 

Architecture being, by definition, the things that are hard to change, I do not
expect to see improvement along these lines by AWS anytime soon. But I'd be
happy to buy some team over there two pizzas to think about this.