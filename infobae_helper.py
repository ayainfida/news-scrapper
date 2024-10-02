from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import os
from bs4 import BeautifulSoup
from json import dumps

options = webdriver.FirefoxOptions()
options.add_argument('--headless') 
driver = webdriver.Firefox(options=options)

def get_html(url, category):
    driver.get(url)

    sleep(5)

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'feed-list-read-more')))

    next_btn = driver.find_element(By.CLASS_NAME, 'feed-list-read-more')
    driver.execute_script("arguments[0].click();",next_btn)

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'feed-list-read-more')))
    driver.execute_script("arguments[0].click();",next_btn)

    page_source = driver.page_source

    with open(f'page_source/{category}.html', 'w') as f:
        f.write(page_source)

categories = [
    ('Fintech World', 'https://www.infobae.com/tag/mundo-fintech/'),
    ('Techno Cars and Mobility', 'https://www.infobae.com/tag/tecno-autos-y-movilidad/'),
    ('Entertainment', 'https://www.infobae.com/entretenimiento/'),
    ('Health', 'https://www.infobae.com/salud/'),
    ('Russia Ukraine War', 'https://www.infobae.com/tag/guerra-rusia-ucrania/'),
    ('Crime and Justice', 'https://www.infobae.com/sociedad/policiales/'),
    ('Society', 'https://www.infobae.com/sociedad/'),
    ('Policy', 'https://www.infobae.com/politica/'),
    ('Music', 'https://www.infobae.com/tag/musica/'),
    ('Arts', 'https://www.infobae.com/tag/arte/'),
    ('Cinema', 'https://www.infobae.com/tag/cine/'),
    ('Series', 'https://www.infobae.com/tag/series/'),
    ('Education', 'https://www.infobae.com/educacion/'),
    ('Tourism', 'https://www.infobae.com/turismo/'),
]

# for category, url in tqdm(categories, desc='Downloading page source for every category'):
#     get_html(url, category=category)

for category in os.listdir('page_source'):
    with open(f'page_source/{category}', 'r') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')

    links = []

    for a_tag in soup.find('article', class_='article').find_all('a'):
        link = f'https://www.infobae.com{a_tag["href"]}'
        if link not in links:
            links.append(link)

    with open(f"links/{category.replace('.html', '')}.json", 'w') as f:
        f.write(dumps(links))

