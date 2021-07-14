import time
from itertools import islice
import requests
from imapclient import IMAPClient
import os
import email
from passwordManager import ProveitEmail, ProveitPassword
import database_writer
import re
from bs4 import BeautifulSoup

HOST = 'outlook.office365.com'  # IMAP Host Server
MAILBOX = 'INBOX/GTC'  # Mailbox to check


# extracts the body from the email
def get_body(msg):  # Need to use that raw var below
    if msg.is_multipart():  # If the message is a multipart(returns True)
        return get_body(msg.get_payload(0))  # Returns the payload
    else:
        return msg.get_payload(None, True)  # Returns nothing


def download(raw_data, search_id):
    root_dir = f'/home/luigi/Documents/Stats Requests/{search_id}'
    Email = ProveitEmail
    Password = ProveitPassword
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.116 Safari/537.36'}
    url = 'https://pe.gtc-uk.co.uk/Plant_Enquiry/Account/Login'

    body = str(get_body(raw_data))
    soup = BeautifulSoup(body, 'html.parser')
    links = soup.find_all('a')  # finds all links
    # print(len(links))  # Prints the number of links in the email

    for num, link in islice(enumerate(links), 0, None):
        pattern = re.search(r'([A-Z]+\d{7}).', link.text, re.IGNORECASE)
        if pattern:
            # print(num, pattern.group(1))

            login_data = {'Email': Email, 'Password': Password}
            # input('press enter')

            with requests.Session() as s:
                r1 = s.get(url, headers=headers)
                soup = BeautifulSoup(r1.content, 'html.parser')
                login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']

                s.post(url, data=login_data, headers=headers)

                req = s.get(link.get('href'))

                file_name = re.sub(r'[^\s\w\.]', '', link.text)
                print(num, os.path.join(root_dir, file_name))

                with open(os.path.join(root_dir, '333 ' + file_name), 'wb') as f:
                    f.write(req.content)


def process_email():
    messages = server.search('ALL')
    print('number of emails in folder', len(messages))  # number of new emails
    response = server.fetch(messages, ['FLAGS', 'BODY', 'RFC822.SIZE', 'ENVELOPE', 'RFC822'])
    for row in rows:
        search_id = row[0]
        print(search_id)
        # save_dir = fr'\\p-fp-032\Data1BackedUp\Prove IT Working Data\STATS Requests\{search_id}'  # save directory
        for msgid, data in response.items():  # Iterates through the collection and assigns to 2 variables one by one
            raw = email.message_from_bytes(data[b'RFC822'])
            subject = data[b'ENVELOPE'].subject.decode()
            body = str(get_body(raw))
            find_ref = re.search(r'Your Enquiry Ref:\s([A-Z0-9]{10})', body)
            print(search_id)
            print(find_ref.group(1))
            if search_id == find_ref.group(1):
                download(raw, search_id)
                server.move(msgid, 'INBOX/GTC/complete')
                database_writer.update_main_searches_gtc_data_received('true', search_id)
            # time.sleep(5)
            print(subject)  # Gets the subject


if __name__ == '__main__':
    while True:
        rows = database_writer.query_main_GTC_search_submitted()
        if rows:
            try:
                with IMAPClient(HOST) as server:  # Picking the server and SSL security. and assigning to var.
                    # Starts with "with" so that if for whatever reason the code terminates, it will log out of the server
                    server.login(ProveitEmail + '\proveit@kier.co.uk', ProveitPassword)  # Signing in with above variables
                    server.select_folder(MAILBOX)  # Selecting mailbox
                    process_email()
                    time.sleep(30)
            except Exception as e:
                print(e)

        else:
            print('scanning for new rows...')
            time.sleep(5)
