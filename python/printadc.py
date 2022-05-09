import serial
import math
import numpy

ser = serial.Serial('/dev/ttyACM0',115200)

def printc(val):
	val = min(val,255)
	val = max(val,0)
	print("\033[48;2;" + str(val) + ";" + str(val) + ";"+ str(val) + "m ", end="")

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

while True:
	vals = [x for x in ser.read(34)][:-1]
	xarr = vals[:20]
	yarr = vals[20:]
	yarr = [yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr = [xarr[i]-min(xarr) for i in range(len(xarr))]
	oxarr = xarr
	oyarr = yarr
	xto = 80
	yto = 40
	#ypolyv = numpy.polyfit(range(len(yarr)),yarr, 2)
	#xpolyv = numpy.polyfit(range(len(xarr)),xarr, 2)
	#ypoly = numpy.poly1d(ypolyv)
	#xpoly = numpy.poly1d(xpolyv)
	#yarr = [ ypoly(i*(len(yarr)/yto))for i in range(yto)]
	#xarr = [ xpoly(i*(len(xarr)/xto))for i in range(xto)]
	mapval = max(max(xarr)*max(yarr)/255,1)
	print("\033c")
	for y in range(len(yarr)):
		for x in range(len(xarr)):
			printc(int((xarr[x]*yarr[y])/mapval))
		printc(int(yarr[y]/(max(max(yarr),1)/255)))
		print("")
	for x in range(len(xarr)):
		printc(int(xarr[x]/(max(max(yarr),1)/255)))
	print("\033[0m")
	for z in range(len(oxarr)):
		print(str(oxarr[z]).rjust(3," "),end="")
	for z in range(len(oyarr)):
		print(str(oyarr[z]).rjust(3," "),end="")
	print()
	#print((xpolyv[1]/(-2*xpolyv[0]))*10)
	#print(xpolyv)
	print()
ser.close()
