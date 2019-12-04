"""Defines main executable"""

from . import STATION_CODES
import os
from slack import RTMClient
from . import slack_api #NOQA

def run():
    #     print('hello world')
    #     print(STATION_CODES.get("Leeds"))
    #     print('LDS' in STATION_CODES.values())

    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()

