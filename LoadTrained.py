# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import os
from processes.face_recognition import init_predictor
from processes.drone_communication import send_subject_to_drone

vid = cv2.VideoCapture(0)
subjects = ["", "Rolando", "Cristian", "Antonio"]
pr = np.zeros([4])

script_dir = os.path.dirname(__file__)
trained_relative = "test.yml"
classier_relative = "opencv-files/lbpcascade_frontalface.xml"
trained_file = os.path.join(script_dir, trained_relative)
classier_file = os.path.join(script_dir, classier_relative)


def reset_present(present):
    return np.zeros([len(present)])


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(trained_file)
predict_face = init_predictor(subjects, face_recognizer, classier_file)

max_samples = 25
samples = 0
accepted_samples = (max_samples+1)//2
prev_subject = 0
start_time = time.time()
face_timeout = 5


while(True):
    current_time = time.time()
    ret, frame = vid.read()
    predicted_img, label = predict_face(frame)
    cv2.imshow('frame', predicted_img)

    if current_time - start_time > face_timeout:
        prev_subject = 0
        start_time = current_time

    if samples > max_samples:
        samples = 0
        index = np.argmax(pr)
        print(pr)
        if pr[index] > accepted_samples and prev_subject != index:
            prev_subject = index
            start_time = current_time
            send_subject_to_drone(subjects, index)
        pr = reset_present(pr)

    if label is not None:
        pr[label] = pr[label] + 1
    samples += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()

# After the loop release the cap object
vid.release()
