from fpdf import FPDF
import re
import os
import datetime
import database_writer
import pandas as pd

search_id = '3D072ZAQQ3'
base_path = rf'\\p-fp-032\Data1BackedUp\Prove IT Working Data\STATS Requests\{search_id}'
companies_list = []

disclaimer = """Whilst every effort has been taken to ensure the accuracy of the data in this STATS Pack the information enclosed should not be used for any purpose other than as a general guide to the location of existing services.
"""
help = 'For help and support please email GIS@kier.co.uk'

kier_image_width = 100
kier_image_adjuster = 0.443333333333333
plus90days = str(datetime.date.today() + datetime.timedelta(days=90))


def get_company_name(company_id):
    df = pd.read_csv(r'Company_IDs.csv')
    row = df.query(f'id == {company_id}')
    company_name = row['name'].item()
    companies_list.append([company_name, str(expiry)])


pdf = FPDF('P', 'mm', 'A3')
pdf.add_page()

pdf.image(r'images\1200px-Kier_Group_logo.svg.png', w=kier_image_width, h=round(kier_image_width * kier_image_adjuster))
pdf.image(r'images\Prove-IT.jpg', x=100, y=70)
pdf.ln(70)

# disclaimer
pdf.set_font('Helvetica', '', 20)
pdf.cell(0, 10, 'disclaimer', ln=True, align='C')
pdf.set_font('Helvetica', '', 16)
pdf.multi_cell(0, 10, disclaimer, ln=True)
pdf.ln(5)

# add companies
pdf.cell(0, 10, 'Featured Utilities', ln=True, align='C')

digdat_companies = database_writer.query_digdat_table_cover_sheet(search_id=search_id)
lsbud_companies = database_writer.query_lsbud_table_cover_sheet(search_id=search_id)
azure_files = database_writer.query_files_table_cover_sheet(search_id=search_id)

for digdat_company in digdat_companies:
    parsed_digdat_company = " ".join(digdat_company[0].replace('supplied by', '').split())
    companies_list.append([parsed_digdat_company, plus90days])


for lsbud_company in lsbud_companies:
    companies_list.append([lsbud_company[0], plus90days])

for azure_file in azure_files:
    company_code = str(azure_file[1]).strip()
    parse_date = re.search(r'(\d{8})-', azure_file[0])

    try:
        expiry = datetime.datetime.strptime(parse_date.group()[:-1], "%Y%m%d").date()
    except AttributeError:
        expiry = 'N/A'
    print(expiry)
    get_company_name(company_code)

pdf.cell(200, 10, 'Company', border=1, align='C')
pdf.cell(0, 10, 'Expiry Date', ln=True, border=1, align='C')

for plan in companies_list:
    print(plan[0])
    pdf.cell(200, 10, plan[0], border=1, align='C')
    pdf.cell(0, 10, plan[1], ln=True, border=1, align='C')

pdf.ln(10)

#  help and support
pdf.cell(0, 10, help, ln=True, align='C')

pdf.output(r'images\pdf1.pdf')
