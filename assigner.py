import database_writer
import time

num_of_accounts = 4

while True:
    for num in range(num_of_accounts):
        while True:

            time.sleep(5)
            # print('scanning...')
            row = database_writer.digdat_account_assignment_query()
            if row:
                print(num)
                print(row)
                database_writer.update_digdat_account_assignment(search_id=row[0], account_num=str(num))
                break

