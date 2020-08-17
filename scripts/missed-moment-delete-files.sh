#!/bin/bash

MISSED_MOMENT_MEDIA_PATH=/missed_moment_media

# create crontab to look for missed moment media files that are
# older than 7 days(mtime +6 is 7 days ago) and deletes it.
find $MISSED_MOMENT_MEDIA_PATH -type f -name 'missed-moment*' -mtime +6 -delete

DATE_TIME=`date`
echo Done $DATE_TIME