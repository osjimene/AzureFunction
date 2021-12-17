import requests
import os

#Not used in the function. Used to give information on the targetted OneDrive using the GraphAPI.

def readDrive(secretkey):
    endpoint = 'https://graph.microsoft.com/v1.0/me/drive/root/children'
    secret = 'Bearer '+ secretkey
    http_headers = {'Authorization' : secret}
    data = requests.get(endpoint, headers = http_headers).json()
    return str(data)