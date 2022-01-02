import cv2 as cv
import numpy as np
import os
import time as waktu
from PIL import Image
import pyautogui
import mss
import sys
import pygetwindow as gw
from windowgame import *
from findimage import *
from windowfocus import *

sct = mss.mss()
			
loop_time = waktu.time()

axiex,axiey,axiew,axieh = setGame("Axie Infinity",0,0)
setActiveWindow("Axie Infinity")
notepadx,notepady,notepadw,notepadh = None,None,None,None

status = "Adventure"

while(True):
	
	scs = sct.grab({
            'left': axiex,
            'top': axiey,
            'width': axiew,
            'height': axieh
        })
	scs = np.array(scs)
	scs = cv.cvtColor(scs, cv.IMREAD_COLOR)

	if status == "Level":
		mata = cv.imread('level1.jpg',cv.IMREAD_UNCHANGED)
		statusLevel = findImage(1,0.95,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
		if statusLevel:
			status = "StartGame"
	elif status == "Adventure":
		mata = cv.imread('adventure.jpg',cv.IMREAD_UNCHANGED)
		statusAdventure = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
		if statusAdventure:
			status = "Level"
	elif status == "StartGame":
		mata = cv.imread('startgame.jpg',0.8,cv.IMREAD_UNCHANGED)
		#statusAdventure = findImage(1,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
		
	print(status, end='\r')
	sys.stdout.write("\033[K")
	
	hasil = cv.imshow('Result',scs);

	try:
		notepadx,notepady,notepadw,notepadh = setGame("Result",int(axiex + axiew),int(axiey-83))
	except Exception as e:	
		pass

	if cv.waitKey(1) == ord('q'):
		cv.destroyAllWindows()
		break
print('Done') 