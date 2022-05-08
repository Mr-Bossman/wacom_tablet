import serial
ser = serial.Serial('/dev/ttyACM0',115200)

def printc(val):
	val = min(val,255)
	val = max(val,0)
	print("\033[48;2;" + str(val) + ";" + str(val) + ";"+ str(val) + "m  ", end="")

while ser.read(1) != b'\xff':
	pass
while True:
	vals = [abs(x-43) for x in ser.read(34)][:-1]
	xarr = vals[:20]
	yarr = vals[20:]
	mapval = max(xarr)*max(yarr)/255
	outs = ""
	print('\033c')
	for y in range(len(yarr)):
		for x in range(len(xarr)):
			printc(int((xarr[x]*yarr[y])/mapval))
		print("\033[0m")
	for z in range(len(vals)):
		print(str(vals[z]).rjust(4," "),end='')
	print()
ser.close()