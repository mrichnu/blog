#!/bin/bash

# Shamelessly stolen from Marco Arment's Second Crack project:
# https://github.com/marcoarment/secondcrack

if [ "$1" == "" ] ; then
    echo ""
    echo "Usage: monitor-blog.sh SOURCE_PATH"
    echo "  where SOURCE_PATH contains your blog posts."
    echo ""
    exit 1
fi

SOURCE_PATH="$1"
FORCE_CHECK_EVERY_SECONDS=30
UPDATE_LOG="${HOME}/tmp/blog-update.log"

BASH_LOCK_DIR="${HOME}/tmp/update.sh.lock"

if mkdir "$BASH_LOCK_DIR" ; then
    trap "rmdir '$BASH_LOCK_DIR' 2>/dev/null ; exit" INT TERM EXIT

    echo "`date` -- updating blog" >> $UPDATE_LOG
	$SOURCE_PATH/etc/update-blog.sh

	while true ; do
		$HOME/bin/inotifywait -q -q -r -t $FORCE_CHECK_EVERY_SECONDS -e close_write -e create -e delete -e moved_from "$SOURCE_PATH"
		if [ $? -eq 0 ] ; then
			echo "`date` -- updating blog, a source file changed" >> $UPDATE_LOG
		else
			echo "`date` -- updating blog, $FORCE_CHECK_EVERY_SECONDS seconds elapsed" >> $UPDATE_LOG
		fi
		
		$SOURCE_PATH/etc/update-blog.sh
	done

    rmdir "$BASH_LOCK_DIR" 2>/dev/null
    trap - INT TERM EXIT
else
   echo "Already running!"
fi
