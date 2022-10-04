import requests

#Not used in the main script but some code I used to test the Graph API functionality
#Used to return the UserInfo via the GraphAPI once Authenticated

def userinfo(secretkey):
    endpoint = 'Https://graph.microsoft.com/v1.0/me'
    secret = 'Bearer ' + secretkey
    http_headers = {'Authorization': secret}
    data = requests.get(endpoint, headers= http_headers, stream = False).json()
    return str(data)