import sqlite3
import time
from telebot import TeleBot, types
from threading import Timer

TOKEN = 'YOUR_BOT_TOKEN'
bot = TeleBot(TOKEN)

dbPath = r"D:\JelezkaBot\DataBase\PCBuild.db"

# Локальные сборки
user_builds = {}

# Таймер для удаления несохранённых сборок
def delete_unsaved_build(user_id):
    if user_id in user_builds:
        del user_builds[user_id]
        print(f"Сборка пользователя {user_id} удалена из памяти.")

# Начало процесса сборки
@bot.message_handler(commands=['start_build'])
def start_build(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Укажите ваш бюджет (в рублях):")
    bot.register_next_step_handler(message, set_budget)

def set_budget(message):
    try:
        budget = int(message.text)
        chat_id = message.chat.id
        user_builds[chat_id] = {'budget': budget, 'components': {}}
        # InlineKeyboard для выбора назначения
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Игры", callback_data="purpose_gaming"))
        keyboard.add(types.InlineKeyboardButton("Работа", callback_data="purpose_work"))
        keyboard.add(types.InlineKeyboardButton("Графика", callback_data="purpose_graphics"))
        keyboard.add(types.InlineKeyboardButton("Бюджет", callback_data="purpose_budget"))
        bot.send_message(chat_id, "Выберите назначение сборки:", reply_markup=keyboard)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите бюджет числом. Попробуйте снова:")
        bot.register_next_step_handler(message, set_budget)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith("purpose_"))
def set_purpose(call):
    chat_id = call.message.chat.id
    purpose = call.data.split("_")[1]
    if chat_id in user_builds:
        user_builds[chat_id]['purpose'] = purpose
        bot.send_message(chat_id, "Теперь выберите процессор:")
        suggest_component(chat_id, "processors")
        # Запускаем таймер на 15 минут для удаления сборки
        Timer(900, delete_unsaved_build, args=[chat_id]).start()

def suggest_component(user_id, component_type):
    build = user_builds[user_id]
    budget = build['budget']
    purpose = build['purpose']

    # Подключение к базе данных и выбор подходящих комплектующих
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id, name, price 
        FROM {component_type} 
        WHERE category = ? AND price BETWEEN ? AND ? 
        ORDER BY price ASC
    """, (purpose, budget * 0.1, budget * 0.3))
    components = cursor.fetchall()
    conn.close()

    # InlineKeyboard с компонентами
    if components:
        keyboard = types.InlineKeyboardMarkup()
        for comp_id, name, price in components:
            keyboard.add(types.InlineKeyboardButton(f"{name} ({price} руб.)", callback_data=f"select_{component_type}_{comp_id}"))
        bot.send_message(user_id, f"Выберите {component_type[:-1]}:", reply_markup=keyboard)
    else:
        bot.send_message(user_id, f"Подходящих {component_type[:-1]} не найдено в рамках бюджета.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def select_component(call):
    user_id = call.message.chat.id
    data = call.data.split("_")
    component_type = data[1]
    component_id = int(data[2])

    # Сохраняем выбранный компонент
    if user_id in user_builds:
        user_builds[user_id]['components'][component_type] = component_id
        next_component = get_next_component(component_type)
        if next_component:
            suggest_component(user_id, next_component)
        else:
            # Завершаем сборку
            finish_build(user_id)

def get_next_component(current):
    # Определяем следующий тип комплектующих
    order = ["processors", "ram", "gpus", "power_supplies", "storage"]
    try:
        return order[order.index(current) + 1]
    except (ValueError, IndexError):
        return None
def finish_build(user_id):
    # InlineKeyboard для завершения сборки
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сохранить сборку", callback_data="save_build"))
    keyboard.add(types.InlineKeyboardButton("Пропустить", callback_data="discard_build"))
    bot.send_message(user_id, "Сборка завершена. Вы хотите сохранить её?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "save_build")
def save_build(call):
    user_id = call.message.chat.id
    if user_id in user_builds:
        build = user_builds.pop(user_id)
        # Сохраняем сборку в базу данных
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_builds (user_id, budget, purpose, processor_id, ram_id, gpu_id, power_supply_id, storage_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, build['budget'], build['purpose'],
              build['components'].get('processors'),
              build['components'].get('ram'),
              build['components'].get('gpus'),
              build['components'].get('power_supplies'),
              build['components'].get('storage')))
        conn.commit()
        conn.close()
        bot.send_message(user_id, "Сборка успешно сохранена!")
    else:
        bot.send_message(user_id, "Сборка не найдена.")

@bot.callback_query_handler(func=lambda call: call.data == "discard_build")
def discard_build(call):
    user_id = call.message.chat.id
    if user_id in user_builds:
        del user_builds[user_id]
    bot.send_message(user_id, "Сборка удалена.")

# Запуск бота
bot.polling(none_stop=True)
