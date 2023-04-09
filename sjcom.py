import os
import requests
from pprint import pprint
from itertools import count
from collections import defaultdict


def get_vacancies(api_key_sj, 
                  language="Python", 
                  page=0, 
                  period=30, 
                  city_id=4, 
                  catalogues=48):
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        "town" : city_id,
        "keyword" : language,
        "page" : page,
        "period" : period,
        "catalogues" : catalogues
    }
    headers = {
        "X-Api-App-Id" : api_key_sj
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


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


def get_vacancies_statistics(api_key_sj, language="Python"):
    averages_salaries = []
    for page in count(0, 1):
        vacancies = get_vacancies(api_key_sj, language, page)
        
        for vacancy in vacancies['objects']:
            if not (vacancy["payment_to"] or vacancy["payment_from"]):
                continue
            if not vacancy["currency"] == "rub":
                continue
            averages_salaries.append(
                calculate_average_salary(
                    vacancy['payment_from'],
                    vacancy['payment_to']
                )
            )
        if not vacancies['more']:
            break

    if averages_salaries:
        average_salary = int(
            sum(averages_salaries) / len(averages_salaries)
        )
    else:
        average_salary = None

    vacancies_amount = vacancies['total']

    vacancies_statistics = {
        "average_salary": average_salary,
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(averages_salaries)
    }
    return vacancies_statistics


def get_languages_statistics_sj(api_key_sj, languages):
    amount_languages_vacancies = defaultdict()
    for language in languages:
        amount_languages_vacancies[language] = get_vacancies_statistics(api_key_sj, language)
    return amount_languages_vacancies
