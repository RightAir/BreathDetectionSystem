##%

# NOTES

# Precision Scores
# 0: 0.95 - inhale
# 1: 0.78 - no action
# 2: 0.91 - exhale

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%

# Create class labeling function

def label_fix(label):
    if label < -7.5:
        return 0
    elif label > 7.5:
        return 2
    else:
        return 1
    
# Create moving average to remove single outliers
        
def movingAvg(Class, windowSize):
    
    filteredClass = []
    
    for i in range(0, len(Class)):
        
        if i <= windowSize:
            
            filteredClass.append(Class[i])
            
        elif Class[i] != Class[i - 1]:
            
            if sum(Class[i - windowSize:i]) / windowSize > 1:
                
                filteredClass.append(2)
                
            elif sum(Class[i - windowSize:i]) / windowSize < 1:
                
                filteredClass.append(0)
                
            else:
                
                filteredClass.append(Class[i])
                
        elif Class[i] == Class[i - 1]:
            
            filteredClass.append(Class[i])
        
    return filteredClass

#%%

# Read in data

df = pd.read_csv('fbdh1.csv')
df['Class'] = df['Flow'].apply(label_fix)

#%%
    
# Create the data matrix and normalize data columns

X = df.drop('Class', axis = 1)
X.drop('Flow', axis = 1, inplace = True)
scaler = StandardScaler()
scaler.fit(X)
scaled_features = scaler.transform(X)
X = pd.DataFrame(scaled_features, columns = X.columns[:])

# Create the classification matrix

y = df['Class']

# Perform train test split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

#%%

# Develop keras sequential model with optimized parameters through grid search cv

model = keras.Sequential()
model.add(keras.layers.Dense(150, activation = tf.nn.relu, input_dim = 8))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(50, activation = tf.nn.relu))
model.add(keras.layers.Dropout(0.4))
model.add(keras.layers.Dense(3, activation = tf.nn.softmax))

model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])
model.summary()

EPOCHS = 50
model.fit(X_train, y_train, epochs = EPOCHS)

#%%

# Sort both x and y test back into the correct order

X_test.sort_index(inplace = True)
y_test.sort_index(inplace = True)

predictions = model.predict(X_test)

final_pred = []

for i in range(0, len(predictions)):
    
    final_pred.append(np.argmax(predictions[i]))

# Scoring the model on testing data from same dataset
    
#%%

print(classification_report(y_test, final_pred))

#%%

# Decision algorithm (V2) - confidence threshold
# Create confidence threshold just for switching to class 2
# Note you can only use this when the data is in order

#def confidenceFilter(confidenceList):
#    
#    new_pred = []
#    
#    for i in range(0, len(predictions)):
#        
#        if i == 0:
#            
#            new_pred.append(np.argmax(confidenceList[i]))
#        
#        else:
#        
#            if np.max(confidenceList[i]) > 0.65:
#
#                new_pred.append(np.argmax(confidenceList[i]))
#            
#            else:
#            
#                new_pred.append(new_pred[i - 1])
#                
#    return new_pred

#%%
    
#print(classification_report(y_test, confidenceFilter(predictions)))














