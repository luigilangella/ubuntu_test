import concurrent.futures
import time
import PyPDF2
from PyPDF2 import PdfFileMerger
import os
from PIL import Image
import pandas as pd
import re
import database_writer
import shutil
from azure.storage.blob import BlobClient
from passwordManager import connection_string
import zipfile

# has csv dependencies!!!!!


directory = '/home/luigi/Documents/Stats Requests'
working_directory = os.getcwd()


def company_name_parser(f, search_id):
    pattern = re.search(r'-(\d{3}\s)|_(\d{3}\s)|(\d{3}\s)', f)
    print(f, search_id)

    if pattern is not None:
        reader = pd.read_csv('Company_IDs.csv')
        if re.search(r'^\d{3}\s', f):
            row = reader.query(f'id == {pattern.group()}')
        else:
            row = reader.query(f'id == {pattern.group()[1:]}')
        company_name = row['name'].item()

        if 'NO ASSETS AFFECTED' in f.upper():
            return company_name + ' Not Affected'
        elif 'NOT AFFECTED' in f.upper():
            return company_name + ' Not Affected'
        elif 'LETTER' in f.upper():
            return company_name + ' Letter'
        elif 'SUPPLY' in f.upper():
            return company_name + ' Supply'
        elif 'WASTE' in f.upper():
            return company_name + ' Waste'
        else:
            return company_name
    elif 'LSBUD' in f:
        company_name = 'Linesearch'
        return company_name
    else:
        company_name = 'Other'
        return company_name


def ignore_list(ignore):
    string_list = ['Charging Structure', 'can-you-dig-it-dial-before-you-dig', 'Lookout Look Up',
                   'Avoidance of Danger', 'general_condns', 'gen_condns_wwu', 'additional_high_pressure_conditions',
                   'Dig Safely Measures to avoid injury', 'Boundary Key', 'Safety-Info_GAS',
                   'WPD Webmap Letter and Guidance Notes',
                   'Guidelines when working in vicinity', 'Dig Safely Measures', "Know what's below",
                   'Valve safety advice',
                   'Map key', 'Safe working practices in the vicinity', 'Watch Out Cables About ', 'Safety-Info_GAS',
                   'Guide to Interpreting', 'Safety_Info', 'symbol_guides', 'Excavation leaflet', 'SESW Symbols',
                   'HSG47', '_WPD ', '406 South', 'Eastern_symbol_guide']
    for i in string_list:
        if re.search(i, ignore):
            return True
    else:
        return False


def compile_pdf(grid, search_id):
    print(grid, search_id)
    base_path = os.path.join(directory, search_id)  # base path of your files you wish to append
    image_bucket = os.path.join(directory,
                                'pdf_staging')  # path where image file will be converted to pdf ready for appending
    merger = PdfFileMerger(strict=False)
    file_list = [file for file in os.listdir(base_path) if
                 file.upper().endswith('PDF') or file.upper().endswith('PNG')]  # filters out all mgs files

    for find_wpd in file_list:
        if re.search('\d{8}_WPD', find_wpd):
            rotate_pdf(find_wpd, search_id)
            wpdr = '422 western power rotated.pdf'
            if wpdr in file_list:
                wpd_index = file_list.index(wpdr)
                file_list.pop(wpd_index)

            file_list.append(wpdr)  # appends the rotated WPD map to the compiling list

    for file in file_list:

        if ignore_list(file):
            pass
        else:
            parsed_name = company_name_parser(file, search_id)
            file_name, ext = (os.path.splitext(file))  # file name without file extension
            file_location = os.path.join(base_path, file)
            pdf_save_location = os.path.join(image_bucket, file_name + '.pdf')

            if file.upper().endswith('.PDF'):
                merger.append(file_location, parsed_name)

            else:
                image_to_pdf = Image.open(file_location)
                image1 = image_to_pdf.convert('RGB')
                image1.save(pdf_save_location)
                merger.append(pdf_save_location, parsed_name)
    merged_pdf_location = fr'{directory}\pdfs\{search_id}.pdf'
    merger.setPageMode('/UseOutlines')
    merger.write(merged_pdf_location)
    merger.close()
    return merged_pdf_location


