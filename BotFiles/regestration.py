import telebot
from telebot import types

from DataBase.data_base_code import *
from cfg import *

bot = API


def connect_db():
    conn = sqlite3.connect(dbPath)
    return conn


def create_users_table():
    """Создает таблицу users, если её еще нет."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
    """)
    conn.commit()
    conn.close()


create_users_table()  # Убедимся, что таблица существует


def register_user(telegram_id, username, first_name, last_name):
    """Добавляет пользователя в базу данных, если он еще не зарегистрирован."""
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    # Проверка на существование пользователя
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (telegram_id, username, first_name, last_name)
        )
        conn.commit()
        return True  # Пользователь успешно зарегистрирован
    else:
        return False  # Пользователь уже зарегистрирован
    conn.close()


@bot.message_handler(commands=["register"])
def start_registration(message):
    """Обработчик команды /start или /register."""
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    first_name = message.from_user.first_name or "No first name"
    last_name = message.from_user.last_name or "No last name"

    if register_user(user_id, username, first_name, last_name):
        keyboard_register = types.InlineKeyboardMarkup()

        # Кнопки
        add_build_button = types.InlineKeyboardButton(text="Создать сборку", callback_data='add_build')

        # Inline клавиатура
        keyboard_register.add(add_build_button)
        bot.send_message(message.chat.id, f"Так-то лучше! 😅\nПриятно познакомиться, {first_name}")
        bot.send_message(message.chat.id, "Предлогаю вам выбрать действия из перечисленных ниже:",
                         reply_markup=keyboard_register)

    else:
        keyboard_register = types.InlineKeyboardMarkup()

        # Кнопки
        add_build_button = types.InlineKeyboardButton(text="Создать сборку", callback_data='add_build')
        saved_build_button = types.InlineKeyboardButton(text="Посмотреть сохранённые", callback_data="saved_builds")

        # Inline клавиатура
        keyboard_register.add(add_build_button)
        keyboard_register.add(saved_build_button)
        bot.send_message(message.chat.id, f"Мы уже знакомы, {first_name}. 😊")
        bot.send_message(message.chat.id, "Предлогаю тебе выбрать действия из перечисленных ниже:",
                         reply_markup=keyboard_register)


@bot.callback_query_handler(func=lambda callback: True)
def response(callback):
    if callback.data == "add_build":
        try:
            bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Создать сборку'!")
        except:
            return
    elif callback.data == "saved_builds":
        try:
            bot.send_message(callback.message.chat.id, "Вы нажали кнопку 'Создать сборку'!")
        except:
            return
