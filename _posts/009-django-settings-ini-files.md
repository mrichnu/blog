Title: Factor Your Django Settings Into uwsgi Ini Files
Date: 2014-03-25 16:15
Tags: django, opslife
Slug: django-settings-ini-files
Author: Matthew Rich
Summary: If you have one codebase and multiple sites, keep your settings in ini-files.

Although this is certainly not the usual use case for a Django site, I am
deploying a new site that will be used by several programs at the school where
I work. Each program will have its own specific Django settings file with its
own values (for example, the database connection info) but for the most part
the sites share a base `settings_production.py` file. Here is a sample of this
file:

	from mysite.settings import *

	DEBUG = False
	TEMPLATE_DEBUG = DEBUG

	ALLOWED_HOSTS.append('.university.edu')

	INSTALLED_APPS.append(
			'websso'
	)

	MIDDLEWARE_CLASSES.append(
			'django.contrib.auth.middleware.RemoteUserMiddleware'
	)

	AUTHENTICATION_BACKENDS.append(
			'websso.backends.RegistryRemoteUserBackend'
	)

	DATABASES = {
			'default': {
					'ENGINE': 'django.db.backends.postgresql_psycopg2',
					'NAME': os.environ.get('MYSITE_DB_NAME'),
					'USER': os.environ.get('MYSITE_DB_USER'),
					'PASSWORD': os.environ.get('MYSITE_DB_PASSWORD'),
					'HOST': os.environ.get('MYSITE_DB_HOST'),
					'PORT': '5432',
			}
	}

As you can see, we get the database connection values from the environment.

I am using Apache (with mod_proxy_uwsgi) and uwsgi in emperor mode to run the
site, and each site has a uwsgi ini file that actually sets all the relevant
per-site settings via the
[env](http://uwsgi-docs.readthedocs.org/en/latest/Options.html#env)
configuration option. This was quite easy to set up, and this is an example
uwsgi `ini` file:

	[uwsgi]
	chdir=/srv/myvirtualenv/mysite
	module=mysite.wsgi:application
	max-requests=5000
	socket=127.0.0.1:3032
	logto=/tmp/uwsgi-example.log
	env = DJANGO_SETTINGS_MODULE=mysite.settings_production
	env = MYSITE_DB_NAME=mysite_dbname
	env = MYSITE_DB_USER=mysite_username
	env = MYSITE_DB_PASSWORD=abc123
	env = MYSITE_DB_HOST=mysite-dbname.hostname.us-east-1.rds.amazonaws.com

So far so good -- we can run uwsgi in emperor mode, point it at our `conf/`
directory full of ini files, and everything works fine.

Now, what if we want to use `manage.py shell`? We have fully factored these
settings out of the `settings_production.py` file and we can't rely on envdir
because the uwsgi emperor won't know how to use it.

The answer (for me anyway) is [fabric](http://fabric.readthedocs.org/) and
python's [ConfigParser](http://docs.python.org/2/library/configparser.html)
module. With a little work we can actually write helper functions in our
fabfile that use `ConfigParser` objects to read the uwsgi ini files and set the
appropriate environment variables before calling `manage.py`.

The important wrinkle here is that the `env` setting is used several times in
the ini file, while the default behavior of `ConfigParser` is to use a simple
dict to store each option found in the ini file, and if an option is specified
multiple times, only the last one is saved. We can override this however by
specifying our own dict type to hold the option values:

	from fabric.api import task, shell_env, local
	from collections import OrderedDict
	import ConfigParser

	@task
	def shell(site_name):
		filename = 'conf/uwsgi-%s.ini' % (site_name,)
		env_settings = parse_uwsgi_ini_env_settings(filename)
		with shell_env(**env_settings):
				local('python manage.py shell --settings=mysite.settings_production')

	class MultiOrderedDict(OrderedDict):
		def __setitem__(self, key, value):
			if isinstance(value, list) and key in self:
				self[key].extend(value)
			else:
				super(OrderedDict, self).__setitem__(key, value)

	def parse_uwsgi_ini_env_settings(filename):
		env_settings = {}
		config = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)
		config.read(filename)
		for env_setting in config.get('uwsgi', 'env'):
			key, val = env_setting.split('=', 1)
			env_settings[key] = val

		return env_settings


Now rather than run `python manage.py shell`, run `fab shell:foo` your
environment variables will be read from `conf/uwsgi-foo.ini` and set properly.
