sct = mss.mss()

loop_time = waktu.time()
while(True):
	scs = sct.grab({
            'left': 0,
            'top': 60,
            'width': 420,
            'height': 250
        })
	scs = np.array(scs)
	scs = cv.cvtColor(scs, cv.IMREAD_COLOR)
	mata = cv.imread('adventure.jpg',cv.IMREAD_UNCHANGED)

	print('FPS {}'.format(1 / (waktu.time() - loop_time)))
	loop_time = waktu.time()

	result = cv.matchTemplate(scs,mata,cv.TM_CCOEFF_NORMED)

	min_val,max_val,min_loc,max_loc = cv.minMaxLoc(result)

	#print('Best match %s' % str(max_loc))
	#print('Best match confidence %s' % (max_val))

	threshold = 0.5

	locations = np.where(result >= threshold)
	locations = list(zip(*locations[::-1]))


	eye_w = mata.shape[1]
	eye_h = mata.shape[0]

	rectangles = []
	for loc in locations:
		rect = [int(loc[0]),int(loc[1]),eye_w,eye_h]
		rectangles.append(rect)
		rectangles.append(rect)

	rectangles , weights = cv.groupRectangles(rectangles,1,0.5)

	if locations :
		# print('Found Eye')

		for (x,y,w,h) in rectangles:

			top_left = (x,y)
			bottom_right = (x + w , y + h)

			center_x = x + int(w/2)
			center_y = y + int(h/2)

			cv.rectangle(scs,top_left,bottom_right,
				color=(0,255,0),thickness = 2,lineType=cv.LINE_4)

			cv.drawMarker(scs,(center_x,center_y),(255,0,255),cv.MARKER_CROSS)

			pyautogui.click(center_x, center_y+60)
			
	
	else:
		print('Not Found')

	cv.imshow('Result',scs);

	if cv.waitKey(1) == ord('q'):
		cv.destroyAllWindows()
		break

print('Done')