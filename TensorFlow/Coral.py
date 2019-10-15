"""
CORAL BREATH DETECTION SCRIPT

WORKING VERSION

Purpose:
	Gather sensor data in real time and perform predictions to actuate blowers

Outputs:
	Real time actuation to blowers
	Raw data from sensors stored over period of classification
	Stored classification data

Change Log:
	10.15 - Created initial script

Improvements:
	Real time data scaling
	Read in all data (beyond proximity sensor)
	Format script as a Coral object with methdos for:
		Classification streaming
		Instantaneous class
		Data gathering only
	Create user input for methods to stop classification or data gathering
	Execute control of the valve based on classification
		Note that this control could be held until the ~10th classification to
		let the system stabilize first
	Could potentially include a training method to gather a certain amount of data,
	create the model, and then start performing classifications

"""

# Import Libraries
import Proximity_Sensor
import time

# Setup Sensor Objects
Proximity = Proximity_Sensor.VCNL4010()

# Instantiate TF Lite Model
interpreter = Interpreter(model_path = "my_tflite_model_4.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Create Empty Data Storage
Raw_Data = []
Predictions = []

while(True):

	input_data = np.float32([Proximity.proximity])
	Raw_Data.append(input_data)

	interpreter.set_tensor(input_details[0]['index'], input_data)
	interpreter.invoke()

	if len(Predictions) < 5:
		Current_Class = np.argmax(interpreter.get_tensor(output_details[0]['index']))
		Predictions.append(np.argmax(interpreter.get_tensor(output_details[0]['index'])))
		print(Current_Class)

	else:
		Predictions.append(np.arg(interpreter.get_tensor(output_details[0]['index'])))
		Predictions = classSwitch(Predictions)
		Current_Class = Predictions[-1]
		print(Current_Class)

return Predictions