import json
from abc import ABC, abstractmethod


class SaveInFile(ABC):
    """Абстрактный класс для сохранения данных в файл"""

    @abstractmethod
    def write_down(self, information: list[dict]):
        pass

    @abstractmethod
    def get_from(self, criteria: dict):
        pass

    @abstractmethod
    def delete_from(self, criteria: dict):
        pass

    @abstractmethod
    def clear_file(self):
        pass


class Json(SaveInFile):
    """Класс для сохранения данных в JSON-файл"""

    file: str

    def __init__(self, file: str = "data/save.json"):
        self.__file = file

    def write_down(self, information: list[dict]) -> None:
        """Добавление вакансий в файл"""
        with open(self.__file, "r", encoding="utf-8") as f:
            reading_data = json.load(f)
        if not reading_data:
            reading_data = []

        for info in information:
            if info not in reading_data:
                reading_data.append(info)

        with open(self.__file, "w", encoding="utf-8") as file:
            json.dump(reading_data, file, ensure_ascii=False, indent=4)

    def _read_file(self) -> list[dict] | str:
        """Чтение данных файла"""
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return "Файл не найден."

    def _find_vacancy(self, criteria: dict) -> list[dict]:
        """Поиск вакансий в файле"""
        data = self._read_file()

        list_of_vacancies = []

        for vacancy in data:
            if "name" in criteria and criteria["name"] not in vacancy.get("name"):
                continue

            match = all(
                vacancy.get(key) == value
                for key, value in criteria.items()
                if key != "name" and criteria["salary"]["from"] <= vacancy["salary"]["from"]
            )

            if match:
                list_of_vacancies.append(vacancy)

        return list_of_vacancies

    def get_from(self, criteria: dict) -> list[dict]:
        """Получение данных о вакансии по определенным критериям"""
        return self._find_vacancy(criteria)

    def delete_from(self, criteria: dict) -> None:
        """Удаление информации о вакансиях по заданным критериям"""
        data = self._read_file()

        list_to_delete = self._find_vacancy(criteria)

        new_list = [vacancy for vacancy in data if vacancy not in list_to_delete]

        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump(new_list, f, ensure_ascii=False, indent=4)

    def clear_file(self) -> None:
        """Очистка файла (запись пустого списка)"""
        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)


"""
Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл, 
получения данных из файла по указанным критериям и удаления информации о вакансиях. 
Создать класс для сохранения информации о вакансиях в JSON-файл. 
Дополнительно, по желанию, можно реализовать классы для работы с другими форматами, 
например с CSV- или Excel-файлом, с TXT-файлом.
Данный класс выступит в роли основы для коннектора, заменяя который (класс-коннектор), можно использовать в качестве 
хранилища одну из баз данных или удаленное хранилище со своей специфической системой обращений.

В случае если какие-то из методов выглядят не используемыми для работы с файлами, то не стоит их удалять. 
Они пригодятся для интеграции к БД. Сделайте заглушку в коде.
"""
