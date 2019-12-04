import os
from slack import RTMClient, WebClient
import re

from . import STATION_CODES

SLACK_TOKEN = os.environ['SLACK_API_TOKEN']
_BOT_ID = None


@RTMClient.run_on(event="message")
def call_bot(**payload):
    data = payload['data']
    # print(payload)
    # print(data)
    web_client = payload['web_client']
    bot_id = 'UR8R3SBT6'
    if 'text' in data and f"<@{bot_id}>" in data['text']:
        channel_id = data['channel']
        user = data['user']

        response = dummy_method(data['blocks'][0]['elements'][0]['elements'][1]['text'])

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"<!here> {response} for <@{user}>!\n"
        )


def parse_message(message):
    mtch = re.match('^\s+schedule to (.+) at (.+)$', message)

    if mtch is not None:
        if mtch.group(1) in STATION_CODES.values():
            print("Scheduled")
            #CALL METHOD
        else:
            try:
                #CALL METHOD
                print(STATION_CODES[mtch.group(1)])
                #CALL METHOD
            except KeyError as e:
                print("ERROR")

    mtch =re.match('^\s+trains to (.+)$', message)

    if mtch is not None:
        if mtch.group(1) in STATION_CODES.values():
            print("not scheduled")
            #CALL METHOD
        else:
            try:
                print(STATION_CODES[mtch.group(1)])
            except KeyError as e:
                print("ERROR")

    #INVALID MESSAGE
