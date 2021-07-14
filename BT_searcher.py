import requests
import base64
import time
import re
import database_writer
from passwordManager import BT_Searcher_user, BT_Searcher_passW, BT_username, BT_password


# ATTENTION!!!!! set correct planSize variable

planSize = 500

url = 'https://www.swns.bt.com/pls/mbe/MAPSBYEMAIL.sendMail'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
user = BT_Searcher_user
passW = BT_Searcher_passW
username = BT_username
password = BT_password
userpass = username + ':' + password
encoded_u = 'basic ' + base64.b64encode(userpass.encode()).decode()
h = {'Authorization': encoded_u, 'User-agent': user_agent}

if __name__ == '__main__':
    while True:
        row = database_writer.query_searches_main_bt()
        if row:
            search_id = database_writer.query_searches_main_bt()[0]
            CEas = database_writer.query_searches_main_bt()[7]
            CNor = database_writer.query_searches_main_bt()[8]
            print('searching coords', CEas, CNor)
            # input()
            try:
                r = requests.post(url,
                                  data=f"boundary={planSize}&in_referencing_system=27700&postcode=&location=osgrid&teasting=" + str(CEas) + "&tnorthing=" + str(CNor) + "&mapref=",
                                  headers=h)
                find_ref = re.search(r'(Reference Number:\s)([A-Z0-9]{9})', r.text)
                print(r.text[3714:3723])
                # print(r.text)
                ref = find_ref.group(2)
                database_writer.insert_bt_table(search_id=search_id, bt_ref=ref)
                database_writer.update_main_searches_bt(search_id=search_id)
            except Exception as e:
                print(e)
                time.sleep(5)
        else:
            print('looking for new searches...')
        time.sleep(8)