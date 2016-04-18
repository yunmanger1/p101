import os
import json


def on_message(message):
    cmd = message.content['text']
    stream = os.popen(cmd)
    message.reply_channel.send({
        "text": json.dumps({
            "type": "response",
            "payload": stream.read()
        })
    })
