import logging

from decouple import config
from slackclient import SlackClient

SLACK_API_TOKEN = config('SLACK_API_TOKEN', default=None)


def slack(file_path, file_name):
    """
    Slack is an unoffical feature.
    """
    if SLACK_API_TOKEN:
        try:
            sc = SlackClient(SLACK_API_TOKEN)
            with open(file_path, 'rb') as f:
                response = sc.api_call('files.upload', file=f, filetype='mp4',
                                       channels='samantha', filename=file_name)
                if not response['ok']:
                    logging.error('Error from Slack {}'.format(response))
        except Exception as e:
            logging.error('Unhandled exception uploading files - {}'.format(e))
