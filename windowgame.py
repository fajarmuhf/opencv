import pygetwindow as gw
import cv2 as cv

def setGame(name,x,y):
	hasil = gw.getWindowGeometry(name)
	cv.moveWindow(name, int(x),int(y));
	return hasil
