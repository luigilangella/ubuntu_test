import psycopg2
from passwordManager import DB_USER, DB_NAME, DB_HOST, DB_PORT, DB_P


# Write the new searches to the database
def insert_search_row(search_id, request_email_address, account, intersecting_tile, x, y, reference, contract):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " INSERT INTO searches_main (search_id, request_email_address, account, intersecting_tile, easting, northing, reference, contract ) VALUES "
        "(%s,%s,%s,%s,%s,%s,%s,%s)",
        (search_id, request_email_address, account, intersecting_tile, x, y, reference, contract))
    conn.commit()
    conn.close()


# except:
#     input('unable connect')


def update_main_searches_DD(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET digdat_search_complete = True WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def insert_DigDat_table(search_id, digdat_ref):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " INSERT INTO digdat_searches (search_id, digdat_ref, search_complete) VALUES (%s,%s,%s)",
        (search_id, digdat_ref, True))
    conn.commit()
    conn.close()


def insert_LSBUD_table(search_id, lsbud_ref, company_name, search_status_type):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " INSERT INTO lsbud_searches (search_id, lsbud_ref, company, search_status_type) VALUES (%s,%s,%s,%s)",
        (search_id, lsbud_ref, company_name, search_status_type))
    conn.commit()
    conn.close()


def insert_LSBUD_table_blue(search_id, lsbud_ref, company_name, contact_number, preferred_contact_method):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " INSERT INTO lsbud_blue_table (search_id, lsbud_ref, company, contact_number, preferred_contact_method) VALUES (%s,%s,%s,%s,%s)",
        (search_id, lsbud_ref, company_name, contact_number, preferred_contact_method))
    conn.commit()
    conn.close()


def query_searches_main_digdat():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL; ")
    row = cur.fetchone()
    conn.close()
    return row


def insert_digdat_companies(digdat_id, company, company_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " INSERT INTO digdat_companies (digdat_id, company, company_id) VALUES (%s,%s,%s)",
        (digdat_id, company, company_id))
    conn.commit()
    conn.close()



def query_searches_main_lsbud():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE lsbud_search_complete IS NULL; ")
    row = cur.fetchall()
    conn.close()
    return row


def update_main_searches_LSBUD(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET lsbud_search_complete = True WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def update_lsbud_table(company, lsbud_ref):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE lsbud_searches SET search_complete = True WHERE company = %s AND lsbud_ref = %s",
                (company, lsbud_ref))
    conn.commit()
    conn.close()


def update_lsbud_table_difficult_companies(company, lsbud_ref):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE lsbud_searches SET search_complete = False WHERE company = %s AND lsbud_ref = %s",
                (company, lsbud_ref))
    conn.commit()
    conn.close()

def query_lsbud_table(reference):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM lsbud_searches WHERE lsbud_ref = %s", (reference,))
    row = cur.fetchall()
    conn.close()
    return row


def query_lsbud_table_all_data_returned(reference):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM lsbud_searches WHERE lsbud_ref = %s AND search_complete IS NULL", (reference,))
    row = cur.fetchall()
    conn.close()
    return row


def query_lsbud_table_join_fetch_user_ref(reference):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT searches_main.reference, searches_main.request_email_address FROM searches_main INNER JOIN lsbud_searches ON searches_main.search_id = lsbud_searches.search_id WHERE lsbud_searches.search_id = %s ", (reference,))
    row = cur.fetchone()
    conn.close()
    return row


