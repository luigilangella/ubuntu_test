from passwordManager import account_key, connection_string

from datetime import datetime, timedelta
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions

account_name = 'delveblobstore'
container_name = 'proveit'


def get_blob_sas(blob_name):
    sas_blob = generate_blob_sas(account_name=account_name,
                                 container_name=container_name,
                                 blob_name=blob_name,
                                 account_key=account_key,
                                 permission=BlobSasPermissions(read=True),
                                 expiry=datetime.utcnow() + timedelta(days=90))
    return sas_blob


def upload_blob(connection_string, file_path, blob_name):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name,
                                             blob_name=blob_name)
    with open(file_path, "rb") as data:
        blob.upload_blob(data, overwrite=True)
    print(f'uploaded {blob_name} to blob')


if __name__ == '__main__':
    pass
    # upload_blob(connection_string=connection_string, file_path=file_path)
    #
    # blob = get_blob_sas(blob_name)
    # url = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + blob
    # print('the url = ', url)
