#!/bin/bash
# This script will be called via a cron, so the working directory will be the home folder of the $USER defined in install.sh
current_dir=`pwd`
missed_moment_dir=$current_dir/missed-moment/missed_moment

# source config file
. $missed_moment_dir/config.py

echo current_dir $current_dir, missed_moment_dir $missed_moment_dir, MEDIA_DIR $MEDIA_DIR, DAYS_TO_KEEP_FILES $DAYS_TO_KEEP_FILES

# create crontab to look for missed moment media files that are
# older than DAYS_TO_KEEP_FILES plus 1 day.  If DAYS_TO_KEEP_FILES is 6 (mtime +6 is 7 days ago) and deletes it.
find $MEDIA_DIR -type f -name 'missed-moment*' -mtime +$DAYS_TO_KEEP_FILES -delete

DATE_TIME=`date`
echo Done $DATE_TIME