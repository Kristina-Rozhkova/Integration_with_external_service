from typing import Optional


class Vacation:
    """Класс для работы с вакансиями hh.ru"""

    name: str
    salary_min: int | str
    salary_max: int | str
    link: str
    description: str
    experience: str
    vacation_list: list = []
    vacation_list_without_salary: list = []
    __slots__ = ("name", "salary_min", "salary_max", "link", "description", "experience")

    def __init__(self, vacation: dict) -> None:
        self.name = vacation["name"]
        self.salary_min = vacation["salary"]["from"] if vacation["salary"] and "from" in vacation["salary"] else None
        self.salary_max = vacation["salary"]["to"] if vacation["salary"] and "to" in vacation["salary"] else None
        self.link = vacation["alternate_url"]
        self.description = vacation["snippet"]["requirement"]
        self.experience = vacation["experience"]["name"]
        self._have_salary()

    def __str__(self) -> str:
        if isinstance(self.salary_max, int):
            return (
                f"Данные о вакансии: {self.name}, "
                f"зарплата: {self.salary_min}-{self.salary_max}, "
                f"подробнее о вакансии: {self.link}"
            )
        elif isinstance(self.salary_max, str):
            return (
                f"Данные о вакансии: {self.name}, "
                f"зарплата: {self.salary_min}, "
                f"подробнее о вакансии: {self.link}"
            )

    def __validation(self) -> None:
        """Валидация данных"""
        if not self.salary_min:
            self.salary_min = "Зарплата не указана"
        if not self.salary_max:
            self.salary_max = "Зарплата не указана"

    def _have_salary(self) -> None:
        """Метод фильтрации вакансий по наличию зарплаты"""
        self.__validation()
        if isinstance(self.salary_min, int):
            Vacation.vacation_list.append(self)
        elif isinstance(self.salary_min, str):
            Vacation.vacation_list_without_salary.append(self)

    def __le__(self, other: Optional["Vacation"] | int) -> bool:
        """Метод сравнения зарплаты вакансии на ее минимум"""
        other_vacation = other.salary_min if isinstance(other, Vacation) else other
        return self.salary_min >= other_vacation

    @classmethod
    def max_salary(cls) -> Optional["Vacation"] | str:
        """Метод сравнения вакансий по зарплате, поиск максимального значения"""
        if not cls.vacation_list:
            return "Вакансий с указанной зарплатой не нашлось."
        max_salary = max(cls.vacation_list, key=lambda x: x.salary_min)
        return max_salary

    @classmethod
    def choose_min_salary(cls, min_salary: int) -> str:
        """Метод поиска вакансий с фильтрацией по минимальной зарплате"""
        if not isinstance(min_salary, int):
            raise TypeError("Введите число.")
        if min_salary <= 0:
            raise ValueError("Значение зарплаты должно быть больше 0.")
        return_data = ""
        for vacancy in cls.vacation_list:
            if vacancy.__le__(min_salary):
                return_data += f"{str(vacancy)}\n"
        return return_data

    @classmethod
    def get_vacancies_without_salary(cls) -> str:
        """Получение вакансий без информации о зарплате"""
        if cls.vacation_list_without_salary:
            str_vacancy = ""
            for vacancy in cls.vacation_list_without_salary:
                str_vacancy += f"{str(vacancy)}\n"
            return str_vacancy
        raise ValueError("Список пуст.")

    @classmethod
    def clear_vacation_list(cls) -> None:
        """Очистка списка вакансий"""
        cls.vacation_list = []
        cls.vacation_list_without_salary = []


"""
Создать класс для работы с вакансиями. 
В этом классе самостоятельно определить атрибуты, такие как название вакансии, ссылка на вакансию, зарплата, 
краткое описание или требования и т. п. (всего не менее четырех атрибутов). 
Класс должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные, которыми инициализируются его атрибуты.

Способами валидации данных может быть проверка, указана или нет зарплата. 
В этом случае выставлять значение зарплаты 0 или «Зарплата не указана» в зависимости от структуры класса.
"""
