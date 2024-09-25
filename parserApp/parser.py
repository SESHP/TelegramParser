
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import random
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме без GUI, уберите этот аргумент, если хотите видеть браузер
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service('/Users/buzeoff/Downloads/chromedriver-mac-arm64/chromedriver')  # Замените 'path_to_chromedriver' на путь к вашему chromedriver

# Создаем объект браузера
driver = webdriver.Chrome(service=service, options=chrome_options)

# Вводим имена и формируем URL
names = '%20'.join(input().split(' '))
url = f'https://zachestnyibiznes.ru/search?query={names}'

# Переходим на сайт
driver.get(url)


for i in tqdm(range(100)):
    time.sleep(random.uniform(0.03, 0.4))

# Задержка для загрузки страницы (иногда это необходимо)
# time.sleep(6)


# Получаем HTML-код страницы
html = driver.page_source

# Закрываем браузер
driver.quit()

# Теперь можно парсить HTML через BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
searchResult = soup.find(id = 'search_result')


digit = 0
textDigit = searchResult.find(id = 'block-curr-filters-1').text
for i in textDigit.split():
    if i.isdigit():
        digit += int(i)


resultSearching = {}
for i in range(digit):
    div = searchResult.find_all('div', 'background-grey-blue-light p-15 b-radius-5 m-b-20')[i]
    namePars = div.find('a', 'no-underline-full').text.strip()
    linkPars = f'https://zachestnyibiznes.ru{div.find('a', 'no-underline-full')['href'].strip()}'
    
    resultSearching[namePars] = linkPars


print(resultSearching)


