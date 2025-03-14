import os

import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
URL_API = os.getenv("URL_API")
API_SECRET = os.getenv("API_SECRET")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


def send_message(data, id):
    bot.send_chat_action(id, "typing")
    response = requests.post(URL_API, json=data)
    print(f"Status Code: {response.status_code}")
    ans = response.json()

    if response.status_code == 200:
        print(f"- Bot: {ans['message']}")
        return ans["message"]
    
    print(f"Error {response.status_code}: {response.text}")
    return "Ha ocurrido un error"
