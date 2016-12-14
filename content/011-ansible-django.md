Title: Easy Django Deployments with Ansible
Date: 2015-10-09 14:15
Tags: django, ansible, devops
Slug: easy-django-deployments-with-ansible
Author: Matthew Rich
Summary: Get your Django project up and running in production in seconds.

There are multiple ways to get a python web application running in production,
including [Docker](https://www.docker.com), push-to-deploy PaaS services like
[Heroku](https://www.heroku.com/), using one of the many configuration
management tools now available (e.g. Puppet, Chef, Salt, and Ansible), or old
fashioned manual configuration of a server. The last is a road that too many
newcomers to Django and python web applications are led down, as when you are
new to a whole language and suite of tools it is difficult and frustrating to
learn a whole other category of tools on top of Django just to get your project
running somewhere that other people can see it!

One thing I like to do when learning a new technology is to build, from
scratch, the simplest possible thing that will work using that tech. That might
be the [simplest possible Django
project](https://github.com/technivore/django-hello-world) or the minimum
configuration needed to use [SAML authentication with
Django](https://bitbucket.org/technivore/django-saml-example/). So I decided to
create the simplest [Ansible](http://docs.ansible.com/ansible/) playbook I
could that would take you from a freshly created VM to a running Django site,
with as little configuration as possible.

This playbook will do the following:

- Install git, nginx, gunicorn, postgres, and a few other libraries
- Configure and run nginx (the web server)
- Configure and run gunicorn (the python application server)
- Create your postgres database and user
- Clone your git repository and make sure it has the latest version of master checked out
- Install any requirements listed in your requirements.txt
- Run `manage.py migrate`
- Run `manage.py collectstatic`
- Restart nginx and/or gunicorn if anything changes

### Step 1: Create a VM

I highly recommend [Digital
Ocean](https://www.digitalocean.com/?refcode=a2f33871dc28) for both personal
hobby projects and production. A hobbyist or student does not need the full
power of AWS right away, and with tools like the one I'm describing here, we
can also do without the expense of a hosted PaaS like Heroku. But whether you
go with Digital Ocean or another provider, all you need is an Ubuntu VM.

Our ansible playbook assumes that SSH public key authentication is already set
up for our server, so to do that just run this command:

```
ssh-copy-id root@xxx.xxx.xxx.xxx
```

(replacing the xxx's with the actual public IP address or hostname of your server).

### Step 2: Install Ansible

You will need to have Ansible installed on your computer, which unfortunately
does not work on Windows (yet). But if you are on a Mac or Linux, just `sudo
pip install ansible` to get the latest version.

### Step 3: Clone the playbook repository

You can view the playbook on the web here:
[https://github.com/technivore/ansible-django](https://github.com/technivore/ansible-django).
Clone it to your machine with this command:

```
git clone git@github.com:technivore/ansible-django.git
```

### Step 4: Edit the `vars.yml` file

The repository contains an `ansible` directory that has a file called
`vars.yml`. Edit this file to set things like your project name, the URL of
your own git repository, the database username and password you want to use,
etc.

### Step 5: Edit the `hosts` file

The `hosts` file contains the address of the server we are installing on.

### Step 6: Run the playbook!

First `cd` into the `ansible` directory, then:

```
ansible-playbook -i hosts provision.yml
```

Sit back and watch the messages scroll by! When it completes, your app will be
up and running!

### Next steps

Of course as you keep developing your app you'll be pushing new versions to
your git repository. To update your site you don't want to run through the
whole provisioning playbook again, so you can run just the `deploy.yml`
playbook to update your code (as well as install any new dependencies and
restart the services if necessary):

```
ansible-playbook -i hosts deploy.yml
```

### Final notes

This playbook is explicitly not a "best practices" guide to follow. Its aim is
simplicity and ease of use, while following common practices for Django project
layout. There are many things it does *not* do:

- Set up SSL
- Configure a firewall
- Set up and use a non-root local user
- Handle databases besides postgres :)

If you are ready to move beyond this playbook because your project has
different requirements, it should at least make a good template to work off of.

