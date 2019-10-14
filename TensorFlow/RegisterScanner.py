from periphery import I2C

i2c = I2C('/dev/i2c-1')

for i in range(80, 90):

	msgs = [I2C.Message([0xi]), I2C.Message([0x00], read=True)]
	i2c.transfer(0x13, msgs)
	print(msgs[1].data)