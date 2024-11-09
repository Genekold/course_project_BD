import psycopg2


class DBManager:
    """
    Класс для работы с базой данных
    """

    def __init__(self, dbname, params):
        self.__dbname = dbname
        self.__params = params
        self.conn = psycopg2.connect(dbname=self.__dbname, **self.__params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        print("1")

        self.cur.execute(
            """
            SELECT employers.name_employers, COUNT(vacancies.name_vacancies)
            FROM employers INNER JOIN vacancies
            USING (employer_id)
            GROUP BY employers.name_employers
        """
        )
        data = self.cur.fetchall()

        return data

    def get_all_vacancies(self) -> list[tuple]:
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cur.execute(
            """
            SELECT employers.name_employers, vacancies.name_vacancies, vacancies.vacancies_url
            FROM vacancies INNER JOIN employers
            USING (employer_id)
        """
        )
        data = self.cur.fetchall()

        return data

    def get_avg_salary(self) -> list[tuple]:
        """
        Функция получает среднюю зарплату по всем вакансиям.
        """
        self.cur.execute(
            """
            SELECT SUM(salary_avg)/ COUNT(salary_avg)
            FROM vacancies
            WHERE salary_avg != 0
        """
        )
        data = self.cur.fetchall()

        return data

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = round(self.get_avg_salary()[0][0], 1)

        self.cur.execute(
            f"""
                    SELECT name_vacancies, salary_avg, vacancies_url
                    FROM vacancies
                    WHERE salary_avg >= {avg_salary}
                """
        )
        data = self.cur.fetchall()

        return data

    def get_vacancies_with_keyword(self, keyword) -> list[tuple]:
        """Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова"""

        self.cur.execute(
            f"""
                    SELECT name_vacancies, salary_avg, vacancies_url FROM vacancies
                    WHERE LOWER(name_vacancies) LIKE '%{keyword}%'
                """
        )
        data = self.cur.fetchall()

        return data

    def exit_db(self):
        """Функция закрывает базу данных"""
        self.cur.close()
        self.conn.close()
