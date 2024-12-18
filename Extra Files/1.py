# Добавление завершения сборки и ввода её названия
@bot.message_handler(commands=['finish_build'])
def finish_build(message):
    user_id = message.chat.id
    if user_id not in user_build_progress or len(user_build_progress[user_id]) < 7:
        bot.send_message(user_id, "Вы ещё не завершили сборку! Пожалуйста, добавьте все комплектующие.")
        return

    bot.send_message(user_id, "Введите название для вашей сборки:")

    # Обработка названия сборки
    def process_build_name(msg):
        build_name = msg.text.strip()
        if not build_name:
            bot.send_message(msg.chat.id, "Название не может быть пустым. Попробуйте ещё раз.")
            return

        # Сохраняем сборку в базу данных
        save_build_to_db(user_id, build_name)
        bot.send_message(msg.chat.id, f"Сборка '{build_name}' успешно сохранена!")
        start_build(msg)  # Вернуться в меню

    bot.register_next_step_handler(message, process_build_name)

# Сохранение сборки в базу данных
def save_build_to_db(user_id, build_name):
    build = user_build_progress[user_id]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_builds (telegram_id, build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        build_name,
        build.get("cpus"),
        build.get("motherBoards"),
        build.get("gpus"),
        build.get("rams"),
        build.get("powerSupplies"),
        build.get("storages"),
        build.get("computerCases")
    ))
    conn.commit()
    conn.close()
    del user_build_progress[user_id]  # Очистить временные данные

# Просмотр сохранённых сборок
@bot.message_handler(commands=['saved_builds'])
def view_saved_builds(message):
    user_id = message.chat.id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case
        FROM user_builds WHERE telegram_id = ?
    """, (user_id,))
    builds = cursor.fetchall()
    conn.close()

    if not builds:
        bot.send_message(user_id, "У вас ещё нет сохранённых сборок.")
        return

    # Формирование списка сохранённых сборок
    response = "Ваши сохранённые сборки:\n\n"
    for idx, build in enumerate(builds, start=1):
        build_name, cpu, motherboard, gpu, ram, power_supply, storage, computer_case = build
        response += f"Сборка {idx}: {build_name}\n"
        response += f"- Процессор: {cpu}\n"
        response += f"- Материнская плата: {motherboard}\n"
        response += f"- Видеокарта: {gpu}\n"
        response += f"- Оперативная память: {ram}\n"
        response += f"- Блок питания: {power_supply}\n"
        response += f"- Накопитель: {storage}\n"
        response += f"- Корпус: {computer_case}\n\n"

    bot.send_message(user_id, response)
