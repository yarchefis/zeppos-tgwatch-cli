import os
import asyncio
import threading
import signal
from modules import first_setup, connect_watch, server
from telethon import TelegramClient
from prompt_toolkit import prompt
from art import *
import git

# Функция для запуска HTTP-сервера в отдельном потоке
def run_http_server():
    try:
        server.start_http_server()
    except Exception as e:
        print("Ошибка при запуске HTTP-сервера:", e)

# Функция для обработки сигнала прерывания
def signal_handler(sig, frame):
    print("\nПрограмма завершена.")
    os._exit(0)

# Функция для проверки обновлений в репозитории Git
def check_for_updates():
    repo = git.Repo(search_parent_directories=True)
    origin = repo.remotes.origin
    origin.fetch()
    if repo.is_dirty():
        print("В вашем репозитории есть изменения, пожалуйста, сохраните их перед обновлением.")
        return False
    else:
        head = repo.head.reference
        if len(list(repo.iter_commits(f"{head}@{{upstream}}..{head}"))) > 0:
            print("В репозитории есть обновления.")
            return True
        else:
            print("Ваш репозиторий обновлен до последней версии.")
            return False

# Асинхронная функция для запуска Telethon
async def main():
    # Устанавливаем обработчик сигнала прерывания
    signal.signal(signal.SIGINT, signal_handler)

    # Проверяем обновления в репозитории Git
    if check_for_updates():
        print("Инструкции по обновлению...")
        return

    # Проверяем, существует ли файл сессии
    if not os.path.exists("session_file.session"):
        await first_setup.setup_session()

    import config
    # Получаем ID после успешной регистрации
    async with TelegramClient("session_file", config.api_id, config.api_hash) as client:
        # Получаем информацию о себе
        os.system("cls" if os.name == "nt" else "clear")
        me = await client.get_me()
        print("Ваш id:", me.id, 'а это значит что все работает отлично.')
        logo = text2art("TGWATCH")
        print(logo)

    # Запускаем HTTP-сервер в отдельном потоке
    http_server_thread = threading.Thread(target=run_http_server)
    http_server_thread.start()

    while True:
        command = await asyncio.to_thread(prompt, "Выберите код команды и введите его:\n1 - подключить/переподключить часы\n8 - сброс\n9 - выход\n")
        if command == '1':
            connect_watch.start_server_connect()
        elif command == "9":
            os.system("cls" if os.name == "nt" else "clear")
            print("Программа завершена.")
            os._exit(0)
        elif command == "8":
            with open('config.py', 'w') as f:
                f.truncate(0)  # Очистка содержимого файла
                f.write("api_id = None\n")
                f.write("api_hash = None\n")
                f.write("chats_per_page = 10\n")
                f.write("max_msg = 10\n")
                f.write("key = ''\n")
            if os.path.exists("session_file.session"):
                os.remove("session_file.session")
            os.system("cls" if os.name == "nt" else "clear")
            print("Сервер был обнулен!")
            print("Введите 9 чтобы завершить программу, а зтем запустите ее еще раз!")

# Запускаем асинхронное приложение
if __name__ == "__main__":
    asyncio.run(main())
