import Proximity_Sensor
import time

Proximity = Proximity_Sensor.VCNL4010()

Proximity_Data = []
try:
	print('Ctrl-C to end')
	while(True):
		Proximity_Data.append(Proximity.proximity)
		print(Proximity.proximity)
		time.sleep(1)
	except KeyboardInterrupt, e:
		print('Stopped')
		raise