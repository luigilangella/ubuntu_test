from bs4 import BeautifulSoup
import re
import requests
import os
import database_writer

# directory = r'C:\Users\richard.trivett\Desktop'
directory = '/home/luigi/Documents/Stats Requests'

HarlaxtonEnergy = '335'
VirginMedia = '414'
BristolWater = '290'
HafrenDyfrdwy = '505'
SouthernWater = '391'
SevernTrentWater = '382'
AnglianWater = '281'
ThamesWater = '402'


def download_now(html, folder):
    companyCode = ''
    make_directory = os.path.join(directory, folder)
    if not os.path.exists(make_directory):
        os.makedirs(make_directory)

    soup = BeautifulSoup(html, 'html.parser')

    orders = soup.find_all(class_='gridPlotItem')

    table = soup.find_all('table')[17]
    companies = re.findall('>(.*?)</td>', str(table))

    for index, order in enumerate(orders):
        company_list = [company for company in companies if 'supplied' in company]

        link = order.find('a')['href']
        href = re.search('/Controls.+', str(link))
        downloadLink = 'https://utilities.digdat.co.uk/' + href.group(0)

        filename = (company_list[index])

        if 'Virgin' in filename:
            companyCode = VirginMedia
            print(filename, companyCode)
        elif 'Bristol' in filename:
            companyCode = BristolWater
            print(filename, companyCode)
        elif 'Harlaxton' in filename:
            companyCode = HarlaxtonEnergy
            print(filename, companyCode)
        elif 'Hafren' in filename:
            companyCode = HafrenDyfrdwy
            print(filename, companyCode)
        elif 'Southern Water' in filename:
            companyCode = SouthernWater
            print(filename, companyCode)
        elif 'Severn' in filename:
            companyCode = SevernTrentWater
            print(filename, companyCode)
        elif 'Anglian' in filename:
            companyCode = AnglianWater
            print(filename, companyCode)
        elif 'Thames' in filename:
            companyCode = ThamesWater
            print(filename, companyCode)

        database_writer.insert_digdat_companies(digdat_id=DD_id(html), company=filename, company_id=companyCode)

        r = requests.get(downloadLink, verify=False)
        with open(os.path.join(directory, make_directory, companyCode + ' ' + filename) + '.pdf', 'wb') as f:
            f.write(r.content)

        print(downloadLink, company_list[index])


def DD_id(html):
    soup = BeautifulSoup(html, 'html.parser')

    orders = soup.find_all(class_='gridPlotItem')

    DigDat_Ref = orders[0].find('td').text.split(' ')[0]
    print(DigDat_Ref)
    return DigDat_Ref


def download_later():
    pass


# def package_and_send_files():


if __name__ == '__main__':
    with open('lastpagedigdat.html') as f:
        html_of_page = f.read()
        DD_id(html_of_page)
    # download_now(html_of_page)
