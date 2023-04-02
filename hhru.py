import requests
from itertools import count
from collections import defaultdict


def get_vacancies(language="Python"):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text" : language
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_vacancies_statistics(language="Python"):
    averages_salaries = []
    for page in count(0):
        vacancies = get_vacancies(language)
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


def calculate_average_salary(vacancy_salary_from=None, vacancy_salary_to=None):
    if vacancy_salary_to and vacancy_salary_from:
        average_salary = (int(vacancy_salary_from) + int(vacancy_salary_to))/2
    elif not vacancy_salary_from:
        average_salary = int(vacancy_salary_to) * 0.8
    elif not vacancy_salary_to:
        average_salary = int(vacancy_salary_from) * 1.2
    else:
        average_salary = None
    return average_salary


def get_languages_statistics_hhru(languages):
    amount_languages_vacancies = defaultdict()
    for language in languages:
        amount_languages_vacancies[language] = get_vacancies_statistics(language)
    return amount_languages_vacancies
