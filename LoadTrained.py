# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
from processes.face_recognition import predict
from processes.drone_comunication import send_subject_to_drone

vid = cv2.VideoCapture(0) 
subjects = ["", "Rolando", "Cristian", "Antonio"]
pr = np.zeros([4])

def reset_present (present):
    return np.zeros([len(present)])

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("test.yml")

max_samples = 25
samples = 0
accepted_samples = (max_samples+1)//2
prev_subject = 0
start_time = time.time()
face_timeout = 5
    

while(True):

    current_time = time.time()      
    ret, frame = vid.read()
    predicted_img, label = predict(frame,subjects,face_recognizer)
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
            send_subject_to_drone(subjects,index)
        pr = reset_present(pr)
        
    if label is not None:
        pr[label] = pr[label]+1  
    samples +=1 
        
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
            
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()

# After the loop release the cap object 
vid.release() 