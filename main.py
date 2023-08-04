import time
import re
import json
import requests
import fake_headers
from bs4 import BeautifulSoup
from application.get_html import get_html
from application.scrap_pages import scrap_pages
from application.create_json import create_json

headers_gen = fake_headers.Headers(browser="firefox", os="win")

if __name__ == '__main__':

    all_vacancy_parsed = {}
    total_get = []
    page = 0
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&"
    how_many_search = 30 # указать после скольки найденных подходящих вакансий остановить парсинг
    while len(total_get) < how_many_search:
        time.sleep(0.5)
        vacancy_list_tag, vacancy_tags = get_html(url, 5, page, headers_gen.generate())
        if vacancy_list_tag is not None:
            page += 1
        else:
            print('Сбор данных завершен')
            break

        vacancy_parsed, all_get = scrap_pages(vacancy_tags, headers_gen.generate(), '₽') # по умолчанию '₽', для поиска з/п в долларах поставить третьим аргументом '$'
        all_vacancy_parsed.update(vacancy_parsed)
        total_get.extend(all_get)

        print(f'страница {page}')
        print(f'В цикле обработано {len(all_get)} вакансий. Всего подошло по условиям вакансий {len(all_vacancy_parsed)}')

        create_json(all_vacancy_parsed)

    print()
    print(f'всего обработано {len(total_get)} вакансий из них подошло по условиям {len(all_vacancy_parsed)} вакансий')