#%% LeanTaaS Problem Set
# Michael Furr
# October 2019

# INPUTS
# .db file with transaction_id, parent_transaction_id, action, scheduler, 
# surgeon, created_timeframe, snapshot_date, start_time, end_time, room_name,
# location

# OUTPUTS
# Excel file with Approval Rates / Denial Rates, Total Time per Transaction, 
# Average Response Time
# Figures displaying total transaction time, approval rates, and time for
# response for each transaction

#%% Import Libraries

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

#%% QUESTION 1

#%% Extract Data into Pandas DF

conn = sqlite3.connect('LeanTaaSTestDB.db')
df = pd.read_sql_query("select * from exchange_transactions;", conn)

# Clean 'created_datetime' column'

for i in range(0, len(df)):
    
    df['created_datetime'][i] = df['created_datetime'][i].split('.')[0]

df['created_datetime'] = pd.to_datetime(df['created_datetime'])

#%% Generate functions to pull release, transfer, and request time

def releaseTime(df):
    
    # Empty list for storage
    Release_IDs = []
    
    # Add Release transaction IDs to storage
    for i in range(0, len(df)):

        if df['action'][i] == 'RELEASE':
        
            Release_IDs.append(df['transaction_id'][i])
    
    releaseTime = []
    
    # Append time difference between parent transaction and when related
    # 'Marked_Completed' instance has occured to close the transaction
    for i in range(0, len(Release_IDs)):
    
        releaseTime.append(df[df['parent_transaction_id'] == Release_IDs[i]]\
                           ['created_datetime']\
                           [df.index[df['parent_transaction_id']\
                                     == Release_IDs[i]][0]] - \
                                     df[df['transaction_id'] == \
                                        Release_IDs[i]]['created_datetime']\
                                        [df.index[df['transaction_id'] == \
                                                  Release_IDs[i]][0]])
        
    # Store the gathered release time in minutes
    for i in range(0, len(releaseTime)):
    
        releaseTime[i] = releaseTime[i].total_seconds()/60
        
    # Sum all release times to obtain total time spent on release transactions    
    totalReleaseTime = sum(releaseTime)
    
    # Return all stored data
    return Release_IDs, releaseTime, totalReleaseTime

Release_IDs, releaseTime, totalReleaseTime = releaseTime(df)

def transferTime(df):
    
    Transfer_IDs = []

    for i in range(0, len(df)):
    
        if df['action'][i] == 'TRANSFER':
        
            Transfer_IDs.append(df['transaction_id'][i])
            
    transferTime = []
    
    # Traverse transfer IDs and find where the transaction ID connected to the
    # parent has been "Mark_Updated" or Denied. Then count the length of time
    # it took to either Complete or Deny the transaction
    for i in range(0, len(Transfer_IDs)):
        
        a = df[df['parent_transaction_id'] == Transfer_IDs[i]]
    
        if len(a[a['action'] == 'MARK_UPDATED']) == 1:
        
            index_a = a.index[a['action'] == 'MARK_UPDATED'][0]
    
            b = df[df['transaction_id'] == Transfer_IDs[i]]
            index_b = b.index[0]
    
            transferTime.append(a['created_datetime'][index_a] - \
                                b['created_datetime'][index_b])
        
        elif len(a[a['action'] == 'DENY_TRANSFER']) == 1:
            
            index_a = a.index[a['action'] == 'DENY_TRANSFER'][0]
            
            b = df[df['transaction_id'] == Transfer_IDs[i]]
            index_b = b.index[0]
            
            transferTime.append(a['created_datetime'][index_a] - \
                                b['created_datetime'][index_b])
        
    for i in range(0, len(transferTime)):
    
        transferTime[i] = transferTime[i].total_seconds()/60
        
    totalTransferTime = sum(transferTime)
    
    return Transfer_IDs, transferTime, totalTransferTime

Transfer_IDs, transferTime, totalTransferTime = transferTime(df)

