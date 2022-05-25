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
print(total_width - (track_spaceing*(countx-1)*((total_width/track_spaceing)//(countx-1))))
def createtrack(board,sp,ep,width,layer,net):
	track = PCB_TRACK(board)
	track.SetStart(wxPointMM(sp[0],sp[1]))
	track.SetEnd(wxPointMM(ep[0],ep[1]))
	track.SetWidth(width)
	track.SetLayer(layer)
	board.Add(track)
	track.SetNetCode(0)

class SimplePlugin(pcbnew.ActionPlugin):
	def defaults(self):
		self.name = "SensorMK"
		self.category = "N/A"
		self.description = "Plugin to create sensor for tablet"

	def Run(self):
		board = GetBoard()
		for i in range(countx):
			last_start = track_spaceing*(countx-1)*((total_width/track_spaceing)//(countx-1))
			last_end = last_start+(count_per-1)*track_spaceing
			offsets = (total_width-last_end)/2
			offset = (track_spaceing*i*((total_width/track_spaceing)//(countx-1))) + offsets
			for b in range(count_per):
				sp = ((b*track_spaceing)+corner[0]+offset,corner[1])
				ep = ((b*track_spaceing)+corner[0]+offset,corner[1]+total_height)
				createtrack(board,sp,ep,FromMM(track_width),F_Cu,'GND')
		for i in range(county):
			last_start = track_spaceing*(county-1)*((total_height/track_spaceing)//(county-1))
			last_end = last_start+(count_per-1)*track_spaceing
			offsets = (total_height-last_end)/2
			offset = track_spaceing*i*((total_height/track_spaceing)//(county-1)) + offsets
			for b in range(count_per):
				sp = (corner[0],(b*track_spaceing)+offset+corner[1])
				ep = (corner[0]+total_width,(b*track_spaceing)+offset+corner[1])
				createtrack(board,sp,ep,FromMM(track_width),B_Cu,'GND')
SimplePlugin().register()
