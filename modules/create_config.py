def create_config_file():
    # Открыть файл config.py для записи
    with open("config.py", "w") as f:
        # Записать необходимые строки
        f.write("api_id = ''\n")
        f.write("api_hash = ''\n")
        f.write("chats_per_page = 10\n")
        f.write("max_msg = 10\n")
        f.write("key = ''\n")