"""Defines main executable"""

from . import STATION_CODES
import os
from slack import RTMClient
from . import slack_api
from . import sched

def run():
    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = RTMClient(token=slack_token)
    sched.start()
    rtm_client.start()

