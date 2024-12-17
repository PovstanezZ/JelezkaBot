import sqlite3
import time
from telebot import TeleBot, types

# Инициализация бота
TOKEN = "YOUR_BOT_TOKEN"
bot = TeleBot(TOKEN)

# Подключение к базе данных
db_path = r'D:\JelezkaBot\DataBase\PCBuild.db'

# Словарь для хранения локальных сборок
active_builds = {}

# Хендлер для команды "/create_build"
@bot.message_handler(commands=['create_build'])
def create_build_handler(message):
    user_id = message.chat.id
    active_builds[user_id] = {
        "budget": None,
        "purpose": None,
        "components": {},
        "last_update": time.time()
    }
    bot.send_message(user_id, "Введите бюджет сборки (в рублях):")

@bot.message_handler(func=lambda message: message.chat.id in active_builds and active_builds[message.chat.id]["budget"] is None)
def handle_budget(message):
    user_id = message.chat.id
    try:
        budget = int(message.text)
        if budget < 10000:
            bot.send_message(user_id, "Бюджет слишком мал. Укажите сумму не менее 10 000 рублей.")
            return
        active_builds[user_id]["budget"] = budget
        bot.send_message(user_id, "Каково назначение сборки? (например: gaming, work, graphics, budget)")
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, укажите корректное числовое значение бюджета.")

@bot.message_handler(func=lambda message: message.chat.id in active_builds and active_builds[message.chat.id]["purpose"] is None)
def handle_purpose(message):
    user_id = message.chat.id
    purpose = message.text.lower()
    if purpose not in ['gaming', 'work', 'graphics', 'budget']:
        bot.send_message(user_id, "Неверное назначение. Укажите одно из: gaming, work, graphics, budget.")
        return
    active_builds[user_id]["purpose"] = purpose
    bot.send_message(user_id, "Теперь начнем выбор комплектующих. Выберите процессор.", reply_markup=get_components_keyboard('processors', user_id))

# Генерация клавиатуры с компонентами
def get_components_keyboard(component_type, user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    budget = active_builds[user_id]["budget"]
    purpose = active_builds[user_id]["purpose"]
    min_price, max_price = budget * 0.1, budget * 0.3
    cursor.execute(f"SELECT id, name, price FROM {component_type} WHERE category = ? AND price BETWEEN ? AND ?", (purpose, min_price, max_price))
    components = cursor.fetchall()
    conn.close()

    keyboard = types.InlineKeyboardMarkup()
    for component in components:
        keyboard.add(types.InlineKeyboardButton(f"{component[1]} ({component[2]} руб.)", callback_data=f"{component_type}_{component[0]}"))
    return keyboard

# Обработчик выбора компонента
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in ['processors', 'ram', 'gpus', 'power_supplies', 'storage'])
def handle_component_selection(call):
    user_id = call.message.chat.id
    component_type, component_id = call.data.split('_')
    active_builds[user_id]["components"][component_type] = int(component_id)
    next_step = {
        'processors': 'ram',
        'ram': 'gpus',
        'gpus': 'power_supplies',
        'power_supplies': 'storage',
        'storage': None
    }[component_type]

    if next_step:
        bot.edit_message_text(f"Вы выбрали {component_type}. Теперь выберите {next_step}.", call.message.chat.id, call.message.message_id, reply_markup=get_components_keyboard(next_step, user_id))
    else:
        bot.edit_message_text("Сборка завершена. Вы можете сохранить её или пропустить.", call.message.chat.id, call.message.message_id, reply_markup=get_save_keyboard())

# Генерация клавиатуры для сохранения сборки
def get_save_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сохранить сборку", callback_data="save_build"))
    keyboard.add(types.InlineKeyboardButton("Пропустить", callback_data="skip_build"))
    return keyboard


# Сохранение сборки
@bot.callback_query_handler(func=lambda call: call.data in ["save_build", "skip_build"])
def handle_save_or_skip(call):
    user_id = call.message.chat.id
    if call.data == "save_build":
        save_build_to_db(user_id)
        bot.edit_message_text("Сборка успешно сохранена!", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text("Сборка пропущена.", call.message.chat.id, call.message.message_id)
    del active_builds[user_id]

# Сохранение сборки в базу данных
def save_build_to_db(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    build = active_builds[user_id]
    components = build["components"]
    cursor.execute("""
        INSERT INTO user_builds (user_id, processor_id, ram_id, gpu_id, power_supply_id, storage_id, budget, purpose)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, components.get('processors'), components.get('ram'), components.get('gpus'), components.get('power_supplies'), components.get('storage'), build["budget"], build["purpose"]))
    conn.commit()
    conn.close()

# Автоудаление сборки через 15 минут
def cleanup_inactive_builds():
    current_time = time.time()
    for user_id in list(active_builds.keys()):
        if current_time - active_builds[user_id]["last_update"] > 900:
            del active_builds[user_id]

# Регулярная проверка для очистки неактивных сборок
import threading

def schedule_cleanup():
    while True:
        cleanup_inactive_builds()
        time.sleep(60)

cleanup_thread = threading.Thread(target=schedule_cleanup, daemon=True)
cleanup_thread.start()


