import pytest

from src.vacation import Vacation


@pytest.fixture
def vacation():
    list_of_data = [
        {
            "id": 1,
            "name": "Python",
            "salary": None,
            "alternate_url": "url",
            "snippet": {"requirement": "Python"},
            "experience": {"name": "1 год"},
        },
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
        {
            "id": 5,
            "name": "Python",
            "salary": None,
            "alternate_url": "url",
            "snippet": {"requirement": "Python"},
            "experience": {"name": "1 год"},
        },
    ]

    Vacation.clear_vacation_list()

    for data in list_of_data:
        Vacation(data)

    return Vacation


@pytest.fixture
def data():
    return [
        {
            "name": "Тестировщик комфорта квартир",
            "salary": {"from": 350000, "to": 450000},
            "alternate_url": "https://hh.ru/vacancy/93353083",
        },
        {
            "name": "Удаленный диспетчер чатов (в Яндекс)",
            "salary": {"from": 30000, "to": 44000},
            "alternate_url": "https://hh.ru/vacancy/92223756",
        },
        {
            "name": "Удаленный специалист службы поддержки (в Яндекс)",
            "salary": {"from": 30000, "to": 44000},
            "alternate_url": "https://hh.ru/vacancy/92223870",
        },
    ]
