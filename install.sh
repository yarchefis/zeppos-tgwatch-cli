#!/bin/bash

# Обновляем пакеты
pkg update -y

# Устанавливаем Git, Python 3 и pip
apt install git python3 python-pip -y

# Переходим в домашнюю директорию
cd

# Клонируем репозиторий с сервером tgwatch_cli
git clone https://github.com/yarchefis/tgwatch_cli_server

# Создаем виртуальное окружение
python3 -m venv tg_cli

# Активируем виртуальное окружение
source tg_cli/bin/activate

# Устанавливаем необходимые пакеты через pip
pip install telethon prompt_toolkit art

# Перемещаем файлы из tgwatch_cli_server в tg_cli
cp -r tgwatch_cli_server/* tg_cli/

echo "#!/bin/bash" > run.sh
echo "cd ~/tg_cli && python main.py" >> run.sh

# Даем права на выполнение созданному скрипту
chmod +x run.sh
