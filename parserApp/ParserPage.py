from ParserSearch import ParserSearching
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import random
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

googlePath = os.getenv("googlePath")

parser = ParserSearching(googlePath)
input_names = input("Введите имена для поиска: ")
results = parser.run(input_names)


keys = list(results.keys())
for idx, key in enumerate(keys, 1):
    print(f"{idx}. {key}")

url = ''

try:
    selected_index = int(input("Выберите номер нужного вам ключа: ")) - 1

    if 0 <= selected_index < len(keys):
        selected_key = keys[selected_index]
        selected_value = results[selected_key]
        url = selected_value
        # print(f"Вы выбрали: {selected_key}, ссылка: {selected_value}")
        # print(url)
    else:
        print("Ошибка: введен неправильный номер.")

except ValueError:
    print("Ошибка: введите число.")


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service('/Users/buzeoff/Downloads/chromedriver-mac-arm64/chromedriver')  # Замените 'path_to_chromedriver' на путь к вашему chromedriver

# Создаем объект браузера
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)

for i in tqdm(range(100)):
    time.sleep(random.uniform(0.03, 0.4))


html = driver.page_source

driver.quit()

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())
