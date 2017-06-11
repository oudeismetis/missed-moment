
from time import gmtime, strftime

from decouple import config
from slackclient import SlackClient

SLACK_API_TOKEN = config('SLACK_API_KEY', default=None)


def slack(msg):
    """
    Slack is an unoffical feature - This is a work in progress.
    """
    try:
        slack = '{} {}'.format(msg, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        sc = SlackClient(SLACK_API_TOKEN)
        sc.api_call('chat.postMessage', channel='#missed-moment', text=slack)
    except Exception as e:
        print('Unhandled exception while uploading files - {}'.format(e))
