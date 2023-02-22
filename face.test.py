import face_recognition
import numpy as np
import cv2


img = cv2.imread("face.jpg")
img = face_recognition.face_encodings(img)[0]
img2 = cv2.imread("img.jpg")
img2 = face_recognition.face_encodings(img2)[0]

result = face_recognition.compare_faces([img2],img,tolerance=0.3)
print(result)