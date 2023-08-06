import time
import unicodedata
import re
import json
import requests
from bs4 import BeautifulSoup


class HhScrap:

    def __init__(self, url, item, headers, money='₽', how_many_search=100):
        self.url = url
        self.item = item
        self.headers = headers
        self.money = money
        self.how_many_search = how_many_search

    def get_html(self, page):
        params = {
            'items_on_page': self.item,
            'page': page
        }
        response = requests.get(url=self.url, params=params, headers=self.headers)
        html_data = response.text
        hh_filter = BeautifulSoup(html_data, 'lxml')
        vacancy_list_tag = hh_filter.find('div', id="a11y-main-content")
        vacancy_tags = vacancy_list_tag.find_all('div', class_="serp-item")
        return vacancy_list_tag, vacancy_tags

    def scrap_pages(self, vacancy_tags):
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
            company_text = unicodedata.normalize("NFKD", company_tag.text)
            city_text = city_tag.text.split()[0].strip(',')
            id_vacancy = re.search('\d+', link).group()

            description_page = requests.get(link, headers=self.headers)
            description = BeautifulSoup(description_page.text, 'lxml')
            description_body_tag = description.find('div', class_="vacancy-section")
            description_body_text = description_body_tag.text

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
            time.sleep(0.5)
            vacancy_list_tag, vacancy_tags = self.get_html(page)
            if vacancy_list_tag is not None:
                page += 1
            else:
                print('Собраны все существующие вакансии')
                break
            vacancy_parsed, all_get = self.scrap_pages(vacancy_tags)
            all_vacancy_parsed.update(vacancy_parsed)
            total_get.extend(all_get)
            print(f'страница {page}')
            print(
                f'В цикле обработано {len(all_get)} вакансий. Всего подошло по условиям вакансий {len(all_vacancy_parsed)}')
        print('Сбор данных завершен')
        print(
            f'всего обработано {len(total_get)} вакансий из них подошло по условиям {len(all_vacancy_parsed)} вакансий')
        return all_vacancy_parsed

    def create_json(self):
        with open('data/vacancy_parsed.json', 'w', encoding='utf-8') as file:
            json.dump(self.get_all_vacancy(), file, indent=4, ensure_ascii=False)
        print('Файл "vacancy_parsed.json" успешно создан')