---
title: "Weeknotes: Week of February 20, 2022"
tags: weeknotes
---

Did you know AWS CloudFormation has typed parameters?

<!-- more -->

## AWS CloudFormation Parameter Types

Go beyond "string" for your CloudFormation parameters! If you specify certain
types, e.g. `AWS::EC2::KeyPair::KeyName` or `AWS::EC2::SecurityGroup::Id`,
CloudFormation will actually validate that the supplied value exists in the
account before trying to create the stack. And when deploying the stack via the
web console, it will even show a select pre-populated with the valid resources!
(Yes experienced users won't need this, but it's great for handing off to a less
experienced AWS administrator or customer). You can see the valid AWS parameter
types here:
[https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types)

