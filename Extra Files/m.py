import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import os

from DataBase.data_base_code import db_path
from cfg import *

# Токен вашего бота
bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Хранилище для текущих сборок пользователей
user_sessions = {}

# Регистрация пользователя
@bot.message_handler(commands=['start', 'registration'])
def register_user(message):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Проверка на существующего пользователя
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,))
    user = cursor.fetchone()

    if user:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")
    else:
        # Добавление нового пользователя
        cursor.execute("INSERT INTO users (telegram_id, first_name, last_name) VALUES (?, ?, ?)", (
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name or ""
        ))
        conn.commit()
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")

    conn.close()
    show_main_menu(message)

# Главное меню
def show_main_menu(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Начать сборку", callback_data="start_build"))
    markup.add(InlineKeyboardButton("Мои сборки", callback_data="view_builds"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Начало сборки
@bot.callback_query_handler(func=lambda call: call.data == "start_build")
def start_build(call):
    # Инициализация новой сессии сборки
    user_sessions[call.message.chat.id] = {"budget": None, "usage": None, "components": {}}
    bot.send_message(call.message.chat.id, "Введите ваш бюджет в рублях:")
    bot.register_next_step_handler(call.message, get_budget)

def get_budget(message):
    try:
        budget = int(message.text)
        user_sessions[message.chat.id]["budget"] = budget
        bot.send_message(message.chat.id, "Выберите назначение сборки:", reply_markup=get_usage_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, get_budget)

def get_usage_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Игровые", callback_data="usage_gaming"),
        InlineKeyboardButton("Для работы", callback_data="usage_work"),
        InlineKeyboardButton("Бюджетные", callback_data="usage_budget"),
        InlineKeyboardButton("Графика", callback_data="usage_graphics")
    )
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("usage_"))
def select_usage(call):
    usage = call.data.split("_")[1]
    user_sessions[call.message.chat.id]["usage"] = usage
    ask_component(call.message, "cpus")

# Дальше аналогично реализуйте выбор компонентов...
def ask_component(message, component_type):
    chat_id = message.chat.id
    session = user_sessions.get(chat_id)
    if not session:
        bot.send_message(chat_id, "Сессия сборки не найдена. Пожалуйста, начните заново.")
        return

    # Получаем комплектующие из базы данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Фильтрация комплектующих по бюджету и назначению
    budget = session["budget"]
    usage = session["usage"]
    query = f"""
        SELECT id, name, specs, price 
        FROM {component_type} 
        WHERE category = ? AND price <= ?
    """
    cursor.execute(query, (usage, budget))
    components = cursor.fetchall()
    conn.close()

    if not components:
        bot.send_message(chat_id, f"Нет доступных {component_type} для вашего бюджета и назначения.")
        cancel_build(message)
        return

    # Генерируем клавиатуру с вариантами
    markup = InlineKeyboardMarkup()
    for comp in components:
        comp_id, name, specs, price = comp
        markup.add(InlineKeyboardButton(f"{name} ({price} руб.)", callback_data=f"{component_type}_{comp_id}"))

    # Добавляем кнопку отмены сборки
    markup.add(InlineKeyboardButton("Отмена сборки", callback_data="cancel_build"))
    bot.send_message(chat_id, f"Выберите {component_type}:", reply_markup=markup)

# Обработка выбора компонента
@bot.callback_query_handler(func=lambda call: "_" in call.data and call.data.split("_")[0] in [
    "cpus", "mother_boards", "gpus", "rams", "power_supplies", "storages", "computer_case"])
def select_component(call):
    chat_id = call.message.chat.id
    component_type, component_id = call.data.split("_")
    session = user_sessions.get(chat_id)
    if not session:
        bot.send_message(chat_id, "Сессия сборки не найдена. Пожалуйста, начните заново.")
        return

    # Сохраняем выбранный компонент в текущей сессии
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, specs, price FROM {component_type} WHERE id = ?", (component_id,))
    component = cursor.fetchone()
    conn.close()

    if component:
        session["components"][component_type] = {
            "name": component[0],
            "specs": component[1],
            "price": component[2]
        }

        # Выбор следующего компонента
        next_components = [
            "cpus", "mother_boards", "gpus", "rams",
            "power_supplies", "storages", "computer_case"
        ]
        current_index = next_components.index(component_type)
        if current_index + 1 < len(next_components):
            ask_component(call.message, next_components[current_index + 1])
        else:
            # Завершение сборки
            finish_build(call.message)
    else:
        bot.send_message(chat_id, "Ошибка при выборе компонента. Попробуйте снова.")
def finish_build(message):
    chat_id = message.chat.id
    session = user_sessions.get(chat_id)
    if not session:
        bot.send_message(chat_id, "Сессия сборки не найдена. Пожалуйста, начните заново.")
        return

    # Подсчитываем итоговую стоимость
    total_price = sum(comp["price"] for comp in session["components"].values())

    # Формируем итоговый список комплектующих
    build_summary = "Сборка завершена!\n\nВыбранные комплектующие:\n"
    for component_type, component in session["components"].items():
        build_summary += f"{component_type.capitalize()}: {component['name']} ({component['price']} руб.)\n"

    build_summary += f"\nИтоговая стоимость: {total_price} руб."

    # Предлагаем сохранить сборку
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Сохранить сборку", callback_data="save_build"))
    markup.add(InlineKeyboardButton("Отменить сборку", callback_data="cancel_build"))
    bot.send_message(chat_id, build_summary, reply_markup=markup)

# Сохранение сборки
@bot.callback_query_handler(func=lambda call: call.data == "save_build")
def save_build(call):
    chat_id = call.message.chat.id
    session = user_sessions.pop(chat_id, None)
    if not session:
        bot.send_message(chat_id, "Сессия сборки не найдена. Пожалуйста, начните заново.")
        return

    bot.send_message(chat_id, "Введите название для вашей сборки:")
    bot.register_next_step_handler(call.message, save_build_name)

def save_build_name(message):
    chat_id = message.chat.id
    build_name = message.text
    session = user_sessions.pop(chat_id, None)
    if not session:
        bot.send_message(chat_id, "Сессия сборки не найдена. Пожалуйста, начните заново.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_builds (telegram_id, build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        message.chat.id, build_name,
        session["components"]["cpus"]["name"],
        session["components"]["mother_boards"]["name"],
        session["components"]["gpus"]["name"],
        session["components"]["rams"]["name"],
        session["components"]["power_supplies"]["name"],
        session["components"]["storages"]["name"],
        session["components"]["computer_case"]["name"]
    ))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, f"Сборка '{build_name}' успешно сохранена!")
