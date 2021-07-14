from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import database_writer
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import DigDatDownloader
import re
import random
from passwordManager import KarlU, KarlP, AimanU, AimanP, AndrewU, AndrewP, LuigiU, LuigiP, RebeccaU, RebeccaP, RobertU, RobertP
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

HarlaxtonEnergy = '335'
VirginMedia = '414'
BristolWater = '290'
HafrenDyfrdwy = '505'
SouthernWater = '391'
SevernTrentWater = '382'
AnglianWater = '281'
ThamesWater = '402'

# paper size IDs
A0 = "mapctrl_sidebar_editborder_papersize_group_A0"
A2 = "mapctrl_sidebar_editborder_papersize_group_A2"
A1 = "mapctrl_sidebar_editborder_papersize_group_A1"

url = 'https://utilities.digdat.co.uk/Account/Login.aspx?ReturnUrl=%2fAccount%2fMyAccount.aspx'


def random_wait():
    random.uniform(0.5, 2)


def spinner_frame_wait(driver):
    try:
        time.sleep(0.5)
        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_WaterMap_spinner_frame')))
    except TimeoutException:
        print("Timed out waiting for page to load")


def submit_search(easting, northing, search_id, reference='', user='', password=''):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(chrome_options=options)
    user_agent = driver.execute_script("return navigator.userAgent;")
    print(user_agent)
    driver.get(url)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtUserName').send_keys(LuigiU)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtPassword').send_keys(LuigiP)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginButton').click()
    driver.set_window_size(1936, 1056)
    # driver.maximize_window()

    timeout = 120
    try:
        element_present = EC.presence_of_element_located((By.ID, 'sidebar_searchtype_select'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    ddEl = Select(driver.find_element_by_id('sidebar_searchtype_select'))
    ddEl.select_by_visible_text('Co-ordinates')
    driver.find_element_by_id('sidebar_easting').clear()
    time.sleep(0.2)
    driver.find_element_by_id('sidebar_easting').send_keys(easting)
    driver.find_element_by_id('sidebar_northing').clear()
    time.sleep(0.2)
    driver.find_element_by_id('sidebar_northing').send_keys(northing)
    time.sleep(0.2)
    driver.find_element_by_xpath(
        '//*[@id="sidebar_searchtype_location"]/table/tbody/tr[1]/td[2]/span[1]').click()
    spinner_frame_wait(driver)
    driver.find_element_by_xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_WaterMap_panel"]/div[1]/span[4]').click()
    time.sleep(0.5)
    driver.find_element_by_id('mapctrl_sidebar_editborder_title').send_keys(search_id)
    ddEl = Select(driver.find_element_by_id('mapctrl_sidebar_editborder_printscale'))
    ddEl.select_by_visible_text('1:1250')
    spinner_frame_wait(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    find_datasets = soup.find('div', class_='listbox short inline_block')
    datasets = re.findall('mapctrl.+?"', string=str(find_datasets))

    for dataset in set(datasets):  # select datasets
        # if 'Harlaxton' not in dataset:
            if 'Ordnance' not in dataset:
                driver.find_element_by_id(dataset[:-1]).click()
                random_wait()
    # input()
    ddEl = Select(driver.find_element_by_id('mapctrl_sidebar_editborder_printscale'))
    ddEl.select_by_visible_text('1:1000')
    driver.find_element_by_id(A2).click()

    spinner_frame_wait(driver)
    driver.find_element_by_id('mapctrl_sidebar_confirm').click()
    time.sleep(0.5)
    driver.find_element_by_name('SelectBorder_Sidebar').click()
    random_wait()
    driver.find_element_by_id('border_addbasket0').click()
    random_wait()
    driver.find_element_by_id('mapctrl_lightbox_confirm').click()
    random_wait()
    spinner_frame_wait(driver)
    random_wait()
    driver.find_element_by_class_name('big_button_linked').click()
    random_wait()
    try:
        element_present = EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_chkTermsAndConditions'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.find_element_by_id('ctl00_ContentPlaceHolder1_chkTermsAndConditions').click()

    driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnContinue').click()

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'gridPlotItem'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    for num in range(60):  # looks within the html for the downloads to be ready. cycles through 60 times before closing and submitting search again
        htmlorderpage = driver.page_source
        soup = BeautifulSoup(htmlorderpage, 'html.parser')
        grid_items = len(soup.find_all(class_='gridPlotItem'))
        link_items = len(soup.find_all('a', id=re.compile('_lnkPdf')))
        download_error = len(soup.find_all(id=re.compile('_error')))
        print(f'downloads available {link_items}/{grid_items}')

        if download_error:
            print('error!')
            time.sleep(300)
            driver.quit()

        if num > 60:
            break

        time.sleep(2)

        if link_items == grid_items:
            DigDatDownloader.download_now(htmlorderpage, folder=search_id)
            database_writer.update_main_searches_DigDat_data_received(search_id)  # updates main table to data received

            database_writer.insert_DigDat_table(search_id=search_id,
                                                 digdat_ref=DigDatDownloader.DD_id(htmlorderpage))
            database_writer.update_main_searches_DD(search_id)
            break

    driver.quit()


if __name__ == "__main__":
    while True:
        # row = database_writer2.query_searches_main_digdat()  # looks for new and incomplete searches in the digdat table
        row = database_writer.digdat_account_2()  # looks for 1s
        if row:
            search_values = list(row)
            print('new search found')
            try:
                submit_search(easting=str(search_values[7]), northing=str(search_values[8]), search_id=search_values[0],
                              reference=search_values[9])
            except Exception as e:
                print(e)

        print('searching....')
        time.sleep(8)
