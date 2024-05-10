# установка(термукс)
копируем и вставляем    
```pkg update -y```    

```apt install git python3 python-pip -y```    

```cd```    

```git clone https://github.com/yarchefis/tgwatch_cli_server```    

```python3 -m venv tg_cli```    

```source tg_cli/bin/activate```    

```pip install telethon prompt_toolkit art```    

```cp -r tgwatch_cli_server/* tg_cli/```    

```echo "#!/bin/bash" > run.sh```    

```echo "cd ~/tg_cli && python main.py" >> run.sh```    

```chmod +x run.sh```
