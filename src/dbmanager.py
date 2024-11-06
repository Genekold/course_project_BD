import psycopg2


def create_db(db_name: str):
    """
    Функция для создания БД
    :param db_name: Название базы данных
    :return: функция создаст базу данных.
    """

    conn = psycopg2.connect(
        host='localhost',
        database='test',
        user='postgres',
        password='356645',
        port='5433'
    )

    cur = conn.cursor()
