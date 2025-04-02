import pytest

from src.vacation import Vacation


def test_vacation_init(vacation):
    """Тестирование инициализации экземпляра класса Vacation"""
    assert vacation.vacation_list[0].name == "Python"


def test_vacation_max_salary(vacation):
    """Тестирование поиска вакансии с наибольшей зарплатой"""
    assert str(vacation.max_salary()) == "Данные о вакансии: Python, зарплата: 5000, подробнее о вакансии: url"


def test_vacation_max_salary_in_clear_list(vacation):
    """Тестирование вывода сообщения, если список вакансий с указанной зарплатой пуст"""
    vacation.clear_vacation_list()
    assert vacation.max_salary() == "Вакансий с указанной зарплатой не нашлось."


def test_get_vacancies_without_salary(vacation):
    """Тестирование получения списка с вакансиями без информации о зарплате"""
    assert vacation.get_vacancies_without_salary().strip() == (
        "Данные о вакансии: Python, зарплата: Зарплата не указана, подробнее о вакансии: url\n"
        "Данные о вакансии: Python, зарплата: Зарплата не указана, подробнее о вакансии: url"
    )


def test_get_vacancies_without_salary_error():
    """Тестирование выброса ошибки при пустом списке с вакансиями без информации о зарплате"""
    Vacation.clear_vacation_list()
    data = [
        {
            "id": 2,
            "name": "Python",
            "salary": {"from": 1000, "to": None},
            "alternate_url": "url",
            "snippet": {"requirement": "Python"},
            "experience": {"name": "1 год"},
        },
        {
            "id": 3,
            "name": "Python",
            "salary": {"from": 1000, "to": 2000},
            "alternate_url": "url",
            "snippet": {"requirement": "Python"},
            "experience": {"name": "1 год"},
        },
        {
            "id": 4,
            "name": "Python",
            "salary": {"from": 5000, "to": None},
            "alternate_url": "url",
            "snippet": {"requirement": "Python"},
            "experience": {"name": "1 год"},
        },
    ]

    for vacancy in data:
        Vacation(vacancy)

    with pytest.raises(ValueError) as ex:
        Vacation.get_vacancies_without_salary()
    assert str(ex.value) == "Список пуст."


def test_choose_min_salary(vacation):
    """Тестирование фильтрации по заданной минимальной зарплате"""
    first_result = vacation.choose_min_salary(3000)
    assert first_result.strip() == "Данные о вакансии: Python, зарплата: 5000, подробнее о вакансии: url"

    second_result = vacation.choose_min_salary(1000)
    assert second_result.strip() == (
        "Данные о вакансии: Python, зарплата: 1000, подробнее о вакансии: url\n"
        "Данные о вакансии: Python, зарплата: 1000-2000, подробнее о вакансии: url\n"
        "Данные о вакансии: Python, зарплата: 5000, подробнее о вакансии: url"
    )


def test_choose_min_salary_type_error(vacation):
    """Тестирование выброса ошибки при передаче неправильного типа аргумента в метод choose_min_salary"""
    with pytest.raises(TypeError) as ex:
        vacation.choose_min_salary("5000")
    assert str(ex.value) == "Введите число."


def test_choose_min_salary_value_error(vacation):
    """Тестирование выброса ошибки при передаче числа в метод choose_min_salary меньше или равного 0"""
    with pytest.raises(ValueError) as ex:
        vacation.choose_min_salary(0)
    assert str(ex.value) == "Значение зарплаты должно быть больше 0."
