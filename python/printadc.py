import serial
import math
import numpy as np

ser = serial.Serial('/dev/ttyACM0',115200)

def printc(val):
	val = min(val,255)
	val = max(val,0)
	print("\033[48;2;" + str(val) + ";" + str(val) + ";"+ str(val) + "m  ", end="")

def printR(val):
	val = min(val,255)
	val = max(val,0)
	print("\033[48;2;" + str(val) + ";" + str(0) + ";"+ str(0) + "m  ", end="")

def cleanme(arr):
	maxed = -1
	for i in range(len(arr)):
		if(maxed != -1):
			if(arr[i] > maxed):
				arr[i] = arr[i-1]
			maxed = arr[i]
		if (arr[i] == max(arr)):
			maxed = arr[i]
	maxed = -1
	for i in reversed(range(len(arr))):
		if(maxed != -1):
			if(arr[i] > maxed):
				arr[i] = arr[i+1]
			maxed = arr[i]
		if (arr[i] == max(arr)):
			maxed = arr[i]
	return arr

def interp(val,max,arr):
	ind = len(arr)/(max+1)
	tot = (val*ind)-1
	a = math.floor(tot)
	b = math.ceil(tot)
	return ((arr[b]-arr[a])*(tot-a))+arr[a]

while ser.read(1) != b'\xff':
	pass
def find_nearest(a, a0):
    idx = np.abs(a - a0).argmin()
    return a.flat[idx]

while True:
	vals = [x for x in ser.read(34)][:-1]
	xarr = vals[:20]
	yarr = vals[20:]
	#xarr = [0,1,0,0,1,0,0,0,0,0,20,22,16,5,0,0]
	#yarr = [0,0,1,0,0,0,5,10,3,0,0,1]
	yarr = [0.01 + yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr = [0.01 + xarr[i]-min(xarr) for i in range(len(xarr))]
	oxarr = xarr
	oyarr = yarr
	xto = 40
	yto = 20

	meanx = sum(i*j for i, j in enumerate(xarr))/sum(xarr)
	xpoint = round(meanx*xto/len(xarr))
	dv = math.sqrt(sum((i-meanx)**2 * j for i, j in enumerate(xarr))/sum(xarr))
	div = math.sqrt(2*math.pi)*dv
	xarr = [math.exp(-0.5*((i - meanx)/dv)**2)/div for i in np.arange(0,len(xarr),len(xarr)/xto)]

	meany = sum(i*j for i, j in enumerate(yarr))/sum(yarr)
	ypoint = round(meany*yto/len(yarr))
	dv = math.sqrt(sum((i-meany)**2 * j for i, j in enumerate(yarr))/sum(yarr))
	div = math.sqrt(2*math.pi)*dv
	yarr = [math.exp(-0.5*((i - meany)/dv)**2)/div for i in np.arange(0,len(yarr),len(yarr)/yto)]
	print("\033c")
	mapval = 255/(max(xarr)*max(yarr))
	for y in range(len(yarr)):
		for x in range(len(xarr)):
			if(x == xpoint and y == ypoint):
				printR(int(xarr[x]*yarr[y]*mapval))
			else:
				printc(int(xarr[x]*yarr[y]*mapval))
		if(y == ypoint):
			printR(int(yarr[y]*(255/max(yarr))))
		else:
			printc(int(yarr[y]*(255/max(yarr))))
		print()
	for x in range(len(xarr)):
		if(x == xpoint):
			printR(int(xarr[x]*(255/max(xarr))))
		else:
			printc(int(xarr[x]*(255/max(xarr))))


	print("\033[0m")
	for z in range(len(oxarr)):
		print(str(int(oxarr[z])).rjust(3," "),end="")
	for z in range(len(oyarr)):
		print(str(int(oyarr[z])).rjust(3," "),end="")
	print()

	#for z in range(len(oyarr)):
	#	print(str(oyarr[z]).rjust(3," "),end="")
	print(meanx*150/12,meany*95/12)
	#print((xpolyv[1]/(-2*xpolyv[0])))
	#print((ypolyv[1]/(-2*ypolyv[0])))
	#print(xpoly)
	#print()
#ser.close()
