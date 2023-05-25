## Курсовая работа SkyPro №5
___
> Привет! :wave:  Данный проект представляет собой парсер данных с площадки [hh.ru](https://hh.ru/).
> Программа создает БД "hh_ru", в ней таблицы с данными Компаний, их открытых вакансий.
> Навигация происходит через консоль путем ввода цифр, соответствующих пунктам меню.
___
**Зависимости проекта:**
+ [python 3.11](https://www.python.org/downloads/release/python-3110/)
+ [requests 2.28.2](https://pypi.org/project/requests/)
+ [psycopg2](https://pypi.org/project/psycopg2/)
+ [tqdm 4.65.0](https://github.com/tqdm/tqdm)

___
**Для запуска необходимо:**

+ Установленный и запущенный в ОС [PostgreSQL](https://www.postgresql.org/).
+ Установленные зависимости проекта.
+ В корень проекта необходимо положить файл `database.ini` с параметрами для подключения к БД.
+ + По умолчанию программа подключается к базе данных 'postgres'

Пример содержания `.ini` файла:
```
[postgresql]
host=localhost
user=postgres
password=12345
port=5432
```
+ Запустить main.py