@bot.message_handler(commands=['saved_builds'])
def view_saved_builds(message):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, build_name FROM user_builds WHERE telegram_id = ?", (message.chat.id,))
    builds = cursor.fetchall()
    conn.close()

    if not builds:
        bot.send_message(message.chat.id, "У вас нет сохранённых сборок.")
        return

    # Генерируем кнопки для просмотра сборок
    markup = InlineKeyboardMarkup()
    for build_id, build_name in builds:
        markup.add(InlineKeyboardButton(build_name, callback_data=f"view_build_{build_id}"))
    bot.send_message(message.chat.id, "Ваши сборки:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_build_"))
def view_build(call):
    build_id = int(call.data.split("_")[2])
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case 
        FROM user_builds 
        WHERE id = ?
    """, (build_id,))
    build = cursor.fetchone()
    conn.close()

    if not build:
        bot.send_message(call.message.chat.id, "Сборка не найдена.")
        return

    build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case = build
    build_summary = (
        f"Сборка: {build_name}\n"
        f"Процессор: {cpu}\n"
        f"Материнская плата: {motherboard}\n"
        f"Видеокарта: {gpu}\n"
        f"Оперативная память: {ram}\n"
        f"Блок питания: {power_supply}\n"
        f"Накопитель: {storage}\n"
        f"Корпус: {computer_case}"
    )
    bot.send_message(call.message.chat.id, build_summary)
@bot.callback_query_handler(func=lambda call: call.data == "cancel_build")
def cancel_build(call):
    chat_id = call.message.chat.id
    user_sessions.pop(chat_id, None)
    bot.send_message(chat_id, "Сборка отменена.")
