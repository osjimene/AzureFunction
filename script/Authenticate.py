from msal import PublicClientApplication
import os
import requests
import json


#Not used in script but used it to authenticate using AAD if necessary
def getcredentials():
    Scope= [os.environ['SCOPES']]
    app = PublicClientApplication(
        client_id = os.environ["CLIENT_ID"],
        authority = os.environ["TENANT"],
    )

    result = None

    if not result:
        flow = app.initiate_device_flow(scopes= Scope)
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4)
            )
        print(flow["message"])

        result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return(result['access_token'])
    else:
        return(result)



