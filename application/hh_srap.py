import time
import datetime
import os
import unicodedata
import re
import json
from functools import wraps
import requests
from bs4 import BeautifulSoup
from application.decorators_ws import logger, with_attempts, with_attempts_data, log_clean


class HhScrap:

    def __init__(self, url, item, headers, money='₽', how_many_search=100):
        self.url = url
        self.item = item
        self.headers = headers
        self.money = money
        self.how_many_search = how_many_search

    @with_attempts(max_attempts=5, timeout=0.5)
    @logger(path='data/requests.log')
    def requests_conn(self, url, params=None):
        response = requests.get(url=url, params=params, headers=self.headers)
        return response, response.status_code, url

    @with_attempts_data(max_attempts=5, timeout=0.5)
    def get_html(self, page):
        params = {
            'items_on_page': self.item,
            'page': page
        }
        response = self.requests_conn(self.url, params=params)[0]
        html_data = response.text
        hh_filter = BeautifulSoup(html_data, 'lxml')
        vacancy_list_tag = hh_filter.find('div', id="a11y-main-content")
        if vacancy_list_tag is not None:
            vacancy_tags = vacancy_list_tag.find_all('div', class_="serp-item")
        else:
            print(f'Данные страницы не получены')
            vacancy_tags = None
        return vacancy_tags, f'Страница с перечнем вакансий № {page + 1}'

    @with_attempts_data(max_attempts=5, timeout=0.5)
    def get_vacancy_description(self, url):
        description_page = self.requests_conn(url)[0]
        description = BeautifulSoup(description_page.text, 'lxml')
        description_body_tag = description.find('div', class_="vacancy-section")
        return description_body_tag, url

    def scrap_pages(self, vacancy_tags):
        vacancy_parsed = {}
        all_get = []
        for vacancy_tag in vacancy_tags:
            time.sleep(0.1)
            header_tag = vacancy_tag.find('h3')
            a_tag = header_tag.find('a')
            company_tag = vacancy_tag.find('div', class_="vacancy-serp-item__meta-info-company")
            city_tag = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
            salary_tag = vacancy_tag.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

            header_text = header_tag.text
            link = a_tag['href']
            company_text = unicodedata.normalize("NFKD", company_tag.text)
            city_text = city_tag.text.split()[0].strip(',')
            id_vacancy = re.search('\d+', link).group()

            # description_page = self.requests_conn(link)[0]
            # description = BeautifulSoup(description_page.text, 'lxml')
            # description_body_tag = description.find('div', class_="vacancy-section")
            description_body_tag = self.get_vacancy_description(link)[0]
            if description_body_tag is not None:
                description_body_text = description_body_tag.text
            else:
                print(f'Страница {link} пропущена т.к. данные не получены')
                continue

            if salary_tag is not None:
                salary_text = unicodedata.normalize("NFKD", salary_tag.text)
            else:
                salary_text = 'Доход не указан'

            search_django = re.findall('django', description_body_text, re.I)
            search_flask = re.findall('flask', description_body_text, re.I)
            search_usd = re.search('[$]', salary_text)
            if self.money != '$':
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

    def get_all_vacancy(self):
        all_vacancy_parsed = {}
        total_get = []
        page = 0
        while len(all_vacancy_parsed) < self.how_many_search:
            time.sleep(0.1)
            vacancy_tags = self.get_html(page)[0]
            if vacancy_tags is not None:
                page += 1
            else:
                print()
                print('Собраны все существующие вакансии')
                break
            vacancy_parsed, all_get = self.scrap_pages(vacancy_tags)
            all_vacancy_parsed.update(vacancy_parsed)
            total_get.extend(all_get)
            print(f'страница {page}')
            print(f'В цикле обработано {len(all_get)} вакансий. Всего подошло по условиям вакансий {len(all_vacancy_parsed)}')
        print()
        print('Сбор данных завершен')
        print(f'всего обработано {len(total_get)} вакансий из них подошло по условиям {len(all_vacancy_parsed)} вакансий')
        return all_vacancy_parsed, total_get

    @log_clean(path='data/requests.log')
    def create_json(self):
        with open('data/vacancy_parsed.json', 'w', encoding='utf-8') as file:
            dict_vacancy, total_get = self.get_all_vacancy()
            json.dump(dict_vacancy, file, indent=4, ensure_ascii=False)
        print('Файл "vacancy_parsed.json" успешно создан')
        return total_get
