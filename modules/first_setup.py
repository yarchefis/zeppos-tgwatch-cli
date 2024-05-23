import os

# Асинхронная функция для настройки сессии
async def setup_session():
    # Проверка наличия файла конфигурации
    if os.path.exists('config.py'):
        # Если файл конфигурации существует, удаляем его
        os.remove('config.py')

    # Создание нового файла конфигурации
    with open('config.py', 'w') as f:
        f.write("api_id = None\n")
        f.write("api_hash = None\n")
        f.write("chats_per_page = 10\n")
        f.write("max_msg = 10\n")
        f.write("key = ''\n")

    # Импорт модуля config
    import config
    
    # Запрос и сохранение api_id и api_hash
    config.api_id = input("Введите API ID: ")
    config.api_hash = input("Введите API Hash: ")
    
    with open('config.py', 'w') as f:
        f.write(f"api_id = '{config.api_id}'\n")
        f.write(f"api_hash = '{config.api_hash}'\n")
        f.write("chats_per_page = 10\n")
        f.write("max_msg = 10\n")
        f.write("key = ''\n")

    # Запрос на ввод номера телефона и кода подтверждения
    
    # Запускаем процесс авторизации
    from telethon import TelegramClient
    async with TelegramClient("session_file", config.api_id, config.api_hash) as client:
        await client.start()
