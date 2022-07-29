import numpy as np
import serial
import math

ser = serial.Serial('/dev/ttyUSB1',115200)
xto = 150
yto = 95
def calc(arr):
	#maps = list(filter(lambda i:i[1]>5,sorted(,key=lambda i:i[1])))
	maximal = maps[-1][0]
	maps = list(filter(lambda a: abs(maximal-a[0]) <= 2,enumerate(arr)))
	return [m[1] for m in maps]
def prii(arr):
	for z in range(len(arr)):
		print(str(int(arr[z])).rjust(3," "),end="")
	print()
	for z in range(len(arr)):
		print(str(z).rjust(3," "),end="")
	print()

while ser.read(1) != b'\xff':
	pass

while True:
	vals = [int(x) for x in ser.read(34)][:-1]
	xarr = list(reversed(vals[:20]))
	yarr = vals[20:]
	yarr = [yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr =list(reversed([xarr[i]-min(xarr) for i in range(len(xarr))]))
	print("\033c")

	all = list(filter(lambda i:i[1] > max(xarr)/2, enumerate(xarr)))
	all.append((all[-1][0]+1,0))
	#all = [(all[0][0]+1,0)] + all
	print(all)
	x = np.array([i[0] for i in all])
	y = np.array([i[1] for i in all])
	z = np.polyfit(x, y, 2)
	print(round((-z[1]/(2*z[0]))*(xto/20),2))
	prii(xarr)
	meanx = sum(i*j for i, j in enumerate(xarr))/sum(xarr)
	print(meanx)
	#meany = sum(i*j for i, j in enumerate(yarr))/sum(yarr)
