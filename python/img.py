import cv2
import numpy as np
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',115200)
xto = 150
yto = 95
cv2.namedWindow('pix', cv2.WINDOW_NORMAL)
img = np.zeros([yto,xto,3],dtype=np.uint8)
cons = math.sqrt(2*math.pi)
def gkey(item):
	return item[1]
while ser.read(1) != b'\xff':
	pass

while True:
	(x,y,w,h) = cv2.getWindowImageRect('pix')
	w -= 1
	if(xto != w):
		yto = int(w*yto/xto)
		xto = w
		img = np.zeros([yto,xto,3],dtype=np.uint8)
	vals = [int(x) for x in ser.read(34)][:-1]
	#vals =[0,0,0,0,0,0,0,0,0,0,0,0,0,7,8,2,0,0,0,0,0,8,8,0,0,0,0,0,0,0,0,0,0]
	xarr = list(reversed(vals[:20]))
	yarr = vals[20:]
	print("\033c")
	print(sorted(enumerate(xarr),key=gkey)[-5:])
	yarr = [0.01 + yarr[i]-min(yarr) for i in range(len(yarr))]
	xarr = [0.01 + xarr[i]-min(xarr) for i in range(len(xarr))]
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
	dvx = math.sqrt(sum((i-meanx)**2 * j for i, j in enumerate(xarr))/sum(xarr))
	divx = cons*dvx

	meany = sum(i*j for i, j in enumerate(yarr))/sum(yarr)
	dvy = math.sqrt(sum((i-meany)**2 * j for i, j in enumerate(yarr))/sum(yarr))
	divy = cons*dvy

	#print(meanx*150/20,meany*95/12)

	mapval = 255*2.3
	img = cv2.circle(img,(round(meanx*xto/20),round(meany*yto/12)),0,(0,0,255),5)
	cv2.imshow('pix', img)
	if cv2.waitKey(10) != -1:
		break
