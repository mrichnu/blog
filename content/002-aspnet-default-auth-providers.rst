.NET Land: The Trouble With ASP.NET Default Authentication Providers
####################################################################

:date: 2011-08-11 17:00
:tags: dotnet, rants
:author: Matthew Rich
:summary: A Python guy learns to swim in the waters of ASP.NET. In this update: authentication!
:slug: dotnet-land-the-trouble-with-aspnet-default-authentication-providers

.. sidebar:: About this series

   Currently at my job I'm helping another developer implement a "line of
   business" application in Silverlight 4.0. Although I'm usually a Python
   developer I have done some .NET development in the past and so I have a
   passing familiarity with Visual Studio and C#. To say that I have had some
   challenges in learning this new environment would be the understatement of the
   year however. This is one in a series of blog posts chronicling my journey
   through .NET-land.

Today's small victory came when I was able to get Active Directory
authentication working in our staging environment. We try to do all
authentication here through our Active Directory setup in order to save our
users and ourselves on the IT staff the hassle of having to manage multiple
user accounts, plus it's pretty well supported by most 3rd party applications
out there. The documentation is not great though, which I'm finding is an
unfortunate fact of life in the world of Microsoft technologies.

So wiring up AD authentication in the project was not too difficult. I more or
less followed the steps in Chapter 8 of the very good book "Pro Business
Applications with Silverlight 4" by Chris Anderson. Really all it comes down
to is adding an Authentication service containing a class that
inherits from the generic ``AuthenticationBase<T>`` and then in the web.config
for your web project configuring that service to use the
ActiveDirectoryMembershipProvider rather than the SqlMembershipProvider. Easy
peasy and it worked straight away in debug mode within Visual Studio. I
naively considered it to be "working" and told my co-worker so. (Brief aside
here: I'm not great at unit testing although I really am working hard to get
better at it, but Visual Studio's setup and workflow really do not lend
themselves well to unit testing at all, so I'm afraid it's reinforcing my bad
habits.)

That evening he emailed me to tell me that authentication was not working in
our staging environment. I tried it myself and it was true: I fed it my
credentials and was greeted with a 
``System.ServiceModel.DomainServices.Client.DomainOperationException`` containing
a ``query 'Login' failed`` message.

No stack trace.

And here I was confronted with the full enormity of the scope of things I DO NOT KNOW about the .NET
world.

Where to even begin? The `documentation for this exception
<http://msdn.microsoft.com/en-us/library/system.servicemodel.domainservices.client.domainoperationexception(v=vs.91).aspx>`_
is monumentally unhelpful. In addition, the fact that it is such a general
exception (it seems that the WCF stack will wrap pretty much any unhandled
exception with this exception) makes it difficult to find anything useful by
Googling the error message. The lack of a stack trace meant I had no idea at
what point the error was occuring. The fact that it worked inside Visual
Studio but not in IIS was somewhat useful information but raised even more
questions. Is it permissions? Is it because SSL is not currently enabled on
the staging environment? Is it some misconfiguration deep in the bowels of the
IIS management UI? Did we not deploy the web application properly? etc etc
etc.

My first step in solving the problem was discovering that if I entered bad
credentials in the login UI, I actually received the "invalid
username/password" message that I expected. So that told me that the AD
authentication piece was actually working properly and the error was occuring
*after* authentication, which I would expect meant some sort of database
interaction was going badly. I started then thinking about the other
components that I had seen mentioned in the book chapter I read but had not
bothered to investigate more fully, the role manager and the profile provider.
I had enabled these in the web.config file but not provided any configuration
information, and they worked in local debug mode. However, it seemed to me
that these components would be hitting the database and yet I had not provided
any connection string or anything like that in web.config... so how were they
working in local debug mode? For reference, here is what the relevant parts of
my web.config looked like at this time:

