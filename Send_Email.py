import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from passwordManager import ProveitEmail, ProveitPassword, u, p
from email.mime.base import MIMEBase
from email import encoders
import os
from html_proveit import html_email, html_email_download
import database_writer
import store_to_Azure_blob
from store_to_Azure_blob import account_name, container_name, connection_string
from arcgis.gis import GIS
import json


def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location=''):
    email_sender = 'gis@kier.co.uk'  # proveit@kier.co.uk

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'html'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        with open(attachment_location, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(ProveitEmail, ProveitPassword)
            text = msg.as_string()
            server.sendmail(email_sender, email_recipient, text)
            print('email sent')
    except Exception as e:
        print(e)
    return True


def send_email_plain_text(email_recipient,
                          email_subject,
                          email_message,
                          attachment_location=''):
    email_sender = 'gis@kier.co.uk'  # proveit@kier.co.uk

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        with open(attachment_location, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(ProveitEmail, ProveitPassword)
            text = msg.as_string()
            server.sendmail(email_sender, email_recipient, text)
            print('email sent')
    except Exception as e:
        print(e)
    return True


def get_file_size(path):
    """tests for the file size"""
    size_in_bytes = os.path.getsize(path)
    file_size = (round(size_in_bytes / 1024))
    print(file_size)
    return file_size


def url_to_feature():

    """queries layer for search_id and updates the url field with download link"""
    print('here')
    gis = GIS(username=u, password=p)
    search_results = gis.content.search('title: New_STATS_Requests', 'Feature Layer')
    l1 = search_results[0]
    l1 = l1.layers
    flayer = l1[0]
    query_result1 = flayer.query(where=f"search_id = '{search_id}'")
    query_result1.features[0].attributes['dlurl'] = f'{url}'
    query_result1.features[0].attributes['processed'] = 'Complete'

    flayer_row = query_result1.sdf
    email = flayer_row['email'][0]
    if str(email).lower() == 'geopal@geopal.co.uk':
        send_via_API(link=url, ref=user_ref)
        api = True
    else:
        api = False

    flayer.edit_features(updates=query_result1.features)
    return api


def send_via_API(link, ref):
    url = link
    ref = ref
    endpoint = 'https://iot.test.geopalsolutions.co.uk/iot/c100001_proveitreceivefileinfo'
    json_ = {
        "url": url,
        "reference": ref
    }
    request_json = json.dumps(json_)
    r = requests.post(url=endpoint, data=request_json)
    print('API request response code:', r.status_code)


if __name__ == '__main__':
    directory = '/home/luigi/Documents/Stats Requests'
    while True:
        data_ready = database_writer.query_ready_to_send()
        if data_ready:
            user_email = data_ready[1]
            user_name = data_ready[4]
            user_ref = data_ready[9]
            search_id = data_ready[0]
            contract = data_ready[10]
            if contract == 'BTONSA':
                file_path = os.path.join(directory, f'zips/{search_id}.zip')
            elif contract == 'openreachswindon':
                file_path = os.path.join(directory, f'zips/{search_id}.zip')

            else:
                file_path = os.path.join(directory, f'pdfs/{search_id}.pdf')
            blob_name = os.path.basename(file_path)

            print('sending', file_path)

            try:
                store_to_Azure_blob.upload_blob(connection_string=connection_string, file_path=file_path,
                                                blob_name=blob_name)
            except Exception as e:
                print(e)

            blob = store_to_Azure_blob.get_blob_sas(blob_name)
            url = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + blob
            print('the url = ', url)

            if get_file_size(file_path) < 19000:
                print('file size okay')
            else:
                print('File size too large, only download link will be sent')
                file_path = ''
            try:
                if url_to_feature():
                    pass
                else:
                    send_email(email_recipient=user_email, email_subject=f'Prove-IT STATS Pack for {user_ref}',
                               email_message=html_email_download(user_ref, hyperlink=url),
                               attachment_location='')  # file_path

                database_writer.update_main_searches_data_sent(search_id=search_id)
            except Exception as e:
                print(e)
                database_writer.update_main_searches_ready_to_send(search_id=search_id)
                time.sleep(5)

        print('scanning rows')
        time.sleep(5)
