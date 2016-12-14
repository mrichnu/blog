#!/bin/sh

source $HOME/.virtualenvs/technivore-blog/bin/activate && $HOME/local/bin/pelican -q -s $HOME/Dropbox/textfiles/blog/etc/pelicanconf.py
