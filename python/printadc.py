import serial
ser = serial.Serial('/dev/ttyACM0',115200)
while ser.read(1) != b'\xff':
	pass
while True:
	vals = [x-43 for x in ser.read(34)][:-1]
	print(*vals, end="\r\t\t\t\t\t\t\t\t\t\t\r")
ser.close()