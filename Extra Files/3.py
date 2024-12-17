import sqlite3
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer

dbPath = os.path.join('D:', '\JelezkaBot', 'DataBase', 'PCBuild.db')
bot = telebot.TeleBot("ВАШ_ТОКЕН")

# Словарь для временного хранения сборок
user_builds = {}

# Удаление сборки через 15 минут
def remove_build(user_id):
    if user_id in user_builds:
        del user_builds[user_id]
        print(f"Сборка пользователя {user_id} удалена за бездействие.")

# Команда "создать сборку"
@bot.message_handler(commands=["add_builds"])
def create_build(message):
    user_id = message.from_user.id
    user_builds[user_id] = {
        "budget": 0,
        "purpose": "",
        "components": {"processor": None, "ram": None, "gpu": None, "power_supply": None, "storage": None},
    }
    bot.send_message(user_id, "Введите ваш бюджет для сборки:")
    bot.register_next_step_handler(message, set_budget)

# Установка бюджета
def set_budget(message):
    try:
        budget = int(message.text)
        user_id = message.from_user.id
        user_builds[user_id]["budget"] = budget

        # Предлагаем выбрать назначение сборки
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Игры", callback_data="gaming"),
            InlineKeyboardButton("Работа", callback_data="work"),
            InlineKeyboardButton("Графика", callback_data="graphics"),
            InlineKeyboardButton("Бюджетная", callback_data="budget"),
        )
        bot.send_message(user_id, "Выберите назначение сборки:", reply_markup=markup)

        # Устанавливаем таймер на удаление сборки
        Timer(900, remove_build, args=[user_id]).start()
    except ValueError:
        bot.send_message(message.from_user.id, "Пожалуйста, введите числовое значение бюджета.")
        bot.register_next_step_handler(message, set_budget)

# Обработка выбора назначения сборки
@bot.callback_query_handler(func=lambda call: call.data in ["gaming", "work", "graphics", "budget"])
def set_purpose(call):
    user_id = call.from_user.id
    purpose = call.data
    user_builds[user_id]["purpose"] = purpose
    bot.send_message(user_id, "Начинаем подбор комплектующих.")
    select_component(user_id, "processor")

# Выбор комплектующих
def select_component(user_id, component_type):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    # Запрос подходящих комплектующих
    purpose = user_builds[user_id]["purpose"]
    budget = user_builds[user_id]["budget"]

    query = f"""
    SELECT id, name, price FROM {component_type}s 
    WHERE category = ? AND price <= ? ORDER BY price DESC
    """
    cursor.execute(query, (purpose, budget * 0.3))  # Ограничение на 30% бюджета
    components = cursor.fetchall()
    conn.close()

    if components:
        # Создаем InlineKeyboard с комплектующими
        markup = InlineKeyboardMarkup()
        for comp in components:
            comp_id, name, price = comp
            markup.add(InlineKeyboardButton(f"{name} - {price}₽", callback_data=f"{component_type}:{comp_id}"))

        bot.send_message(user_id, f"Выберите {component_type}:", reply_markup=markup)
    else:
        bot.send_message(user_id, f"Нет доступных вариантов для {component_type}. Пропускаем...")
        next_component(user_id, component_type)

# Обработка выбора комплектующих
@bot.callback_query_handler(func=lambda call: ":" in call.data)
def save_component(call):
    user_id = call.from_user.id
    component_type, component_id = call.data.split(":")
    user_builds[user_id]["components"][component_type] = int(component_id)
    next_component(user_id, component_type)

# Переход к следующему компоненту
def next_component(user_id, current_type):
    component_order = ["processor", "ram", "gpu", "power_supply", "storage"]
    next_index = component_order.index(current_type) + 1
    if next_index < len(component_order):
        select_component(user_id, component_order[next_index])
    else:
        finish_build(user_id)

# Завершение сборки
def finish_build(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Сохранить сборку", callback_data="save_build"),
        InlineKeyboardButton("Пропустить", callback_data="discard_build"),
    )
    bot.send_message(user_id, "Сборка завершена. Что сделать с ней?", reply_markup=markup)

# Сохранение сборки
@bot.callback_query_handler(func=lambda call: call.data == "save_build")
def save_build(call):
    user_id = call.from_user.id
    build = user_builds.get(user_id)

    if build:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_builds (user_id, processor_id, ram_id, gpu_id, power_supply_id, storage_id, budget, purpose) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                build["components"]["processor"],
                build["components"]["ram"],
                build["components"]["gpu"],
                build["components"]["power_supply"],
                build["components"]["storage"],
                build["budget"],
                build["purpose"],
            ),
        )
        conn.commit()
        conn.close()

        bot.send_message(user_id, "Сборка сохранена!")
        del user_builds[user_id]
    else:
        bot.send_message(user_id, "Нет сборки для сохранения.")

# Пропуск сохранения
@bot.callback_query_handler(func=lambda call: call.data == "discard_build")
def discard_build(call):
    user_id = call.from_user.id
    if user_id in user_builds:
        del user_builds[user_id]
    bot.send_message(user_id, "Сборка была удалена.")
