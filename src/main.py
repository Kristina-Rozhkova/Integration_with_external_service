from src.api_hh import HeadHunterParser
from src.save_in_file import Json
from src.vacation import Vacation


def work_with_hh_vacancies():
    """Функция для взаимодействия с пользователем"""
    list_of_vacancies = []
    print("Здравствуйте!\nДавайте начнем работу с приложением.\n")
    print("Хотите (1) ввести новый поисковой запрос на hh.ru или (2) получить вакансии из выгруженных данных?")
    user_start = input("Введите 1 или 2: ")

    if user_start == "1":
        print("Введите ключевое слово или фразу, по которым будет осуществляться поиск вакансии.")

        vacancies = HeadHunterParser()
        flag = True  # флаг для повторения цикла
        while flag:
            try:
                user_keyword = input()
                list_of_vacancies = vacancies.get_vacations(user_keyword)
                flag = False
            except ValueError as ex:
                print(str(ex))

    elif user_start == "2":
        js = Json("data/vacancies.json")
        user_name_vacancy = input("Введите название должности: ").capitalize()
        list_of_vacancies = js.get_from({"name": user_name_vacancy})

    print(f"Нашлось {len(list_of_vacancies)} вакансий.")
    user_answer = input(
        "(1) Вывести список сейчас или (2) хотите получить топ вакансий по зарплате?\n" "Введите 1 или 2: "
    )

    if user_answer == "1":
        return list_of_vacancies
    elif user_answer == "2":

        try:
            user_top = int(input("сколько вакансий хотите получить? "))
            if user_top > len(list_of_vacancies):
                return "В списке нет столько вакансий. Попробуйте снова."

            for vacancy in list_of_vacancies:
                Vacation(vacancy)

            if not Vacation.vacation_list:
                return "Вакансий с зарплатой не нашлось."

            sorted_vacancies = sorted(Vacation.vacation_list, key=lambda x: x.salary_min, reverse=True)

            top_vacancies = sorted_vacancies[:user_top]

            for element in top_vacancies:
                print(str(element))

            top_vacancies_dicts = [
                {
                    "name": vacancy.name,
                    "salary_min": vacancy.salary_min,
                    "salary_max": vacancy.salary_max,
                    "link": vacancy.link,
                    "description": vacancy.description,
                    "experience": vacancy.experience,
                }
                for vacancy in top_vacancies
            ]

            list_to_save = Json()
            list_to_save.write_down(top_vacancies_dicts)
            Vacation.clear_vacation_list()

            return "Запрашиваемые данные сохранены в файл."
        except ValueError:
            return "В ответе ожидаются только числа. Попробуйте снова."

    else:
        return "Введен неверный ответ. Попробуйте снова"
