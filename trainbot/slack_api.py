import os
from slack import RTMClient, WebClient
import re

from trainbot import train_api
from . import STATION_CODES
from . import sched

SLACK_TOKEN = os.environ['SLACK_API_TOKEN']
_BOT_ID = None


@RTMClient.run_on(event="message")
def call_bot(**payload):
    data = payload['data']
    bot_id = 'UR8R3SBT6'
    if 'text' in data and f"<@{bot_id}>" in data['text']:
        channel_id = data['channel']

        parse_message(channel_id, data['blocks'][0]['elements'][0]['elements'][1]['text'])


def send_message(channel, short_code, origin_code):
    web_client = WebClient(token=SLACK_TOKEN)
    board = train_api.board_for_shortcode(short_code, origin_code)
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

def send_message_text(channel, text):
    web_client = WebClient(token=SLACK_TOKEN)
    web_client.chat_postMessage(
        channel=channel,
        text=text
    )

def parse_message(channel_id, message):
    mtch = re.match('^\s+schedule to (.+?(?= from | at )).*?((?<= from ).+(?= at ))? at (\d\d:\d\d).*?((?<= on )[A-Z-]+)?$', message)

    if mtch is not None:
        # print(mtch.groups())
        origin_code = mtch.group(2) if mtch.group(2) else 'LDS'
        days = 'MON-FRI' if not mtch.group(4) else mtch.group(4)

        try:
            if origin_code not in STATION_CODES.values():
                origin_code = STATION_CODES[origin_code]
            if mtch.group(1) not in STATION_CODES.values():
                dest_code = STATION_CODES[mtch.group(1)]
            else:
                dest_code = mtch.group(1)
            sched.set_user_reminder(channel_id, mtch.group(3), lambda :send_message(channel_id, dest_code, origin_code), days=days)
            send_message_text(channel_id, 'reminder set at {}'.format(mtch.group(3)))
            return
        except KeyError as e:
            send_message_text(channel_id, "Hmmm... Maybe you haven't spelt your station full name correctly")
            return

    mtch = re.match('^\s+trains to (.+?(?= from |$)).*?((?<= from ).+)?$', message)


    if mtch is not None:
        # print(mtch.groups())
        origin_code = mtch.group(2) if mtch.group(2) else 'LDS'

        try:
            if origin_code not in STATION_CODES.values():
                origin_code = STATION_CODES[origin_code]
            if mtch.group(1) not in STATION_CODES.values():
                dest_code = STATION_CODES[mtch.group(1)]
            else:
                dest_code = mtch.group(1)
            send_message(channel_id, dest_code, origin_code)
            return
        except KeyError as e:
            send_message_text(channel_id, "Hmmm... Maybe you haven't spelt your station full name correctly")
            return
    if re.match('.*help.*', message):
        send_message_text(channel_id, """Usage:
            trains to <dest>[ from <origin>]
            schedule to <dest>[ from <origin>] at HH:MM[ on <days>]
            days = e.g. MON-FRI
        """)
        return
    send_message_text(channel_id, "I don't know what you mean")
    #INVALID MESSAGE