def requestTime(df):
    
    Request_IDs = []

    for i in range(0, len(df)):
    
        if df['action'][i] == 'REQUEST':
        
            Request_IDs.append(df['transaction_id'][i])
            
    requestTime = []

    # Traverse request IDs and find where the transaction ID connected to the
    # parent has been "Mark_Updated" or Denied. Then count the length of time
    # it took to either Complete or Deny the transaction
    for i in range(0, len(Request_IDs)):
        
        a = df[df['parent_transaction_id'] == Request_IDs[i]]
    
        if len(a[a['action'] == 'MARK_UPDATED']) == 1:
        
            index_a = a.index[a['action'] == 'MARK_UPDATED'][0]
    
            b = df[df['transaction_id'] == Request_IDs[i]]
            index_b = b.index[0]
    
            requestTime.append(a['created_datetime'][index_a] - \
                               b['created_datetime'][index_b])
        
        elif len(a[a['action'] == 'DENY_REQUEST']) == 1:
            
            index_a = a.index[a['action'] == 'DENY_REQUEST'][0]
            
            b = df[df['transaction_id'] == Request_IDs[i]]
            index_b = b.index[0]
            
            transferTime.append(a['created_datetime'][index_a] - \
                                b['created_datetime'][index_b])
        
    for i in range(0, len(requestTime)):
    
        requestTime[i] = requestTime[i].total_seconds()/60
        
    totalRequestTime = sum(requestTime)
        
    return Request_IDs, requestTime, totalRequestTime

Request_IDs, requestTime, totalRequestTime = requestTime(df)

#%% EDA - Plotting total response time for completed and denied transactions

results = pd.DataFrame([totalRequestTime, totalTransferTime, \
                        totalReleaseTime], columns = ['Total Duration (min)'])
results.sort_values('Total Duration (min)', inplace = True)
results['Action Type'] = ['Transfer', 'Release', 'Request']

fig1 = plt.figure(figsize = (7.5, 5.5))
plt.title('Total Duration per Action Type')
sns.barplot(x = 'Action Type', y = 'Total Duration (min)', \
            data = results, palette = 'Blues_d')
fig1.savefig('Total_Action_Duration.png')

#%% EDA - Plotting perecentage time spent on each type of transaction

colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig2, ax2 = plt.subplots(figsize = (5.5, 5.5))
ax2.pie(results['Total Duration (min)'], colors = colors, \
                labels = results['Action Type'], autopct='%1.1f%%', \
                startangle=90)
plt.title('Action Type Distribution by Time')
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig3 = plt.gcf()
fig3.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
ax2.axis('equal')  
plt.tight_layout()

results.iplot(kind = 'bar', x = 'Action Type', 
              y = 'Total Duration (min)', 
              title = 'Total Duration per Action Type', 
             xTitle = 'Action Type', 
             yTitle = 'Total Duration (min)', color = 'rgba(50, 171, 96, 1.0)')

fig3.savefig('Action_Type_Distribution.png')

#%% QUESTION 2

# Create function to log IDs of both approved and denied transactions
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

# Gather the total amount of approved and denied transactions, respectively
totalApprovedTransfers = len(transferApproval_ID)
totalDeniedTransfers = len(transferDenial_ID)

# Calculate approval and denial rates
Approval_Rate_Transfers = totalApprovedTransfers / \
(totalApprovedTransfers + totalDeniedTransfers)
Denial_Rate_Transfers = totalDeniedTransfers / \
(totalApprovedTransfers + totalDeniedTransfers)

#%%
# Plot approval and denial rates as pi chart
labels = ['Denial Rate %', 'Approval Rate %']
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
fig4, ax4 = plt.subplots(figsize = (5.5, 5.5))
ax4.pie([Denial_Rate_Transfers, Approval_Rate_Transfers], labels = labels, \
        colors = colors, autopct='%1.1f%%', startangle=90)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig5 = plt.gcf()
fig5.gca().add_artist(centre_circle)
ax4.axis('equal')  
plt.title('Transfers Approval Rate', {'horizontalalignment': 'left'})
plt.tight_layout()

fig5.savefig('Approval_Rate_Transfers.png')

#%%
# Perform same analysis for request transactions
# Note that release transactions were not considered since they are
# accepted automatically
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

Approval_Rate_Requests = totalApprovedRequests / \
(totalApprovedRequests + totalDeniedRequests)
Denial_Rate_Requests = totalDeniedRequests / \
(totalApprovedRequests + totalDeniedRequests)

#%%
# Plotting
labels = ['Denial Rate %', 'Approval Rate %']
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
fig6, ax6 = plt.subplots(figsize = (5.5, 5.5))
ax6.pie([Denial_Rate_Requests, Approval_Rate_Requests], \
        labels = labels, colors = colors, autopct='%1.1f%%', startangle=90)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig7 = plt.gcf()
