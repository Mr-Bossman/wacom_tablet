import sys
import os
import pcbnew
from pcbnew import *
countx = 36
county = 24
count_per = 6
total_height = 95
total_width = 150
track_width = 0.25
track_spaceing = 0.4
corner = (75,200)

TRACK_loopover = [[(0.0, 0.0), (0.0, -2.8), (1.2, -4), (4.6, -4), (7.0, -6.4), (10.4, -6.4), (11.4, -7.4), (11.4, -8.8)],
[(-0.0, 0.0), (-0.0, -3.0), (1.4, -4.4), (4.8, -4.4), (7.2, -6.8), (10.6, -6.8), (10.8, -7.0), (10.8, -8.8)],
[(0.0, 0.0), (0.0, -3.2), (1.6, -4.8), (5.0, -4.8), (7.4, -7.2), (9.6, -7.2), (10.2, -7.8), (10.2, -8.8)],
[(0.0, 0.0), (0.0, -3.4), (1.8, -5.2), (5.2, -5.2), (7.6, -7.6), (9.2, -7.6), (9.6, -8.0), (9.6, -8.8)],
[(0.0, 0.0), (0.0, -3.6), (2.0, -5.6), (5.4, -5.6), (7.8, -8.0), (8.6, -8.0), (9.0, -8.4), (9.0, -8.8)],
[(-0.0, 0.0), (-0.0, -3.8), (2.2, -6.0), (5.6, -6.0), (8.6, -9.0), (8.6, -9.4), (8.8, -9.6), (13.6, -9.6), (14.4, -8.8)]]

TRACK_loop = [[(0.0, 0.0), (0.0, -3.8), (2.2, -6.0), (5.6, -6.0), (8.0, -8.4), (9.0, -8.4), (9.4, -8.8)],
[(0.0, 0.0), (0.0, -3.6), (2.0, -5.6), (5.4, -5.6), (7.8, -8.0), (9.6, -8.0), (10.0, -8.4), (10.0, -8.8)],
[(0.0, 0.0), (0.0, -3.4), (1.8, -5.2), (5.2, -5.2), (7.6, -7.6), (10.2, -7.6), (10.6, -8.0), (10.6, -8.8)],
[(0.0, 0.0), (0.0, -3.2), (1.6, -4.8), (5.0, -4.8), (7.4, -7.2), (10.6, -7.2), (11.2, -7.8), (11.2, -8.8)],
[(0.0, 0.0), (0.0, -3.0), (1.4, -4.4), (4.8, -4.4), (7.2, -6.8), (11.6, -6.8), (11.8, -7.0), (11.8, -8.8)],
[(0.0, 0.0), (0.0, -2.8), (1.2, -4.0), (4.6, -4.0), (7.0, -6.4), (11.4, -6.4), (12.4, -7.4), (12.4, -8.8)]]

TRACK_jump = [[(-10.6, -8.8), (-8.25, -6.3), (-5.95, -6.3), (-2.9, -3.15), (-0.7, -3.15), (-0.7, -3.0)],
[(-10.0, -8.8), (-8.05, -6.85), (-6.3, -6.85), (-3.15, -3.7), (-0.8, -3.7), (-0.5, -3.4), (-0.5, -2.1)],
[(-9.4, -8.8), (-9.4, -8.4), (-8.25, -7.25), (-6.5, -7.25), (-3.35, -4.1), (-1.0, -4.1), (-0.1, -3.2), (-0.1, -3.0)],
[(-8.8, -8.8), (-8.8, -8.2), (-8.25, -7.65), (-6.7, -7.65), (-3.55, -4.5), (-0.8, -4.5), (0.1, -3.6), (0.1, -2.1)],
[(-8.2, -8.8), (-8.2, -8.4), (-7.85, -8.05), (-6.85, -8.05), (-3.85, -5.0), (-1.0, -5.0), (0.5, -3.5), (0.5, -3.0)],
[(-7.6, -8.8), (-7.15, -8.8), (-4.05, -5.65), (-1.2, -5.65), (0.7, -3.75), (0.7, -2.1)]]

TRACK_spurr = [[(0,0),(0,-1.1),(-0.7,-1.8),(-0.7,-3)],
[(0,0),(0,-1.2),(-0.5,-1.7),(-0.5,-2.1)],
[(0,0),(0,-1.3),(-0.2,-1.5),(-0.2,-2.9),(-0.1,-3)],
[(0,0),(0,-2),(0.1,-2.1)],
[(0,0),(0,-1.4),(0.5,-1.9),(0.5,-3)],
[(0,0),(0,-1.2),(0.7,-1.9),(0.7,-2.1)]]

def createtrack(board,sp,ep,width,layer,net):
	track = PCB_TRACK(board)
	track.SetStart(wxPointMM(sp[0],sp[1]))
	track.SetEnd(wxPointMM(ep[0],ep[1]))
	track.SetWidth(width)
	track.SetLayer(layer)
	board.Add(track)
	track.SetNetCode(0)

