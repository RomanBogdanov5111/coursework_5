from configparser import ConfigParser

import psycopg2


def config_parser(filename='database.ini', section="postgresql"):

    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))

    return db


def create_database(params: dict, dbname='hh_ru') -> None:
    """
    Создает базу данных hh_ru
    :param dbname: Название базы данных.
    :param params: Словарь с параметрами для подключения к БД
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
        cur.execute(f"CREATE DATABASE {dbname}")
    conn.close()


def execute_sql_script(params: dict, dbname='hh_ru', path_to_sql_script='create_db.sql') -> None:
    """
    Выполняет скрипт из sql файлаю
    :param params: Словарь с параметрами для подключения к БД.
    :param dbname: Имя базы данных, для которой будет выполнен скрипт.
    :param path_to_sql_script: Путь до sql файла со скриптом.
    """
    with open(path_to_sql_script, 'r') as file:
        sql_script = file.read()

    conn = psycopg2.connect(dbname=dbname, **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(sql_script)
    conn.close()


def db_hh_ru_fill_employers_table(cur: psycopg2, employer_data: dict) -> None:
    """
    Заполняет таблицу employers данными.
    :param cur: Курсор модуля psycopg2.
    :param employer_data: Данные, которыми будет заполнена таблица.
    """
    employer_id = employer_data['id']
    employer_name = employer_data['name']
    employer_industry = employer_data['industries'][0]['name']
    employer_city = employer_data['area']['name']
    employer_url = employer_data['site_url']
    employer_open_vacancies = employer_data['open_vacancies']

    cur.execute("""
    INSERT INTO employers (employer_id, 
                           employer_name, 
                           employer_industry, 
                           employer_city, 
                           employer_url, 
                           employer_open_vacancies) 
    VALUES (%s, %s, %s, %s, %s, %s) """, (
                            employer_id,
                            employer_name,
                            employer_industry,
                            employer_city,
                            employer_url,
                            employer_open_vacancies)
                )


def db_hh_ru_fill_vacancies_table(cur: psycopg2, vacancy_data: dict) -> None:
    """
    Заполняет таблицу vacancies данными.
    :param cur: Курсор модуля psycopg2.
    :param vacancy_data: Данные, которыми будет заполнена таблица.
    """

    vacancies = vacancy_data['items']

    for vacancy in vacancies:

        vacancy_id = vacancy['id']
        vacancy_name = vacancy['name']
        vacancy_city = vacancy['area']['name']
        vacancy_url = vacancy['alternate_url']
        # Приведение зарплаты "от" и "до" к одному значению.
        vacancy_salary = None
        if vacancy['salary']:
            if vacancy['salary']["from"] and vacancy['salary']["to"]:
                vacancy_salary = (vacancy['salary']["from"] + vacancy['salary']["to"]) / 2

            elif vacancy['salary']["from"] is not None:
                vacancy_salary = vacancy['salary']["from"]

            elif vacancy['salary']["to"] is not None:
                vacancy_salary = vacancy['salary']["to"]
        published_at = vacancy['published_at']
        employer_id = vacancy['employer']['id']

        cur.execute("""
        INSERT INTO vacancies (vacancy_id, 
                               vacancy_name,
                               vacancy_city,
                               vacancy_url,
                               vacancy_salary,
                               published_at,
                               employer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                               vacancy_id,
                               vacancy_name,
                               vacancy_city,
                               vacancy_url,
                               vacancy_salary,
                               published_at,
                               employer_id)
                    )