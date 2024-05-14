import http.server
import socketserver
from telethon import TelegramClient
from telethon.tl.types import User, Channel
import json
import config  # Импортируем переменные api_id, api_hash и key из config.py
import asyncio
from urllib.parse import urlparse, parse_qs
import urllib.parse

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Обрабатываем запрос к корневому URL
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello, world!')
        else:
            # Если URL не корневой, возвращаем 404
            self.send_error(404, "Not Found")
            
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path_components = parsed_url.path.split('/')

        if self.path.startswith('/api/chats'):
            # Проверяем наличие тела запроса
            if 'Content-Length' not in self.headers:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'missing body'}).encode('utf-8'))
                return

            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'empty body'}).encode('utf-8'))
                return

            # Получаем данные из тела запроса
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)

            # Проверяем, есть ли в теле запроса ключ, соответствующий ключу из конфига
            if 'key' not in request_data or request_data['key'] != config.key:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'error key'}).encode('utf-8'))
                return

            # Если ключ совпадает, продолжаем обработку запроса
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Извлекаем параметр страницы из запроса, если он есть
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            page = int(query_params.get('page', [1])[0])

            # Получаем список чатов для указанной страницы
            chats = asyncio.run(get_chats(api_id, api_hash, page, config.chats_per_page))

            # Отправляем список чатов в формате JSON
            self.wfile.write(chats)

        elif self.path.startswith('/api/chat/'):
            # Проверяем наличие тела запроса
            if 'Content-Length' not in self.headers:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'missing body'}).encode('utf-8'))
                return

            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'empty body'}).encode('utf-8'))
                return

            # Получаем данные из тела запроса
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)

            # Проверяем, есть ли в теле запроса ключ, соответствующий ключу из конфига
            if 'key' not in request_data or request_data['key'] != config.key:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'error key'}).encode('utf-8'))
                return

            # Если ключ совпадает, продолжаем обработку запроса
            components = self.path.split('/')
            chat_id = components[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            chat = asyncio.run(get_chat(api_id, api_hash, chat_id, config.max_msg))

            # Send the chat data in JSON format
            self.wfile.write(chat)

        
        elif self.path.startswith('/api/chatformsg/'):
            # Проверяем наличие тела запроса
            if 'Content-Length' not in self.headers:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'missing body'}).encode('utf-8'))
                return

            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'empty body'}).encode('utf-8'))
                return

            # Получаем данные из тела запроса
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)

            # Проверяем, есть ли в теле запроса ключ, соответствующий ключу из конфига
            if 'key' not in request_data or request_data['key'] != config.key:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'error key'}).encode('utf-8'))
                return

            # Если ключ совпадает, продолжаем обработку запроса
            components = self.path.split('/')
            chat_id = components[-2]
            message_text_encoded = components[-1]
            message_text = urllib.parse.unquote(message_text_encoded.replace('_', ' '))
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Отправляем сообщение в указанный чат
            asyncio.run(send_message(api_id, api_hash, chat_id, message_text))
            self.wfile.write(json.dumps({'status': 1, 'message': 'well done'}).encode('utf-8'))
        
        elif self.path.startswith('/api/getme'):
            if 'Content-Length' not in self.headers:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'missing body'}).encode('utf-8'))
                return

            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'empty body'}).encode('utf-8'))
                return

            # Получаем данные из тела запроса
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)

            # Проверяем, есть ли в теле запроса ключ, соответствующий ключу из конфига
            if 'key' not in request_data or request_data['key'] != config.key:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 0, 'message': 'error key'}).encode('utf-8'))
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            user_info = asyncio.run(get_me(api_id, api_hash))
            self.wfile.write(json.dumps(user_info, ensure_ascii=False, indent=4).encode('utf-8'))


        else:
            super().do_POST()


async def get_me(api_id, api_hash):
    async with TelegramClient('session_file', api_id, api_hash) as client:
        me = await client.get_me()
        return {
            'id': me.id,
            'first_name': me.first_name,
            'last_name': me.last_name
        }



async def send_message(api_id, api_hash, chat_id, message_text):
    async with TelegramClient('session_file', api_id, api_hash) as client:
        await client.send_message(int(chat_id), message_text)


async def get_chats(api_id, api_hash, page, chats_per_page):
    async with TelegramClient('session_file', api_id, api_hash) as client:
        dialogs = client.iter_dialogs()
        chats = []
        start_index = (page - 1) * chats_per_page
        end_index = start_index + chats_per_page
        async for dialog in dialogs:
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
        return json.dumps(chats[start_index:end_index], ensure_ascii=False, indent=4).encode('utf-8')


async def get_chat(api_id, api_hash, chat_id, max_msg):
    async with TelegramClient('session_file', api_id, api_hash) as client:
        messages = await client.get_messages(int(chat_id), limit=max_msg)
        me = await client.get_me()
        messages_list = []
        for message in messages:
            sender_name = None
            if message.sender:
                if isinstance(message.sender, User):
                    sender_name = message.sender.first_name
                    if not sender_name:
                        sender_name = message.sender.username
                elif isinstance(message.sender, Channel):
                    sender_name = message.sender.title  # Для каналов используем атрибут title
            you = True if message.sender_id == me.id else False
            message_text = message.text if message.text else ''  # Проверяем наличие текста
            message_data = {
                'id': message.id,
                'text': message_text,
                'sender_id': message.sender_id,
                'sender_name': sender_name,
                'date': message.date.timestamp(),
                'you': you
            }
            if message.media is not None:
                if hasattr(message.media, 'photo'):
                    message_data['text'] += "\n(ФОТО)"
                elif hasattr(message.media, 'document'):
                    if message.media.document.mime_type.startswith('audio'):
                        message_data['text'] += "\n(ГОЛОСОВОЕ СООБЩЕНИЕ)"
                    elif message.media.document.mime_type.startswith('video'):
                        message_data['text'] += "\n(ВИДЕО)"
                    elif message.media.document.mime_type.startswith('image'):
                        message_data['text'] += "\n(ИЗОБРАЖЕНИЕ или СТИКЕР)"
                    elif message.media.document.mime_type.startswith('application') or message.media.document.mime_type.startswith('text'):
                        message_data['text'] += "\n(ФАЙЛ)"
                elif hasattr(message.media, 'sticker'):
                    message_data['text'] += "\n(СТИКЕР)"
            messages_list.append(message_data)
        return json.dumps(messages_list, ensure_ascii=False, indent=4).encode('utf-8')



def start_http_server():
    PORT = 8007

    # Задаем адрес и порт для сервера
    Handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("HTTP-сервер запущен на порту", PORT)
        # Ожидаем запросов
        httpd.serve_forever()

# Получаем переменные api_id, api_hash и key из config.py
api_id = config.api_id
api_hash = config.api_hash
