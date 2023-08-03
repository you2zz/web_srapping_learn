# <div data-qa="vacancy-serp__results" id="a11y-main-content"> - лента
# <div class="serp-item" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_premium"> - блок с вакансией
# <h3 data-qa="bloko-header-3" class="bloko-header-section-3"> - заголовок вакансии
# <a class="serp-item__title" data-qa="serp-item__title" target="_blank" href="https://spb.hh.ru/vacancy/80002041?from=vacancy_search_list&amp;query=python"> - ссылка вакансии
# <span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-2"> - зарплата вакансии
# <div class="vacancy-serp-item__meta-info-company"> - компания
#  <div data-qa="vacancy-serp__vacancy-address" class="bloko-text"> - город

import json
import requests
import fake_headers
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers_gen = fake_headers.Headers(browser="firefox", os="win")

response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2",headers=headers_gen.generate())
html_data = response.text

hh_filter = BeautifulSoup(html_data, 'lxml')
vacancy_list_tag = hh_filter.find('div', id="a11y-main-content")
# vacancy_tags = vacancy_list_tag.find_all('div', class_="serp-item")
vacancy_tags = vacancy_list_tag.find_all('div', class_="vacancy-serp-item__layout")

vacancy_parsed = []
for vacancy_tag in vacancy_tags:
    header_tag = vacancy_tag.find('h3')
    a_tag = header_tag.find('a')
    company_tag = vacancy_tag.find('div', class_="vacancy-serp-item__meta-info-company")
    city_tag = vacancy_tag.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy-address'})
    salary_tag = vacancy_tag.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

    header_text = header_tag.text
    link = a_tag['href']
    company_text = company_tag.text
    city_text = city_tag.text.split()[0].strip(',')

    if salary_tag != None:
        salary_text = salary_tag.text
    else:
        salary_tag = 'Зарплата не указана'

    vacancy_parsed.append({
        'vacancy_name': header_text,
        'link': link,
        'salary': salary_text,
        'company': company_text,
        'city': city_text
    })

print(vacancy_parsed)
print(len(vacancy_parsed))

# with open('vacancy_parsed2.json', 'a', encoding='utf-8') as file:
#     json.dump(vacancy_parsed, file, indent=4, ensure_ascii=False)