import requests
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import database_writer
from passwordManager import u, p, ProveitEmail, ProveitPassword
import random
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
email = ProveitEmail  
password = ProveitPassword  


def superquickwait():
    time.sleep(random.uniform(0.3, 2))


def run_search(search_id, easting, northing):
    # launch website and configure option settings
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    url = 'https://pe.gtc-uk.co.uk/Plant_Enquiry/Account/Login'
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.set_window_size(1936, 1056)
    actions = ActionChains(driver)

    # login
    driver.find_element_by_id('Email').send_keys(email)
    superquickwait()
    driver.find_element_by_id('Password').send_keys(password)
    superquickwait()
    driver.find_element_by_css_selector('#loginForm > form > fieldset > input[type=submit]').click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'UserReference'))).send_keys(search_id)
    superquickwait()
    driver.find_element_by_id('Eastings').send_keys(easting)
    superquickwait()
    driver.find_element_by_id('Northings').send_keys(northing)
    superquickwait()
    driver.find_element_by_xpath('//*[@id="body"]/section/form/fieldset/input').click()

    hover = driver.find_element_by_id('OpenLayers_Map_7_OpenLayers_ViewPort')

    def twitch(number_1, number_2):
        return random.uniform(number_1, number_2)

    print(hover.size)

    actions.move_to_element_with_offset(hover, twitch(857, 860), twitch(331, 335)).click().perform()

    actions.move_to_element_with_offset(hover, twitch(894, 896), twitch(331, 335)).click().perform()

    actions.move_to_element_with_offset(hover, twitch(894, 896), twitch(367, 370)).click().perform()

    actions.move_to_element_with_offset(hover, twitch(857, 860), twitch(367, 370)).double_click().perform()
    time.sleep(5)
    driver.find_element_by_id('submitEnquiry').click()
    time.sleep(10)
    m = driver.page_source
    print('Search successful!')
    database_writer.update_main_searches_gtc_search_complete(value='true', search_id=search_id)
    driver.quit()
    time.sleep(20)


def query_gtc_layer(x, y):
    gis = GIS(username=u, password=p)
    url = f'https://services2.arcgis.com/4mdxlPzHnZKtJJX9/arcgis/rest/services/GTC_Polygons/FeatureServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry={x}%2C+{y}&geometryType=esriGeometryPoint&inSR=27700&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=27700&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&returnTrueCurves=false&distance=40&resultOffset=&resultRecordCount=&f=pjson'
    layer = FeatureLayer(gis=gis, url=url)
    sites = layer.properties.features
    for num, site in enumerate(sites):
        print(num, site["attributes"]['PROJECT_RE'])
    return len(sites)


def generate_token(user, password):
    """function no longer in use"""

    url = f'https://www.arcgis.com/sharing/generateToken?f=json&username={user}&password={password}&referer=https%2F%2F.arcgis.com%2F'
    r = requests.post(url)
    return r.json()['token']


if __name__ == '__main__':
    while True:
        row = database_writer.query_main_GTC()
        if row:
            search_values = list(row)
            easting = str(search_values[7])
            northing = str(search_values[8])
            search_id = search_values[0]
            print('new search found', search_id)
            try:
                if query_gtc_layer(easting, northing) > 0:
                    print('sites found!')
                    run_search(easting=easting, northing=northing, search_id=search_id)
                else:
                    print('no GTC in area')
                    database_writer.update_main_searches_gtc_search_complete(value='no sites in area',
                                                                             search_id=search_id)
                    database_writer.update_main_searches_gtc_data_received('no sites in area', search_id=search_id)

            except Exception as e:
                print(e)
        else:
            print('scanning...')
            time.sleep(5)
