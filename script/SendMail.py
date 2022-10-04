from wsgiref import headers
import requests
import os
import base64

#Not used in the main script but some code I used to test the Graph API functionality
#Used to return the UserInfo via the GraphAPI once Authenticated

def draft_attachment(file):
    with open(file, 'rb') as upload:
            media_content = base64.b64encode(upload.read())

    data_body = {
        '@odata.type': '#microsoft.graph.fileAttachment',
        'contentBytes': media_content.decode('utf-8'),
        'name': 'Powerpoint.pptx'
    }

def sendAttachment(attachment):
    endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'
    secret = os.environ['GRAPH_API']
    http_headers = {'Authorization' : 'Bearer ' + secret}
    requests_body = {
        'message': {
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': 'osjimene@microsoft.com'
                    }
                }
            ],
            'subject': "You've got mail",
            'importance': 'normal',
            'body': {
                'contentType': 'HTML',
                'content': '<b>Be Awesome</b>'
            },
            #include attachments
            'attachments': [
                attachment
            ]
        }
    }
    response = requests.post(endpoint, http_headers, json=requests_body)
    if response.status_code == 202:
        return("email send successfully")
    else:
        return(response.reason)    
    


