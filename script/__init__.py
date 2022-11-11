#These are all the requirements in case they dont come up on requirements.txt 
import logging
import pandas as pd
from datetime import datetime
from script import upload
from script.ADO_Pull import API_Pull
from script.create_ppt import create_ppt
from script.upload import upload_file_to_storage
from script.RZ_Selector import RZ_Selector
from script.putfile import putfile
import os
import base64

import azure.functions as func


#Main entry function to call the HTTP request.
def main(req: func.HttpRequest) -> func.HttpResponse:
    # blob_sas_url = ""
    message = "Your file has successfully been uploaded"
    http_status = 200
    
    logging.info('Python HTTP trigger function processed a request.')
    #List makes sure that the only Parameters accepted by the API are the ones below.     
    RZList = ['M365','Azure','EMM','Identity','Power','PBI','SDP','MIP','D365','Commerce']
    #Checks for the declared paremeter in the Function URL e.g. Localhost.api/script?RedZone=MIP
    RedZone = req.params.get('RedZone')
    
    #Checks the body of the API request in case the value is sent through the body via JSON
    if not RedZone:
        try: 
            logging.info("Attempting to get parameters via the API Request body...")
            req_body = req.get_json()
            logging.info("Attempting to parse out the RedZone from the json body...")
            RedZone = req_body.get('RedZone')
            logging.info(f"successfully grabbed the body request [{RedZone}] from the request body... ")
        except ValueError:
            pass
        else:
            logging.info("Attempting to parse out the RedZone from the json body...")
            RedZone = req_body.get('RedZone')
            logging.info(f"successfully grabbed the body request [{RedZone}] from the request body... ")
    #Chooses the right tags and title for the presentation and the ADO API pull        
    logging.info('Selecting the proper RedZone variables...')
    meeting = RZ_Selector(RedZone)
    #If everything runs correctly, you select the proper RedZone to generate for and everything is working then the powerpoint is then generated. 
    if RedZone in RZList:
        #Sets the Tag and Title variables from the RZ_Selector class
        logging.info(f"Selected the RZTag[{meeting[0]}] and RZTitle [{meeting[1]} ...]")
        RZTag = meeting[0]
        RZTitle = meeting[1] 
        #Function that will pull data from ADO via the API call
        logging.info("Gathering the ADO Workitem information...")
        data = API_Pull(RZTag)
        #This formats the filename to an appropriate format that can be tracked by date
        logging.info("Naming file...")
        outfilename = str((RZTitle)+" {:%B %Y %H%M%S}.pptx".format(datetime.now()))
        logging.info(f"File named {outfilename} ...")
        #Function that will create the powerpoint presentation based on the HHTP parameters in the URL
        presentationfile = create_ppt(outfilename, data, RZTitle)
        #Function that will upload this generated file into blob storage and then return a temporary URL that the requestor can use. 
        blob_sas_url = upload_file_to_storage(presentationfile, outfilename)
        message = " File created and uploaded to storage. You can <a href='" + blob_sas_url + "'>download it </a> for the next 1 hour."
        # message = putfile(presentationfile,outfilename)

        
        



        return func.HttpResponse(
            mimetype = "text/html",
            body = message,
            status_code = http_status
        )
        