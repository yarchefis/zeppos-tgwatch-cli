import os
from modules import  create_config
# Асинхронная функция для настройки сессии
async def setup_session():
    # # Проверка наличия файла конфигурации
    # if os.path.exists('config.py'):
    #     # Если файл конфигурации существует, удаляем его
    #     os.remove('config.py')

    # create_config.create_config_file()
    # # Создание нового файла конфигурации
    # with open('config.py', 'w') as f:
    #     f.write("api_id = None\n")
    #     f.write("api_hash = None\n")
    #     f.write("chats_per_page = 10\n")
    #     f.write("max_msg = 10\n")
    #     f.write("key = ''\n")

    # Импорт модуля config
    import config
    
    # Запрос и сохранение api_id и api_hash
    config.api_id = input("Введите API ID: ")
    config.api_hash = input("Введите API Hash: ")
    
        # Читаем содержимое файла
    with open('config.py', 'r') as f:
        lines = f.readlines()

    # Заменяем значения
    lines[0] = f"api_id = '{config.api_id}'\n"
    lines[1] = f"api_hash = '{config.api_hash}'\n"

    # Записываем обновленное содержимое обратно в файл
    with open('config.py', 'w') as f:
        f.writelines(lines)

    # Запрос на ввод номера телефона и кода подтверждения
    
    # Запускаем процесс авторизации
    from telethon import TelegramClient
    async with TelegramClient("session_file", config.api_id, config.api_hash) as client:
        await client.start()
