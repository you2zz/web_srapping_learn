import time
import re
from bs4 import BeautifulSoup
import requests

def scrap_pages(vacancy_tags, headers, money='₽'):
    vacancy_parsed = {}
    all_get = []
    for vacancy_tag in vacancy_tags:
        time.sleep(0.33)
        header_tag = vacancy_tag.find('h3')
        a_tag = header_tag.find('a')
        company_tag = vacancy_tag.find('div', class_="vacancy-serp-item__meta-info-company")
        city_tag = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
        salary_tag = vacancy_tag.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

        header_text = header_tag.text
        link = a_tag['href']
        company_text = company_tag.text
        city_text = city_tag.text.split()[0].strip(',')
        id_vacancy = re.search('\d+', link).group()

        description_page = requests.get(link, headers=headers)
        description = BeautifulSoup(description_page.text, 'lxml')
        description_body_tag = description.find('div', class_="vacancy-section")
        description_body_text = description_body_tag.text

        if salary_tag is not None:
            salary_text = salary_tag.text
        else:
            salary_text = 'Доход не указан'

        search_django = re.findall('django', description_body_text, re.I)
        search_flask = re.findall('flask', description_body_text, re.I)
        search_usd = re.search('[$]', salary_text)
        if money != '$':
            if len(search_django) > 0 and len(search_flask) > 0:
                vacancy_parsed.setdefault(id_vacancy, {
                    'vacancy_name': header_text,
                    'link': link,
                    'salary': salary_text,
                    'company': company_text,
                    'city': city_text,
                })
        else:
            if len(search_django) > 0 and len(search_flask) > 0 and search_usd is not None:
                vacancy_parsed.setdefault(id_vacancy, {
                    'vacancy_name': header_text,
                    'link': link,
                    'salary': salary_text,
                    'company': company_text,
                    'city': city_text,
                })
        all_get.append(id_vacancy)
    return vacancy_parsed, all_get