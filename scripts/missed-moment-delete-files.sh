#!/bin/bash

# source constants file
. ../constants.py

echo MEDIA_DIR $MEDIA_DIR, DAYS_TO_KEEP_FILES $DAYS_TO_KEEP_FILES

# create crontab to look for missed moment media files that are
# older than DAYS_TO_KEEP_FILES plus 1 day.  If DAYS_TO_KEEP_FILES is 6 (mtime +6 is 7 days ago) and deletes it.
find $MEDIA_DIR -type f -name 'missed-moment*' -mtime +$DAYS_TO_KEEP_FILES -delete

DATE_TIME=`date`
echo Done $DATE_TIME