#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Matthew Rich'
SITENAME = 'Technically Voracious'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Central'

DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'blog'

THEME = "theme"

DISPLAY_PAGES_ON_MENU = True
DISPLAY_TAGS_ON_SIDEBAR = False

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

STATIC_PATHS = [
    'images',
    'extra',
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SOCIAL = (('twitter', 'http://twitter.com/technivore'),
          ('github', 'http://github.com/technivore'),
          ('bitbucket', 'http://bitbucket.com/technivore'))

DEFAULT_PAGINATION = 8

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TYPOGRIFY = False

# MD_EXTENSIONS = ['fenced_code', 'codehilite(css_class=highlight, linenums=False)', 'extra']
