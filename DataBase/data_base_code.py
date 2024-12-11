import sqlite3
import os

dbPath = os.path.join('D:','\JelezkaBot','DataBase', 'PCBuild.db')
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Таблица для регистрации пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT
);
""")

# Таблицы для комплектующих
cursor.execute("""
CREATE TABLE IF NOT EXISTS processors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
    price INTEGER NOT NULL,
    cores INTEGER NOT NULL,
    threads INTEGER NOT NULL,
    frequency REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ram (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
    price INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    speed INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gpus (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
    price INTEGER NOT NULL,
    vram INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS power_supplies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
    price INTEGER NOT NULL,
    wattage INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS storage (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('gaming', 'work', 'graphics', 'budget')),
    price INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('SSD', 'HDD')),
    capacity INTEGER NOT NULL
);
""")

# Таблица для сохранения сборок пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_builds (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT,
    processor_id INTEGER,
    ram_id INTEGER,
    gpu_id INTEGER,
    power_supply_id INTEGER,
    storage_id INTEGER,
    budget INTEGER,
    purpose INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(processor_id) REFERENCES processors(id),
    FOREIGN KEY(ram_id) REFERENCES ram(id),
    FOREIGN KEY(gpu_id) REFERENCES gpus(id),
    FOREIGN KEY(power_supply_id) REFERENCES power_supplies(id),
    FOREIGN KEY(storage_id) REFERENCES storage(id)
);
""")

