import cv2
import freenect
import numpy as np
import time
from datetime import datetime
from additional_modules import headWeather
from additional_modules import autopull
from additional_modules import jargon
import textwrap

height = 0
width = 0
def get_video():
	array,_ = freenect.sync_get_video()
	array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
	return array
def get_depth():
	depth,_ = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= 627, depth <= 850)
	return depth.astype(np.uint8)
def get_dimensions(sample_image):
	height = len(sample_image)
	width = len(sample_image[0])
	return height, width
def grayScale(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def drawPanel(img, coordinates, dimensions, color, text=' ', centerCoordinates=True):
	leftCorner = None
	rightCorner = None
	if centerCoordinates == True:
		#mounts the panel so that it's center is at the provided coordinates
		for i in range(len(dimensions)):
			if dimensions[i] %2 == 1:
				dimensions[i] += 1
		length = dimensions[0]
		height = dimensions[1]
		x_coor = coordinates[0]
		y_coor = coordinates[1]
		#compute the coordinates based on the center
		leftCorner = (int(x_coor - (length / 2)), int(y_coor + (height / 2)))
		rightCorner = (int(x_coor + (length / 2)), int(y_coor - (length / 2)))

	else:
		length = dimensions[0]
		height = dimensions[1]
		left_x = coordinates[0]
		left_y = coordinates[1]
		leftCorner = (left_x, left_y)
		rightCorner = (left_x + length, left_y - height)
	#draw the rectangle
	#cv2.rectangle(img, leftCorner, rightCorner, color, 1)
	img = (img * 0.5).astype(np.uint8)
	if text != ' ':
		text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
		cv2.putText(img, text, (leftCorner[0], rightCorner[1] + 2 * text_height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250))
	return img

def getDepthROI(depth, Color):
	f_argmax = np.argmax(depth, axis=0)
	f_amax = np.amax(depth, axis=0)
	c = f_argmax[f_amax == 255]
	try:
		top = np.amin(c)
		bottom = np.amax(c)
	except:
		#To handle when the screen is completely black
		top = 0
		bottom = 0
	s_argmax = np.argmax(depth, axis=1)
	s_amax = np.amax(depth, axis=1)
	g = s_argmax[s_amax == 255]
	try:
		left = np.amin(g)
		right = np.amax(g)
	except:
		#To handle when the screen is completely black
		left = 0
		right = 0
	roi = Color[top:bottom, left:right]
	return roi

headWeather.init(location='North Plainfield, New Jersey')
headLines = autopull.wired_magazine()[5:]
lineCount = 0
present_headLines = [headLines[lineCount], headLines[lineCount + 1]]
hc = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
hc_alt = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
sample_frame = get_video()
height, width = get_dimensions(sample_frame)
print('Sampling frame for dimensions...')
rectWidth = 200
rectHeight = 100
face_point = None
overlay_activate = False 
saved_time = time.time()
frameCount = 0




faces_seen = False
init = time.time()
prev = 0
while True:
	frame = get_video()
	depth = get_depth()
	depthROI = getDepthROI(depth, frame)
	gray = grayScale(depthROI)
	faces = hc.detectMultiScale(gray, 1.1, 3)
	alt_faces = hc_alt.detectMultiScale(gray, 1.1, 3)
	if len(faces) > 0 or len(alt_faces) > 0:
		face_point = time.time()
		overlay_activate = True
	elif face_point != None and time.time() - face_point > 10:
		overlay_activate = False 
	if overlay_activate == True:
		dist = int(time.time() - init)
		if dist % 3 == 0 and dist != prev:
			try:
				present_headLines = [headLines[lineCount], headLines[lineCount + 1]]
				lineCount += 1
			except:
				pass
		if lineCount == len(headLines) - 1:
			lineCount == 0
		prev = dist

		frame = drawPanel(frame, (0, 120), (rectWidth, rectHeight), (255, 0, 255), text=present_headLines[0], centerCoordinates=False)
		frame = drawPanel(frame, (0, 150), (rectWidth, rectHeight), (255, 0, 255), text=present_headLines[1], centerCoordinates=False)
		frame = drawPanel(frame, (width - rectWidth - 10, height - rectHeight), (rectWidth, rectHeight), (255, 0, 150), text=str(headWeather.getTemperature()) + ' degrees fahrenheit', centerCoordinates=False)
		if faces_seen == False:
			faces_seen = True
			jargon.speak("Greetings, user.")
			jargon.speak("The temperature outside is " + str(headWeather.getTemperature()) + " degreees")
		
	#retrieves frames displayed in the last 1 second interval
	tts = time.time() - saved_time
	if tts >= 1:
		
		saved_time = time.time()
		print(str(frameCount) + ' frames')
		frameCount = 0
	else:
		frameCount += 1
	cv2.imshow('HUD', frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		print('--done!--')
		break
raise freenect.Kill
cv2.destroyAllWindows()
