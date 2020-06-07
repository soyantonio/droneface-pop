# -*- coding: utf-8 -*-

import cv2
import os
from processes.face_recognition import init_predictor

subjects = ["", "Rolando", "Cristian", "Antonio"]

script_dir = os.path.dirname(__file__)
trained_relative = "test.yml"
classier_relative = "opencv-files/lbpcascade_frontalface.xml"
trained_file = os.path.join(script_dir, trained_relative)
classier_file = os.path.join(script_dir, classier_relative)


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(trained_file)
predict_face = init_predictor(subjects, face_recognizer, classier_file)


class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        # extracting frames
        ret, frame = self.video.read()

        if frame is None:
            return 0, None

        predicted_img, label = predict_face(frame)
        ret, jpeg = cv2.imencode('.jpg', predicted_img)
        return label, jpeg.tobytes()
