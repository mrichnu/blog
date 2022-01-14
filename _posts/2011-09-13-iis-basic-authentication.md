---
title: ".NET Land: Basic Authentication in IIS 7"
categories:
- Coding
---

A Python guy learns to swim in the waters of ASP.NET. In this update:
more authentication!

<!-- more -->

**About this series**

Currently at my job I'm helping another developer implement a "line of
business" application in Silverlight 4.0. Although I'm usually a Python
developer I have done some .NET development in the past and so I have a
passing familiarity with Visual Studio and C#. To say that I have had
some challenges in learning this new environment would be the
understatement of the year however. This is one in a series of blog
posts chronicling my journey through .NET-land.

In what may be a totally wrongheaded move, I've decided to write a set
of RESTful WCF services to act as an intermediate layer between the
pure-.NET/SQL Server backend stuff my co-worker is doing and the
customer facing web apps I plan to write in python. There is still a lot
of stuff to work out (namely a real data synchronization strategy; I
hope to one day write a series of blog posts about how I knocked that
one of the park!) but I think the basic idea is sound enough.

Currently the services have been stubbed out and I'm just writing simple
unit tests using the `python requests library`\_ that hit all the
endpoints and verbs and look for the expected stub response. Just want
to make sure the basic plumbing works before I go building the whole
thing out with Entity Framework models. So that was pretty easy to do
once I got the project's `web.config`\_ set up properly and figured out
the web app deployment tool in IIS.

The next step is to secure the service. There are (as always) a few
options here, including integrated Windows authentication (yuck),
ASP.NET forms authentication (/shudder), HTTP Digest auth, and also
apparently something called "ASP.NET Impersonation" which just sounds
like a bad idea. IIS also supports good old HTTP Basic auth, which in
combination with SSL/TLS and the judicious use of firewall rules should
keep our service plenty secure. (I recognize that my security needs are
really basic, as I only expect there to ever only be one or two hosts
actually consuming this service, since it's just a thin layer on top of
a database and meant for consumption by another web app, not to be used
directly by user agents. So no need for API keys or anything like that.)
Anyway SSL certs are pretty easy to import and use in Windows and my
organization has a wildcard cert that will work just fine on this host.

So now the purpose of this post: enabling and configuring HTTP Basic
Auth on IIS for linux gnomes like me. I'm pretty sure I've got the basic
steps covered below.

1.  **In Server Manager -\> Roles, under Web Server (IIS), click "Add
    Role Services" and enable Basic Authentication.**
2.  **Browse to the site/directory/web app you want to secure in IIS
    Manager. Open the "Authentication" feature under IIS. Disable all
    auth types except for "Basic Authentication".** (Actually it might
    be possible to have say Windows Auth and Basic Auth at the same
    time; I do know that Basic and Forms auth are incompatible though so
    if you don't need the others turn them off.)
3.  **With "Basic Authentication" highlighted, click the "Edit..."
    button to set the default domain and realm.** I had a lot of trouble
    with these settings and I think they are more finicky than the
    documentation would lead you to believe. What worked for me was
    using the machine name for the Default Domain setting (since I set
    up a local user account, see below) and leaving the Realm setting
    empty, which meant IIS defaulted to using the machine's FQDN as the
    realm it presents to the user agent in the 401 response.
4.  **Grant some user or group permissions on the directory/virtual
    directory/site/web app/whatever.** I did this the old fashioned way,
    in Windows Explorer (right click on the folder -\> Properties -\>
    Security -\> Edit -\> Add... and then find the group or user you
    want to grant permission to. One interesting wrinkle is that if
    you're only doing GET/POST/DELETE requests then you only need to
    grant the user Read and Execute permissions, but if your API uses
    PUT requests you also need to grant the Write permission. I have no
    idea why this is.
5.  **Test it!**

For reference, here are obfuscated versions of the settings I used::

Default Domain: MACHINENAME Realm: `<empty>`{=html}

And a simple test. Note that the realm is the same as the host name,
this is because I did not specify a realm in the Basic auth settings so
IIS defaults to just using the whole hostname (I think). You could
probably edit the realm in IIS's settings and change your client code to
match it, but I prefer to do the least configuration possible.

.. sourcecode:: python

import requests import simplejson as json import unittest import urllib

class StudentServiceTestCase(unittest.TestCase):

       SCHEME = 'https'
       HOST = 'host.university.edu'
       APP_PREFIX = 'MyService'
       SERVICE_NAME = 'StudentService.svc'
       USERNAME = 'machinename\serviceaccount'
       PASSWORD = 'p@ssw0rd'
       REALM = 'host.university.edu'

       def setUp(self):
           self.auth = requests.api.AuthObject(self.USERNAME, self.PASSWORD,
             realm=self.REALM)
       
       def test_get_students(self):
           email = 'matthew@technivore.org'
           url = '%s://%s/%s/%s/students/%s' % (self.SCHEME, self.HOST,
             self.APP_PREFIX, self.SERVICE_NAME, urllib.quote(email))

           resp = requests.get(url, auth=self.auth)
           
           self.assertTrue(resp.status_code == 200)
           
           students = json.loads(resp.content)

           self.assertTrue(len(students) == 1)

           student = students[0]

           self.assertTrue(student['ParentEmail'] == email)
           self.assertTrue(student['Id'] == 12345)

We do actually have an Active Directory server here I could have used to
create the user account (rather than a local machine user account) and
that would possibly have been even easier to set up, as IIS seems to
just want to use AD accounts wherever possible. I just didn't want to
pollute our AD user account namespace. I do at the very least recommend
you assign the security permissions to a group rather than a user so
that if you decide later to add more accounts, either local or AD, you
can just add those accounts to the group that already has access.

.. \_python requests library: http://python-requests.org/ ..
\_web.config:
/posts/2011/08/11/dotnet-land-the-trouble-with-aspnet-default-authentication-providers.html
