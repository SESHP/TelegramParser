from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import random
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from ParserSearch import ParserSearching  # Важно, что класс называется ParserPage, как мы договорились

load_dotenv()

class WebScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def load_page(self, url):
        self.driver.get(url)
        for _ in tqdm(range(100)):  # Задержка для имитации прогресса загрузки страницы
            time.sleep(random.uniform(0.03, 0.4))

    def get_html(self):
        return self.driver.page_source

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        general_info = soup.find('div', 'm-t-10 details-content').text
        general_information = general_info.split()

        # Извлекаем необходимую информацию
        info_ie = ' '.join(general_information[0:4])
        info_tin = ' '.join(general_information[4:6])
        info_ogrn = ' '.join(general_information[6:8])
        info_reg = ' '.join(general_information[8:14])
        info_status = ' '.join(general_information[14:16])
        info_ond = ' '.join(general_information[16:28])

        return info_ie, info_tin, info_ogrn, info_reg, info_status, info_ond

    def run(self, url):
        self.init_driver()
        self.load_page(url)
        html = self.get_html()
        self.close_driver()
        return self.parse_page(html)


class UserInteraction:
    def __init__(self, parser, scraper):
        self.parser = parser
        self.scraper = scraper

    def get_user_input(self):
        input_names = input("Введите имена для поиска: ")
        results = self.parser.run(input_names)

        keys = list(results.keys())
        for idx, key in enumerate(keys, 1):
            print(f"{idx}. {key}")

        return results, keys

    def select_result(self, keys, results):
        try:
            selected_index = int(input("Выберите номер нужного вам ключа: ")) - 1

            if 0 <= selected_index < len(keys):
                selected_key = keys[selected_index]
                return results[selected_key]
            else:
                print("Ошибка: введен неправильный номер.")
                return None

        except ValueError:
            print("Ошибка: введите число.")
            return None

    def display_information(self, info):
        info_ie, info_tin, info_ogrn, info_reg, info_status, info_ond = info
        print('\n', info_ie, '\n', info_tin, '\n', info_ogrn, '\n', info_reg, '\n', info_status, '\n', info_ond)

    def run(self):
        results, keys = self.get_user_input()
        selected_url = self.select_result(keys, results)

        if selected_url:
            info = self.scraper.run(selected_url)
            self.display_information(info)


# Основная программа
if __name__ == '__main__':
    google_path = os.getenv("googlePath")

    # Создаем объекты парсера и веб-скрапера
    parser = ParserSearching(google_path)
    scraper = WebScraper(google_path)

    # Инициализируем взаимодействие с пользователем
    user_interaction = UserInteraction(parser, scraper)
    user_interaction.run()