def zip_files(search_id):
    zip_file_location = fr'{directory}\zips\{search_id}'
    file_location = os.path.join(directory, search_id)
    shutil.make_archive(zip_file_location, 'zip', file_location)


def GeoPal_zip(search_id, png_file):
    try:
        download_png(png_file=png_file)
        zip_file_location = fr'{directory}\pngs'
        pdf_file_location = fr'{directory}\pdfs\{search_id}.pdf'
        png_location = os.path.join(directory, 'pngs', png_file)
        with zipfile.ZipFile(os.path.join(zip_file_location, search_id + '.zip'), 'w') as zip_file:
            os.chdir(os.path.dirname(pdf_file_location))
            zip_file.write(os.path.basename(pdf_file_location))
            os.chdir(os.path.dirname(png_location))
            if os.path.exists(png_location):
                zip_file.write(os.path.basename(png_location))
    except Exception as e:
        print(e)


def rotate_pdf(wpd_file, search_id):
    base_path = os.path.join(directory, search_id)

    pdf_in = open(os.path.join(base_path, wpd_file), 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in, strict=False)
    pdf_writer = PyPDF2.PdfFileWriter()
    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(90)
        pdf_writer.addPage(page)
    pdf_out = open(os.path.join(base_path, '422 western power rotated.pdf'), 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()


def retrieve_folder_data(tile, copy_to, search_id):
    root_of_files = str(database_writer.query_lookup_directories_table(tile_name=tile)[0])
    list_files = os.listdir(root_of_files)
    for file in list_files:
        if not re.search('\d{8}-\d{8}', file):
            print(file, search_id)
            shutil.copyfile(os.path.join(root_of_files, file), os.path.join(copy_to, file))


def download_png(png_file):
    """downloads sww png from Azure"""

    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="swwpngs", blob_name=png_file)
    if blob.exists():
        with open(os.path.join(directory, 'pngs', png_file), "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)
    else:
        print('no png')


def download_files(tile, download_to, search_id):
    """downloads files from Azure"""
    for blob in database_writer.return_files_list(tile):
        blob_name = blob[0].replace('https://delveblobstore.blob.core.windows.net/files/', '')
        print(blob_name, search_id, 'from Azure')
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="files",
                                                 blob_name=blob_name)
        with open(os.path.join(download_to, os.path.basename(blob_name)), "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)


def run(row):
    grid = row[6]
    search_id = row[0]
    email = row[1]
    contract = row[10]
    user_ref = row[9]
    row_id = row[23]
    copy_to_path = os.path.join(directory, search_id)
    if not os.path.exists(copy_to_path):
        os.makedirs(copy_to_path)

    try:
        download_files(tile=grid, download_to=copy_to_path, search_id=search_id)
        # retrieve_folder_data(tile=grid, copy_to=copy_to_path, search_id=search_id)

    except Exception as e:
        print(e, 'Could not retrieve data')


    print(search_id, user_ref)

    linesearch_found = [linesearch for linesearch in os.listdir(copy_to_path) if '0 LSBUD-' in linesearch]

    if linesearch_found:
        if contract == 'BTONSA' or contract == 'openreachswindon':  # zips all individual files for the contract rather than compiling pdf
            zip_files(search_id=search_id)
            print('ready to send!')
            database_writer.update_main_searches_ready_to_send_mutlithreader(row_id=row_id)

        elif str(email).lower() == 'geopal@geopal.co.uk':
            compile_pdf(grid=grid, search_id=search_id)
            GeoPal_zip(search_id=search_id, png_file=grid + '.png')
            print('ready to send!')
            database_writer.update_main_searches_ready_to_send_mutlithreader(row_id=row_id)

        else:
            compile_pdf(grid=grid, search_id=search_id)
            print('ready to send!')
            database_writer.update_main_searches_ready_to_send_mutlithreader(row_id=row_id)

    else:
        print('LSBUD not found yet')


if __name__ == '__main__':
    while True:
        try:
            rows = database_writer.query_main_table_to_compile()  # retrieves the next row ready for compiling
            if rows:
                with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
                    executor.map(run, rows)
            else:
                print('looking for new rows ready for compiling...')
        except Exception as e:
            print(e)
            time.sleep(2)

        time.sleep(10)
