from msal import PublicClientApplication
import os

#Not used in script but used it to authenticate using AAD if necessary
def getcredentials():
    Scope= ["Files.ReadWrite"]
    app = PublicClientApplication(
        client_id = os.environ['Client'], 
        authority = os.environ['Tenant'],
        client_credential= None
    )

    result = None

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes= Scope, account = accounts[0])

    if not result:
        result = app.acquire_token_interactive(scopes = Scope)

    return(result['access_token'])