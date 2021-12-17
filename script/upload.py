from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobClient, BlobSasPermissions, generate_blob_sas
import os

def upload_file_to_storage(testfile):
    blob_client = BlobClient.from_connection_string(conn_str=os.environ['FileAccountConnection'], container_name=os.environ['FileContainer'], blob_name=testfile)

    with open(testfile, 'w') as data:
        data.write(str('This is a test file to show that I can make this work!'))

    with open(testfile, "rb") as data:
        blob_client.upload_blob(data)

    #Generate a SAS-Protected URL for the item which will allow the caller to download teh file for 1 hour. 
    startTime = datetime.now(tz=timezone.utc)
    endTime = startTime + timedelta(hours=1)
    return 'https://'+ os.environ['FileStorageAccount'] + '.blob.core.windows.net/' + os.environ["FileContainer"]+ "/" + testfile + "?" + generate_blob_sas(os.environ["FileStorageAccount"],os.environ["FileContainer"],blob_name=testfile,account_key=os.environ["FileStorageKey"],permission=BlobSasPermissions(read=True),start=startTime,expiry=endTime)

    