def update_main_searches_LSBUD_data_received(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_lsbud = True WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def update_main_searches_DigDat_data_received(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_digdat = True WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def query_lookup_directories_table(tile_name):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM lookup_directories WHERE folder = %s", (tile_name,))
    row = cur.fetchone()
    conn.close()
    return row


def query_main_table_to_compile():
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " SELECT * FROM searches_main WHERE data_received_lsbud IS NOT NULL AND data_received_bt IS NOT NULL AND data_received_cityfibre IS NOT NULL AND data_received_digdat IS NOT NULL AND data_received_gtc IS NOT NULL AND data_sent IS NULL")
    row = cur.fetchall()
    conn.close()
    return row


def update_main_searches_ready_to_send(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_sent = %s WHERE search_id = %s", ('ready to send', search_id,))
    conn.commit()
    conn.close()


def update_main_searches_ready_to_send_mutlithreader(row_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_sent = %s WHERE id = %s", ('ready to send', row_id,))
    conn.commit()
    conn.close()


def update_main_searches_data_sent(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_sent = True WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def query_ready_to_send():
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE data_sent = %s", ('ready to send',))
    row = cur.fetchone()
    conn.close()
    return row


def query_main_table_return_row(search_id):
    # try:
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE search_id = %s", (search_id,))
    row = cur.fetchone()
    conn.close()
    return row


# -------------------------------------------------------- BT queries

def update_main_searches_bt(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET bt_search_complete = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


def query_searches_main_bt():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE  bt_search_complete IS NULL; ")
    row = cur.fetchone()
    conn.close()
    return row


def insert_bt_table(search_id, bt_ref):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" INSERT INTO bt_searches (search_id, bt_reference) VALUES (%s,%s)",
                (search_id, bt_ref))
    conn.commit()
    conn.close()


def query_bt_table():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM bt_searches WHERE search_complete IS NULL; ")
    row = cur.fetchall()
    conn.close()
    return row


def update_main_searches_bt_data_received(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_bt = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


def update_bt_table(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE bt_searches SET search_complete = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


# ------------------------------------------------------------ CityFibre queries

def update_main_searches_cityfibre(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET cityfibre_search_complete = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


def query_searches_main_cityfibre():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE  cityfibre_search_complete IS NULL; ")
    row = cur.fetchone()
    conn.close()
    return row


def insert_cityfibre_table(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()

    cur.execute(" INSERT INTO cityfibre_searches (search_id) VALUES (%s)", (search_id,))
    conn.commit()
    conn.close()


def query_cityfibre_table():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM cityfibre_searches WHERE search_complete IS NULL; ")
    row = cur.fetchall()

    conn.close()
    return row


def update_main_searches_cityfibre_data_received(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_cityfibre = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


def update_cityfibre_table(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE cityfibre_searches SET search_complete = %s WHERE search_id = %s", ('true', search_id))
    conn.commit()
    conn.close()


def query_searches_main_cityfibre_resbumit():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " SELECT * FROM searches_main WHERE data_received_cityfibre IS NULL AND datetime_requested < NOW() - INTERVAL '4' MINUTE; ")
    row = cur.fetchone()
    conn.close()
    return row


def query_searches_main_cityfibre_resubmit2():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " SELECT * FROM searches_main INNER JOIN cityfibre_searches ON searches_main.search_id = cityfibre_searches.search_id WHERE searches_main.data_received_cityfibre IS NULL AND cityfibre_searches.datetime_requested < NOW() - INTERVAL '4' MINUTE; ")
    row = cur.fetchone()
    conn.close()
    return row


def update_searches_main_cityfibre_to_null(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET cityfibre_search_complete = NULL WHERE search_id = %s", (search_id,))
    conn.commit()
    conn.close()


def resubmit_missing_cityfibre():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(""" SELECT cf.id, main.search_id, main.id
                        FROM public.cityfibre_searches cf
                        INNER JOIN public.searches_main main
                        ON main.search_id = cf.search_id
                        WHERE main.data_received_cityfibre IS NULL AND cf.datetime_requested < NOW() - INTERVAL '15' MINUTE """)
    row = cur.fetchone()
    if row:
        print('Searching CityFibre again', row)
        cur.execute("""UPDATE cityfibre_searches SET datetime_requested = NOW() WHERE id = %s""", (row[0],))
        conn.commit()

        cur.execute("""UPDATE searches_main SET cityfibre_search_complete = NULL WHERE id = %s""", (row[2],))
        conn.commit()

    cur.close()
    conn.close()
    return row

# ---------------------------------------------------------------------------- digdat search divider

def digdat_account_assignment_query():  # returns new searches
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL AND assigned_account IS NULL; ")
    row = cur.fetchone()
    conn.close()
    return row


def update_digdat_account_assignment(search_id, account_num):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET assigned_account = %s WHERE search_id = %s; ", (account_num, search_id))
    conn.commit()
    conn.close()


def digdat_account_1():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL AND assigned_account = '0'; ")
    row = cur.fetchone()
    conn.close()
    return row


def digdat_account_2():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL AND assigned_account = '1'; ")
    row = cur.fetchone()
    conn.close()
    return row


def digdat_account_3():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL AND assigned_account = '2'; ")
    row = cur.fetchone()
    conn.close()
    return row


def digdat_account_4():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE digdat_search_complete IS NULL AND assigned_account = '3'; ")
    row = cur.fetchone()
    conn.close()
    return row
# ---------------------------------------------------------------------------- lsbud search divider


def lsbud_account_1():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE lsbud_search_complete IS NULL AND assigned_account = '0'; ")
    row = cur.fetchone()
    conn.close()
    return row


def lsbud_account_2():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE lsbud_search_complete IS NULL AND assigned_account = '1'; ")
    row = cur.fetchone()
    conn.close()
    return row


def lsbud_account_3():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE lsbud_search_complete IS NULL AND assigned_account = '2'; ")
    row = cur.fetchone()
    conn.close()
    return row


def lsbud_account_4():  # returns new searches with assigned account number
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE lsbud_search_complete IS NULL AND assigned_account = '3'; ")
    row = cur.fetchone()
    conn.close()
    return row

# ---------------------------------------------- Scottish Water

def query_main_scottish_water():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE contract = %s AND scottishwater_search_complete IS NULL;",
                ('VMScotland',))
    row = cur.fetchone()
    conn.close()
    return row


def query_main_scottish_water_search_complete():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " SELECT * FROM searches_main WHERE contract = %s AND scottishwater_search_complete = %s AND data_received_scottishwater IS NULL;",
        ('VMScotland', 'true'))
    row = cur.fetchall()
    conn.close()
    return row


def update_scottishwater_data_received(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_scottishwater = %s WHERE search_id = %s; ",
                ('true', search_id))
    conn.commit()
    conn.close()


def update_scottishwater_search_complete(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET scottishwater_search_complete = %s WHERE search_id = %s; ",
                ('true', search_id))
    conn.commit()
    conn.close()


def update_main_searches_VMScotland_ready_to_send(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_sent = %s WHERE search_id = %s", ('ready to send', search_id,))
    conn.commit()
    conn.close()


def query_main_table_to_compile_VMScotland():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(
        " SELECT * FROM searches_main WHERE data_received_lsbud IS NOT NULL AND data_received_digdat IS NOT NULL AND data_received_scottishwater = %s AND data_sent IS NULL",
        ('true',))
    row = cur.fetchone()
    conn.close()
    return row


# ------------------------------------------------------------------ GTC

def query_main_GTC():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE gtc_search_complete IS NULL;")
    row = cur.fetchone()
    conn.close()
    return row


def update_main_searches_gtc_search_complete(value, search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET gtc_search_complete = %s WHERE search_id = %s", (value, search_id,))
    conn.commit()
    conn.close()


def update_main_searches_gtc_data_received(value, search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" UPDATE searches_main SET data_received_gtc = %s WHERE search_id = %s", (value, search_id,))
    conn.commit()
    conn.close()


def query_main_GTC_search_submitted():
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT * FROM searches_main WHERE gtc_search_complete = %s AND data_received_gtc IS NULL", ('true',))
    row = cur.fetchall()
    conn.close()
    return row


# ----------------------------------------------------------------- download files

def return_files_list(tile):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT url FROM files WHERE tile = %s AND status = %s ", (tile, 'valid'))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ------------------------------------------------------------------- cover sheet
def query_lsbud_table_cover_sheet(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT company FROM lsbud_searches WHERE search_id = %s", (search_id,))
    row = cur.fetchall()
    conn.close()
    return row


def query_digdat_table_cover_sheet(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT company FROM digdat_companies INNER JOIN digdat_searches ON digdat_id = digdat_ref WHERE digdat_searches.search_id = %s", (search_id,))
    row = cur.fetchall()
    conn.close()
    return row



def query_files_table_cover_sheet(search_id):
    conn = psycopg2.connect(user=DB_USER,
                            password=DB_P,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)

    cur = conn.cursor()
    cur.execute(" SELECT url, company_code FROM files INNER JOIN searches_main ON intersecting_tile = tile WHERE searches_main.search_id = %s", (search_id,))
    row = cur.fetchall()
    conn.close()
    return row


if __name__ == '__main__':
    i = query_lsbud_table_join_fetch_user_ref('7T0XMNFUKB')
    print(i[0], i[1])
