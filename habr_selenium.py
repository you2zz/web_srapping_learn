from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions

def wait_element(browser, delay_second=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_second).until(expected_conditions.presence_of_element_located(by, value))

chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(excutable_path=chrome_driver_path)
browser = webdriver.Chrome(service=browser_service)

# browser.get('https://yandex.ru')
browser.get('https://habr.com/ru/all')

articles = browser.find_element((By.CLASS_NAME, 'tm-articles-list'))
parsed_articles = []
for article in articles.find_elements(By.TAG_NAME, 'article'):
    h2 = article.find_element(By.TAG_NAME,'h2')
    a = h2.find_element(By.TAG_NAME, 'a')
    time_tag = wait_element(browser, 1, By.TAG_NAME, 'time')

    header_text = h2.text
    publication_time = time_tag.get_attribute('datetime')
    link = a.get_attribute('href')
    link = f'https://habr.com{link}'
    parsed_articles.append({
        'header': header_text,
        'link': link,
        'publication_time': publication_time
    })

for parsed_article in parsed_articles:
    browser.get(parsed_article['link'])
    article = wait_element( browser, 1, By.ID, 'post-content-body')
    parsed_article['text'] = article.text
