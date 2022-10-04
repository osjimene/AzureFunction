import azure.functions as func

#This takes the parameter input and createst the proper variables for API calling ADO. 

def RZ_Selector(RedZone):

    if RedZone == 'M365':
        RZTag = 'RZ-M365'
        RZName= 'M365'
        return RZTag, RZName
    elif RedZone == 'Azure':
        RZTag = 'RZ-Azure'
        RZName = 'Azure'
        return RZTag, RZName
    elif RedZone == 'EMM':
        RZTag = 'RZ-EMM'
        RZName = 'EMM'
        return RZTag, RZName
    elif RedZone == 'Identity':
        RZTag = 'RZ-Identity'
        RZName = 'Identity'
        return RZTag, RZName
    elif RedZone == 'Power':
        RZTag = 'RZ-Power'
        RZName = 'Power Platform'
        return RZTag, RZName
    elif RedZone == 'PBI':
        RZTag = 'RZ-PBI'
        RZName = 'Power Bi'
        return RZTag, RZName
    elif RedZone == 'SDP':
        RZTag = 'RZ-SDP'
        RZName = 'Securing the Developer Pipleine'
        return RZTag, RZName
    elif RedZone == 'MIP':
        RZTag = 'RZ-MIP'
        RZName = 'Microsoft Information Protection'
        return RZTag, RZName
    elif RedZone == 'D365':
        RZTag = 'RZ-D365'
        RZName = 'Dynamics 365'
        return RZTag, RZName
    elif RedZone == 'Commerce':
        RZTag = 'RZ-Comm'
        RZName = 'Commerce'
        return RZTag, RZName
    else:
        status = "This HTTP triggered function executed successfully. Pass a correct RedZone meeting to compile a proper report."
        return status             
        