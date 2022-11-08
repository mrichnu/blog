---
title: "Let a Thousand PaaSes Bloom"
tags: architecture
---

A brief but unassailably accurate history of deploying web apps:

<!-- more -->

- 1994 - 2001: FTP your Perl CGI script to the server
- 2001 - 2006: FTP your PHP script to the server
- 2006 - 2010: Holy cow Rails is rad! Now how do I deploy this thing
- 2010 - 2015: Heroku 💪
- 2015 - present: Docker I guess?

The point here is that Heroku was genuinely amazing. Rails started a revolution in web
development ~2006 with a "highly opinionated" web framework that leveraged an incredibly
expressive, high level language in Ruby. There was a huge problem though, which today is 
often forgotten because of the advanced CI/CD tooling available. Back then, most web servers
were still hand-configured Apache httpd and Ruby as a server-side language was extremely finicky
to set up. The same went for Django (written in Python) and other new server side web frameworks.

The folks at Heroku addressed this problem with a highly opinionated solution of their own: You
uploaded your code and it magically figured out how to run it across a fleet of managed servers.
And thus the Platform-as-a-Service was born.

Heroku's engineers invented a whole [methodology](https://www.12factor.net) for building
PaaS-friendly apps which reverberates today. Amazon (Elastic Beanstalk) and Google (App Engine)
both shamelessly copied Heroku. 

And then Docker happened, and monolithic web apps became very un-cool, Heroku's new owner
Salesforce stopped investing in it, and Heroku kinda died on the vine. Also it was kind of
expensive and not feasible for apps with very large user bases.

But I would argue the *idea* of Heroku, the beautifully engineered, highly opinionated, cool-kid
deployment platform never died.

And the world changed again around 2013 when Angular and React were released and quickly gained 
popularity. Now developers could build powerful, real-time-ish applications and deliver them
*directly to the browser*. But! The Javascript development toolchain was (and probably still is?)
an even bigger nightmare than getting a Ruby app to run under Apache.

This led to the so-called [Jamstack](https://jamstack.org), an architectural approach to building
web applications made up of Javascript, APIs, and simple Markup. Developers now had new, exciting, productive, and highly expressive frameworks to
create cool apps with, but staying on top of the complex and constantly changing build/deploy
toolchain was a huge cognitive tax. Thus the scenario that led to
Heroku was re-created!

Another generation of PaaS providers, directly inspired by Heroku, has filled this gap: 
[Netlify](https://netlify.com/) (which hosts this blog), [Vercel](https://vercel.com/),
[Fly.io](htps://fly.io), and doubtless others I don't know about are capturing developer
hearts.

And why should I, a lowly cloud architect, or you, the reader of this post, care? Because we put
enormous effort into the guardrails that will allow our developers to safely and effectively use
IaaS primitives to deploy their apps, but a coming generation of developers raised on Netlify
et al. are going to bypass that stuff altogether. Governance in some form will still be needed,
but what does that look like?

I'll be sure to let you know here as soon as I figure it out.