.. sourcecode:: xml

    <system.web>
      <!-- snip -->
      <authentication mode="Forms">
        <forms name=".FOO_BAR_ASPXAUTH" />
      </authentication>

      <profile>
        <properties>
          <add name="FriendlyName"/>
        </properties>
      </profile>

      <membership defaultProvider="MyADMembershipProvider">
        <providers>
          <add name="MyADMembershipProvider"
		  type="System.Web.Security.ActiveDirectoryMembershipProvider, System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
          connectionStringName="ADConnectionString"
          attributeMapUsername="sAMAccountName"
          connectionUsername="xxxxxxxx"
          connectionPassword="xxxxxxxx"
          connectionProtection="Secure"
           />
        </providers>
      </membership>
    </system.web>

Long story short, after a couple of missteps with web.config I was able to get
a bare minimum of required configuration to get these components to work: each
needed a name, a database connection string, and a type/assembly reference.
Also I had to run the "aspnet_regsql.exe" wizard that ships with ASP.NET to
create the required tables and stored procedures that these providers rely on.
After putting the correct values in place and publishing the application, it
worked! The relevant sections of my web.config:

.. sourcecode:: xml

   <system.web>
     <!-- snip -->
     <authentication mode="Forms">
       <forms name=".FOO_BAR_ASPXAUTH" />
     </authentication>
     <profile defaultProvider="MyProfileProvider">
       <providers>
         <clear/>
         <add
           name="MyProfileProvider"
           connectionStringName="MyConnStr"
           type="System.Web.Profile.SqlProfileProvider, System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a" />
       </providers>
       <properties>
         <add name="FriendlyName"/>
       </properties>
     </profile>
 
     <roleManager enabled="true" defaultProvider="MyRoleProvider">
       <providers>
         <clear />
         <add 
            name="MyRoleProvider"
            connectionStringName="MyConnStr"
            type="System.Web.Security.SqlRoleProvider, System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a" />
       </providers>
     </roleManager>
      
     <membership defaultProvider="MyADMembershipProvider">
       <providers>
         <add name="MyADMembershipProvider"
 		type="System.Web.Security.ActiveDirectoryMembershipProvider, System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
         connectionStringName="ADConnectionString"
         attributeMapUsername="sAMAccountName"
         connectionUsername="xxxxxxxx"
         connectionPassword="xxxxxxxx"
         connectionProtection="Secure"
            />
       </providers>
     </membership>
   </system.web>

*LESSONS LEARNED:*

* The .NET documentation is bad. This is a function of several factors I
  think: one is that there is just so damned much of it that it's hard to find
  what you need. Also there are some in-depth blog posts and such on MSDN that
  would be useful but when you're new-ish to the technology it's hard to
  figure out which techniques apply to what you want to do, and there
  are so many similar technologies and libraries within the .NET stack that it
  can be difficult to find the one that best fits to your needs.

* ``web.config`` SUCKS. This is my biggest problem so far: that so many
  components and technologies within the ASP.NET and WCF worlds add their own
  bits of configuration to web.config and there is no central reference that I
  can find. What attributes, if any, can the ``<httpModules />`` element contain?
  Who knows? What are all the possible child elements of the ``<system.web/>``
  element? Who can say?? What's the difference between ``<webScriptEndpoint/>`` and
  ``<webHttpEndpoint/>``? Good luck finding out!! And not only is MSDN useless for
  this, but the million horrible blogs about .NET all have conflicting advice
  and/or encourage you to just paste seemingly random chunks of XML into your
  web.config. God I miss the world of simple, well documented, ini-style (or
  pure python) config files.

* Closed source libraries are a drag. When trying to debug the problem one of the
  first things I did was find the definition of the ``AuthenticationBase`` class
  I'm using to see what its ``Login()`` method does. Turns out, you can't! Because
  all you get shipped is a partial class file with the comments and method
  signatures, but the implementation itself lives in some compiled assembly
  somewhere on the system. This is one of those areas where I think not only
  does the open source world have it all over closed source -- namely, you can
  figure out if the library itself is the problem or the way you're using it
  is the problem -- but I don't even understand why Microsoft *wouldn't* ship
  the source code to a library like this. What's the harm in letting us see a
  reference implementation of authenticating against Active Directory? Is that
  some big trade secret?? I'm by no means an open source advocate, I do not
  give a single shit about the GPL or "libre" software or whatever, I'm just a
  developer trying to get things done. And when I can read the source code of
  the libraries I'm using, I get things done faster and better. And I can
  learn from them, to boot.

