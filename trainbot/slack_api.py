import os
from slack import RTMClient, WebClient

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
        # MAKE METHOD CALL RETRIEVE DATA AND PUT IT IN TEXT
        # for the method call
        print(data['blocks'][0]['elements'][0]['elements'][1]['text'])
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"<!here> train train!! <@{user}>!\n"
        )