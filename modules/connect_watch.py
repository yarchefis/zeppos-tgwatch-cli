import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
import re
import os
class MyRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/api/connect/':
            self.server.generated_code = str(random.randint(100000, 999999))
            print("Сгенерированный код:", self.server.generated_code)
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response_data = json.dumps({'status': 1, 'message': 'Код сгенерирован', 'code': self.server.generated_code}, ensure_ascii=False)
            self.wfile.write(response_data.encode('utf-8'))
        elif self.path.startswith('/api/connect/'):
            received_code = self.path.split('/')[-1]
            if self.server.generated_code is None:
                self.send_response(404)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response_data = json.dumps({'status': 0, 'message': 'Код не был сгенерирован'}, ensure_ascii=False)
                self.wfile.write(response_data.encode('utf-8'))
            elif received_code == self.server.generated_code:
                # Чтение тела запроса и извлечение ключа
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                request_data = json.loads(body)
                key = request_data.get('key')

                # Замена значения переменной key в файле config.py
                with open('config.py', 'r') as config_file:
                    config_content = config_file.read()
                config_content = re.sub(r"key\s*=\s*'.*'", f"key = '{key}'", config_content)
                with open('config.py', 'w') as config_file:
                    config_file.write(config_content)

                # Отправка ответа
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response_data = json.dumps({'status': 1, 'message': 'Код верный'}, ensure_ascii=False)
                self.wfile.write(response_data.encode('utf-8'))
                self.server.shutdown()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response_data = json.dumps({'status': 0, 'message': 'Неверный код'}, ensure_ascii=False)
                self.wfile.write(response_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response_data = json.dumps({'status': 0, 'message': 'Неверный путь'}, ensure_ascii=False)
            self.wfile.write(response_data.encode('utf-8'))

class MyHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.generated_code = None

def start_http_server():
    server_address = ('', 9013)
    httpd = MyHTTPServer(server_address, MyRequestHandler)
    print('Сервер запущен на порту 9013.')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Сервер остановлен.')
    os.system("cls" if os.name == "nt" else "clear")

# Пример использования функции
def start_server_connect():
    start_http_server()
