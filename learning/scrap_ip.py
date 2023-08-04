# <span class="table-ip4-home"> 188.68.84.31</span>
# strong class="text-underline"><span class="table-ip4-home"> 188.68.84.31</span></strong>
from bs4 import BeautifulSoup
import requests


response = requests.get("https://www.iplocation.net/")
html_data = response.text

soup = BeautifulSoup(html_data, 'lxml')
span_tag = soup.find('span', class_='table-ip4-home')
ip_addr = span_tag.text.strip()
print(span_tag)
print(ip_addr)