from imapclient import IMAPClient
import time
import re
import database_writer
import csv
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from passwordManager import ProveitEmail, ProveitPassword
import os
import email
from Send_Email import send_email
from html_proveit import html_email

HOST = 'outlook.office365.com'  # IMAP Host Server
MAILBOX = 'INBOX/other'  # Mailbox to check


class Linesearch:
    # root_path = r'C:\Users\richard.trivett\Desktop'

    root_path = '/home/luigi/Documents/Stats Requests'

    def __init__(self, raw_data, subj, email_address, search_id, company, user_ref, user_email):
        self.raw = raw_data
        self.subject = subj
        self.email_address = email_address
        self.search_id = search_id
        self.company = company
        self.destination = os.path.join(self.root_path, search_id)
        self.user_ref = user_ref
        self.user_email = user_email

    # extracts the body from the email
    def get_body(self):  # Need to use that raw var below
        if self.raw.is_multipart():  # If the message is a multipart(returns True)
            return self.raw.get_payload(0)  # Returns the payload
        else:
            return self.raw.get_payload(None, True)  # Returns nothing

    # allows you to download attachments
    def get_attachments(self):

        # Takes the raw data and breaks it into different 'parts' & python processes it 1 at a time [1]
        for part in self.raw.walk():

            if part.get_content_maintype() == 'multipart':  # Checks if the email is the correct 'type'.
                # If it's a 'multipart', then it is incorrect type of email that can possible have an attachment
                continue  # Continue command skips the rest of code and checks the next 'part'

            # if part.get('Content-Disposition') is None:  # Checks the 'Content-Disposition' field of the message.
            # If it's empty, or "None", then we need to leave and go to the next part
            # continue  # Continue command skips the rest of code and checks the next 'part'
            # So if the part isn't a 'multipart' type and has a 'Content-Disposition'...

            file_name = part.get_filename()  # Get the filename
            # print(file_name)

            if bool(file_name):  # If bool(file_name) returns True

                if company_id is None:
                    file_path = os.path.join(self.destination, '0-' + file_name)
                else:
                    file_path = os.path.join(self.destination, company_id + ' ' + file_name.replace('\r\n',
                                                                                                    ''))  # Combine the save directory and file name to make file_path
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))  # make directory if now found
                print(file_path)

                try:
                    with open(file_path,
                              'wb') as file:  # Opens file, w = creates if it doesn't exist / b = binary mode [2]
                        file.write(
                            part.get_payload(
                                decode=True))  # Returns the part is carrying, or it's payload, and decodes [3]

                    if '0 LSBUD' not in file_path:
                        self.send_missing_plans(file_path)
                except:
                    pass

    def download_plans(self):
        """downloads and extracts zip files from emails which have links"""

        look_for_link = self.get_body()
        link_finder = re.search(r'(https:.+\.zip)', str(look_for_link))

        if link_finder:
            print(link_finder.group(1))
            with urlopen(link_finder.group(1)) as zip_response:
                with ZipFile(BytesIO(zip_response.read())) as zfile:
                    zfile.extractall(self.destination)
            return link_finder.group(1)

    def multiple_emails(self):
        """if email is one of many, this function will ensure all emails are received before sending to client"""

        pattern = re.search(r'Email\s(\d+)\sof\s(\d+)', self.subject)
        if pattern:
            files_in_directory = os.listdir(self.destination)
            msgs = [file for file in files_in_directory if
                    file.endswith('.txt') and re.search(r'Email\s(\d+)\sof\s(\d+)', file)]
            print(len(msgs), pattern.group(2))  # prints the number of emails found and the number of emails expected

            if str(pattern.group(2)) == str(len(msgs)):
                print('found all')
                database_writer.update_lsbud_table(company=self.company_lookup(), lsbud_ref=ref)
            return pattern.group(1), pattern.group(2)

    def company_lookup(self):
        """performs a lookup on a csv list of email strings against the email address. If found, will return the company
         name from the adjacent row"""

        with open('company lookup.csv') as f:
            read_csv = csv.reader(f)
            next(read_csv)
            for row in read_csv:
                match_string = row[0]
                company_name = row[1]
                if match_string in self.email_address:
                    return company_name

    def company_id_lookup(self):
        """performs a lookup on a csv list of email strings against the email address. If found, will return the company
         ID from the adjacent row"""

        with open('company lookup.csv') as f:
            read_csv = csv.reader(f)
            next(read_csv)
            for row in read_csv:
                match_string = row[0]
                company_id = row[3]
                if match_string in self.email_address:
                    return company_id

    def send_missing_plans(self, file_path):
        """sends manually returned plans. These are plans which tend to take a long time to be received"""
        company_list = ['Concept Solutions People Ltd', 'Jurassic Fibre Ltd']
        if self.company in company_list:
            print('sending', self.company)
            send_email(email_recipient=self.user_email,
                       email_subject=f'Prove-IT STATS Pack for {self.user_ref} ({self.company})',
                       email_message=html_email(self.user_ref),
                       attachment_location=file_path)  # file_path


