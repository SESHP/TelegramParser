from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import random
from bs4 import BeautifulSoup


class ParserSearching:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = None
        self.url = None

    def init_driver(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

    def generate_url(self, names):
        formatted_names = '%20'.join(names.split(' '))
        self.url = f'https://zachestnyibiznes.ru/search?query={formatted_names}'

    def open_page(self):
        if self.url:
            self.driver.get(self.url)

    def wait_for_page_load(self, duration=100):
        for _ in tqdm(range(duration)):
            time.sleep(random.uniform(0.03, 0.4))

    def get_html(self):
        return self.driver.page_source

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        search_result = soup.find(id='search_result')

        digit = 0
        text_digit = search_result.find(id='block-curr-filters-1').text
        for i in text_digit.split():
            if i.isdigit():
                digit += int(i)

        result_searching = {}
        for i in range(digit):
            div = search_result.find_all('div', 'background-grey-blue-light p-15 b-radius-5 m-b-20')[i]
            name_pars = div.find('a', 'no-underline-full').text.strip()
            link_pars = f"https://zachestnyibiznes.ru{div.find('a', 'no-underline-full')['href'].strip()}"
            result_searching[name_pars] = link_pars

        return result_searching

    def run(self, names):
        self.init_driver()
        self.generate_url(names)
        self.open_page()
        self.wait_for_page_load()
        html = self.get_html()
        self.close_driver()
        return self.parse_html(html)


