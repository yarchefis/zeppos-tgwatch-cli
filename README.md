```
 _____   ____ __        __    _     _____   ____  _   _
|_   _| / ___|\ \      / /   / \   |_   _| / ___|| | | |
  | |  | |  _  \ \ /\ / /   / _ \    | |  | |    | |_| |
  | |  | |_| |  \ V  V /   / ___ \   | |  | |___ |  _  |
  |_|   \____|   \_/\_/   /_/   \_\  |_|   \____||_| |_|
```
# установка(термукс)
копируем и вставляем    
```pkg update -y``` выполнение может остановится, нажимай enter чтобв продолжить


```apt install git python3 python-pip -y && git clone https://github.com/yarchefis/zeppos-tgwatch-cli && pip install telethon prompt_toolkit art --break-system-packages``` 

```
echo "#\!/bin/bash" > run.sh
echo "cd ~/zeppos-tgwatch-cli && python main.py" >> run.sh  
chmod +x run.sh
```

запускай просто ./run.sh