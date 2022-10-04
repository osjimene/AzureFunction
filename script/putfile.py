import requests
import os

#Not used in main script. Used for testing upload to Onedrive Functionality. 

# def putfile(secretkey,filename):
#     dir = os.path.dirname(__file__)
#     file = os.path.join(dir, filename)
#     testfile = open(file,'rb')
#     endpoint = f'https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content'
#     secret = 'Bearer ' + secretkey
#     http_headers = {'Authorization': secret}
#     requests.put(endpoint, headers= http_headers, data = testfile)
#     response = 'Your File has been uploaded successfully!' 
#     return response

def putfile(file, filename):
    testfile = open(file,'rb')
    endpoint = f'https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content'
    secretkey = os.environ['GRAPH_API']
    secret = 'Bearer ' + secretkey
    http_headers = {'Authorization': secret}
    response = requests.put(endpoint, headers= http_headers, data = testfile)
    status = response.reason 
    return status
