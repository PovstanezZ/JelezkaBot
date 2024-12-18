import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import os

from DataBase.data_base_code import db_path
from cfg import *

bot = API

active_builds = {}
# Промежуточное состояние пользователя
user_build_progress = {}
user_budgets = {}  # Хранение бюджета пользователей


# /////////////// #
# -Команда start- #
# /////////////// #

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую, друг 👋\n"
                                      "Я бот Железяка, приятно познакомиться! 😊\n"
                                      "Я помогу тебе собрать компьютер исходя из той суммы которая у тебя есть.\n"
                                      "Для того чтобы я смог это сделать, давай для начала познакомимся 😅\n"
                                      "Для того чтобы я узнал тебя пропиши команду /register или выбери её из списка команд. 👇\n\n"
                                      "Для более подробной информации по командам пропиши /help, или так же выбери её из списка 👇")

# ////////////// #
# -Команда help- #
# ////////////// #

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "Разберём команды:\n"
                                      "/register - Познакомиться с ботом (регистрация)\n"
                                      "/add_build - Начать сборку\n"
                                      "/saved_builds - Сохранённые сборки")





# Загрузка комплектующих из базы данных
def get_components(component_type, max_price=None, compatibility=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT id, name, specs, price, compatibility FROM {component_type}"
    params = []

    # Фильтрация по бюджету
    if max_price:
        query += " WHERE price <= ?"
        params.append(max_price)

    # Фильтрация по совместимости
    if compatibility:
        if "WHERE" in query:
            query += " AND"
        else:
            query += " WHERE"
        query += " compatibility LIKE ?"
        params.append(f"%{compatibility}%")

    cursor.execute(query, params)
    components = cursor.fetchall()
    conn.close()
    return components

# Команда для установки бюджета
@bot.message_handler(commands=['set_budget'])
def set_budget(message):
    bot.send_message(message.chat.id, "Введите ваш бюджет (в рублях):")

    def process_budget(msg):
        if not msg.text.isdigit():
            bot.send_message(msg.chat.id, "Пожалуйста, введите число!")
            return
        user_budgets[msg.chat.id] = int(msg.text)
        bot.send_message(msg.chat.id, f"Ваш бюджет установлен: {msg.text} руб.")
        start_build(msg)

    bot.register_next_step_handler(message, process_budget)

# Начало подбора сборки
@bot.message_handler(commands=['start_build'])
def start_build(message):
    if message.chat.id not in user_budgets:
        bot.send_message(message.chat.id, "Пожалуйста, сначала установите бюджет с помощью команды /set_budget.")
        return

    user_build_progress[message.chat.id] = {}
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
    types.InlineKeyboardButton(text="Процессор", callback_data="select_cpus"),
    types.InlineKeyboardButton(text="Материнская плата", callback_data="select_mother_boards"),
    types.InlineKeyboardButton(text="Видеокарта", callback_data="select_gpus"),
    types.InlineKeyboardButton(text="Оперативная память", callback_data="select_rams"),
    types.InlineKeyboardButton(text="Блок питания", callback_data="select_power_supplies"),
    types.InlineKeyboardButton(text="Накопитель", callback_data="select_storages"),
    types.InlineKeyboardButton(text="Корпус", callback_data="select_computer_cases")
    ]
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, "Выберите тип комплектующего:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def select_component(call):
    # Маппинг callback_data на имена таблиц в базе данных
    component_map = {
        "cpus": "cpus",
        "mother_boards": "motherBoards",  # Убедитесь, что имя таблицы совпадает с этим ключом
        "gpus": "gpus",
        "rams": "rams",
        "power_supplies": "powerSupplies",  # Имя таблицы совпадает
        "storages": "storages",
        "computer_cases": "computerCases"  # Имя таблицы совпадает
    }

    # Извлечение типа компонента из callback_data
    component_type_key = call.data[len("select_"):]  # Получаем часть после "select_"
    component_type = component_map.get(component_type_key)

    if not component_type:
        bot.answer_callback_query(call.id, f"Ошибка: неверный тип комплектующего ({component_type_key})!")
        return

    # Получение бюджета пользователя
    max_price = user_budgets.get(call.message.chat.id)

    # Совместимость для специфических комплектующих
    compatibility = None
    if component_type == "motherBoards":
        # Совместимость с процессором
        compatibility = user_build_progress[call.message.chat.id].get("cpus")
    elif component_type == "rams":
        # Совместимость с материнской платой
        compatibility = user_build_progress[call.message.chat.id].get("motherBoards")

    # Получение данных из базы
    components = get_components(component_type, max_price, compatibility)

    if not components:
        bot.answer_callback_query(call.id, "Нет доступных комплектующих.")
        return

    # Создание клавиатуры
    keyboard = InlineKeyboardMarkup()
    for comp_id, name, specs, price, _ in components:
        keyboard.add(InlineKeyboardButton(
            text=f"{name} ({price} руб.) - {specs}",
            callback_data=f"add_{component_type}_{comp_id}"
        ))

    # Добавляем кнопку возврата в меню
    keyboard.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_menu"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f"Выберите {component_type_key} (можно использовать фильтрацию по бюджету):",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_build(call):
    _, component_type, comp_id = call.data.split("_")
    user_build_progress[call.message.chat.id][component_type] = comp_id
    bot.answer_callback_query(call.id, f"{component_type.capitalize()} добавлен в сборку!")
    bot.send_message(call.message.chat.id, f"{component_type.capitalize()} успешно добавлен.")

    # Проверка завершенности сборки
    if len(user_build_progress[call.message.chat.id]) == 7:
        save_build_to_db(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Сборка завершена и сохранена!")
    else:
        start_build(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "return_to_menu")
def return_to_menu(call):
    start_build(call.message)

# Сохранение сборки в базу данных
def save_build_to_db(user_id):
    build = user_build_progress[user_id]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_builds (telegram_id, cpu, motherboard, gpu, ram, power_supply, storage, computer_case)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        build.get("cpus"),
        build.get("mother_boards"),
        build.get("gpus"),
        build.get("rams"),
        build.get("power_supplies"),
        build.get("storages"),
        build.get("computer_cases")
    ))
    conn.commit()
    conn.close()
    del user_build_progress[user_id]
    bot.send_message(user_id, "Сборка успешно сохранена!")

# Запуск бота
bot.polling()


