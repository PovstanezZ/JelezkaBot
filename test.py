import telebot
from telebot import types

from cfg import *

bot = API


@bot.message_handler(commands=["test"])
def hui(message):
    keyboard_register = types.InlineKeyboardMarkup()

    # Кнопки
    add_build_button = types.InlineKeyboardButton(text="Создать сборку", callback_data='btn1')
    saved_build_button = types.InlineKeyboardButton(text="Посмотреть сохранённые", callback_data="saved_builds")

    # Inline клавиатура
    keyboard_register.add(add_build_button)
    keyboard_register.add(saved_build_button)
    bot.send_message(message.chat.id, "Предлогаю вам выбрать действия из перечисленных ниже:",
                     reply_markup=keyboard_register)

@bot.message_handler(commands=["start"])
def hui(message):
    bot.send_message(message.chat.id, "Приветствую, друг 👋\n"
                                      "Я бот Железяка🤖,/n"
                                      "приятно познакомиться! 😊\n"
                                      "Для того чтобы я смог это сделать, давай для начала познакомимся 😅\n"
                                      "Для того чтобы я узнал тебя пропиши команду /register")


@bot.callback_query_handler(func=lambda callback: True)
def response(callback):
    if callback.data == "add_build":
        try:
            bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Создать сборку'!")
        except:
            return