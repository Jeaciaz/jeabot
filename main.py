import telebot
import re
from dotenv import load_dotenv
import os

from sed import sed, sed_regex

load_dotenv()
bot = telebot.TeleBot(os.getenv('API_TOKEN'))

@bot.message_handler(commands=['start'])
def welcome(message):
  bot.send_message(message.chat.id, "Hi, I am Jeaciaz's personal bot. To learn more about what I can do, type /help.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """\
Hi there, I am Jeaciaz's personal bot for stuff.

Right now I only do message editing, to do so reply to a message with 's/thing/replacement/g', and I will replace the "thing" in message replied to with "replacement". I also support Python RegExp syntax, and you can use the regex flags after the last slash.
""")

@bot.message_handler(func=lambda message: re.match(sed_regex, message.text) is not None and message.reply_to_message is not None)
def echo_message(message):
    bot.reply_to(message, sed(message))

bot.infinity_polling()
