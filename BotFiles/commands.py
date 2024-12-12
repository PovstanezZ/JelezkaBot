import telebot
from telebot import types

from cfg import *

bot = API

# Словарь для временного хранения сборок
active_builds = {}


# Команда start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую, друг 👋\n"
                                      "Я бот Железяка, приятно познакомиться! 😊\n"
                                      "Я помогу тебе собрать компьютер исходя из той суммы которая у тебя есть.\n"
                                      "Для того чтобы я смог это сделать, давай для начала познакомимся 😅\n"
                                      "Для того чтобы я узнал тебя пропиши команду /register или выбери её из списка команд. 👇\n\n"
                                      "Для более подробной информации по командам пропиши /help, или так же выбери её из списка 👇")


# Команда help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "Разберём команды:\n"
                                      "/register - Познакомиться с ботом (регистрация)\n"
                                      "/add_build - Начать сборку\n"
                                      "/saved_builds - Сохранённые сборки")
