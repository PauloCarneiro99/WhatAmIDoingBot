from telegram.ext import Updater, CommandHandler
import requests
import re
from sys import argv
import os

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_dogo_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def _help(bot, update):
    commands = [
        "Type /dogo or /dog to get a random dog",
        "Type /cat to get a random cat",
        "To insert/suggest new funcionalities check my github repo :  https://github.com/PauloCarneiro99/WhatAmIDoingBot"
    ]
    s = "\n".join(commands)
    chatID = update.message.chat_id
    bot.send_message(chat_id=chatID, text=s)

def start(bot,update):
    s = "Welcome to this random Bot.\n\n Use /help to see random commands already implemented.\n\n Hope you enjoy"
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=s)

def dogo(bot, update):
    url = get_dogo_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def cat(bot,update):
    cat = requests.get('https://api.thecatapi.com/v1/images/search').json()
    url = cat[0]['url']
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
	updater = Updater(os.environ['BOT_KEY'])
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('help',_help))
	dp.add_handler(CommandHandler('start',start))
	dp.add_handler(CommandHandler('dogo',dogo))
	dp.add_handler(CommandHandler('dog',dogo))
	dp.add_handler(CommandHandler('cat',cat))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()