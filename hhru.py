from itertools import count
from collections import defaultdict

import requests

from calculate_average_salary import calculate_average_salary


def get_vacancies(language="Python",
                  page=0,
                  professional_role=96,
                  city_id="1",
                  period=30):
                  
    url = "https://api.hh.ru/vacancies"
    params = {
        "page" : page,
        "professional_role" : professional_role,
        "text" : language,
        "area" : city_id,
        "period" : period
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_vacancies_statistics(language="Python"):
    averages_salaries = []
    for page in count(0):
        vacancies = get_vacancies(language, page)
        if page >= vacancies["pages"]-1:
            break
        for vacancy in vacancies["items"]:
            if not vacancy["salary"]:
                continue
            if not vacancy["salary"]["currency"] == "RUR":
                continue

            averages_salaries.append(
                calculate_average_salary(
                    vacancy["salary"]["from"],
                    vacancy["salary"]["to"]
                )
            )

    if averages_salaries:
        average_salary = int(
            sum(averages_salaries) / len(averages_salaries)
        )
    else:
        average_salary = None

    vacancies_amount = vacancies["found"]

    vacancies_statistics = {
        "average_salary": average_salary,
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(averages_salaries)
    }
    return vacancies_statistics


def get_languages_statistics_hhru(languages):
    amount_languages_vacancies = defaultdict()
    for language in languages:
        amount_languages_vacancies[language] = get_vacancies_statistics(language)
    return amount_languages_vacancies
