from selenium import webdriver
from selenium.webdriver.support.ui import Select
import database_writer
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
import random
import datetime
import Send_Email
import os
from passwordManager import edit_u, edit_p, allan_email, allan_password, rich_u, rich_p, aiman_username, aiman_password, ellie_u, ellie_p, matt_u, matt_p, casey_u, casey_p, jose_u, jose_p, erin_u, erin_p, Tom_u, Tom_p, sergiu_u, sergiu_p, robertu, robertp, rebeccau, rebeccap, andrewu, andrewp, heliu, helip
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

random_number = random.randint(20, 50)
todays_date = datetime.date.today()
plus90days = todays_date + datetime.timedelta(days=random_number)
scheme_date = plus90days.strftime('%d/%m/%Y')
company_ignore_list = ['Concept Solutions People Ltd', 'Jurassic Fibre Ltd']
directory = '/home/luigi/Documents/Stats Requests'

# user = 'new user'  # the user variable is the email of the person who submitted the search
# request_id = 1  # the unique reference that ties the DigDat and LSBUD searches together
timeout = 120

# Start_Date = '19/04/2021'
# End_Date = '19/04/2021'
# Reference = 'H357864'
Scale = '2500'
On_Behalf_of = 'Other'
Authority = ''
# Easting = '294750'
# Northing = '91750'


credentials = [
    (casey_u, casey_p),
    (matt_u, matt_p)
               ]


def random_account_picker():
    """randomly selects account details from list of tuples"""
    random_choice = random.randint(0, len(credentials) - 1)
    u = credentials[random_choice][0]
    p = credentials[random_choice][1]
    return u, p


def quickwait():
    time.sleep(random.uniform(1, 2))


def longwait():
    time.sleep(randint(2, 3))


def superquickwait():
    time.sleep(random.uniform(0.3, 1.3))


