```_____   ____ __        __    _     _____   ____  _   _
|_   _| / ___|\ \      / /   / \   |_   _| / ___|| | | |
  | |  | |  _  \ \ /\ / /   / _ \    | |  | |    | |_| |
  | |  | |_| |  \ V  V /   / ___ \   | |  | |___ |  _  |
  |_|   \____|   \_/\_/   /_/   \_\  |_|   \____||_| |_|
```
# установка(термукс)
копируем и вставляем    
```pkg update -y``` выполнение может остановится, нажимай enter чтобв продолжить

```apt install git python3 python-pip -y```    

```cd```    

```git clone https://github.com/yarchefis/zeppos-tgwatch-cli && python3 -m venv tg_cli && source tg_cli/bin/activate```    

```pip install telethon prompt_toolkit art```    

```cp -r zeppos-tgwatch-cli/* tg_cli/```    

```rm -rf zeppos-tgwatch-cli/```    

```
echo "#\!/bin/bash" > run.sh
echo "source ~/tg_cli/bin/activate" >> run.sh
echo "cd ~/tg_cli && python main.py" >> run.sh  
chmod +x run.sh
```

запускай просто ./run.sh