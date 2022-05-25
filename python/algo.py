import cv2
import numpy as np
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',115200)
xto = 150
yto = 95
totalx = (20-2)*2
def gkey(item):
	return item[1]
def check(item):
	return item[1]>5
while ser.read(1) != b'\xff':
	pass

while True:
	vals = [int(x) for x in ser.read(34)][:-1]
	xarr = list(reversed(vals[:20]))
	yarr = vals[20:]
	yarr = [yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr = [xarr[i]-min(xarr) for i in range(len(xarr))]
	print("\033c")
	maps=[]
	for i in range(totalx):
		out = 2
		if(i%2 == 0):
			out += i//2
		else:
			out += (i-5)//2
		if(out < 4):
			if(out == 0): out = 1
			elif(out == 1): out = 3
			elif(out == 2): out = 0
			elif(out == 3): out = 2
		maps.append((i,xarr[out]));
	print(list(filter(check,sorted(maps,key=gkey))))

	for z in range(len(xarr)):
		print(str(int(xarr[z])).rjust(3," "),end="")
	print()
	for z in range(len(xarr)):
		print(str(z).rjust(3," "),end="")
	print()
	for z in range(len(yarr)):
		print(str(int(yarr[z])).rjust(3," "),end="")
	print()
	for z in range(len(yarr)):
		print(str(z).rjust(3," "),end="")
	print()
	meanx = sum(i*j for i, j in enumerate(xarr))/sum(xarr)

	meany = sum(i*j for i, j in enumerate(yarr))/sum(yarr)
