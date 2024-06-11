from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import random
import time



AMENITIES = [
    "piscina",
    "pileta"
    "salon de usos múltiples",
    "SUM",
    "gimnasio",
    "parrilla",
    "spa",
    "sauna",
    "sala de cine",
    "solarium",
    "terraza",
    "espacio de plaza",
    "juegos"
]

chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]
user_agent = random.choice(user_agents)
chrome_options.add_argument(f'user-agent={user_agent}')
driver = uc.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

# 9 pages to scrape

def scrape_zonaprop():
    driver.get('https://www.zonaprop.com.ar/departamentos-venta-rosario.html')
    time.sleep(10)

    data = []
    count = 1
    while count<=2:
        cards_container = driver.find_elements(by=By.CSS_SELECTOR, value=".CardContainer-sc-1tt2vbg-5.fvuHxG")
        for card in cards_container:
            # price_container = card.find_element(by=By.CSS_SELECTOR, value=".PriceContainer-sc-12dh9kl-2.ePWLec")
            # address_location = card.find_element(by=By.CSS_SELECTOR, value=".LocationBlock-sc-ge2uzh-1.cVCbkm").text.split("\n")

            data.append({
                'url'       : card.find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href'),
                # 'address'   : address_location[0],
                # 'location'  : address_location[1],
                # 'price'     : price_container.find_element(by=By.CSS_SELECTOR, value=".Price-sc-12dh9kl-3.geYYII").text
            })
        if count != 2:
            links_nex_page_container = driver.find_element(by=By.CSS_SELECTOR, value=".Container-sc-n5babu-0.gQpXFk")
            driver.get(links_nex_page_container.find_elements(by=By.CSS_SELECTOR, value="a")[-1].get_attribute('href'))
        count+=1

    driver.quit()
    print(data)
    print(data.__len__())

# scrape_zonaprop()
