import logging
from sys import getprofile
from pptx import Presentation
from pptx.util import Inches, Pt
import argparse
import pandas as pd
from datetime import date
import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from pandas.io.json import json_normalize
import dateutil.parser
from pptx.dml.color import RGBColor
import os
from TestFunction.ADO_Pull import API_Pull
from TestFunction.Authenticate import getcredentials
from TestFunction.RZ_Selector import RZ_Selector
from TestFunction.create_ppt import create_ppt

from TestFunction.putfile import putfile 
from .GetProfile import userinfo
from .readDrive import readDrive

import azure.functions as func



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #List makes sure that the only Parameters accepted by the API are the ones below.     
    RZList = ['M365','Azure','EMM','Identity','Power','PBI','SDP','MIP','D365','Commerce']
    #Checks for the declared paremeter in the Function URL e.g. Localhost.api/TestFunction?RedZone=MIP
    RedZone = req.params.get('RedZone')
    User = req.params.get('User')
    #Just a test function to make sure I know where the onedrive/AAD information is pulling from and storing into. 
    if User == 'Info':
        graphkey = getcredentials() 
        response = readDrive(graphkey)
        return func.HttpResponse(response)
    #Checks the body of the API request in case the value is sent through the body via JSON
    if not RedZone:
        try: 
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            RedZone = req_body.get('RedZone')
    #Chooses the right tags and title for the presentation and the ADO API pull        
    meeting = RZ_Selector(RedZone)
    #If everything runs correctly, you select the proper RedZone to generate for and everything is working then the powerpoint is then pushed to the OneDrive Folder of choice. 
    if RedZone in RZList:
        #Sets the Tag and Title variables from the RZ_Selector class
        RZTag = meeting[0]
        RZTitle = meeting[1] 
        #Inputs the proper ADO Tag to then pull all the relevant ADO information via an API call and formats it into a Pandas Dataframe
        data = API_Pull(RZTag)
        #This formats the filename to an appropriate format that can be tracked by date
        outfilename = str((RZTitle)+" {:%B %Y}.pptx".format(date.today()))
        #Creates the powerpoint presentation using the create_ppt class
        create_ppt(outfilename,data, RZTitle)
        #Pulls the GraphAPI key from the local.settings.json file
        #graphkey = os.environ['GraphKey']
        logging.info('Python HTTP trigger pulled GraphKey from Local.settings.json')
        #Ammend to use authentication method to grab Graph key
        graphkey = getcredentials()    
        #Puts the file information into your OneDrive of choice. 
        data = putfile(graphkey,outfilename)
        return func.HttpResponse("File uploaded to your onedrive successfully!")
    #If not the API call will just tell you that you need to put in a valid entry and all you get is the status code. 
    else:
        return func.HttpResponse(meeting, status_code=200)
        

