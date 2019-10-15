import pandas as pd
import numpy as np
from tflite_runtime.interpreter import Interpreter
from sklearn import preprocessing

# Create moving average to remove single outliers
        
def movingAvg(Class, windowSize):
    
    filteredClass = []
    
    for i in range(0, len(Class)):
        
        if i < windowSize - 1:
            
            filteredClass.append(Class[i])
            
        elif Class[i] != Class[i - 1]:
            
            if sum(Class[i - (windowSize - 1):(i + 1)]) / windowSize > 1:
                
                filteredClass.append(2)
                
            elif sum(Class[i - (windowSize - 1):(i + 1)]) / windowSize < 1:
                
                filteredClass.append(0)
                
            else:
                
                filteredClass.append(Class[i])
                
        elif Class[i] == Class[i - 1]:
            
            filteredClass.append(Class[i])
        
    return filteredClass

def classSwitch(Class):

    decision = []
    switchLog = []

    for i in range(0, len(Class)):
        
        if i >= 1:
            
            if Class[i] != Class[i - 1]:
            
                # Log when it changes to 1
                
                if Class[i] == 1:
                
                    switchLog.append(i)
                    
                # If it changes to 0 or 2, add to final
                
                if Class[i] == 2 or Class[i] == 0:

                    decision.append(Class[i])
            
            # If the values continue to be 1, change to value before switch
            
            if Class[i] == 1:
                
                decision.append(Class[switchLog[-1] - 1])
                
            # If the value does not change and it is not 1, add to final
            
            elif Class[i] == Class[i - 1] and Class[i] != 1:
                
                decision.append(Class[i])
                
        # Add first value to final
        
        else:
            
            decision.append(Class[i])
            
    # Return the moving average with a window of 3 for the final list
    # to remove jumps between classes
    return movingAvg(decision, 3)
    
#%%

def main():

    data = pd.read_csv('fbdh1.csv')
    data.drop(['Flow'], axis = 1, inplace = True)
    scaler = preprocessing.MinMaxScaler(feature_range = (0, 1))
    scaler.fit(data)
    data = scaler.transform(data)
    data = np.float32(data.values)
    
    interpreter = Interpreter(model_path="my_tflite_model_4.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    predictions = []
    
    for i in range(0, len(data)):
        
        input_data = data[i]
        input_data = map(scale, input_data)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        predictions.apppend(interpreter.get_tensor(output_details[0]['index']))
    
    return predictions
    
main()