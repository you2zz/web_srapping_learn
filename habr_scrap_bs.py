# вытаскиваем заголовки всех статей на главной странице habr.com
# дата публикации
# ссылка на статью
# заголовок статьи
# переход по ссылке и получение текста статьи

# <div class="tm-articles-list">
# <article id="751906" data-navigatable="" tabindex="0" class="tm-articles-list__item">
# <time datetime="2023-08-02T06:31:32.000Z" title="2023-08-02, 11:31">
# <h2 class="tm-title tm-title_h2">
# <a href="/ru/articles/751906/" class="tm-title__link" data-test-id="article-snippet-title-link" data-article-link="true">
# <div id="post-content-body">
import json
import requests
import fake_headers
from bs4 import BeautifulSoup

headers_gen = fake_headers.Headers(browser="firefox", os="win")

response = requests.get("https://habr.com/ru/all/page1", headers=headers_gen.generate())
html_data = response.text

habr_main = BeautifulSoup(html_data, 'lxml')
article_list_tag = habr_main.find('div', class_='tm-articles-list')

article_tags = article_list_tag.find_all('article')

articles_parsed = []
for article_tag in article_tags:
    header_tag = article_tag.find('h2')
    a_tag = header_tag.find('a')
    time_tag = article_tag.find('time')

    header_text = header_tag.text
    link = a_tag['href']
    link = f'https://habr.com{link}'
    publication_time = time_tag['datetime']

    article_response = requests.get(link, headers=headers_gen.generate())
    article = BeautifulSoup(article_response.text, 'lxml')
    article_body_tag = article.find('div', id='post-content-body')
    article_body_text = article_body_tag.text[:20]

    articles_parsed.append({
        'header': header_text,
        'link': link,
        'publication_time': publication_time,
        'article_text': article_body_text
    })

# print(articles_parsed)
with open('articles_parsed.json', 'a', encoding='utf-8') as file:
    json.dump(articles_parsed, file, indent=4, ensure_ascii=False)