def loopNumX(i):
	return track_spaceing*i*((total_width/track_spaceing)//(countx-1))

def loopNumY(i):
	return track_spaceing*i*((total_height/track_spaceing)//(county-1))

def routeArr(board,line,width,layer,net):
	for i in range(1,len(line)):
		createtrack(board,line[i-1],line[i],width,layer,net)

def offsetArr(line,offset):
	l = list(line)
	for i in range(len(line)):
		l[i] = (line[i][0] + offset[0], line[i][1] + offset[1])
	return l

def mulArr(line,offset):
	l = list(line)
	for i in range(len(line)):
		l[i] = (line[i][0] * offset[0], line[i][1] * offset[1])
	return l

def swapArr(line):
	l = list(line)
	for i in range(len(line)):
		l[i] = (line[i][1], line[i][0])
	return l

def run_viaFront(board,offset):
	#spurr top and bottom
	tracesF = TRACK_spurr
	for i in range(len(tracesF)):
		arr = offsetArr(tracesF[i],(offset[0]+i*track_spaceing,offset[1]))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')
		arr = offsetArr(mulArr(tracesF[i],(-1,-1)),(offset[0]+(-i*track_spaceing)-(track_spaceing*(count_per-1)),offset[1]+total_height))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')
	#back top and bottom
	tracesB = TRACK_jump
	for i in range(len(tracesB)):
		arr = offsetArr(tracesB[i],(offset[0]+i*track_spaceing,offset[1]))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')
		arr = offsetArr(mulArr(tracesB[i],(-1,-1)),(offset[0]+(-i*track_spaceing)-(track_spaceing*(count_per-1)),offset[1]+total_height))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')
	#front top
	tracesF = TRACK_loop
	for i in range(len(tracesF)):
		arr = offsetArr(tracesF[i],(offset[0]+(i*track_spaceing)-loopNumX(1),offset[1]))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')
	#front bottom
	tracesF = TRACK_loopover
	for i in range(len(tracesF)):
		arr = offsetArr(mulArr(tracesF[i],(-1,-1)),(offset[0]+(i*track_spaceing),offset[1]+total_height))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')

def run_viaBack(board,offset):
	#spurr top and bottom
	tracesF = TRACK_spurr
	for i in range(len(tracesF)):
		arr = offsetArr(swapArr(tracesF[i]),(offset[0],offset[1]+i*track_spaceing))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')
		arr = offsetArr(mulArr(swapArr(tracesF[i]),(-1,-1)),(offset[0]+total_width,offset[1]+(-i*track_spaceing)-(track_spaceing*(count_per-1))))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')
	#back top and bottom
	tracesB = TRACK_jump
	for i in range(len(tracesB)):
		arr = offsetArr(swapArr(tracesB[i]),(offset[0],offset[1]+i*track_spaceing))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')
		arr = offsetArr(mulArr(swapArr(tracesB[i]),(-1,-1)),(offset[0]+total_width,offset[1]+(-i*track_spaceing)-(track_spaceing*(count_per-1))))
		routeArr(board,arr,FromMM(track_width),F_Cu,'GND')
	#front top
	tracesF = TRACK_loop
	for i in range(len(tracesF)):
		arr = offsetArr(swapArr(tracesF[i]),(offset[0],offset[1]+(i*track_spaceing)-loopNumY(1)))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')
	#front bottom
	tracesF = TRACK_loopover
	for i in range(len(tracesF)):
		arr = offsetArr(mulArr(swapArr(tracesF[i]),(-1,-1)),(offset[0]+total_width,offset[1]+(i*track_spaceing)))
		routeArr(board,arr,FromMM(track_width),B_Cu,'GND')

class SimplePlugin(pcbnew.ActionPlugin):
	def defaults(self):
		self.name = "SensorMK"
		self.category = "N/A"
		self.description = "Plugin to create sensor for tablet"

	def Run(self):
		last_startx = loopNumX(countx-1)
		last_endx = last_startx+(count_per-1)*track_spaceing
		offsetsx = (total_width-last_endx)/2
		last_starty =loopNumY(county-1)
		last_endy = last_starty+(count_per-1)*track_spaceing
		offsetsy = (total_height-last_endy)/2
		board = GetBoard()
		for i in range(countx):
			offset = loopNumX(i) + offsetsx
			for b in range(count_per):
				sp = ((b*track_spaceing)+corner[0]+offset,corner[1])
				ep = ((b*track_spaceing)+corner[0]+offset,corner[1]+total_height)
				createtrack(board,sp,ep,FromMM(track_width),F_Cu,'GND')
			if(i%2):
				run_viaFront(board,(corner[0]+offset,corner[1]))
		for i in range(county):
			offset = loopNumY(i) + offsetsy
			for b in range(count_per):
				sp = (corner[0],(b*track_spaceing)+offset+corner[1])
				ep = (corner[0]+total_width,(b*track_spaceing)+offset+corner[1])
				createtrack(board,sp,ep,FromMM(track_width),B_Cu,'GND')
			if(i%2):
				run_viaBack(board,(corner[0],corner[1]+offset))
SimplePlugin().register()
