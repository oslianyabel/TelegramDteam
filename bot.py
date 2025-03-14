import os
import time

import telebot
from dotenv import load_dotenv
from flask import Flask, request
from pyngrok import conf, ngrok
from telebot.types import ReplyKeyboardRemove
from waitress import serve

import utils

load_dotenv()
secret = os.getenv("API_SECRET")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
web_server = Flask(__name__)


def send_message(msg_obj, msg):
    bot.send_chat_action(msg_obj.chat.id, "typing")
    bot.send_message(msg_obj.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@web_server.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200


@bot.message_handler(commands=["start"])
def cmd_start(message):
    print("/start")
    data = {
        "chat_id": str(message.chat.id),
        "message": "Hola, en qué me puedes ayudar?",
        "secret": secret,
    }
    ans = utils.send_message(data, message.chat.id)
    send_message(message, ans)


@bot.message_handler(content_types=["text"])
def reply_text(message):
    print(f"- User: {message.text}")
    data = {
        "chat_id": str(message.chat.id),
        "message": message.text,
        "secret": secret,
    }
    ans = utils.send_message(data, message.chat.id)
    send_message(message, ans)


if __name__ == "__main__":
    print("Iniciando Bot")
    if os.getenv("ENV") == "prod":
        bot.set_webhook(url=os.getenv("URL_BOT"))
    else:
        conf.get_default().config_path = "./config_ngrok.yml"
        conf.get_default().region = "eu"
        ngrok.set_auth_token(os.getenv("NGROK_TOKEN"))
        ngrok_tunel = ngrok.connect(os.getenv("PORT_BOT"), bind_tls=True)
        ngrok_url = ngrok_tunel.public_url
        print(ngrok_url)
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=ngrok_url)

    serve(web_server, host="0.0.0.0", port=os.getenv("PORT_BOT"))
