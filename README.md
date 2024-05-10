# установка(термукс)
копируем и вставляем    
```pkg update -y``` нажимаем ентер если выполнение останавливается    

```apt install git python3 python-pip -y```    

```cd```    

```git clone https://github.com/yarchefis/zeppos-tgwatch-cli```    

```python3 -m venv tg_cli```    

```source tg_cli/bin/activate```    

```pip install telethon prompt_toolkit art```    

```cp -r zeppos-tgwatch-cli/* tg_cli/```    


```echo "#\!/bin/bash" > run.sh
echo "source ~/tg_cli/bin/activate" >> run.sh
echo "cd ~/tg_cli && python main.py" >> run.sh  
chmod +x run.sh```
