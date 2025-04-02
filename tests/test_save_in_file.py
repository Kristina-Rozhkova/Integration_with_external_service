import json

from src.save_in_file import Json


def test_json_write_down(data):
    """Тестирование добавления информации о вакансиях"""
    save_js = Json("tests/test_data/test_save.json")
    save_js.write_down(data)

    with open("tests/test_data/test_save.json", "r", encoding="utf-8") as f:
        datas = json.load(f)

    assert datas[0]["name"] == "Тестировщик комфорта квартир"
    assert len(datas) == 3


def test_file_not_found_error():
    """Тестирование вывода сообщения ошибки при попытке прочитать данные в несуществующем файле"""
    js = Json("test.json")
    result = js._read_file()
    assert result == "Файл не найден."


def test_json_get_from():
    """Тестирование получения информации из файла по заданным критериям"""
    criteria = {"name": "Яндекс", "salary": {"from": 30000, "to": 44000}}

    js = Json("tests/test_data/test_save.json")
    result = js.get_from(criteria)
    assert result == [
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


def test_json_delete_from():
    """Тестирование удаления вакансий из файла по заданным критериям"""
    criteria = {"name": "Яндекс", "salary": {"from": 30000, "to": 44000}}

    js = Json("tests/test_data/test_save.json")
    js.delete_from(criteria)

    with open("tests/test_data/test_save.json", "r", encoding="utf-8") as f:
        info = json.load(f)

    assert info == [
        {
            "name": "Тестировщик комфорта квартир",
            "salary": {"from": 350000, "to": 450000},
            "alternate_url": "https://hh.ru/vacancy/93353083",
        }
    ]


def test_clear_file():
    """Тестирование очистки файла"""
    js = Json("tests/test_data/test_save.json")
    js.clear_file()
    with open("tests/test_data/test_save.json", "r", encoding="utf-8") as f:
        info = json.load(f)

    assert info == []