# Заполнение таблиц данными
# Расширенные данные для заполнения
components = {
    "processors": [
        ("Ryzen 5 5600X", "gaming", 18900, 6, 12, 4.6),
        ("Intel i5-12400", "work", 17500, 6, 12, 4.4),
        ("Ryzen 9 5900X", "graphics", 49900, 12, 24, 4.8),
        ("Intel i3-10100", "budget", 9500, 4, 8, 4.1),
        ("Ryzen 7 5800X", "gaming", 26000, 8, 16, 4.7),
        ("Intel i7-12700K", "work", 32000, 12, 20, 5.0),
        ("Ryzen 3 3100", "budget", 6700, 4, 8, 3.9),
        ("Intel i9-12900K", "graphics", 54000, 16, 24, 5.2),
        ("Ryzen 7 7700X", "gaming", 30000, 8, 16, 4.5),
        ("Intel i5-13600KF", "work", 27000, 14, 20, 5.1),
        ("Ryzen 9 7950X", "graphics", 73000, 16, 32, 5.7),
        ("Intel i3-13100F", "budget", 11000, 4, 8, 4.5),
        ("Ryzen 5 7600", "gaming", 21000, 6, 12, 5.0),
        ("Intel i7-13700", "work", 40000, 16, 24, 5.4),
        ("Ryzen 9 7900", "graphics", 60000, 12, 24, 5.6),
        ("Intel Pentium Gold G7400", "budget", 4700, 2, 4, 3.7),
        ("Ryzen Threadripper 3960X", "graphics", 145000, 24, 48, 4.5),
        ("Intel i9-11900K", "work", 42000, 8, 16, 5.3),
        ("Ryzen 5 5600G", "budget", 15000, 6, 12, 4.4),
        ("Intel Celeron G5905", "budget", 4300, 2, 2, 3.5),
    ],
    "ram": [
        ("Corsair Vengeance 16GB 3200MHz", "gaming", 6200, 16, 3200),
        ("Crucial 16GB 2666MHz", "work", 5700, 16, 2666),
        ("G.Skill Trident Z 32GB 3600MHz", "graphics", 14000, 32, 3600),
        ("Kingston ValueRAM 8GB 2400MHz", "budget", 2200, 8, 2400),
        ("HyperX Fury 16GB 3200MHz", "gaming", 6800, 16, 3200),
        ("TeamGroup Elite 8GB 2666MHz", "work", 2100, 8, 2666),
        ("Patriot Signature 4GB 2400MHz", "budget", 1400, 4, 2400),
        ("Corsair Dominator Platinum 32GB 4000MHz", "graphics", 23000, 32, 4000),
        ("ADATA XPG 16GB 3000MHz", "gaming", 5000, 16, 3000),
        ("Crucial Ballistix 16GB 3200MHz", "work", 6500, 16, 3200),
        ("Kingston HyperX Predator 32GB 3600MHz", "graphics", 15000, 32, 3600),
        ("TeamGroup T-Force Vulcan 8GB 3000MHz", "budget", 3000, 8, 3000),
        ("G.Skill Ripjaws V 16GB 3600MHz", "gaming", 7000, 16, 3600),
        ("Samsung 8GB 2666MHz", "work", 2500, 8, 2666),
        ("Crucial 32GB 2400MHz", "graphics", 12000, 32, 2400),
        ("Patriot Viper Steel 16GB 3600MHz", "gaming", 7400, 16, 3600),
        ("ADATA Premier 8GB 2400MHz", "budget", 1900, 8, 2400),
        ("Kingston Fury Beast 32GB 3200MHz", "graphics", 16000, 32, 3200),
        ("HyperX Impact 16GB 2666MHz", "work", 7200, 16, 2666),
        ("TeamGroup Delta RGB 16GB 3200MHz", "gaming", 7800, 16, 3200),
    ],
    "gpus": [
        ("NVIDIA RTX 3060", "gaming", 32000, 12),
        ("AMD Radeon RX 6600", "work", 27000, 8),
        ("NVIDIA RTX 3090", "graphics", 145000, 24),
        ("GTX 1650", "budget", 12500, 4),
        ("AMD RX 580", "budget", 14500, 8),
        ("NVIDIA GTX 1660 Super", "gaming", 21000, 6),
        ("NVIDIA RTX 3050", "work", 24000, 8),
        ("AMD RX 6700 XT", "graphics", 47000, 12),
        ("NVIDIA RTX 3070 Ti", "gaming", 60000, 8),
        ("AMD RX 5600 XT", "work", 35000, 6),
        ("NVIDIA RTX 4080", "graphics", 180000, 16),
        ("AMD RX Vega 64", "budget", 20000, 8),
        ("NVIDIA GTX 1080 Ti", "gaming", 27000, 11),
        ("AMD RX 590", "work", 17000, 8),
        ("NVIDIA RTX 3060 Ti", "graphics", 43000, 8),
        ("AMD RX 550", "budget", 8500, 2),
        ("NVIDIA RTX 4050", "gaming", 25000, 8),
        ("AMD RX 6400", "work", 22000, 4),
        ("NVIDIA RTX 3090 Ti", "graphics", 165000, 24),
        ("AMD RX 6600 XT", "gaming", 36000, 8),
    ],
    "power_supplies": [
        ("Corsair RM750x", "gaming", 9800, 750),
        ("Cooler Master MWE 550", "work", 5200, 550),
        ("EVGA SuperNOVA 1000", "graphics", 18500, 1000),
        ("Thermaltake Litepower 450", "budget", 2700, 450),
        ("Seasonic Focus GX-750", "gaming", 8800, 750),
        ("Deepcool DQ750-M", "work", 6900, 750),
        ("Chieftec Proton 650W", "budget", 5000, 650),
        ("Cooler Master V850", "graphics", 12000, 850),
        ("Corsair CX550M", "budget", 4300, 550),
        ("FSP Hyper 700W", "gaming", 6200, 700),
        ("Be Quiet! Straight Power 11 650W", "work", 8700, 650),
        ("Gigabyte P750GM", "graphics", 9600, 750),
        ("Aerocool KCAS 700W", "budget", 4900, 700),
        ("NZXT C650", "gaming", 7900, 650),
        ("XPG Core Reactor 750W", "work", 7400, 750),
        ("Zalman WattBit 600W", "budget", 3300, 600),
        ("Corsair HX1000i", "graphics", 15800, 1000),
        ("Thermaltake Toughpower GX1 600W", "budget", 4400, 600),
        ("Deepcool DA700", "gaming", 6500, 700),
        ("FSP Raider II 750W", "work", 8100, 750),
    ],
        "storage": [
        ("Samsung 970 EVO 1TB", "gaming", 9800, "SSD", 1000),
        ("WD Blue 500GB", "work", 4500, "HDD", 500),
        ("Seagate Barracuda 2TB", "graphics", 7400, "HDD", 2000),
        ("Kingston A400 240GB", "budget", 1800, "SSD", 240),
        ("Samsung 980 Pro 2TB", "gaming", 18000, "SSD", 2000),
        ("Crucial MX500 1TB", "work", 7800, "SSD", 1000),
        ("WD Black SN850 1TB", "graphics", 13500, "SSD", 1000),
        ("Seagate FireCuda 510 1TB", "gaming", 9600, "SSD", 1000),
        ("ADATA SU650 480GB", "budget", 3200, "SSD", 480),
        ("Samsung T7 500GB", "work", 6500, "SSD", 500),
        ("Crucial P3 2TB", "graphics", 14500, "SSD", 2000),
        ("Toshiba P300 1TB", "budget", 3800, "HDD", 1000),
        ("Seagate IronWolf 4TB", "work", 11000, "HDD", 4000),
        ("WD Red Plus 6TB", "graphics", 19500, "HDD", 6000),
        ("Kingston NV1 1TB", "gaming", 8500, "SSD", 1000),
        ("Patriot Burst 240GB", "budget", 2100, "SSD", 240),
        ("WD Blue 2TB", "work", 8700, "HDD", 2000),
        ("Samsung 870 QVO 4TB", "graphics", 24500, "SSD", 4000),
        ("Silicon Power A55 512GB", "budget", 3500, "SSD", 512),
        ("Seagate Expansion 8TB", "work", 22000, "HDD", 8000),
    ]
}


