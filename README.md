# RedZoneFunction
Azure Function code to create a PowerPoint presentation using ADO data. 


Currently the script can pull data from ADO and create a powerpoint for the MSFT Information Protection RedZone. Running the HTTP request will generate a powerpoint presentation and save it to your Onedrive account. 

Limitations:
-Requires manual input of ADO PAT
-Requires manual input of GraphAPI access token @ (graph.microsoft.com)

Features needed:
-Add user authentication for ADO and GraphAPI functionality
-Add link to final message directly to the file that was just generated. 
-Add Authentication to execute the script as an Azure Function. 
