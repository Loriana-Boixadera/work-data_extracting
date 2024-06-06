from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
options.add_argument("start-maximized")
options.add_argument('disable-infobars')

def scrape_zonaprop():
    driver.get('https://www.zonaprop.com.ar/departamentos-venta-rosario.html')

    cards_container = driver.find_elements(by=By.CSS_SELECTOR, value=".CardContainer-sc-1tt2vbg-5.fvuHxG")
    data = []
    pages = 2
    for page in range(pages):
        for card in cards_container:
            price_container = card.find_element(by=By.CSS_SELECTOR, value=".PriceContainer-sc-12dh9kl-2.ePWLec")
            address_location = card.find_element(by=By.CSS_SELECTOR, value=".LocationBlock-sc-ge2uzh-1.cVCbkm").text.split("\n")

            data.append({
                'url'   : card.find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href'),
                'address': address_location[0],
                'location': address_location[1],
                'price' : price_container.find_element(by=By.CSS_SELECTOR, value=".Price-sc-12dh9kl-3.geYYII").text
            })
        links_nex_page_container = driver.find_element(by=By.CSS_SELECTOR, value=".Container-sc-n5babu-0.gQpXFk")
        link_next_page = links_nex_page_container.find_elements(by=By.CSS_SELECTOR, value="a")[-1].get_attribute('href')
        driver.get(link_next_page)
        time.sleep(5)
        # TIME EXCEPTION ERROR IS GIVEN
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
        time.sleep(20)

    driver.quit()
    print(data)

# scrape_zonaprop()

def scrape_propia():
    driver.get('https://www.propia.com.ar/propiedades?operation=1&type=2&location_city_id=1')

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-primary']")))

    count=1
    while count<=12:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary']"))).click()
            count+=1
            time.sleep(15)
        except TimeoutException:
            break

    list_products = driver.find_elements(by=By.CSS_SELECTOR, value=".card")
    data = []
    for card in list_products:
        price, _ = card.find_element(by=By.CSS_SELECTOR, value='.col-md-4.prices').text.split("\n") 
        data.append({
            'url'   : card.find_element(by=By.CSS_SELECTOR, value='.col-md-8 > a').get_attribute("href"),
            'price' : price
        })

    driver.quit()
    print(data)
    print(data.__len__())

scrape_propia()

