import cv2 as cv
import numpy as np
import os
import time as waktu
from PIL import Image
import pyautogui
import mss
#import pygetwindow as gw

def findImage(kliktime,threshold,scs,mata,axiex,axiey,axiew,axieh,notepadw,notepadh):
	statusku = False
	klikmulai = 0
	while (True):
		# print('FPS {}'.format(1 / (waktu.time() - loop_time)))
		loop_time = waktu.time()

		result = cv.matchTemplate(scs,mata,cv.TM_CCOEFF_NORMED)

		locations = np.where(result >= threshold)
		locations = list(zip(*locations[::-1]))

		eye_w = mata.shape[1]
		eye_h = mata.shape[0]

		rectangles = []
		i = 0
		for loc in locations:
			rect = [int(loc[0]),int(loc[1]),eye_w,eye_h]
			rectangles.append(rect)
			rectangles.append(rect)

		rectangles , weights = cv.groupRectangles(rectangles,1,0.5)

		if locations :

			for (x,y,w,h) in rectangles:

				top_left = (x,y)
				bottom_right = (x + w , y + h)

				center_x = x + int(w/2)
				center_y = y + int(h/2)

				cv.rectangle(scs,top_left,bottom_right,
					color=(0,255,0),thickness = 2,lineType=cv.LINE_4)

				cv.drawMarker(scs,(center_x,center_y),(255,0,255),cv.MARKER_CROSS)
				
				statusku = True
				# print(first_loc)

				if notepadw != None :
					if klikmulai < kliktime:
						pyautogui.click(center_x*axiew/(notepadw)+axiex,center_y*axieh/(notepadh)+axiey+20*axieh/(notepadh))
						klikmulai = klikmulai + 1
					if klikmulai == kliktime:
						break
						break
					#return True
		else:
			break
		break
	if notepadw != None :
		return statusku
