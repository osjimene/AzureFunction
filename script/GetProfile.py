import requests

def userinfo(secretkey):
    endpoint = 'Https://graph.microsoft.com/v1.0/me'
    secret = 'Bearer ' + secretkey
    http_headers = {'Authorization': secret}
    data = requests.get(endpoint, headers= http_headers, stream = False).json()
    return str(data)