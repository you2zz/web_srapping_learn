import requests
from bs4 import BeautifulSoup


def get_html(url, item, page, headers):
    params = {
        'items_on_page': item,
        'page': page
    }
    response = requests.get(url=url, params=params, headers=headers)
    html_data = response.text
    hh_filter = BeautifulSoup(html_data, 'lxml')
    vacancy_list_tag = hh_filter.find('div', id="a11y-main-content")
    vacancy_tags = vacancy_list_tag.find_all('div', class_="serp-item")
    return vacancy_list_tag, vacancy_tags
