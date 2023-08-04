import time
import re
import json
import requests
import fake_headers
from bs4 import BeautifulSoup

headers_gen = fake_headers.Headers(browser="firefox", os="win")

page = 0

item = 10

params = {
    'items_on_page':20,
    'page': page
}

all_vacancy =[]

vacancy_parsed = {}

while True:
    time.sleep(0.5)
    # response = requests.get(f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&items_on_page={item}&page={page}", headers=headers_gen.generate())
    response = requests.get(
        f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&", params=params,
        headers=headers_gen.generate())

    html_data = response.text
    hh_filter = BeautifulSoup(html_data, 'lxml')
    vacancy_list_tag = hh_filter.find('div', id="a11y-main-content")
    if vacancy_list_tag != None:
        page += 1
        vacancy_tags = vacancy_list_tag.find_all('div', class_="serp-item")
    else:
        break
    all_vacancy_on_page = []

    for vacancy_tag in vacancy_tags:
        time.sleep(0.33)
        header_tag = vacancy_tag.find('h3')
        a_tag = header_tag.find('a')
        company_tag = vacancy_tag.find('div', class_="vacancy-serp-item__meta-info-company")
        city_tag = vacancy_tag.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy-address'})
        salary_tag = vacancy_tag.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

        header_text = header_tag.text
        link = a_tag['href']
        company_text = company_tag.text
        city_text = city_tag.text.split()[0].strip(',')
        id_vacancy = re.search('\d+', link).group()

        description_page = requests.get(link, headers=headers_gen.generate())
        description = BeautifulSoup(description_page.text, 'lxml')
        description_body_tag = description.find('div', class_="vacancy-section")
        description_body_text = description_body_tag.text

        if salary_tag != None:
            salary_text = salary_tag.text
        else:
            salary_text = 'Зарплата не указана'

        all_vacancy_on_page.append(id_vacancy)

        search_django = re.findall('django', description_body_text, re.I)
        search_flask = re.findall('flask', description_body_text, re.I)
        if len(search_django) > 0:
            vacancy_parsed.setdefault(id_vacancy, {
                'vacancy_name': header_text,
                'link': link,
                'salary': salary_text,
                'company': company_text,
                'city': city_text,
            })

    all_vacancy.extend((all_vacancy_on_page))
    print(f'страница {page}')
    print(
        f'В цикле обработано {len(all_vacancy_on_page)} вакансий. Всего подошло по условиям вакансий {len(vacancy_parsed)}')

with open('../data/vacancy_parsed.json', 'w', encoding='utf-8') as file:
    json.dump(vacancy_parsed, file, indent=4, ensure_ascii=False)



print()
print()
print()
print(f'всего обработано {len(all_vacancy)} вакансий из них подошло по условиям {len(vacancy_parsed)} вакансий')