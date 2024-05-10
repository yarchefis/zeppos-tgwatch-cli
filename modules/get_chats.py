# server.py

import http.server
import socketserver
from telethon import TelegramClient
from telethon.tl.types import User, Channel
import json
import config  # Импортируем переменные api_id и api_hash из config.py
import asyncio
# Класс для обработки HTTP-запросов
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/chats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Получаем список чатов
            chats = asyncio.run(get_chats(api_id, api_hash))

            # Отправляем список чатов в формате JSON
            self.wfile.write(chats)
        else:
            # Обработка других запросов
            super().do_GET()

# Функция для запуска HTTP-сервера
def start_http_server():
    PORT = 8000

    # Задаем адрес и порт для сервера
    Handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("HTTP-сервер запущен на порту", PORT)
        # Ожидаем запросов
        httpd.serve_forever()

# Асинхронная функция для получения списка чатов
async def get_chats(api_id, api_hash):
    async with TelegramClient('session_file', api_id, api_hash) as client:
        dialogs = client.iter_dialogs()
        chats = []
        async for dialog in dialogs:  # Заменяем цикл на асинхронный цикл
            entity = dialog.entity
            if isinstance(entity, User) or isinstance(entity, Channel):
                title = None
                if isinstance(entity, User):
                    title = entity.first_name
                    if entity.last_name:
                        title += ' ' + entity.last_name
                elif isinstance(entity, Channel):
                    title = entity.title
                chat = {
                    'id': entity.id,
                    'title': title,
                    'username': entity.username if entity.username else None
                }
                chats.append(chat)
        return json.dumps(chats, ensure_ascii=False, indent=4).encode('utf-8')

# Получаем переменные api_id и api_hash из config.py
api_id = config.api_id
api_hash = config.api_hash

