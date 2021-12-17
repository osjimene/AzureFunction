import requests
import os
import pandas as pd
from requests.auth import HTTPBasicAuth
from collections import defaultdict
import dateutil.parser


def API_Pull(RZTag):
    ALIAS = os.environ['USER_ALIAS']
    SECRET_KEY= os.environ['ADO_SECRET']
    #Wiql Query that is used to post to the REST API and return the Workitems
    wiql_API_url = 'https://dev.azure.com/MicrosoftIT/OneITVSO/_apis/wit/wiql?api-version=5.1'
    
    query = {"query": """SELECT
        [System.Id]
    FROM workitems
    WHERE
        [System.TeamProject] = @project
        AND (
            (
                [System.WorkItemType] = 'Issue'
                AND [System.State] = 'New'
                OR [System.State] = 'Active'
            )
            AND [System.Tags] CONTAINS '{}'
            AND [System.WorkItemType] = 'Issue'
        )
    ORDER BY [System.Id]""".format(RZTag)}

    r = requests.post(wiql_API_url, json = query , auth= HTTPBasicAuth(ALIAS,SECRET_KEY))
    #This is the raw full format JSON from the API Call
    data = r.json()
    #This is filtered down to the Workitems list of Dictionaries ID:URL
    workitems = data['workItems']
    #This uses the defaultdict module to separate the list of dictionaries into 2 lists
    res = defaultdict(list)
    {res[key].append(sub[key]) for sub in workitems for key in sub}
    #Filters the lists to just the list of Workitem Ids. 
    ids = res['id']

    workitem_API_url = 'https://dev.azure.com/MicrosoftIT/OneITVSO/_apis/wit/workitemsbatch?api-version=5.1'


    data = {
      "ids": ids,
      "fields": [
        'System.Id',
        'System.WorkItemType',
        'System.Title',
        'System.AssignedTo',
        'System.State',
        'System.Tags',
        'Microsoft.VSTS.Scheduling.DueDate',
        'System.Description'
      ]
    }

    r = requests.post(workitem_API_url, json = data , auth= HTTPBasicAuth(ALIAS,SECRET_KEY))
    RZone = r.json()

    RZone = RZone['value']
    

    df = pd.json_normalize(RZone)

    #This extracts the status from the Tags fied
    df.loc[df['fields.System.Tags'].str.contains('RZ-Red'),'Status'] = 'RZ-Red'
    df.loc[df['fields.System.Tags'].str.contains('RZ-Yellow'),'Status'] = 'RZ-Yellow'
    df.loc[df['fields.System.Tags'].str.contains('RZ-Green'),'Status'] = 'RZ-Green'
    df.loc[df['fields.System.Tags'].str.contains('RZ-Blue'),'Status'] = 'RZ-Blue'

    #Parse out the HTML
    #Grabs the Description column in the API data
    description = df['fields.System.Description']

    #Instantiates a blank DF object to append to in the loop below
    df3 = pd.DataFrame()

    #Parses through each HTML and appends it to a Dataframe
    for rows in description:
      html = pd.read_html(rows)
      html = html[0]
    
      headowner = html.iloc[1,0]
      headado = html.iloc[2,0]
      headcomments = html.iloc[3,0]
      owner = html.iloc[1,1]
      ado = html.iloc[2,1]
      comments = html.iloc[3,1]
    
      fields = pd.DataFrame(
        {headowner : [owner],
         headado : [ado],
         headcomments : [comments]
        }
      )
      df3 =df3.append(fields)
    
    #df3

    PG_Owner = df3['PG Owner:'].to_list()
    PG_ADO = df3['PG ADO(URL):'].to_list()
    Comments = df3['Comments(Status):'].to_list()

    #This appends and drops uneccesarry columns to the Dataframe. 

    #This appends the new columns
    df['PG Owner'] = PG_Owner
    df['PG ADO'] = PG_ADO
    df['Comments'] = Comments

    #This deletes unecessary columns
    df = df.drop(columns=['id','rev','url','fields.System.WorkItemType','fields.System.State','fields.System.AssignedTo.url','fields.System.AssignedTo._links.avatar.href',
    'fields.System.AssignedTo.id','fields.System.AssignedTo.imageUrl','fields.System.AssignedTo.descriptor','fields.System.Description','fields.System.Tags'])

    #This makes the ADO ID into a URL
    ado_id = df['fields.System.Id'].to_list()
    ado_url = []
    for items in ado_id:
        url = 'https://microsoftit.visualstudio.com/OneITVSO/_workitems/edit/{}'.format(items)
        ado_url.append(url)

    df['MSD ADO'] = ado_url

    #This renames all the columns foeasier referencing
    df = df.rename(columns = {'fields.System.Id':'MSD ADO ID','fields.System.AssignedTo.displayName':'MSD Owner','fields.System.AssignedTo.uniqueName':'MSD Owner Alias', 'fields.System.Title':'Issue','fields.Microsoft.VSTS.Scheduling.DueDate':'Req Date','MSD ADO': 'MSD ADO URL' })

    #This reformats the Date and Time Block to Month and Year
    for index_label, row_series in df.iterrows():
        if type(df.at[index_label , 'Req Date']) == str:
           df.at[index_label , 'Req Date'] = dateutil.parser.parse(row_series['Req Date']).strftime('%m/%y')
        else:
           df.at[index_label , 'Req Date'] = row_series['Req Date']
    #This sorts all the work items from Blue to Red Status.
    df['Status'] = pd.Categorical(df['Status'], ['RZ-Blue', 'RZ-Green', 'RZ-Yellow', 'RZ-Red'])

    df = df.sort_values('Status')

    return df