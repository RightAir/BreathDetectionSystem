import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read in dataframe from csv file
df = pd.read_csv('fbdh1.csv')

#%%

# Create functions

def label_fix(label):
    if label < -7.5:
        return 0
    elif label > 7.5:
        return 1
    else:
        return 2

df['Class'] = df['Flow'].apply(label_fix)

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

columns = ['D1', 'D2', 'P1', 'P2', 'dD1', 'dD2', 'dP1', 'dP2']

#%%

time = range(0, 6664)
flow = df['Flow']
pressure = df['P1']
distance = df['D1']

fig = plt.figure(figsize = (8, 6))
plt.subplot(3,1,1)
plt.plot(time, flow, 'b') # 'r' is the color red
plt.xlabel('Time')
plt.ylabel('Flow')
plt.title('Flow over Time')

fig = plt.figure(figsize = (8, 6))
plt.subplot(3,1,2)
plt.plot(time, pressure, 'b')
plt.xlabel('Time')
plt.ylabel('Pressure')
plt.title('Pressure over Time')

fig = plt.figure(figsize = (8, 6))
plt.subplot(3,1,2)
plt.plot(time, distance, 'b')
plt.xlabel('Time')
plt.ylabel('Distance')
plt.title('Distance over Time')

#%%

fig = plt.figure(figsize = (18, 5))
sns.scatterplot(y = df['Flow'][0:100], x = range(0, 100), hue = df['Class']\
                [0:100], palette = 'coolwarm')

#%%

fig = plt.figure(figsize = (18, 10))
plt.subplot(4, 1, 1)
sns.scatterplot(y = X['D1'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

plt.subplot(4, 1, 2)
sns.scatterplot(y = X['D2'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

plt.subplot(4, 1, 3)
sns.scatterplot(y = X['P1'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

plt.subplot(4, 1, 4)
sns.scatterplot(y = X['P1'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

#%%

fig = plt.figure(figsize = (18, 10))
plt.subplot(2, 1, 1)
sns.scatterplot(y = X['dD1'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

plt.subplot(2, 1, 2)
sns.scatterplot(y = X['dD2'][0:650], x = range(0, 650), hue = df['Class']\
                [0:650], palette = 'coolwarm')

#%%

# Develop keras sequential model with optimized parameters through
# grid search cv

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

#%%

EPOCHS = 50
model.fit(X_train, y_train, epochs = EPOCHS)

#%%

