from abc import ABC, abstractmethod

import requests


class GetCompanyApi(ABC):
    """Абстрактный класс для получения данных"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def employer_information(self, employer_id):
        pass

    @abstractmethod
    def open_vacancies(self, employer_id):
        pass


class HHCompany(GetCompanyApi):
    """Класс для получения данных с HH.ru"""

    def __init__(self):
        """Конструктор класса"""

        self.__url = "https://api.hh.ru"
        self.emp = "employers"
        self.vac = "vacancies"
        self.employer_id = 0
        self.headers = {"User-Agent": "HH-User-Agent"}

    def employer_information(self, employer_id: int) -> dict:
        """
        Функция для получения информации о работодателе
        :param employer_id: id - работодателя
        :return: словарь с данными о работодателе
        """

        response = requests.get(f"{self.__url}/{self.emp}/{employer_id}")
        response.raise_for_status()
        data_employer = response.json()
        return data_employer

    def open_vacancies(self, employer_id: int) -> list[dict]:
        """
        Функция для получения вакансий одного работодаеля
        :param employer_id: id - работодателя
        :return: список словарей всех вакансий работодателя
        """
        self.employer_id = employer_id
        data_vacancies = []
        params = {"area": 113, "employer_id": employer_id, 'page': 0, 'per_page': 100}

        while True:
            response = requests.get(f"{self.__url}/{self.vac}", params=params)
            response.raise_for_status()
            vacancies_page = response.json()
            if not vacancies_page.get('items') or params['page'] == 19:
                break
            else:
                data_vacancies.extend(vacancies_page['items'])
            params['page'] += 1
        return data_vacancies
