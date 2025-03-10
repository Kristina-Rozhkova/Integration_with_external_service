import re
from abc import ABC, abstractmethod

import requests


class Parser(ABC):

    @abstractmethod
    def _connection(self):
        pass

    @abstractmethod
    def get_vacations(self, keyword):
        pass


class HeadHunterParser(Parser):
    """Класс для получения информации о вакансиях с помощью API hh.ru"""

    def __init__(self) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"page": 0, "per_page": 15, "text": ""}
        self.vacations = []

    def _connection(self) -> str:
        """Получение данных с сайта"""
        response = requests.get(self.url, headers=self.headers, params=self.params)

        if response.status_code != 200:
            raise Exception("Ошибка подключения.")

        return response.json()["items"]

    def __connection(self) -> str:
        """Приватный метод, который вызывает защищенный метод"""
        return self._connection()

    def get_vacations(self, keyword: str) -> list[dict]:
        """Возвращает список вакансий в формате json"""
        if not re.search("[a-zA-ZА-Яа-я]", keyword):
            raise ValueError("Введите слово или фразу")

        self.params["text"] = keyword
        while self.params.get("page") != 10:
            vacations = self.__connection()
            self.vacations.extend(vacations)
            self.params["page"] += 1
        return self.vacations
