import datetime
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    blob_sas_url = ""
    message = ""
    http_status = 200

    logging.info('HTTP trigger function processed a request.')

    purge = req.params.get("purge")

    if not purge:
        try: 
            logging.info("Attempting to get parameters via the API Request body...")
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            logging.info("Attempting to parse out the RedZone from the json body...")
            purge = req_body.get('purge')
            logging.info(f"successfully grabbed the body request [{purge}] from the request body... ")
    
    if purge == 'True':
        try:
    

            blob_client = BlobServiceClient.from_connection_string(conn_str=os.environ["FileAccountConnection"])
            container_client = blob_client.get_container_client(os.environ["FileContainer"])

            old_presentations = container_client.list_blobs()
            container_client.delete_blobs(*old_presentations)

            logging.info("Deleted files.")
            message = 'Your files in the storage container were successfully purged...'
            return func.HttpResponse(
                mimetype = "text/html",
                body = message,
                status_code = http_status
            )
        except:
            logging.error("Failed file processing.")
            message = 'Oops looks like something went wrong. We didnt touch anything! '
            return func.HttpResponse(
                mimetype = "text/html",
                body = message,
                status_code = http_status
            )