import os
import psycopg2
from typing import Any

from dotenv import load_dotenv

from src.hh_api import HHCompany

load_dotenv()
list_id_emp = os.getenv('LIST_ID_EMP')


def get_employer_data(employer_ids: str) -> list[dict[str, Any]]:
    """функция получает данные о работодателях и их вакансияях"""

    data = []
    for employer_id in employer_ids.split(','):
        employer = HHCompany()
        employer_info = employer.employer_information(int(employer_id))

        open_vacancies = employer.open_vacancies(int(employer_id))

        data.append({
            'employer': employer_info,
            'vacansy': open_vacancies
        })

    return data


def create_database(database_name: str, params: dict) -> None:
    """Функция создает базу данных создает таблицы 'employers' и 'vacancies'"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (                
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                description TEXT,
                site_url TEXT,
                city VARCHAR,               
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                name VARCHAR,
                url TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                employer_id INTEGER REFERENCES employers (employer_id),                
                requirement TEXT,
                responsibility TEXT,
                contacts TEXT            
               )
           """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Функция сохраняет данные о компаниях и вакансиях в базу данных"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_info = employer['employer']
            cur.execute(
                """
                INSERT INTO employers (name, description, site_url, city, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_info['name'], employer_info['description'], employer_info['site_url'],
                 employer_info['area']['name'], employer_info['open_vacancies'])
            )
            employer_id = cur.fetchone()[0]
            vacancies_data = employer['vacansy']
            for vacancy in vacancies_data:
                salary_from = vacancy['salary']['from'] if vacancy['salary'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary'] else 0
                snippet = vacancy['snippet']

                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url, requirement, 
                    responsibility, contacts)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancy['name'], salary_from, salary_to, vacancy['alternate_url'],
                     snippet['requirement'], snippet['responsibility'], vacancy['contacts'])
                )

    conn.commit()
    conn.close()
