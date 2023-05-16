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