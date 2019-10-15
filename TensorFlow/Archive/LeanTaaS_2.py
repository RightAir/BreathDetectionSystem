import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()

#%%

conn = sqlite3.connect('LeanTaaSTestDB.db')
df = pd.read_sql_query("select * from exchange_transactions;", conn)

for i in range(0, len(df)):
    
    df['created_datetime'][i] = df['created_datetime'][i].split('.')[0]

df['created_datetime'] = pd.to_datetime(df['created_datetime'])

#%%

def transferApproval(df):

    transferApproval_ID = []
    transferDenial_ID = []

    for i in range(0, len(Transfer_IDs)):

            a = df[df['parent_transaction_id'] == Transfer_IDs[i]]

            if len(a[a['action'] == 'APPROVE_TRANSFER']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_TRANSFER'][0]
                    transferApproval_ID.append(index_a)

            elif len(a[a['action'] == 'DENY_TRANSFER']) == 1:

                index_a = a.index[a['action'] == 'DENY_TRANSFER'][0]
                transferDenial_ID.append(index_a)
                
    return transferApproval_ID, transferDenial_ID

transferApproval_ID, transferDenial_ID = transferApproval(df)

totalApprovedTransfers = len(transferApproval_ID)
totalDeniedTransfers = len(transferDenial_ID)

Approval_Rate_Transfers = totalApprovedTransfers / (totalApprovedTransfers + totalDeniedTransfers)
Denial_Rate_Transfers = totalDeniedTransfers / (totalApprovedTransfers + totalDeniedTransfers)

labels = ['Denial Rate %', 'Approval Rate %']

colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig1, ax1 = plt.subplots(figsize = (8, 8))
ax1.pie([Denial_Rate_Transfers, Approval_Rate_Transfers], labels = labels, colors = colors, autopct='%1.1f%%', startangle=90)

centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')  
plt.tight_layout()

def requestApproval(df):

    requestApproval_ID = []
    requestDenial_ID = []

    for i in range(0, len(Request_IDs)):

            a = df[df['parent_transaction_id'] == Request_IDs[i]]

            if len(a[a['action'] == 'APPROVE_REQUEST']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_REQUEST'][0]
                    requestApproval_ID.append(index_a)

            elif len(a[a['action'] == 'DENY_REQUEST']) == 1:

                index_a = a.index[a['action'] == 'DENY_REQUEST'][0]
                requestDenial_ID.append(index_a)
                
    return requestApproval_ID, requestDenial_ID
    
requestApproval_ID, requestDenial_ID = requestApproval(df)

totalApprovedRequests = len(requestApproval_ID)
totalDeniedRequests = len(requestDenial_ID)

Approval_Rate_Requests = totalApprovedRequests / (totalApprovedRequests + totalDeniedRequests)
Denial_Rate_Requests = totalDeniedRequests / (totalApprovedRequests + totalDeniedRequests)

labels = ['Denial Rate %', 'Approval Rate %']

colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig1, ax1 = plt.subplots(figsize = (8, 8))
ax1.pie([Denial_Rate_Requests, Approval_Rate_Requests], labels = labels, colors = colors, autopct='%1.1f%%', startangle=90)

centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')  
plt.tight_layout()

def responseTimeTransfer(df):

    responseTimeTransfer = []

    for i in range(0, len(Transfer_IDs)):

            a = df[df['parent_transaction_id'] == Transfer_IDs[i]]

            b = df[df['transaction_id'] == Transfer_IDs[i]]
            index_b = b.index[0]

            if len(a[a['action'] == 'APPROVE_TRANSFER']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_TRANSFER'][0]
                    responseTimeTransfer.append(a['created_datetime'][index_a] - b['created_datetime'][index_b])

            elif len(a[a['action'] == 'DENY_TRANSFER']) == 1:

                index_a = a.index[a['action'] == 'DENY_TRANSFER'][0]
                responseTimeTransfer.append(a['created_datetime'][index_a] - b['created_datetime'][index_b])
                
    return responseTimeTransfer

responseTimeTransfer = responseTimeTransfer(df)

for i in range(0, len(responseTimeTransfer)):
    
    responseTimeTransfer[i] = responseTimeTransfer[i].total_seconds()/60

averageResponseTimeTransfer = sum(responseTimeTransfer) / len(responseTimeTransfer)

def responseTimeRequest(df):

    responseTimeRequest = []

    for i in range(0, len(Request_IDs)):

            a = df[df['parent_transaction_id'] == Request_IDs[i]]

            b = df[df['transaction_id'] == Request_IDs[i]]
            index_b = b.index[0]

            if len(a[a['action'] == 'APPROVE_REQUEST']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_REQUEST'][0]
                    responseTimeRequest.append(a['created_datetime'][index_a] - b['created_datetime'][index_b])

            elif len(a[a['action'] == 'DENY_REQUEST']) == 1:

                index_a = a.index[a['action'] == 'DENY_REQUEST'][0]
                responseTimeRequest.append(a['created_datetime'][index_a] - b['created_datetime'][index_b])
                
    return responseTimeRequest

responseTimeRequest = responseTimeRequest(df)              

for i in range(0, len(responseTimeRequest)):
    
    responseTimeRequest[i] = responseTimeRequest[i].total_seconds()/60
    
averageResponseTimeRequest = sum(responseTimeRequest) / len(responseTimeRequest)

plt.figure(figsize = (8, 8))
plt.title('Average Response Time per Action')
plt.xlabel('Action Type')
plt.ylabel('Duratino in minutes')
plt.bar(x = ['Request', 'Transfer'], 
        height = [averageResponseTimeRequest, 
                  averageResponseTimeTransfer], 
                    color = 'g', alpha = 0.3)