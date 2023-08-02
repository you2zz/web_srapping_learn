from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


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
    time_tag = article.find_element(By.TAG_NAME, 'time')

    header = h2.text
    time_text = time_tag.get_attribute('datetime')
    link = a.get_attribute('href')
    link = f'https://'