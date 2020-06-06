# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import os.path as path
from package.detector import detect_face

# define a video capture object
vid = cv2.VideoCapture(0)

# index/label 0 is empty as a fallback
subjects = ["", "Rolando", "Cristian", "Antonio"]

script_dir = path.dirname(__file__)
checkpoint_relative = "test.yml"
classier_relative = "opencv-files/lbpcascade_frontalface.xml"
checkpoint_file = path.join(script_dir, checkpoint_relative)
classier_file = path.join(script_dir, classier_relative)

while(True):
    print("Enter a number Rolando[1], Cristian[2], Antonio[3]")
    subject = input()

    try:
        subject_int = int(subject)
        if subject_int > 0 and subject_int < 4:
            break
    except Exception:
        print(f"{subject} It is not a number")


def prepare_training_data(label: int):
    faces = []
    labels = []
    start = time.time()

    while(True):
        ret, frame = vid.read()
        cv2.imshow('frame', frame)

        current_time = time.time()

        if current_time - start > 1:
            start = current_time

            face, rect = detect_face(frame, classier_file)

            if face is not None:
                faces.append(face)
                labels.append(label)

            print(len(labels))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels


print("Preparing data...")
faces, labels = prepare_training_data(subject_int)
print("Data prepared")

# print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))


# create our LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()


if path.isfile(checkpoint_file):
    face_recognizer.read(checkpoint_file)
    face_recognizer.update(faces, np.array(labels))
else:
    face_recognizer.train(faces, np.array(labels))

face_recognizer.write(checkpoint_file)
