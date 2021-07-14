import time
from imapclient import IMAPClient
import os
import email
from passwordManager import ProveitEmail, ProveitPassword
import database_writer
import re
import random
HOST = 'outlook.office365.com'  # IMAP Host Server
MAILBOX = 'INBOX/CityFibre'  # Mailbox to check


# extracts the body from the email
def get_body(msg):  # Need to use that raw var below
    if msg.is_multipart():  # If the message is a multipart(returns True)
        return get_body(msg.get_payload(0))  # Returns the payload
    else:
        return msg.get_payload(None, True)  # Returns nothing


# allows you to download attachments
def get_attachments(msg, save_dir):
    # Takes the raw data and breaks it into different 'parts' & python processes it 1 at a time [1]
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':  # Checks if the email is the correct 'type'.
            # If it's a 'multipart', then it is incorrect type of email that can possible have an attachment
            continue  # Continue command skips the rest of code and checks the next 'part'

        if part.get('Content-Disposition') is None:  # Checks the 'Content-Disposition' field of the message.
            # If it's empty, or "None", then we need to leave and go to the next part
            continue  # Continue command skips the rest of code and checks the next 'part'
        # So if the part isn't a 'multipart' type and has a 'Content-Disposition'...

        file_name = part.get_filename()  # Get the filename

        if bool(file_name):  # If bool(file_name) returns True
            file_path = os.path.join(save_dir,
                                     '299 ' + file_name)  # Combine the save directory and file name to make file_path
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))  # make directory if now found
            print(file_path)
            with open(file_path, 'wb') as f:  # Opens file, w = creates if it doesn't exist / b = binary mode [2]
                f.write(part.get_payload(decode=True))  # Returns the part is carrying, or it's payload, and decodes [3]


def process_email():
    messages = server.search('ALL')
    print('number of emails in folder', len(messages))  # number of new emails
    response = server.fetch(messages, ['FLAGS', 'BODY', 'RFC822.SIZE', 'ENVELOPE', 'RFC822'])
    for row in rows:
        search_id = row[1]
        save_dir = f'/home/luigi/Documents/Stats Requests/{search_id}'  # save directory
        for msgid, data in response.items():  # Iterates through the collection and assigns to 2 variables one by one
            raw = email.message_from_bytes(data[b'RFC822'])
            subject = data[b'ENVELOPE'].subject.decode()
            body = str(get_body(raw))
            find_ref = re.search('Title:\s([A-Z0-9]{10})', body)
            print(search_id)
            print(find_ref.group(1))
            if search_id == find_ref.group(1):
                # input('match!')
                get_attachments(raw, save_dir=save_dir)
                database_writer.update_main_searches_cityfibre_data_received(search_id=search_id)
                database_writer.update_cityfibre_table(search_id=search_id)
                server.move(msgid, 'INBOX/CityFibre/complete')
            # time.sleep(5)
            print(subject)  # Gets the subject
        # return len(messages)
        # input()


if __name__ == '__main__':
    while True:
        rows = database_writer.query_cityfibre_table()
        if rows:

            try:
                with IMAPClient(HOST) as server:  # Picking the server and SSL security. and assigning to var.
                    # Starts with "with" so that if for whatever reason the code terminates, it will log out of the server
                    server.login(ProveitEmail + r'\proveit@kier.co.uk', ProveitPassword)  # Signing in with above variables
                    server.select_folder(MAILBOX)  # Selecting mailbox
                    process_email()
                    time.sleep(5)
            except Exception as e:
                print(e)

        else:
            print('scanning for new rows...')
            time.sleep(5)

