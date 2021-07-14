import requests
from selenium import webdriver
import time
import database_writer
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from passwordManager import CityFiberUsername, CityFiberPassword
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
send_to = 'svc.Proveit@kier.co.uk'
username = CityFiberUsername
password = CityFiberPassword


def spinner_frame_wait(driver):
    try:
        time.sleep(0.5)
        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.ID, 'emapsSpinner')))
    except TimeoutException:
        print("Timed out waiting for page to load")


def search_cityfibre(ref, es, no):
    print(search_id)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    driver = webdriver.Chrome(chrome_options=options)
    user_agent = driver.execute_script("return navigator.userAgent;")
    print(user_agent)
    driver.get(f'https://{username}:{password}@plant.cityfibre.com/index.html')
    driver.set_window_size(1936, 1056)
    driver.find_element_by_id('plant_tac_checkbox').click()
    driver.find_element_by_xpath('//*[@id="plant_tac_form"]/table/tbody/tr[2]/td[2]/input').click()
    time.sleep(2)
    driver.find_element_by_id('emailAddress').send_keys(send_to)
    driver.find_element_by_xpath('//*[@id="sidebar-controls"]/ul/li[3]/a/i').click()
    driver.find_element_by_id('easting').send_keys(es)
    driver.find_element_by_id('northing').send_keys(no)
    time.sleep(1)
    driver.find_element_by_id('goto').click()
    time.sleep(2)
    driver.find_element_by_id('title').clear()
    driver.find_element_by_id('title').send_keys(ref)
    driver.find_element_by_id('submit').click()

    spinner_frame_wait(driver)
    database_writer.insert_cityfibre_table(search_id=search_id)
    # input()
    database_writer.update_main_searches_cityfibre(search_id=search_id)
    driver.quit()


def cityfibre_search(ref, easting, northing):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    headers = {'User-agent': user_agent}
    url = f'https://plant.cityfibre.com/gss?json=true&service=ejb%2FEmapsLocal&method=requestEmapV2&crs=EPSG%3A27700&centre={easting}%2C{northing}&view_scale=2500&rotation=2&layout_type=emap_2500&email_address=proveit%40kier.co.uk&title={ref}'
    r = requests.get(url=url, headers=headers)
    print(r.text)

    database_writer.insert_cityfibre_table(search_id=search_id)
    database_writer.update_main_searches_cityfibre(search_id=search_id)
    time.sleep(10)


if __name__ == '__main__':
    while True:
        # cityfibre_check = database_writer2.query_searches_main_cityfibre_resubmit2()  # checks for CityFibre return form the last 'n' minutes. If no return is found, resumbmits
        # if cityfibre_check:
        #     database_writer2.update_searches_main_cityfibre_to_null(cityfibre_check[0])
        database_writer.resubmit_missing_cityfibre()
        row = database_writer.query_searches_main_cityfibre()
        if row:
            search_id = database_writer.query_searches_main_cityfibre()[0]
            x = database_writer.query_searches_main_cityfibre()[7]
            y = database_writer.query_searches_main_cityfibre()[8]
            print('search found!', search_id)
            try:
                cityfibre_search(ref=search_id, easting=str(x), northing=str(y))
                # search_cityfibre(ref=search_id, es=str(x), no=str(y))
            except Exception as e:
                print(e)
                time.sleep(30)
        else:
            print('looking for new searches...')
            time.sleep(8)
