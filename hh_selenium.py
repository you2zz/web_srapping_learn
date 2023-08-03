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

browser.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')

vacancy_list = browser.find_element(By.ID, 'a11y-main-content')

parsed_articles = []
for vacancy in vacancy_list.find_elements(By.CLASS_NAME, 'serp-item'):
    h3 = vacancy.find_element(By.TAG_NAME,'h3')
    a = h3.find_element(By.TAG_NAME, 'a')
    company_tag = vacancy.find_element(By.CLASS_NAME, 'vacancy-serp-item__meta-info-company')

    header = h3.text
    link = a.get_attribute('href')
    company_name = company_tag.text
    parsed_articles.append({
        'header': header,
        'link': link,
        'company': company_name
    })

print(parsed_articles)
print(len(parsed_articles))