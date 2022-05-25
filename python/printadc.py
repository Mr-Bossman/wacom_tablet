import cv2
import numpy as np
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',115200)
xto = 150*4
yto = 95*4
img = np.zeros([yto,xto,3],dtype=np.uint8)
cons = math.sqrt(2*math.pi)
while ser.read(1) != b'\xff':
	pass

while True:
	vals = [x for x in ser.read(34)][:-1]
	xarr = vals[:20]
	yarr = vals[20:]
	yarr = [0.01 + yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr = [0.01 + xarr[i]-min(xarr) for i in range(len(xarr))]
	print("\033c")
	for z in range(len(xarr)):
		print(str(int(xarr[z])).rjust(3," "),end="")
	for z in range(len(yarr)):
		print(str(int(yarr[z])).rjust(3," "),end="")
	print()

	meanx = sum(i*j for i, j in enumerate(xarr))/sum(xarr)
	dvx = math.sqrt(sum((i-meanx)**2 * j for i, j in enumerate(xarr))/sum(xarr))
	divx = cons*dvx

	meany = sum(i*j for i, j in enumerate(yarr))/sum(yarr)
	dvy = math.sqrt(sum((i-meany)**2 * j for i, j in enumerate(yarr))/sum(yarr))
	divy = cons*dvy

	print(meanx*150/20,meany*95/12)

	mapval = 255*2

	offx = min(2*dvx,2.5)
	offy = min(2*dvy,2.5)
	img.fill(0)
	for x in range(max(int(xto*(meanx-offx)/len(xarr)),0),min(int(xto*(meanx+offx)/len(xarr)),xto)):
		for y in range(max(int(yto*(meany-offy)/len(yarr)),0),min(int(yto*(meany+offy)/len(yarr)),yto)):
			yind = y*(len(yarr)/yto)
			xind = x*(len(xarr)/xto)
			yval = math.exp(-0.5*((yind - meany)/dvy)**2)/divy
			xval = math.exp(-0.5*((xind - meanx)/dvx)**2)/divx
			bright = int(yval*xval*mapval)
			if abs(meanx-xind) < 0.02 and abs(meany-yind) < 0.02:
				img[y][x] = (0,0,bright)
			else:
				img[y][x] = (bright,bright,bright)
	cv2.imshow('pix', cv2.resize(img, (xto*4,yto*4), interpolation = cv2.INTER_AREA))
	if cv2.waitKey(10) != -1:
		break
