from functools import wraps
import time
import datetime
import os
import unicodedata
import re
import json
from functools import wraps
import requests
import fake_headers
from bs4 import BeautifulSoup
from application.hh_srap import HhScrap

headers_gen = fake_headers.Headers(browser="firefox", os="win")

if __name__ == '__main__':
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&"
    item = 15  # по скольку вакансий запрашивать и обрабатывать в цикле
    headers = headers_gen.generate()
    money = '₽'  # по умолчанию '₽' выдаются результаты и в рублях и в другой валюте, для поиска з/п только в долларах поставить '$'
    how_many_search = 10  # указать после скольки найденных подходящих вакансий остановить парсинг

    hh_scrap = HhScrap(url, item, headers, money, how_many_search)
    hh_scrap.create_json()