fig7.gca().add_artist(centre_circle)
plt.title('Request Approval Rate', {'horizontalalignment': 'left'})
ax6.axis('equal')  
plt.tight_layout()
fig7.savefig('Approval_Rate_Requests.png')

#%%
# Create function to gather time between either an approval or denial
# of a transfer. Note this is the time until an approval and does not
# reflect time to a final "Mark_Updated" transaction
def responseTimeTransfer(df):

    responseTimeTransfer = []

    for i in range(0, len(Transfer_IDs)):

            a = df[df['parent_transaction_id'] == Transfer_IDs[i]]

            b = df[df['transaction_id'] == Transfer_IDs[i]]
            index_b = b.index[0]

            if len(a[a['action'] == 'APPROVE_TRANSFER']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_TRANSFER'][0]
                    responseTimeTransfer.append\
                    (a['created_datetime'][index_a] - b['created_datetime']\
                     [index_b])

            elif len(a[a['action'] == 'DENY_TRANSFER']) == 1:

                index_a = a.index[a['action'] == 'DENY_TRANSFER'][0]
                responseTimeTransfer.append(a['created_datetime']\
                                            [index_a] - \
                                            b['created_datetime'][index_b])
                
    return responseTimeTransfer

responseTimeTransfer = responseTimeTransfer(df)

# Convert to minutes
for i in range(0, len(responseTimeTransfer)):
    
    responseTimeTransfer[i] = responseTimeTransfer[i].total_seconds()/60

# Gather average
averageResponseTimeTransfer = sum(responseTimeTransfer) / \
len(responseTimeTransfer)

# Perform same analysis for request response times
def responseTimeRequest(df):

    responseTimeRequest = []

    for i in range(0, len(Request_IDs)):

            a = df[df['parent_transaction_id'] == Request_IDs[i]]

            b = df[df['transaction_id'] == Request_IDs[i]]
            index_b = b.index[0]

            if len(a[a['action'] == 'APPROVE_REQUEST']) == 1:

                if len(a[a['action'] == 'MARK_UPDATED']) == 1:

                    index_a = a.index[a['action'] == 'APPROVE_REQUEST'][0]
                    responseTimeRequest.append(a['created_datetime']\
                                               [index_a] - \
                                               b['created_datetime'][index_b])

            elif len(a[a['action'] == 'DENY_REQUEST']) == 1:

                index_a = a.index[a['action'] == 'DENY_REQUEST'][0]
                responseTimeRequest.append(a['created_datetime']\
                                           [index_a] - \
                                           b['created_datetime'][index_b])
                
    return responseTimeRequest

responseTimeRequest = responseTimeRequest(df)              

for i in range(0, len(responseTimeRequest)):
    
    responseTimeRequest[i] = responseTimeRequest[i].total_seconds()/60
    
averageResponseTimeRequest = sum(responseTimeRequest) / \
len(responseTimeRequest)

#%%
# Plot comparison between request and transfer response times
fig8 = plt.figure(figsize = (5.5, 5.5))
plt.title('Average Response Time per Action')
plt.xlabel('Action Type')
plt.ylabel('Duratino in minutes')
plt.bar(x = ['Request', 'Transfer'], 
        height = [averageResponseTimeRequest, 
                  averageResponseTimeTransfer], 
                    color = 'g', alpha = 0.3)
fig8.savefig('Average_Response_Time.png')

#%% Save and export data for customer in 
# Excel Spreadsheet (within current folder)

CustomerData = {'Action Type': ['Requests', 'Transfers', 'Releases']\
                , 'Approval Rate': \
                [Approval_Rate_Requests, Approval_Rate_Transfers, '--'], 
               'Denial Rate': \
               [Denial_Rate_Requests, Denial_Rate_Transfers, '--'],
               'Average Response Time': [averageResponseTimeRequest, \
                                         averageResponseTimeTransfer, '--'],
              'Total Request Time': [totalRequestTime, totalTransferTime, \
                                     totalReleaseTime]}

Results = pd.DataFrame(data = CustomerData)
Results.set_index('Action Type', drop = True, inplace = True)

writer = pd.ExcelWriter('TransactionData.xlsx', engine='xlsxwriter')
Results.to_excel(writer, sheet_name = 'Sheet1')
writer.save()
