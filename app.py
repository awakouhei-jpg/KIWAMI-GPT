
from flask import Flask, request
import openai
import requests

app = Flask(__name__)
import os  #

LINE_TOKEN = os.environ["LINE_TOKEN"]
GPT_KEY = os.environ["GPT_KEY"]


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_msg = data["events"][0]["message"]["text"]

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": user_msg}],
        api_key=GPT_KEY
    )
    reply = res['choices'][0]['message']['content']

    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {
        "replyToken": data["events"][0]["replyToken"],
        "messages": [{"type": "text", "text": reply}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)

    return "OK"