# This block of code iterates over the email in an inbox
while True:

    try:
        with IMAPClient(HOST) as server:  # Picking the server and SSL security. and assigning to var.
            # Starts with "with" so that if for whatever reason the code terminates, it will log out of the server
            server.login(ProveitEmail + '\LSBUD@kier.co.uk', ProveitPassword)  # Signing in with above variables
            # input(server.list_folders())
            server.select_folder(MAILBOX)  # Selecting mailbox
            messages = server.search('ALL')
            print('number of emails in folder', len(messages))  # number of new emails
            response = server.fetch(messages, ['FLAGS', 'BODY', 'RFC822.SIZE', 'ENVELOPE', 'RFC822'])

            # print(company, lsbud_ref, search_id)

            for msgid, data in response.items():  # Iterates through the collection and assigns to 2 variables one by one

                raw = email.message_from_bytes(data[b'RFC822'])
                subject = data[b'ENVELOPE'].subject.decode()
                email_addr = raw.get('From')
                #
                try:
                    email_addr = re.search(r'<(.+)>', raw.get('From')).group(1)  # error catching for email parsing
                except Exception as e:
                    email_addr = re.search(r'<(.+)>', raw.get('From'))
                if email_addr is None:
                    email_addr = raw.get('From')

                try:
                    ref = re.search(r'\d{8}', subject).group()

                except AttributeError:
                    ref = ''

                if ref.isdigit():  # tests whether the email contains an 8 digit reference
                    print(ref, subject)
                else:
                    print(ref, subject, 'reference not found...')
                    continue

                rows = database_writer.query_lsbud_table(
                    ref)  # look for LSBUD ref within database and returns all matching rows

                if rows:
                    for row in rows:
                        company = row[1]
                        search_id = row[5]
                        user_ref = database_writer.query_lsbud_table_join_fetch_user_ref(search_id)[0]
                        user_email = database_writer.query_lsbud_table_join_fetch_user_ref(search_id)[1]
                        print(user_ref)

                        ls = Linesearch(raw_data=raw, subj=subject, email_address=email_addr, search_id=search_id,
                                        company=company, user_ref=user_ref, user_email=user_email)

                        company_id = str(ls.company_id_lookup())

                        # print(company_id)
                        if company_id == '0':  # handles linesearches
                            company = 'LSBUD'
                            print('processing linesearch...')
                            ls.get_attachments()

                        if company == ls.company_lookup():
                            print(company + ', processing match!')
                            ls.get_attachments()

                            try:
                                ls.download_plans()  # download and extract plans
                            except Exception as e:
                                print('could not download... trying again')

                            if not os.path.exists(
                                    ls.destination):  # creates the folder where all searches will be copied
                                os.makedirs(ls.destination)

                            with open(os.path.join(ls.destination, subject.replace(':', '').replace('/', '') + '.txt'),
                                      'w') as f:  # creates a .txt file for each email to keep track of multiple email returns
                                f.write('ignore file')

                            if ls.multiple_emails():  # tests for a multiple email response, if true will only update database once all parts are found
                                print('running')
                            else:
                                # pass
                                # input('here now')
                                database_writer.update_lsbud_table(company=ls.company_lookup(),
                                                                   lsbud_ref=ref)  # updates table to true once all attachments are downloaded

                        else:
                            print(company, 'not a match')

                        if database_writer.query_lsbud_table_all_data_returned(
                                reference=ref):  # Checks whether all expected data has been returned
                            print('still awaiting responses for reference', search_id)
                        else:
                            print(f'All data for {search_id} has been returned!')
                            database_writer.update_main_searches_LSBUD_data_received(
                                search_id=search_id)  # updates main table to true if all LSBUD plans received

                    # input('here!')
                    server.move(msgid, 'INBOX/processed')
        print('Looking for new emails...')
        time.sleep(100)

    except Exception as e:
        print(e)
