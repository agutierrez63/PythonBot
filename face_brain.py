"""
Author: Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 18 Jan 2019
"""
"""
This program should first before the AI
starts to check for picture updates to
learn who is who.
"""
import cv2
import os
import pickle
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "")

face_cascade = cv2.CascadeClassifier('')
recognizer = cv2.face.LBPHFaceRecognizer_create()

"""
current_id = 0
label_ids = {}
y_labels = []
x_train = []
"""

def updateImages():
	current_id = 0
	label_ids = {}
	y_labels = []
	x_train = []

	for root, dirs, files in os.walk(image_dir):
	    for file in files:
		    if file.endswith("png") or file.endswith("jpg"):
			    path = os.path.join(root, file)
			    label = os.path.basename(root).replace(" ", "-").lower()
			    # print(label, path)
			    if not label in label_ids:
				    label_ids[label] = current_id
				    current_id += 1
		    id_ = label_ids[label]
		    # print(label_ids)
		    # y_labels.append(label)	# some number
		    # x_train.append(path)	# verify this image, turn into numpy array, GRAY
		    pil_image = Image.open(path).convert("L")	# grayscale
		    size = (550, 550)
		    final_image = pil_image.resize(size, Image.ANTIALIAS)
		    image_array = np.array(final_image, "uint8")
		    # print(image_array)
		    faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

		    for (x, y, w, h) in  faces:
			    roi = image_array[y:y+h, x:x+w]
			    x_train.append(roi)
			    y_labels.append(id_)

	with open("labels.pickle", "wb") as f:
		pickle.dump(label_ids, f)

	recognizer.train(x_train, np.array(y_labels))
	recognizer.save("trainer.yml")