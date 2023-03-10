import telebot
import os
from dotenv import load_dotenv

from sed import Sed

load_dotenv()
bot = telebot.TeleBot(os.getenv('API_TOKEN'))

@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message) -> None:
  bot.send_message(message.chat.id, "Hi, I am Jeaciaz's personal bot. To learn more about what I can do, type /help.")

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message) -> None:
    bot.reply_to(message, """\
Hi there, I am Jeaciaz's personal bot for stuff.

Right now I only do message editing, to do so reply to a message with 's/thing/replacement/g', and I will replace the "thing" in message replied to with "replacement" (the "g" stands as a flag for "replace every occurence instead of the first one"). I also support Python RegExp syntax, and you can use the regex flags after the last slash.
""")

@bot.message_handler(func=lambda message: Sed.is_valid(message))
def echo_message(message: telebot.types.Message) -> None:
    bot.reply_to(message, Sed(message).calc())

bot.infinity_polling()
