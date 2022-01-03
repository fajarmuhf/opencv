import cv2 as cv
import numpy as np
import os
import time as waktu
from PIL import Image
import pyautogui
import mss
import sys
#import pygetwindow as gw
#from windowgame import *
from findimage import *
#from windowfocus import *
import pytesseract
import time

#sct = mss.mss()
			
loop_time = waktu.time()

axiex,axiey,axiew,axieh = (0,0,1136,750)
#setActiveWindow("Chrome")

notepadx,notepady,notepadw,notepadh = None,None,None,None

status = "Result"
awal = 0
hpStatus = 100
	
while(True):
	time.sleep(5)
	axiex,axiey,axiew,axieh = (0,27,1136,750)
	
	scs = pyautogui.screenshot(region=(0,27, 1136, 750))
	scs = np.array(scs)
	scs = cv.cvtColor(scs, cv.COLOR_RGB2BGR)

	scs4 = pyautogui.screenshot(region=(195*2*axiew/1136.0,(205-27)*2*axieh/750.0, 183*2*axiew/1136.0,100*2*axieh/750.0))
        
	scs4 = np.array(scs4)
	scs4 = cv.cvtColor(scs4, cv.COLOR_RGB2BGR)

	scs3 = pyautogui.screenshot(region=(450*2*axiew/1136.0,(370-27)*2*axieh/750.0, 93*2*axiew/1136.0,30*2*axieh/750.0 ))
        
	scs3 = np.array(scs3)
	scs3 = cv.cvtColor(scs3, cv.COLOR_RGB2BGR)

	gray = cv.cvtColor(scs3, cv.COLOR_BGR2GRAY)
	thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

	# Morph open to remove noise
	kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
	opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

	# Perform text extraction
	data3 = pytesseract.image_to_string(opening, lang='eng', config='--psm 10')
	try:
		scs2 = pyautogui.screenshot(region=(95*axiew/1136.0,(162+27)*axieh/750.0, 80*2*axiew/1136.0, 15*axieh/750.0))
	        
		scs2 = np.array(scs2)
		scs2 = cv.cvtColor(scs2, cv.COLOR_RGB2BGR)

		gray = cv.cvtColor(scs2, cv.COLOR_BGR2GRAY)
		thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

		# Morph open to remove noise
		kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
		opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

		# Perform text extraction
		data = pytesseract.image_to_string(opening, lang='eng', config='--psm 4')
		data = data.replace("Z", "3")
		data = data.replace("I", "1")
		data = data.replace("[", "1")
		data = data.replace("f", "/")
		data = data.replace("O", "0")
		data = data.replace("_", "")
		maxdata = (len(data.split("/")[0]))
		mindata = (len(data.split("/")[0])-1)
		print(data)
	except Exception as e:	
			pass
	if (data.split("/")[0][mindata:mindata+1]).isnumeric():
		try:
			hpStatus = int(data.split("/")[0][mindata:maxdata])
		except Exception as e:	
			pass
	mindata = (len(data.split("/")[0])-2)
	if (data.split("/")[0][mindata:mindata+1]).isnumeric():
		try:
			hpStatus = int(data.split("/")[0][mindata:maxdata])
		except Exception as e:	
			#hpStatus = 100
			pass
	mindata = (len(data.split("/")[0])-3)
	if (data.split("/")[0][mindata:mindata+1]).isnumeric():
		try:
			hpStatus = int(data.split("/")[0][mindata:maxdata])
		except Exception as e:	
			#hpStatus = 100
			pass

	try:
		mata = cv.imread('heal.jpg',cv.IMREAD_UNCHANGED)		
		result = cv.matchTemplate(scs,mata,cv.TM_CCOEFF_NORMED)
		
		locations = np.where(result >= 0.9)
		locations = list(zip(*locations[::-1]))

		loadfree = True
		for loc in locations:
			loadfree = False
	except Exception as e:	
		pass

	gray = cv.cvtColor(scs4, cv.COLOR_BGR2GRAY)
	thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

	# Morph open to remove noise
	kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
	opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

	# Perform text extraction
	data = pytesseract.image_to_string(opening, lang='eng', config='--psm 12')
	
	print(loadfree)
	print(data)
	if data.find("transaction") != -1 or data.find("hash") != -1 or data.find("assertion") != -1 or data.find("Hunt Reward.") != -1 or data.find("billed") != -1:
		mata = cv.imread('close.jpg',cv.IMREAD_UNCHANGED)
		statusClose = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
		if statusClose:
			try:
				mata = cv.imread('back.jpg',cv.IMREAD_UNCHANGED)
				statusBack = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
				if statusBack:
					status = "Main menu"
					pass
			except Exception as e:	
				pass
	try:
		mata = cv.imread('continue.jpg',cv.IMREAD_UNCHANGED)
		statusContinue = findImage(1,0.7,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
		if statusContinue:
			status = "Main menu"
			pass
	except Exception as e:	
		pass
	print(hpStatus)
	print(status)
	print(data3)
	if hpStatus >= 23:
		if status == "Map":
			mata = "";
			if hpStatus >= 80:
				mata = cv.imread('forest.jpg',cv.IMREAD_UNCHANGED)
			else:
				mata = cv.imread('swamplands.jpg',cv.IMREAD_UNCHANGED)	
			statusMap = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			if statusMap:
				status = "Hunt"
		elif status == "Main menu" and data3[0:4] == "Free" and loadfree == False:
			if data.find("assertion") != -1 or data.find("Hunt Reward.") != -1 or data.find("billed") != -1:
				mata = cv.imread('close.jpg',cv.IMREAD_UNCHANGED)
				statusClose = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			#try:
			#	pyautogui.click(notepadw/2*axiew/(notepadw)+axiex,notepadh/2*axieh/(notepadh)+axiey+20*axieh/(notepadh))
			#except Exception as e:	
			#	pass
			print("ok");
			mata = cv.imread('map.jpg',cv.IMREAD_UNCHANGED)
			statusAdventure = findImage(1,0.95,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			if statusAdventure:
				status = "Map"	
		elif status == "Hunt":
			mata = cv.imread('hunt.jpg',cv.IMREAD_UNCHANGED)
			statusHunt = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			if statusHunt:
				status = "Result"
		elif status == "Result":
			gray = cv.cvtColor(scs4, cv.COLOR_BGR2GRAY)
			thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

			# Morph open to remove noise
			kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
			opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

			# Perform text extraction
			data = pytesseract.image_to_string(opening, lang='eng', config='--psm 11')
			if data.find("hash") != -1 or data.find("assertion") != -1 or data.find("Hunt Reward.") != -1 or data.find("billed") != -1:
				mata = cv.imread('close.jpg',cv.IMREAD_UNCHANGED)
				statusClose = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
				if statusClose:
					mata = cv.imread('back.jpg',cv.IMREAD_UNCHANGED)
					statusBack = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
					if statusBack:
						status = "Main menu"
			else:
				mata = cv.imread('continue.jpg',cv.IMREAD_UNCHANGED)
				statusContinue = findImage(1,0.7,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
				if statusContinue:
					status = "Main menu"
				
	else:
		if status == "Main menu" and data3[0:4] == "Free" and loadfree == False:
			gray = cv.cvtColor(scs4, cv.COLOR_BGR2GRAY)
			thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

			# Morph open to remove noise
			kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
			opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

			# Perform text extraction
			data = pytesseract.image_to_string(opening, lang='eng', config='--psm 11')
			
			if data.find("hash") != -1 or data.find("assertion") != -1 or data.find("Hunt Reward.") != -1 or data.find("billed") != -1:
				mata = cv.imread('close.jpg',cv.IMREAD_UNCHANGED)
				statusClose = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			mata = cv.imread('heal.jpg',cv.IMREAD_UNCHANGED)
			statusAdventure = findImage(1,0.8,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh)
			if statusAdventure:
				status = "Main menu"
	
	
	#print(status, end='\r')
	#sys.stdout.write("\033[K")
	
	hasil = cv.imshow('Result',scs4);
	cv.moveWindow('Result',int(axiex+axiew),int(axiey-60))

	try:
		notepadx,notepady,notepadw,notepadh = (int(axiex + axiew),int(axiey-60),1136,750)
		if awal == 0:
			pyautogui.click(notepadw/2*axiew/(notepadw)+axiex,notepadh/2*axieh/(notepadh)+axiey+40*axieh/(notepadh))
			awal = 1
	except Exception as e:	
		pass

	if cv.waitKey(1) == ord('q'):
		cv.destroyAllWindows()
		break
print('Done') 
