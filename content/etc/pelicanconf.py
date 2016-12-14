#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Matthew Rich'
SITENAME = u'Technically Voracious'
SITEURL = 'http://technivore.org'
FEED_DOMAIN = SITEURL

PATH = '/home/technivore/Dropbox/textfiles/blog'
OUTPUT_PATH = '/home/technivore/webapps/htdocs'

TIMEZONE = 'US/Central'

DEFAULT_LANG = u'en'
DEFAULT_CATEGORY = 'blog'

THEME = "/home/technivore/pelican-bootstrap3"

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

STATIC_PATHS = [
    'images',
    'extra',
]

PLUGIN_PATHS = ['home/technivore/pelican-plugins']

DISPLAY_TAGS_ON_SIDEBAR = False

SOCIAL = (('twitter', 'http://twitter.com/technivore'),
          ('github', 'http://github.com/technivore'),
          ('bitbucket', 'http://bitbucket.com/technivore'))

DEFAULT_PAGINATION = 8

TAG_FEED_ATOM = 'feeds/%s.atom.xml'

TYPOGRIFY = False

GOOGLE_ANALYTICS = 'UA-22623167-1'
DISQUS_SITENAME = 'technicallyvoracious'

MD_EXTENSIONS = ['fenced_code', 'codehilite(css_class=highlight, linenums=False)', 'extra']
