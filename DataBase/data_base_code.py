import sqlite3
import os

# Путь к базе данных
db_path = os.path.join('D:', '\JelezkaBot', 'DataBase', 'PCBuild.db')

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
        )
    """)

    # Таблицы комплектующих
    component_types = [
        "cpus", "motherBoards", "gpus", "rams",
        "powerSupplies", "storages", "computerCases"
    ]
    for component in component_types:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {component} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,  -- Игровые, Для работы, Бюджетные, Графика
                compatibility TEXT, -- Сокет, частоты и другие параметры
                specs TEXT,         -- Характеристики
                price INTEGER       -- Цена
            )
        """)

    # Таблица сборок пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            build_name TEXT,
            cpu TEXT,
            motherboard TEXT,
            gpu TEXT,
            ram TEXT,
            power_supply TEXT,
            storage TEXT,
            computer_case TEXT,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    """)
    conn.commit()
    conn.close()

# Заполнение базы данных тестовыми комплектующими
def fill_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cpus")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        cpus = [
        # Игровые процессоры
        ("Intel Core i5-12400F", "Игровые", "6 ядер, 12 потоков, 2.5-4.4 GHz, сокет LGA1700", 14000),
        ("AMD Ryzen 5 5600X", "Игровые", "6 ядер, 12 потоков, 3.7-4.6 GHz, сокет AM4", 16000),
        ("Intel Core i7-12700KF", "Игровые", "12 ядер, 20 потоков, 3.6-5.0 GHz, сокет LGA1700", 26000),
        ("AMD Ryzen 7 5800X3D", "Игровые", "8 ядер, 16 потоков, 3.4-4.5 GHz, сокет AM4", 29000),
        ("Intel Core i9-12900K", "Игровые", "16 ядер, 24 потока, 3.2-5.2 GHz, сокет LGA1700", 45000),
        ("AMD Ryzen 9 5900X", "Игровые", "12 ядер, 24 потока, 3.7-4.8 GHz, сокет AM4", 37000),
        ("Intel Core i5-13600K", "Игровые", "14 ядер, 20 потоков, 3.5-5.1 GHz, сокет LGA1700", 27000),
        ("AMD Ryzen 5 7600", "Игровые", "6 ядер, 12 потоков, 3.8-5.1 GHz, сокет AM5", 22000),
        ("Intel Core i7-14700K", "Игровые", "20 ядер, 28 потоков, 3.4-5.6 GHz, сокет LGA1700", 40000),
        ("AMD Ryzen 9 7950X3D", "Игровые", "16 ядер, 32 потока, 4.2-5.7 GHz, сокет AM5", 65000),

        # Процессоры для работы
        ("Intel Core i7-12700", "Для работы", "12 ядер, 20 потоков, 2.1-4.9 GHz, сокет LGA1700", 27000),
        ("AMD Ryzen 7 5800X", "Для работы", "8 ядер, 16 потоков, 3.8-4.7 GHz, сокет AM4", 25000),
        ("Intel Core i9-11900", "Для работы", "8 ядер, 16 потоков, 2.5-5.2 GHz, сокет LGA1200", 35000),
        ("AMD Ryzen 9 5950X", "Для работы", "16 ядер, 32 потока, 3.4-4.9 GHz, сокет AM4", 50000),
        ("Intel Core i5-13400", "Для работы", "10 ядер, 16 потоков, 2.5-4.6 GHz, сокет LGA1700", 18000),
        ("AMD Ryzen 5 PRO 5650G", "Для работы", "6 ядер, 12 потоков, 3.9-4.4 GHz, сокет AM4", 21000),
        ("Intel Xeon W-2255", "Для работы", "10 ядер, 20 потоков, 3.7-4.5 GHz, сокет LGA2066", 55000),
        ("AMD Ryzen 7 7700", "Для работы", "8 ядер, 16 потоков, 3.8-5.3 GHz, сокет AM5", 30000),
        ("Intel Core i9-13900", "Для работы", "24 ядра, 32 потока, 2.0-5.6 GHz, сокет LGA1700", 60000),
        ("AMD Ryzen 9 7900", "Для работы", "12 ядер, 24 потока, 3.7-5.4 GHz, сокет AM5", 45000),

        # Бюджетные процессоры
        ("Intel Pentium Gold G6400", "Бюджетные", "2 ядра, 4 потока, 4.0 GHz, сокет LGA1200", 6000),
        ("AMD Athlon 3000G", "Бюджетные", "2 ядра, 4 потока, 3.5 GHz, сокет AM4", 5500),
        ("Intel Celeron G5905", "Бюджетные", "2 ядра, 2 потока, 3.5 GHz, сокет LGA1200", 4000),
        ("AMD Athlon 220GE", "Бюджетные", "2 ядра, 4 потока, 3.4 GHz, сокет AM4", 4500),
        ("Intel Pentium Gold G7400", "Бюджетные", "2 ядра, 4 потока, 3.7 GHz, сокет LGA1700", 7000),
        ("AMD Ryzen 3 3200G", "Бюджетные", "4 ядра, 4 потока, 3.6-4.0 GHz, сокет AM4", 8000),
        ("Intel Core i3-10100F", "Бюджетные", "4 ядра, 8 потоков, 3.6-4.3 GHz, сокет LGA1200", 8000),
        ("AMD Ryzen 3 4100", "Бюджетные", "4 ядра, 8 потоков, 3.8-4.0 GHz, сокет AM4", 10000),
        ("Intel Core i3-12100F", "Бюджетные", "4 ядра, 8 потоков, 3.3-4.3 GHz, сокет LGA1700", 11000),
        ("AMD Ryzen 5 3500", "Бюджетные", "6 ядер, 6 потоков, 3.6-4.1 GHz, сокет AM4", 12000),

        # Процессоры для графики
        ("Intel Xeon W-2245", "Графика", "8 ядер, 16 потоков, 3.9-4.7 GHz, сокет LGA2066", 50000),
        ("AMD Ryzen Threadripper PRO 3975WX", "Графика", "32 ядра, 64 потока, 3.5-4.2 GHz, сокет sWRX8", 240000),
        ("Intel Core i9-13900KS", "Графика", "24 ядра, 32 потока, 3.2-6.0 GHz, сокет LGA1700", 70000),
        ("AMD Ryzen 9 5950X", "Графика", "16 ядер, 32 потока, 3.4-4.9 GHz, сокет AM4", 50000),
        ("Intel Xeon E-2286G", "Графика", "6 ядер, 12 потоков, 4.0-4.9 GHz, сокет LGA1151", 35000),
        ("AMD Ryzen Threadripper 3960X", "Графика", "24 ядра, 48 потоков, 3.8-4.5 GHz, сокет sTRX4", 150000),
        ("Intel Core i9-10980XE", "Графика", "18 ядер, 36 потоков, 3.0-4.8 GHz, сокет LGA2066", 90000),
        ("AMD Ryzen 9 7950X", "Графика", "16 ядер, 32 потока, 4.5-5.7 GHz, сокет AM5", 60000),
        ("Intel Xeon W-3175X", "Графика", "28 ядер, 56 потоков, 3.1-4.3 GHz, сокет LGA3647", 250000),
        ("AMD Ryzen Threadripper PRO 5995WX", "Графика", "64 ядра, 128 потоков, 2.7-4.5 GHz, сокет sWRX8", 650000)
        ]
        cursor.executemany("INSERT INTO cpus (name, category, specs, price) VALUES (?, ?, ?, ?)", cpus)
        print("Процессоры успешно добавлены в базу данных!")
    else:
        print("Данные процессоров уже существуют в базе данных, пропуск вставки.")

    cursor.execute("SELECT COUNT(*) FROM gpus")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        gpus = [
    # Игровые видеокарты
    ("NVIDIA GeForce RTX 3060", "Игровые", "12GB GDDR6, 3584 CUDA-ядер, 1320-1777 MHz", 30000),
    ("AMD Radeon RX 6700 XT", "Игровые", "12GB GDDR6, 2560 потоковых процессоров, 2321-2581 MHz", 37000),
    ("NVIDIA GeForce RTX 3070", "Игровые", "8GB GDDR6, 5888 CUDA-ядер, 1500-1725 MHz", 50000),
    ("AMD Radeon RX 6800", "Игровые", "16GB GDDR6, 3840 потоковых процессоров, 1815-2105 MHz", 52000),
    ("NVIDIA GeForce RTX 3080", "Игровые", "10GB GDDR6X, 8704 CUDA-ядер, 1440-1710 MHz", 65000),
    ("AMD Radeon RX 6950 XT", "Игровые", "16GB GDDR6, 5120 потоковых процессоров, 1890-2310 MHz", 70000),
    ("NVIDIA GeForce RTX 4080", "Игровые", "16GB GDDR6X, 9728 CUDA-ядер, 2205-2505 MHz", 100000),
    ("AMD Radeon RX 7900 XTX", "Игровые", "24GB GDDR6, 6144 потоковых процессоров, 1855-2499 MHz", 95000),
    ("NVIDIA GeForce RTX 4090", "Игровые", "24GB GDDR6X, 16384 CUDA-ядер, 2235-2520 MHz", 140000),
    ("AMD Radeon RX 7600", "Игровые", "8GB GDDR6, 2048 потоковых процессоров, 2250-2655 MHz", 23000),

    # Видеокарты для работы
    ("NVIDIA Quadro RTX 4000", "Для работы", "8GB GDDR6, 2304 CUDA-ядер, 1005-1545 MHz", 80000),
    ("AMD Radeon Pro W6600", "Для работы", "8GB GDDR6, 1792 потоковых процессоров, 1826 MHz", 55000),
    ("NVIDIA RTX A2000", "Для работы", "6GB GDDR6, 3328 CUDA-ядер, 1200 MHz", 45000),
    ("AMD Radeon Pro W5700", "Для работы", "8GB GDDR6, 2304 потоковых процессоров, 1930 MHz", 60000),
    ("NVIDIA Quadro P2200", "Для работы", "5GB GDDR5X, 1280 CUDA-ядер, 1000-1620 MHz", 30000),
    ("AMD Radeon Pro W6800", "Для работы", "32GB GDDR6, 3840 потоковых процессоров, 2321 MHz", 150000),
    ("NVIDIA RTX A5000", "Для работы", "24GB GDDR6, 8192 CUDA-ядер, 1695 MHz", 210000),
    ("AMD Radeon Pro VII", "Для работы", "16GB HBM2, 3840 потоковых процессоров, 1400-1750 MHz", 160000),
    ("NVIDIA Quadro RTX 6000", "Для работы", "24GB GDDR6, 4608 CUDA-ядер, 1440-1770 MHz", 250000),
    ("AMD Radeon Pro WX 8200", "Для работы", "8GB HBM2, 3584 потоковых процессоров, 1200-1500 MHz", 90000),

    # Бюджетные видеокарты
    ("NVIDIA GeForce GTX 1650", "Бюджетные", "4GB GDDR5, 896 CUDA-ядер, 1485-1665 MHz", 14000),
    ("AMD Radeon RX 6400", "Бюджетные", "4GB GDDR6, 768 потоковых процессоров, 1923-2321 MHz", 12000),
    ("NVIDIA GeForce GTX 1050 Ti", "Бюджетные", "4GB GDDR5, 768 CUDA-ядер, 1290-1392 MHz", 10000),
    ("AMD Radeon RX 560", "Бюджетные", "4GB GDDR5, 1024 потоковых процессоров, 1175-1275 MHz", 9000),
    ("NVIDIA GeForce GTX 1630", "Бюджетные", "4GB GDDR6, 512 CUDA-ядер, 1785 MHz", 12000),
    ("AMD Radeon RX 550", "Бюджетные", "4GB GDDR5, 512 потоковых процессоров, 1100-1183 MHz", 8000),
    ("NVIDIA GeForce GT 1030", "Бюджетные", "2GB GDDR5, 384 CUDA-ядер, 1227-1468 MHz", 7000),
    ("AMD Radeon Vega 8", "Бюджетные", "Интегрированная, 8 ядер, 1200 MHz", 5000),
    ("NVIDIA GeForce GTX 950", "Бюджетные", "2GB GDDR5, 768 CUDA-ядер, 1024-1188 MHz", 9000),
    ("AMD Radeon R7 240", "Бюджетные", "2GB GDDR3, 320 потоковых процессоров, 780-900 MHz", 5000),

    # Видеокарты для графики
    ("NVIDIA RTX A6000", "Графика", "48GB GDDR6, 10752 CUDA-ядер, 1860 MHz", 400000),
    ("AMD Radeon Pro WX 9100", "Графика", "16GB HBM2, 4096 потоковых процессоров, 1200-1500 MHz", 200000),
    ("NVIDIA Quadro GV100", "Графика", "32GB HBM2, 5120 CUDA-ядер, 1450 MHz", 500000),
    ("AMD Radeon Instinct MI100", "Графика", "32GB HBM2, 7680 потоковых процессоров, 1500 MHz", 450000),
    ("NVIDIA Quadro P5000", "Графика", "16GB GDDR5X, 2560 CUDA-ядер, 1607-1733 MHz", 200000),
    ("AMD Radeon Pro V340", "Графика", "32GB HBM2, 3584 потоковых процессоров, 1200-1500 MHz", 300000),
    ("NVIDIA Titan RTX", "Графика", "24GB GDDR6, 4608 CUDA-ядер, 1350-1770 MHz", 250000),
    ("AMD Radeon Pro Duo", "Графика", "16GB HBM, 8192 потоковых процессоров, 1000 MHz", 350000),
    ("NVIDIA RTX A4000", "Графика", "16GB GDDR6, 6144 CUDA-ядер, 1560 MHz", 120000),
    ("AMD Radeon Instinct MI200", "Графика", "128GB HBM2e, 14080 потоковых процессоров, 1700 MHz", 800000)
    ]
        cursor.executemany("INSERT INTO gpus (name, category, specs, price) VALUES (?, ?, ?, ?)", gpus)
        print("Видеокарты успешно добавлены в базу данных!")
    else:
        print("Данные видях уже существуют в базе данных, пропуск вставки.")

    cursor.execute("SELECT COUNT(*) FROM motherBoards")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        mother_boards = [
            # Игровые материнские платы
            ("ASUS ROG Strix Z590-E", "Игровые", "LGA 1200, Intel Z590, ATX, 16-phase VRM, Wi-Fi 6", 25000),
            ("MSI MAG B550 TOMAHAWK", "Игровые", "AM4, AMD B550, ATX, Wi-Fi 6, 2.5Gb Ethernet", 15000),
            ("Gigabyte Z690 AORUS Master", "Игровые", "LGA 1700, Intel Z690, ATX, DDR5, Wi-Fi 6E", 35000),
            ("ASRock B450 Steel Legend", "Игровые", "AM4, AMD B450, ATX, 8-phase VRM", 8000),
            ("EVGA Z490 FTW3", "Игровые", "LGA 1200, Intel Z490, ATX, 12-phase VRM, Wi-Fi 6", 22000),
            ("MSI MEG X570 ACE", "Игровые", "AM4, AMD X570, ATX, PCIe 4.0, Wi-Fi 6", 25000),
            ("Gigabyte B550 AORUS PRO", "Игровые", "AM4, AMD B550, ATX, PCIe 4.0", 12000),
            ("ASUS TUF Gaming X570-Pro", "Игровые", "AM4, AMD X570, ATX, PCIe 4.0, Wi-Fi 6", 16000),
            ("ASRock Z490 Taichi", "Игровые", "LGA 1200, Intel Z490, ATX, 12-phase VRM", 22000),
            ("MSI MEG Z590 UNIFY", "Игровые", "LGA 1200, Intel Z590, ATX, DDR4, Wi-Fi 6", 30000),

            # Обычные материнские платы для работы
            ("ASUS Prime B460M-A", "Для работы", "LGA 1200, Intel B460, mATX, 4 DIMM slots", 8000),
            ("Gigabyte B450M DS3H", "Для работы", "AM4, AMD B450, mATX, 4 DIMM slots", 6000),
            ("MSI B450M Mortar Max", "Для работы", "AM4, AMD B450, mATX, 4 DIMM slots", 7000),
            ("ASRock Z590 Pro4", "Для работы", "LGA 1200, Intel Z590, ATX, 6 SATA slots", 12000),
            ("MSI B550M PRO-VDH WIFI", "Для работы", "AM4, AMD B550, mATX, Wi-Fi 5", 10000),
            ("Gigabyte H510M H", "Для работы", "LGA 1200, Intel H510, mATX, 2 DIMM slots", 6000),
            ("ASRock B450M Pro4", "Для работы", "AM4, AMD B450, mATX, 4 DIMM slots", 6500),
            ("MSI MAG B550M Bazooka", "Для работы", "AM4, AMD B550, mATX, PCIe 4.0", 8000),
            ("ASUS TUF B450-Plus Gaming", "Для работы", "AM4, AMD B450, ATX, 4 DIMM slots", 9000),
            ("Gigabyte Z590 UD", "Для работы", "LGA 1200, Intel Z590, ATX, 6 SATA slots", 14000),

            # Бюджетные материнские платы
            ("ASRock A320M-HDV", "Бюджетные", "AM4, AMD A320, mATX, 2 DIMM slots", 3000),
            ("Gigabyte GA-H110M-S2", "Бюджетные", "LGA 1151, Intel H110, mATX, 2 DIMM slots", 3500),
            ("MSI A320M-A PRO", "Бюджетные", "AM4, AMD A320, mATX, 2 DIMM slots", 3500),
            ("ASUS PRIME A320M-K", "Бюджетные", "AM4, AMD A320, mATX, 2 DIMM slots", 4000),
            ("Biostar A320MH", "Бюджетные", "AM4, AMD A320, mATX, 2 DIMM slots", 3000),
            ("MSI H310M PRO-VD", "Бюджетные", "LGA 1151, Intel H310, mATX, 2 DIMM slots", 4000),
            ("Gigabyte H310M-S2H", "Бюджетные", "LGA 1151, Intel H310, mATX, 2 DIMM slots", 4500),
            ("ASRock B460M-HDV", "Бюджетные", "LGA 1200, Intel B460, mATX, 4 DIMM slots", 5000),
            ("MSI H410M-A PRO", "Бюджетные", "LGA 1200, Intel H410, mATX, 2 DIMM slots", 4500),
            ("ASUS PRIME B365M-A", "Бюджетные", "LGA 1151, Intel B365, mATX, 4 DIMM slots", 6000),

            # Материнские платы для графики
            ("ASUS Z490 ROG Strix", "Графика", "LGA 1200, Intel Z490, ATX, 12-phase VRM", 20000),
            ("Gigabyte Z590 AORUS ELITE", "Графика", "LGA 1200, Intel Z590, ATX, 14-phase VRM", 22000),
            ("MSI MPG Z590 Gaming EDGE WIFI", "Графика", "LGA 1200, Intel Z590, ATX, Wi-Fi 6", 23000),
            ("ASRock Z590 Taichi", "Графика", "LGA 1200, Intel Z590, ATX, 14-phase VRM", 24000),
            ("EVGA Z490 Dark", "Графика", "LGA 1200, Intel Z490, ATX, 10-phase VRM", 35000),
            ("Gigabyte AORUS Xtreme Z590", "Графика", "LGA 1200, Intel Z590, ATX, 20-phase VRM", 30000),
            ("MSI Z490 GODLIKE", "Графика", "LGA 1200, Intel Z490, E-ATX, 18-phase VRM", 40000),
            ("ASUS ROG Zenith II Extreme", "Графика", "sTRX4, AMD X399, E-ATX, 16-phase VRM", 50000),
            ("Gigabyte TRX40 AORUS XTREME", "Графика", "sTRX4, AMD TRX40, E-ATX, 16-phase VRM", 60000),
            ("ASRock TRX40 Taichi", "Графика", "sTRX4, AMD TRX40, ATX, 12-phase VRM", 30000)
        ]
        cursor.executemany("INSERT INTO motherBoards (name, category, specs, price) VALUES (?, ?, ?, ?)", mother_boards)
        print("Материнские платы успешно добавлены в базу данных!")
    else:
        print("мать есть")

    cursor.execute("SELECT COUNT(*) FROM rams")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        rams = [
        # Игровая оперативная память
        ("Corsair Vengeance RGB Pro", "Игровые", "16GB (2x8GB), DDR4, 3600MHz, CL18", 6500),
        ("G.Skill Trident Z Neo", "Игровые", "32GB (2x16GB), DDR4, 3200MHz, CL16", 12000),
        ("Kingston FURY Beast", "Игровые", "16GB (2x8GB), DDR5, 5200MHz, CL40", 14000),
        ("TEAMGROUP T-Force Delta RGB", "Игровые", "16GB (2x8GB), DDR4, 3000MHz, CL16", 6000),
        ("HyperX Predator", "Игровые", "16GB (2x8GB), DDR4, 3200MHz, CL16", 7000),
        ("ADATA XPG Spectrix D50", "Игровые", "32GB (2x16GB), DDR4, 3600MHz, CL18", 11000),
        ("Patriot Viper Steel", "Игровые", "16GB (2x8GB), DDR4, 4000MHz, CL19", 9000),
        ("Corsair Dominator Platinum", "Игровые", "32GB (2x16GB), DDR5, 5600MHz, CL40", 18000),
        ("G.Skill Ripjaws V", "Игровые", "16GB (2x8GB), DDR4, 3600MHz, CL16", 7500),
        ("Kingston FURY Renegade", "Игровые", "32GB (2x16GB), DDR5, 6000MHz, CL32", 22000),

        # Оперативная память для работы
        ("Crucial Ballistix", "Для работы", "16GB (2x8GB), DDR4, 2666MHz, CL16", 5000),
        ("Samsung DDR4", "Для работы", "32GB (2x16GB), DDR4, 2400MHz, CL17", 8500),
        ("Kingston ValueRAM", "Для работы", "16GB (2x8GB), DDR4, 2133MHz, CL15", 4000),
        ("ADATA Premier", "Для работы", "16GB (2x8GB), DDR4, 2400MHz, CL16", 4500),
        ("Corsair Vengeance LPX", "Для работы", "8GB (1x8GB), DDR4, 3000MHz, CL16", 2500),
        ("TEAMGROUP Elite", "Для работы", "8GB (1x8GB), DDR4, 2400MHz, CL16", 2200),
        ("Crucial DDR5", "Для работы", "16GB (1x16GB), DDR5, 4800MHz, CL40", 7000),
        ("Samsung DDR5", "Для работы", "32GB (2x16GB), DDR5, 4800MHz, CL40", 15000),
        ("Kingston DDR4", "Для работы", "16GB (2x8GB), DDR4, 3200MHz, CL22", 6000),
        ("Corsair ValueSelect", "Для работы", "8GB (1x8GB), DDR4, 2400MHz, CL17", 2500),

        # Бюджетная оперативная память
        ("Patriot Signature", "Бюджетные", "8GB (1x8GB), DDR4, 2400MHz, CL17", 2000),
        ("ADATA Premier DDR3", "Бюджетные", "4GB (1x4GB), DDR3, 1600MHz, CL11", 1200),
        ("Kingston DDR3", "Бюджетные", "4GB (1x4GB), DDR3, 1333MHz, CL9", 1000),
        ("TEAMGROUP DDR3", "Бюджетные", "8GB (2x4GB), DDR3, 1600MHz, CL11", 1800),
        ("Crucial DDR3", "Бюджетные", "4GB (1x4GB), DDR3, 1333MHz, CL9", 1200),
        ("Samsung DDR4", "Бюджетные", "8GB (1x8GB), DDR4, 2400MHz, CL16", 2300),
        ("ADATA Premier DDR4", "Бюджетные", "8GB (1x8GB), DDR4, 2666MHz, CL19", 2500),
        ("Patriot DDR4", "Бюджетные", "4GB (1x4GB), DDR4, 2133MHz, CL15", 1500),
        ("Corsair ValueSelect DDR3", "Бюджетные", "8GB (1x8GB), DDR3, 1600MHz, CL11", 2000),
        ("Kingston DDR3L", "Бюджетные", "8GB (1x8GB), DDR3L, 1866MHz, CL13", 2500),

        # Оперативная память для графики
        ("Samsung HBM2", "Графика", "16GB, 1024-bit, 2048 MHz", 50000),
        ("Micron GDDR6", "Графика", "8GB, 256-bit, 1750 MHz", 30000),
        ("SK Hynix HBM", "Графика", "4GB, 4096-bit, 1000 MHz", 25000),
        ("Samsung GDDR5", "Графика", "4GB, 256-bit, 1500 MHz", 20000),
        ("Micron HBM2e", "Графика", "16GB, 4096-bit, 2400 MHz", 60000),
        ("SK Hynix GDDR6X", "Графика", "16GB, 384-bit, 1900 MHz", 40000),
        ("Samsung GDDR5X", "Графика", "8GB, 384-bit, 1600 MHz", 35000),
        ("Micron GDDR6", "Графика", "12GB, 320-bit, 1750 MHz", 45000),
        ("SK Hynix HBM3", "Графика", "24GB, 8192-bit, 2400 MHz", 80000),
        ("Samsung HBM2e", "Графика", "32GB, 4096-bit, 2400 MHz", 100000)
        ]
        cursor.executemany("INSERT INTO rams (name, category, specs, price) VALUES (?, ?, ?, ?)", rams)
        print("Оператива успешно добавлены в базу данных!")
    else:
        print("Ram est, ne trogat")

    cursor.execute("SELECT COUNT(*) FROM powerSupplies")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        power_supplies = [
        # Игровые блоки питания
        ("Corsair RM850x", "Игровые", "850W, 80+ Gold, Fully Modular, ATX", 8000),
        ("EVGA SuperNOVA 1000 G5", "Игровые", "1000W, 80+ Gold, Fully Modular, ATX", 14000),
        ("Seasonic Focus GX-850", "Игровые", "850W, 80+ Gold, Fully Modular, ATX", 12000),
        ("Cooler Master MWE Gold 850W", "Игровые", "850W, 80+ Gold, Fully Modular, ATX", 9000),
        ("Thermaltake Toughpower Grand RGB 850W", "Игровые", "850W, 80+ Gold, Fully Modular, RGB, ATX", 11000),
        ("MSI MPG A850GF", "Игровые", "850W, 80+ Gold, Fully Modular, ATX", 10000),
        ("Corsair HX1000i", "Игровые", "1000W, 80+ Platinum, Fully Modular, ATX", 17000),
        ("Be Quiet! Straight Power 11 850W", "Игровые", "850W, 80+ Platinum, Fully Modular, ATX", 15000),
        ("Antec HCG 850W", "Игровые", "850W, 80+ Gold, Fully Modular, ATX", 9500),
        ("Zotac ZT-T1000W-BG", "Игровые", "1000W, 80+ Platinum, Fully Modular, ATX", 16000),

        # Обычные блоки питания для работы
        ("Corsair CV550", "Для работы", "550W, 80+ Bronze, Non-Modular, ATX", 3000),
        ("Cooler Master MWE Bronze 550W", "Для работы", "550W, 80+ Bronze, Non-Modular, ATX", 3500),
        ("Seasonic S12III 650W", "Для работы", "650W, 80+ Bronze, Non-Modular, ATX", 4000),
        ("EVGA 600 W1", "Для работы", "600W, 80+ White, Non-Modular, ATX", 3500),
        ("Thermaltake Smart 500W", "Для работы", "500W, 80+ White, Non-Modular, ATX", 3000),
        ("FSP Fortron Raider 650W", "Для работы", "650W, 80+ Bronze, Non-Modular, ATX", 4000),
        ("Antec VP650P", "Для работы", "650W, 80+ Bronze, Non-Modular, ATX", 4500),
        ("Gigabyte P650B", "Для работы", "650W, 80+ Bronze, Semi-Modular, ATX", 5000),
        ("Corsair CV650", "Для работы", "650W, 80+ Bronze, Non-Modular, ATX", 4500),
        ("Cooler Master Elite V3 600W", "Для работы", "600W, 80+ White, Non-Modular, ATX", 3500),

        # Бюджетные блоки питания
        ("Aerocool VX-500", "Бюджетные", "500W, 80+ White, Non-Modular, ATX", 2500),
        ("DeepCool DQ500", "Бюджетные", "500W, 80+ Bronze, Semi-Modular, ATX", 3500),
        ("Chieftec Proton BPS-600S", "Бюджетные", "600W, 80+ Bronze, Semi-Modular, ATX", 4000),
        ("Sirius PSU 400W", "Бюджетные", "400W, 80+ White, Non-Modular, ATX", 2500),
        ("LC-Power LC600H-12", "Бюджетные", "600W, 80+ White, Non-Modular, ATX", 3000),
        ("Cougar VTE 500W", "Бюджетные", "500W, 80+ Bronze, Non-Modular, ATX", 3500),
        ("MSI MAG A550BN", "Бюджетные", "550W, 80+ Bronze, Non-Modular, ATX", 3500),
        ("InWin GreenMe 550W", "Бюджетные", "550W, 80+ Bronze, Non-Modular, ATX", 3500),
        ("Thermaltake Litepower 450W", "Бюджетные", "450W, 80+ White, Non-Modular, ATX", 2500),
        ("Gigabyte GP-P450B", "Бюджетные", "450W, 80+ Bronze, Non-Modular, ATX", 3000),

        # Блоки питания для графики
        ("Corsair RM850x", "Графика", "850W, 80+ Gold, Fully Modular, ATX", 8000),
        ("EVGA SuperNOVA 1200 G3", "Графика", "1200W, 80+ Platinum, Fully Modular, ATX", 18000),
        ("Seasonic Prime 1000W", "Графика", "1000W, 80+ Platinum, Fully Modular, ATX", 16000),
        ("Cooler Master MWE Gold 850W", "Графика", "850W, 80+ Gold, Fully Modular, ATX", 9000),
        ("MSI MPG A850GF", "Графика", "850W, 80+ Gold, Fully Modular, ATX", 10000),
        ("Antec Earthwatts Gold Pro 850W", "Графика", "850W, 80+ Gold, Fully Modular, ATX", 12000),
        ("FSP Hydro G Pro 750W", "Графика", "750W, 80+ Gold, Fully Modular, ATX", 10000),
        ("Zotac ZT-T1200W-BG", "Графика", "1200W, 80+ Gold, Fully Modular, ATX", 16000),
        ("Corsair HX1200i", "Графика", "1200W, 80+ Platinum, Fully Modular, ATX", 20000),
        ("Be Quiet! Dark Power Pro 12 1200W", "Графика", "1200W, 80+ Titanium, Fully Modular, ATX", 25000)
    ]
        cursor.executemany("INSERT INTO powerSupplies (name, category, specs, price) VALUES (?, ?, ?, ?)", power_supplies)
        print("Блоки питания успешно добавлены в базу данных!")
    else:
        print("bloki pitaniya est")

    cursor.execute("SELECT COUNT(*) FROM storages")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        storages = [
        # SSD для игр
        ("Samsung 970 EVO Plus 1TB", "Игровые", "1TB, M.2 NVMe, 3500/3300 MB/s", 10500),
        ("WD Black SN850 1TB", "Игровые", "1TB, M.2 NVMe, 7000/5300 MB/s", 12000),
        ("Kingston A2000 1TB", "Игровые", "1TB, M.2 NVMe, 2200/2000 MB/s", 7000),
        ("Corsair MP600 1TB", "Игровые", "1TB, M.2 NVMe, 4950/4250 MB/s", 11500),
        ("Crucial P5 1TB", "Игровые", "1TB, M.2 NVMe, 3400/3000 MB/s", 8500),
        ("Seagate FireCuda 520 1TB", "Игровые", "1TB, M.2 NVMe, 5000/4400 MB/s", 12500),
        ("ADATA XPG Gammix S5 1TB", "Игровые", "1TB, M.2 NVMe, 2100/1500 MB/s", 6500),
        ("PNY XLR8 CS3030 1TB", "Игровые", "1TB, M.2 NVMe, 3500/2000 MB/s", 8500),
        ("Sabrent Rocket 1TB", "Игровые", "1TB, M.2 NVMe, 5000/4000 MB/s", 9500),
        ("TeamGroup T-Force Cardea Zero Z 1TB", "Игровые", "1TB, M.2 NVMe, 3300/3000 MB/s", 8000),

        # SSD для работы
        ("Samsung 860 EVO 500GB", "Для работы", "500GB, SATA III, 550/520 MB/s", 5000),
        ("Crucial MX500 500GB", "Для работы", "500GB, SATA III, 560/510 MB/s", 4500),
        ("Western Digital Blue 500GB", "Для работы", "500GB, SATA III, 560/530 MB/s", 4800),
        ("SanDisk Ultra 3D 500GB", "Для работы", "500GB, SATA III, 560/530 MB/s", 4700),
        ("Kingston A400 480GB", "Для работы", "480GB, SATA III, 500/450 MB/s", 3500),
        ("Intel 660p 512GB", "Для работы", "512GB, M.2 NVMe, 1800/1800 MB/s", 5500),
        ("ADATA Ultimate SU800 512GB", "Для работы", "512GB, SATA III, 560/520 MB/s", 4200),
        ("Seagate Barracuda 120 512GB", "Для работы", "512GB, SATA III, 560/540 MB/s", 4600),
        ("Transcend 370S 512GB", "Для работы", "512GB, SATA III, 550/450 MB/s", 4300),
        ("Patriot Burst 480GB", "Для работы", "480GB, SATA III, 545/450 MB/s", 3700),

        # Бюджетные SSD
        ("Kingston A400 240GB", "Бюджетные", "240GB, SATA III, 500/450 MB/s", 2500),
        ("Western Digital Green 240GB", "Бюджетные", "240GB, SATA III, 545/435 MB/s", 2200),
        ("ADATA SU630 240GB", "Бюджетные", "240GB, SATA III, 520/450 MB/s", 2300),
        ("Crucial BX500 240GB", "Бюджетные", "240GB, SATA III, 540/500 MB/s", 2500),
        ("SanDisk SSD PLUS 240GB", "Бюджетные", "240GB, SATA III, 535/445 MB/s", 2200),
        ("TeamGroup GX2 240GB", "Бюджетные", "240GB, SATA III, 530/440 MB/s", 2100),
        ("Patriot P3 256GB", "Бюджетные", "256GB, M.2 NVMe, 1700/1100 MB/s", 3000),
        ("PNY CS900 240GB", "Бюджетные", "240GB, SATA III, 500/400 MB/s", 2300),
        ("Transcend SSD220S 240GB", "Бюджетные", "240GB, SATA III, 550/450 MB/s", 2200),
        ("Silicon Power A55 240GB", "Бюджетные", "240GB, SATA III, 550/500 MB/s", 2200),

        # Жесткие диски для игр и работы
        ("Seagate BarraCuda 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 6500),
        ("Western Digital Blue 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 6200),
        ("Toshiba P300 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 5900),
        ("Seagate IronWolf 2TB", "Игровые", "2TB, 7200 RPM, NAS, SATA III", 7500),
        ("Hitachi Deskstar 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 6000),
        ("Western Digital Black 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 8000),
        ("Toshiba X300 2TB", "Игровые", "2TB, 7200 RPM, SATA III", 7400),
        ("Seagate FireCuda 2TB", "Игровые", "2TB, 7200 RPM, Hybrid, SATA III", 8500),
        ("Samsung 870 QVO 2TB", "Игровые", "2TB, SATA III, 550/520 MB/s", 10500),
        ("Crucial P2 1TB", "Игровые", "1TB, M.2 NVMe, 2400/1800 MB/s", 5500),

        # Жесткие диски для работы
        ("Western Digital Red 4TB", "Для работы", "4TB, 5400 RPM, NAS, SATA III", 12000),
        ("Seagate Skyhawk 4TB", "Для работы", "4TB, 5900 RPM, Surveillance, SATA III", 13000),
        ("Toshiba N300 4TB", "Для работы", "4TB, 7200 RPM, NAS, SATA III", 14000),
        ("Hitachi Ultrastar 4TB", "Для работы", "4TB, 7200 RPM, SATA III", 13500),
        ("Seagate Exos 4TB", "Для работы", "4TB, 7200 RPM, SATA III", 14500),
        ("Western Digital Red Pro 4TB", "Для работы", "4TB, 7200 RPM, NAS, SATA III", 15000),
        ("HGST Deskstar 4TB", "Для работы", "4TB, 7200 RPM, SATA III", 13000),
        ("Seagate IronWolf 4TB", "Для работы", "4TB, 7200 RPM, NAS, SATA III", 14500),
        ("Toshiba X300 4TB", "Для работы", "4TB, 7200 RPM, SATA III", 13500),
        ("Western Digital Blue 1TB", "Для работы", "1TB, 7200 RPM, SATA III", 5000)
    ]
        cursor.executemany("INSERT INTO storages (name, category, specs, price) VALUES (?, ?, ?, ?)", storages)
        print("Жесткие диски и SSD успешно добавлены в базу данных!")
    else:
        print("ssd yest")

    cursor.execute("SELECT COUNT(*) FROM computerCases")
    cpu_count = cursor.fetchone()[0]
    if cpu_count == 0:
        computer_cases = [
            # Игровые корпуса
            ("Corsair iCUE 4000X RGB", "Игровые", "Mid Tower, ATX, 3x RGB вентиляторов", 8500),
            ("NZXT H510 Elite", "Игровые", "Mid Tower, ATX, Стеклянные панели, 2x RGB вентиляторов", 10500),
            ("Fractal Design Meshify C", "Игровые", "Mid Tower, ATX, Меш-сетка, 2x вентиляторов", 7000),
            ("Cooler Master MasterBox Q300L", "Игровые", "Compact, ATX, Модульная конструкция, 2x вентиляторов", 4500),
            ("Phanteks Eclipse P400A", "Игровые", "Mid Tower, ATX, Стеклянные панели, 3x вентиляторов", 7500),
            ("Be Quiet! Dark Base Pro 900", "Игровые", "Full Tower, ATX, 3x вентиляторов, Шумоизоляция", 14500),
            ("Lian Li PC-011 Dynamic", "Игровые", "Mid Tower, ATX, 3x стеклянные панели, 2x вентиляторов", 9500),
            ("Thermaltake View 71 RGB", "Игровые", "Full Tower, ATX, 4x вентиляторов RGB", 11500),
            ("Corsair 5000X RGB", "Игровые", "Mid Tower, ATX, 3x вентиляторов RGB, стеклянные панели", 12000),
            ("MSI MPG GUNGNIR 110R", "Игровые", "Mid Tower, ATX, Стеклянные панели, 4x вентиляторов RGB", 11500),

            # Корпуса для работы
            ("Fractal Design Define R5", "Для работы", "Mid Tower, ATX, Шумоизоляция, 2x вентиляторов", 8500),
            ("Cooler Master Silencio S600", "Для работы", "Mid Tower, ATX, Шумоизоляция, 1x вентилятор", 7500),
            ("Be Quiet! Silent Base 601", "Для работы", "Mid Tower, ATX, Шумоизоляция, 2x вентиляторов", 10500),
            ("NZXT H510", "Для работы", "Mid Tower, ATX, Стеклянная панель, 1x вентилятор", 6500),
            ("Corsair Carbide 275R", "Для работы", "Mid Tower, ATX, Минималистичный дизайн, 2x вентиляторов", 5500),
            ("Thermaltake Core V21", "Для работы", "Cube, Micro ATX, 2x вентиляторов", 4000),
            ("Phanteks P400A", "Для работы", "Mid Tower, ATX, Хорошая вентиляция, 2x вентиляторов", 6500),
            ("Cooler Master MasterBox NR600", "Для работы", "Mid Tower, ATX, Просторный, 2x вентиляторов", 6500),
            ("Lian Li PC-7HX", "Для работы", "Mid Tower, ATX, Стеклянная панель, 2x вентиляторов", 7500),
            ("SilverStone SST-PS15", "Для работы", "Mid Tower, ATX, 2x вентиляторов", 4000),

            # Бюджетные корпуса
            ("Deepcool Matrexx 30", "Бюджетные", "Mid Tower, ATX, 1x вентилятор", 2500),
            ("Aerocool Cylon", "Бюджетные", "Mid Tower, ATX, 1x вентилятор RGB", 3000),
            ("Thermaltake Versa H15", "Бюджетные", "Mini Tower, Micro ATX, 1x вентилятор", 2000),
            ("Zalman T4", "Бюджетные", "Mid Tower, ATX, 1x вентилятор", 2000),
            ("Cooler Master Elite 110", "Бюджетные", "Mini Tower, Mini-ITX, 1x вентилятор", 2200),
            ("Antec VSK-3000", "Бюджетные", "Mid Tower, ATX, 1x вентилятор", 2200),
            ("Corsair Spec-01", "Бюджетные", "Mid Tower, ATX, 2x вентиляторов", 3200),
            ("Fractal Design Focus G", "Бюджетные", "Mid Tower, ATX, 2x вентиляторов", 3500),
            ("MSI MAG VAMPIRIC 100R", "Бюджетные", "Mid Tower, ATX, 1x вентилятор RGB", 3000),
            ("Deepcool DSH 2", "Бюджетные", "Mini Tower, Micro ATX, 1x вентилятор", 1800),

            # Корпуса для графики
            ("SilverStone LD03", "Графика", "Cube, ITX, Стеклянная панель, 2x вентиляторов", 9500),
            ("NZXT H200i", "Графика", "Mini Tower, ITX, Стеклянная панель, 1x вентилятор", 8500),
            ("Cooler Master MasterBox Q300P", "Графика", "Mini Tower, ITX, Модульный дизайн, 2x вентиляторов", 4500),
            ("Thermaltake Core V1", "Графика", "Mini Tower, ITX, 1x вентилятор", 3000),
            ("Fractal Design Node 202", "Графика", "Mini ITX, Компактный корпус, 1x вентилятор", 7000),
            ("Lian Li TU150", "Графика", "Mini Tower, ITX, Стеклянная панель, 2x вентиляторов", 10000),
            ("Cooler Master Elite 110", "Графика", "Mini Tower, ITX, 1x вентилятор", 2200),
            ("InWin Chopin", "Графика", "Mini Tower, ITX, Компактный, 1x вентилятор", 3000),
            ("Corsair 280X", "Графика", "Cube, Micro ATX, Стеклянные панели, 2x вентиляторов", 9500),
            ("SilverStone RVZ03", "Графика", "Mini Tower, ITX, Стеклянная панель, 2x вентиляторов", 8500),

            # Ультракомпактные корпуса
            ("Cooler Master MasterBox Q300L", "Ультракомпактные", "Mini Tower, Micro ATX, Модульный дизайн, 2x вентиляторов", 5000),
            ("Thermaltake Level 20 VT", "Ультракомпактные", "Mini Tower, ITX, Модульный дизайн, 1x вентилятор", 8000),
            ("Fractal Design Define Nano S", "Ультракомпактные", "Mini Tower, ITX, Шумоизоляция, 2x вентиляторов", 6000),
            ("Cooler Master Elite 110", "Ультракомпактные", "Mini Tower, ITX, 1x вентилятор", 2200),
            ("Lian Li PC-Q21", "Ультракомпактные", "Mini Tower, ITX, Стеклянная панель, 1x вентилятор", 5500),
            ("Antec ISK-110", "Ультракомпактные", "Mini Tower, ITX, Компактный, 1x вентилятор", 3000),
            ("Zalman Z3", "Ультракомпактные", "Mini Tower, ITX, 1x вентилятор", 3500),
            ("Thermaltake Core V1", "Ультракомпактные", "Mini Tower, ITX, 1x вентилятор", 2500),
            ("SilverStone SST-SJ08", "Ультракомпактные", "Mini Tower, ITX, Компактный, 1x вентилятор", 4500),
            ("InWin 301", "Ультракомпактные", "Mid Tower, ATX, Стеклянная панель, 2x вентиляторов", 6500)
        ]
        cursor.executemany("INSERT INTO computerCases (name, category, specs, price) VALUES (?, ?, ?, ?)", computer_cases)
        print("Корпуса успешно добавлены в базу данных!")
    else:
        print("keysi yest")

    conn.commit()
    conn.close()

# Выполнение инициализации и заполнения базы данных
init_db()
fill_db()