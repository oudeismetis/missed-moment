import logging

from slackclient import SlackClient

# TODO - not tested since switching from python-decouple
from config import SLACK_API_TOKEN


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
