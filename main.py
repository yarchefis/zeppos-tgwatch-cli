import os
import sys
import asyncio
import threading
import signal
from modules import first_setup, connect_watch, server, create_config
from telethon import TelegramClient
from prompt_toolkit import prompt
from art import *

def restart_program():
    server.stop_http_server()
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Функция для запуска HTTP-сервера в отдельном потоке
def run_http_server():
    try:
        server.start_http_server()
    except Exception as e:
        print("Упс, ошибка! Давай перезапустим программу: нажми 9 а потом enter и запусти еще раз. Если повторится эта же ошибка попробуй перезапустить телефон", e)

# Функция для обработки сигнала прерывания
def signal_handler(sig, frame):
    print("\nПрограмма завершена.")
    os._exit(0)


# Асинхронная функция для запуска Telethon
async def main():
    # Устанавливаем обработчик сигнала прерывания
    signal.signal(signal.SIGINT, signal_handler)

    # Проверяем, существует ли файл сессии
    if not os.path.exists("session_file.session"):
        await first_setup.setup_session()

    # Проверяем, существует ли файл конфигурации
    if not os.path.exists("config.py"):
        create_config.create_config_file()

    # Импортируем конфигурацию после того, как убедились, что файл существует
    import config

    # Получаем ID после успешной регистрации
    async with TelegramClient("session_file", config.api_id, config.api_hash) as client:
        # Получаем информацию о себе
        os.system("cls" if os.name == "nt" else "clear")
        me = await client.get_me()
        logo = text2art("TgWatch")
        print(logo)
        print("Ваш id:", me.id)
        print('Если вы видите цифры значит вы все успешно настроили.')

    # Запускаем HTTP-сервер в отдельном потоке
    http_server_thread = threading.Thread(target=run_http_server)
    http_server_thread.start()
    menu_text = (
        "------------------\n"
        "  Меню программы\n"
        "------------------\n"
        "Пожалуйста, выберите одну из следующих опций и введите соответствующий номер команды:\n\n"
        "1 - Подключить/переподключить часы\n"
        "2 - Изменить значения конфигурации\n"
        "8 - Сброс\n"
        "9 - Выход\n"
        "Введите номер команды: "
    )
    while True:
        command = await asyncio.to_thread(input, menu_text)
        # command = await asyncio.to_thread(prompt, "Выберите код команды и введите его:\n1 - подключить/переподключить часы\n2 - изменить значения конфига\n8 - сброс\n9 - выход\n")
        if command == '1':
            connect_watch.start_server_connect()
        elif command == "9":
            os.system("cls" if os.name == "nt" else "clear")
            print("Программа завершена.")
            os._exit(0)
        elif command == "8":
            create_config.create_config_file()

            if os.path.exists("session_file.session"):
                os.remove("session_file.session")
            os.system("cls" if os.name == "nt" else "clear")
            print("Все файлы были стерты до завода.")
            print("Введите 9 и enter чтобы завершить программу, а зтем запустите ее еще раз!")
            restart_program()
        elif command == "2":
            chats_per_page = input("Введите кол-во чатов на одной странице (для mi band 7 оптимальное значение 10): ")
            max_msg = input("Введите кол-во сообщений (для mi band 7 оптимальное значение 10): ")

            # Читаем старые значения из файла
            with open('config.py', 'r') as f:
                lines = f.readlines()

            # Заменяем старые значения новыми
            lines[2] = f"chats_per_page = {chats_per_page}\n"
            lines[3] = f"max_msg = {max_msg}\n"

            # Записываем обновленные значения в файл конфигурации
            with open('config.py', 'w') as f:
                f.writelines(lines)
            restart_program()
        elif command == "100":
            keykey = input("Укажи ключ потом перезапусти приложение!: ")

            with open('config.py', 'r') as f:
                lines = f.readlines()

            # Заменяем старые значения новыми
            lines[4] = f"key = '{keykey}'\n"
            with open('config.py', 'w') as f:
                f.writelines(lines)



if __name__ == "__main__":
    asyncio.run(main())