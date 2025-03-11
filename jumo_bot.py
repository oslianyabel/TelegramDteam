import os

import telebot
from dotenv import load_dotenv
from flask import Flask, request
from openai import OpenAI
from telebot.types import ReplyKeyboardRemove
from waitress import serve

import assistant

load_dotenv()
client = OpenAI(
    api_key=os.getenv("AVANGENIO_API_KEY"), baseURL="https://apigateway.avangenio.net"
)
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
    if message.chat.type in ["group", "supergroup"]:
        return

    print("/start")
    data = {"id": message.chat.id, "message": "Hola, en qué me puedes ayudar?"}
    ans = assistant.send_message(data)

    send_message(message, ans)


@bot.message_handler(content_types=["text"])
def reply_text(message):
    if message.chat.type in ["group", "supergroup"]:
        return

    print(f"-User: {message.text}")
    data = {"id": message.chat.id, "message": message.text}
    ans = assistant.send_message(data)
    send_message(message, ans)


if __name__ == "__main__":
    print("Iniciando Bot")
    URL_BOT = os.getenv("URL_BOT")
    PORT_BOT = os.getenv("PORT_BOT")

    """ NGROK_TOKEN = os.getenv('NGROK_TOKEN')
    conf.get_default().config_path = "./config_ngrok.yml"
    conf.get_default().region = "eu"
    ngrok.set_auth_token(NGROK_TOKEN)
    ngrok_tunel = ngrok.connect(1338, bind_tls = True)
    ngrok_url = ngrok_tunel.public_url
    print(ngrok_url)
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url = ngrok_url)"""

    bot.set_webhook(url=URL_BOT)
    serve(web_server, host="0.0.0.0", port=PORT_BOT)
    # web_server.run(host="0.0.0.0", port=5000)
