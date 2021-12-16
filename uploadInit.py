def main(req: func.HttpRequest) -> func.HttpResponse:

    blob_sas_url = ""
    message = ""
    http_status = 200
    
    try:
        #a Filename is required
        fileParam = req.params.get('filename')
        if not fileParam:
            message = "Bad request: 'filename' parameter is required with .txt extension"
            http_status = 400
        else:
            blob_sas_url = upload_file_to_storage(f"{fileParam}.txt")
            message = "File created and uploaded to storage. You can <a href='" + blob_sas_url + "'>download it </a> for the next 1 hour."
        
    except ValueError:
        return func.HttpResponse(f'There was a failure doing anything with azure blobs but the file parameter you entered is {blob_sas_url}')

    return func.HttpResponse(
        mimetype="text/html",
        body=message,
        status_code=http_status
    )

