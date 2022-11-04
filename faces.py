"""
Author: Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 27 Feb 2019
"""
"""
This program should run along with the
voice command also and exit when the
program closes
"""

import numpy as np
import sys
import os
import cv2
import pickle

cascPath = ""
face_cascade = cv2.CascadeClassifier(cascPath)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

def openEye():
	# Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for(x, y, w, h) in faces:
	    # print(x, y, w, h)
	    roi_gray = gray[y:y+h, x:x+w]	# (ycord_start, ycord-end)
	    roi_color = frame[y:y+h, x:x+w]

	    # recognizer?
	    id_, conf = recognizer.predict(roi_gray)
	    if conf>=45 and conf<=85:
		    # print(id_)
		    # print(labels[id_])
		    font = cv2.FONT_HERSHEY_SIMPLEX
		    name = labels[id_]
		    color = (255, 255, 255)
		    stroke = 2
		    cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

	    img_item = "my_image.png"
	    cv2.imwrite(img_item, roi_color)

	    color = (255, 0, 0)		# BGR 0-255
	    stroke = 2
	    end_cordX = x + w
	    end_cordY = y + h
	    cv2.rectangle(frame, (x, y), (end_cordX, end_cordY), color, stroke)
	    """
	    subitems = smile_cascade.detectMultiScale(roi_gray)
	    for (ex, ey, ew, eh) in subitems:
		    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
	    """

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
    	exit(0)

cap.release()
cv2.destroyAllWindows()

"""
# this code belongs on line 73
while(cap.isOpened()):
	try:
		openEye()
	except KeyboardInterrupt:
		print('\nKeyboard Interrupt')
		print('Exit')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
"""