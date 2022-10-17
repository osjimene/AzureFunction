from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobClient, BlobSasPermissions, generate_blob_sas
import os

#This script uploads the generated presentation and returns a Sas URL that is timed for 1 hour to access. 

def upload_file_to_storage(presentationfile,filename):
    blob_client = BlobClient.from_connection_string(conn_str=os.environ['FileAccountConnection'], container_name=os.environ['FileContainer'], blob_name=filename)


    with open(presentationfile, "rb") as data:
        blob_client.upload_blob(data)

    #Generate a SAS-Protected URL for the item which will allow the caller to download the file for 1 hour. 
    startTime = datetime.now(tz=timezone.utc)
    endTime = startTime + timedelta(hours=1)
    return 'https://'+ os.environ['FileStorageAccount'] + '.blob.core.windows.net/' + os.environ["FileContainer"]+ "/" + filename + "?" + generate_blob_sas(os.environ["FileStorageAccount"],os.environ["FileContainer"],blob_name=filename,account_key=os.environ["FileStorageKey"],permission=BlobSasPermissions(read=True),start=startTime,expiry=endTime)

    