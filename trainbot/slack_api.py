import os
from slack import RTMClient, WebClient
import re

from trainbot import train_api
from . import STATION_CODES

SLACK_TOKEN = os.environ['SLACK_API_TOKEN']
_BOT_ID = None


@RTMClient.run_on(event="message")
def call_bot(**payload):
    data = payload['data']
    bot_id = 'UR8R3SBT6'
    if 'text' in data and f"<@{bot_id}>" in data['text']:
        channel_id = data['channel']

        send_message(channel_id, data['blocks'][0]['elements'][0]['elements'][1]['text'])


def send_message(channel, short_code):
    web_client = WebClient(token=SLACK_TOKEN)
    board = parse_message(short_code)
    if board:
        text = '\n'.join(
            (f'{row[0]} : {row[1]} : {row[2]} : {row[3]}' for row in board)
        )
    else:
        text = "Invalid Command or no trains for selected destination"
    web_client.chat_postMessage(
        channel=channel,
        text=text
    )

def parse_message(message):
    mtch = re.match('^\s+schedule to (.+) at (.+)$', message)

    if mtch is not None:
        if mtch.group(1) in STATION_CODES.values():
            print("no")
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
            return train_api.board_for_shortcode(mtch.group(1))
        else:
            try:
                return train_api.board_for_shortcode(STATION_CODES[mtch.group(1)])
                # print(response)
            except KeyError as e:
                print("ERROR")

    #INVALID MESSAGE
