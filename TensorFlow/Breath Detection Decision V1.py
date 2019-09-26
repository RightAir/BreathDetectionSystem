import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%

# Create functions

def label_fix(label):
    if label < -7.5:
        return 0
    elif label > 7.5:
        return 1
    else:
        return 2

def classSwitch(Classes):

    log = []
    decision = []

    for i in range(0, len(Classes)):
        
        if i == len(Classes):
            
            decision.append(Classes[i - 1])
            
            break
        
        elif i > 0:

            if Classes[i] != Classes[i - 1]:
                log.append(i)

                if len(log) > 1 and Classes[log[-1]] != Classes[log[-2] - 1] \
                and Classes[log[-1]] != 2:
                    decision.append(Classes[i])
                    
                elif len(log) > 1 and Classes[log[-1]] == Classes[log[-2] - 1] \
                and Classes[log[-1]] != 2:
                    decision.append(Classes[i])

                elif Classes[i] == 2:
                    decision.append(Classes[i - 1])

            elif Classes[i] == 2:
                decision.append(Classes[log[-1] - 1])

            else:
                decision.append(Classes[i])

        else:
            decision.append(Classes[i])
            
    return decision

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
y_test.reset_index(inplace = True, drop = True)
y_train.reset_index(inplace = True, drop = True)
X_test.reset_index(inplace = True, drop = True)
X_train.reset_index(inplace = True, drop = True)

columns = ['D1', 'D2', 'P1', 'P2', 'dD1', 'dD2', 'dP1', 'dP2']

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

predictions = model.predict(X_test)

final_pred = []
for score in range(0, len(predictions)):
    final_pred.append(np.argmax(predictions[score]))
    
#%%

final_pred = pd.DataFrame(final_pred, index = None, columns = ['Class'])
final_pred['Class'] = classSwitch(final_pred['Class'])

#%%

y_test = pd.DataFrame(y_test, index = None, columns = ['Class'])
y_test['Class'] = classSwitch(y_test['Class'])

#%%

# Scoring the model on testing data from same dataset

print(classification_report(y_test, final_pred))
    











