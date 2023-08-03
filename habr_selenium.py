from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def wait_element(browser, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(expected_conditions.presence_of_element_located((by, value)))

chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(excutable_path=chrome_driver_path)
browser = webdriver.Chrome(service=browser_service)

# browser.get('https://yandex.ru')
browser.get('https://habr.com/ru/all/page1')

articles = browser.find_element(By.CLASS_NAME, 'tm-articles-list')
parsed_articles = []
for article in articles.find_elements(By.TAG_NAME, 'article'):
    h2 = article.find_element(By.TAG_NAME,'h2')
    a = h2.find_element(By.TAG_NAME, 'a')
    time_tag = wait_element(browser, 1, By.TAG_NAME, 'time')

    header = h2.text
    time_text = time_tag.get_attribute('datetime')
    link = a.get_attribute('href')
    # link = f'https://habr.com{link}'
    parsed_articles.append({
        'header': header,
        'link': link,
        'publication_time': time_text
    })

for parsed_article in parsed_articles:
    browser.get(parsed_article['link'])
    article = wait_element(browser, 1, By.ID, 'post-content-body')
    parsed_article['text'] = article.text

print(parsed_articles)