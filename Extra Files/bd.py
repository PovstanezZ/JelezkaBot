import sqlite3
import os

# Путь к базе данных
db_path = os.path.join('D:', 'JelezkaBot', 'DataBase', 'PCBuild.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Инициализация базы данных
# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
telegram_id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT)
""")

# Таблицы комплектующих
component_types = [
    "cpus", "mother_boards", "gpus", "rams",
    "power_supplies", "storages", "computer_case"
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

    cursor.executemany("INSERT INTO mother_boards (name, category, specs, price) VALUES (?, ?, ?, ?)", mother_boards)
    print("Материнские платы успешно добавлены в базу данных!")

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

    cursor.executemany("INSERT INTO power_supplies (name, category, specs, price) VALUES (?, ?, ?, ?)", power_supplies)
    print("Блоки питания успешно добавлены в базу данных!")

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
        (
            "Cooler Master MasterBox Q300L", "Ультракомпактные",
            "Mini Tower, Micro ATX, Модульный дизайн, 2x вентиляторов",
            5000),
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

    cursor.executemany("INSERT INTO computer_case (name, category, specs, price) VALUES (?, ?, ?, ?)", computer_cases)
    print("Корпуса успешно добавлены в базу данных!")

    conn.commit()
    conn.close()


fill_db()
