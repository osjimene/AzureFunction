import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

#Set your environment variables from your local machine. 
TENANT_ID = os.environ.get("TESTING_TENANT_ID", "")
CLIENT_ID = os.environ.get("TESTING_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("TESTING_CLIENT_SECRET", "")
CLIENT_KEY = os.environ.get("TESTING_CLIENT_VALUE", "")

KEYVAULT_NAME = os.environ.get("KEYVAULT_NAME","")
KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"


#Pass the secret credentials to the method below
_credential = ClientSecretCredential(
    tenant_id=TENANT_ID, 
    client_id=CLIENT_ID, 
    client_secret=CLIENT_KEY
    )


#retrieve the secrets using the client and the service principal set up to use the secrets. 
_sc = SecretClient(vault_url= KEYVAULT_URI, credential= _credential)
graphapi = _sc.get_secret("GraphAPI").value
secret = _sc.get_secret("Secret").value