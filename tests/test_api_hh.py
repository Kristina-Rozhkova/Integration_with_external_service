from unittest.mock import Mock, patch

import pytest

from src.api_hh import HeadHunterParser


def test_get_vacation():
    """Тестирование получения вакансии с HeadHunterParser"""

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "117485514", "name": "Python"}]}
        mock_get.return_value = mock_response

        parser = HeadHunterParser()
        # заменяем параметр страницы, чтобы ожидаемое значение не дублировалось 10 раз (из-за цикла while)
        parser.params["page"] = 9
        result = parser.get_vacations("Python")

        assert len(result) == 1
        assert result == [{"id": "117485514", "name": "Python"}]


def test_get_vacation_error():
    """Тестирование выброса ошибки при получении ключевого слова, не содержащего букв"""
    parser = HeadHunterParser()

    with pytest.raises(ValueError) as ex:
        parser.get_vacations("1")
    assert str(ex.value) == "Введите слово или фразу"


def test_init():
    """Тестирование инициализации экземпляра класса HeadHunterParser"""
    parser = HeadHunterParser()
    assert parser.url == "https://api.hh.ru/vacancies"


def test_connection_error():
    """Тестирование неуспешного подключения к сайту"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        data = HeadHunterParser()
        with pytest.raises(Exception) as ex:
            data._connection()
        assert str(ex.value) == "Ошибка подключения."
