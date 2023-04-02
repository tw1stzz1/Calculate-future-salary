import os
from terminaltables import AsciiTable, DoubleTable, SingleTable

from hhru import get_languages_statistics_hhru
from sjcom import get_languages_statistics_sj


def create_table(languages_statistics):   
    title_table = [
        [
            'Языки программирования',
            'Средняя зп',
            'Вакансий найдено',
            'Вакансий обработано'
        ],
    ]

    for language, vacancies_statistics in languages_statistics.items():
        title_table.append(
           [
             language,
              vacancies_statistics["average_salary"],
              vacancies_statistics["vacancies_found"],
              vacancies_statistics["vacancies_processed"]
          ]
    
        )
    table_instance = AsciiTable(title_table)
    return table_instance.table



def main():
    api_key_sj = os.environ['API_KEY_SJ']
    languages = [
        "Python",
        "JavaScript",
        "Java",
        "C++",
        "C#",
        "C",
        "PHP",
        "Ruby"
    ]
    languages_statistics_hhru = get_languages_statistics_hhru(languages)
    print(create_table(languages_statistics_hhru))

    languages_statistics_sj = get_languages_statistics_sj(api_key_sj, languages)
    print(create_table(languages_statistics_sj))



if __name__ == "__main__":
    main()
