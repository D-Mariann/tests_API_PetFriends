import os
from dotenv import load_dotenv # Анализирует файл .env и загружает все найденные переменные в качестве переменных окружения

load_dotenv() # Вызываем этот метод из библиотеки дотенв

valid_email = os.getenv('valid_email') # getenv возвращает переменную окружения
valid_password = os.getenv('valid_password')