def run_search(easting, northing, search_id, reference):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    url = 'https://onecall.linesearchbeforeudig.co.uk/uk-b4-en/Account/Login'
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    # driver.maximize_window()
    driver.set_window_size(1936, 1056)
    actions = ActionChains(driver)
    account_details = random_account_picker()  # invokes random account picker function
    driver.find_element_by_css_selector(
        '#mui-useraname-error > div > div > div.text-field-input > input[type=text]').send_keys(account_details[0])
    # driver.find_element_by_css_selector(
    #     '#loginForm > div > div:nth-child(2) > div > div.text-field-input > input[type=password]').send_keys(
    #     account_details[1])
    script = f'document.querySelector("#loginForm > div > div:nth-child(2) > div > div.text-field-input > input[type=password]").value = "{account_details[1]}";'
    driver.execute_script(script)
    quickwait()  # waiting...

    hover = driver.find_element_by_css_selector(
        '#loginForm > div > div.checkbox.checkbox-primary.login-checkbox > label > span > a')
    actions.move_to_element_with_offset(hover, -5, 0).click().perform()

    quickwait()  # waiting...
    user_agent = driver.execute_script("return navigator.userAgent;")
    print(user_agent)
    size = driver.get_window_size()
    print(size)
    driver.find_element_by_id('login-submit').click()

    # Commence Search ---------------------------------------------------------

    longwait()  # waiting...
    quickwait()  # waiting...

    try:
        driver.find_element_by_xpath('//*[@id="WorkBenchPanel"]/div/div[3]/div/div[2]').click()
    except Exception as e:
        print(e, 'could not find by xpath')
        driver.find_element_by_css_selector('#WorkBenchPanel > div > div:nth-child(4) > div > div.BenchTool.NewEnquiry.Orange').click()
        print('found by css selector!')

    quickwait()  # waiting...

    driver.find_element_by_id('NewEnquiry.CommencesOn').send_keys(scheme_date)
    superquickwait()  # waiting...
    driver.find_element_by_id('NewEnquiry.CompletesOn').send_keys(scheme_date)
    superquickwait()  # waiting...
    driver.find_element_by_id('NewEnquiry.UserReference').send_keys(search_id)
    superquickwait()  # waiting...
    scale_dropdown = Select(driver.find_element_by_id('NewEnquiry.PaperPlanScale'))
    scale_dropdown.select_by_visible_text(Scale)
    superquickwait()
    behalf_of_dropdown = Select(driver.find_element_by_id('NewEnquiry.WorkingOnBehalfOf'))
    behalf_of_dropdown.select_by_visible_text(On_Behalf_of)
    superquickwait()  # waiting...

    # authority_dropdown = Select(driver.find_element_by_id('NewEnquiry.WorkingOnBehalfOfAuthority'))
    # authority_dropdown.select_by_visible_text(Authority)
    quickwait()  # waiting...

    driver.find_element_by_css_selector(
        '#EnquiryDetailsPanel > div > div > div > table:nth-child(4) > tbody > tr > td:nth-child(2) > div > button').click()
    quickwait()  # waiting...

    driver.find_element_by_css_selector('#Coordinates\.East').send_keys(easting)
    superquickwait()
    driver.find_element_by_css_selector('#Coordinates\.North').send_keys(northing)

    quickwait()  # waiting...

    driver.find_element_by_xpath(
        '//*[@id="EnquiryLocationPanel"]/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/div/button').click()

    longwait()  # waiting...

    # submit search................................................................................
    driver.find_element_by_css_selector(
        '#EnquiryLocationPanel > div > div > div:nth-child(4) > div > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2) > div > button').click()

    longwait()
    time.sleep(4)

    driver.find_element_by_css_selector(
        '#EnquirySummaryListsPanel > div > div:nth-child(7) > div:nth-child(2) > div:nth-child(2) > h4.Blue > span').click()
    quickwait()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    blue_table = soup.find(class_='BlueList')
    enquiry_id = soup.find(id='SubmittedEnquiry.Id').text

    # this block of code parses the blue tables and extracts the contents...........................
    for t_row in blue_table.find_all("tr"):
        cells = t_row.find_all("td")
        if len(cells) == 0:
            pass
        else:
            blue_company = cells[0].text
            contact_number = cells[2].text
            preferred_contact_method = cells[1].text
            database_writer.insert_LSBUD_table_blue(search_id=search_id, lsbud_ref=enquiry_id,
                                                    company_name=blue_company, contact_number=contact_number,
                                                    preferred_contact_method=preferred_contact_method)

    # the following block of code parses the red table and extracts the companies....................

    red_table = soup.find(class_='RedList')
    red_data = red_table.find_all('tr')
    table_contents = []
    for data_row in red_data:
        table_contents.append(data_row.text.split('\n'))
    df = pd.DataFrame(table_contents)
    df = df.T.set_index(0).T

    # Write the new searches to the database..........................................................
    for index, _ in df.iterrows():
        company = df['Asset Owner'][index]
        status = df['Status'][index]

        database_writer.insert_LSBUD_table(company_name=company, lsbud_ref=enquiry_id, search_id=search_id,
                                            search_status_type=status)

        NG = 'National Grid Gas (Above 7 bar), National Grid Gas Distribution Limited (Above 2 bar) and National Grid Electricity Transmission'
        if company != NG:
            if status == 'Email Additional Info':
                database_writer.update_lsbud_table(company=company, lsbud_ref=enquiry_id)  # email additional info handling

        if company in company_ignore_list:
            # if company found in ignore list set search_complete to false
            database_writer.update_lsbud_table_difficult_companies(company=company, lsbud_ref=enquiry_id)

    # If no companies are found update database and creates a LSBUD txt file in the search id directory
    if len(red_data) == 1:
        save_path = os.path.join(directory, search_id)

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path, '0 LSBUD-.txt'), 'w') as f:
            f.write('lsbud file')
            print('lsbud txt created!!!!')
        database_writer.update_main_searches_LSBUD_data_received(search_id=search_id)

    print('search successful!')
    driver.quit()
    database_writer.update_main_searches_LSBUD(search_id=search_id)  # updates main table with completed search


if __name__ == "__main__":
    while True:
        # row = database_writer2.query_searches_main_lsbud()  # looks for new and incomplete searches in main table
        row = database_writer.lsbud_account_2()  # looks for 1s
        if row:
            search_values = list(row)
            print(search_values)
            print('new search found')
            try:
                run_search(easting=str(search_values[7]), northing=str(search_values[8]), search_id=search_values[0],
                           reference=search_values[9])
            except Exception as e:
                print(e)
        print('searching....')
        time.sleep(8)
