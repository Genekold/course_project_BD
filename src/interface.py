import os

from dotenv import load_dotenv

from config import config
from src.dbmanager import DBManager
from src.utils import create_database, get_employer_data, save_data_to_database

load_dotenv()
list_id_emp = os.getenv("LIST_ID_EMP")

params = config()


def interface() -> None:
    print(
        """
    Привет пользователь. Сейчас я создам базу данных о компаниях и
    их вакансиях, после этого с ней можно будет работать
    """
    )

    db_name = input("Введите название базы данных для её создания: ")

    print("Идет созание и заполнение базы данных. Ожидайте...")
    data_employers_vacancies = get_employer_data(list_id_emp)
    create_database(db_name, params)
    save_data_to_database(data_employers_vacancies, db_name, params)

    print("Ура! База данных создана!")
    print("Выберите действие:")

    while True:
        message = """
        1. Вывод на экран списка всех компаний и количество вакансий в каждой из них.
        2. Вывод на экран списка всех вакансий с указанием названий компании, вакансии, ссылки на вакансию.
        3. Вывод на экран средней зарплаты по всем вакансиям.
        4. Вывод на экран списка вакансий, зарплата которых выше среднего уровня заработной платы по всем вакансиям.
        5. Вывод на экран списка названий вакансий, в названии которых содержатся переданные слова.
        6. Выход.
    """

        operaton = int(input(message))

        user = DBManager(db_name, params)
        if operaton == 1:
            data = user.get_companies_and_vacancies_count()
            for i in data:
                print(f"Компания - {i[0]} - колличество выкансий - {i[1]}")

        elif operaton == 2:
            data = user.get_all_vacancies()
            print("Это все вакансии которые найдены:")
            for i in data:
                print(f"{i[0]} - {i[1]} - {i[2]}")

        elif operaton == 3:
            data = user.get_avg_salary()
            print(
                f"Средняя зарплата по всем вакансиям (у которых ЗП указана): {data[0][0]}"
            )

        elif operaton == 4:
            data = user.get_vacancies_with_higher_salary()
            for i in data:
                print(f"{i[0]} - {i[1]} - {i[2]}")

        elif operaton == 5:
            keyword = input("Введите слово для поиска: ")
            data = user.get_vacancies_with_keyword(keyword)
            for i in data:
                print(f"{i[0]} - {i[1]} - {i[2]}")

        elif operaton == 6:
            break

        else:
            print("Вы ввели неверный код! Повторите ввод: ")

    user.exit_db()

    print("До скорых встреч!")