# Вставка данных
insert_queries = {
    "processors": "INSERT INTO processors (name, category, price, cores, threads, frequency) VALUES (?, ?, ?, ?, ?, ?)",
    "ram": "INSERT INTO ram (name, category, price, capacity, speed) VALUES (?, ?, ?, ?, ?)",
    "gpus": "INSERT INTO gpus (name, category, price, vram) VALUES (?, ?, ?, ?)",
    "power_supplies": "INSERT INTO power_supplies (name, category, price, wattage) VALUES (?, ?, ?, ?)",
    "storage": "INSERT INTO storage (name, category, price, type, capacity) VALUES (?, ?, ?, ?, ?)",
}
# Функция для проверки существования записи
def check_and_insert(table, query, data, unique_field):
    # Создаем запрос для проверки существования записи
    check_query = f"SELECT 1 FROM {table} WHERE {unique_field} = ? LIMIT 1"
    cursor.execute(check_query, (data[0],))  # Предполагаем, что первое поле (например, name) уникально
    if not cursor.fetchone():  # Если запись не найдена
        cursor.execute(query, data)  # Добавляем новую запись
        print(f"Added to {table}: {data[0]}")
    else:
        print(f"Skipped duplicate in {table}: {data[0]}")

# Вставка данных с проверкой
insert_queries = {
    "processors": "INSERT INTO processors (name, category, price, cores, threads, frequency) VALUES (?, ?, ?, ?, ?, ?)",
    "ram": "INSERT INTO ram (name, category, price, capacity, speed) VALUES (?, ?, ?, ?, ?)",
    "gpus": "INSERT INTO gpus (name, category, price, vram) VALUES (?, ?, ?, ?)",
    "power_supplies": "INSERT INTO power_supplies (name, category, price, wattage) VALUES (?, ?, ?, ?)",
    "storage": "INSERT INTO storage (name, category, price, type, capacity) VALUES (?, ?, ?, ?, ?)",
}

# Цикл для добавления данных
for table, query in insert_queries.items():
    for item in components[table]:
        check_and_insert(table, query, item, "name")  # Указываем уникальное поле "name"

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
