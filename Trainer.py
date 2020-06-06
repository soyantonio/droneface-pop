# -*- coding: utf-8 -*-

import cv2
import numpy as np 
import time
import os.path as path
from package.detector import detect_face
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 

#there is no label 0 in our training data so subject name for index/label 0 is empty
subjects = ["", "Rolando", "Cristian", "Antonio"]

while(True):
    print("Enter a number Rolando[1], Cristian[2], Antonio[3]")
    subject = input()
    
    try:
        subject_int = int(subject)
        
        if subject_int > 0 and subject_int < 4:
            break
    except:
        print(f"{subject} It is not a number")
        
    
    



checkpoint_file = "test.yml"

def prepare_training_data(label:int):  
    faces = []
    labels = []
    start = time.time()
    
    while(True): 
        ret, frame = vid.read() 
        cv2.imshow('frame', frame)
        
        current_time = time.time()
        
        if current_time - start > 1:
            start = current_time
            
            face, rect = detect_face(frame)
            
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

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))


#create our LBPH face recognizer 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()


if path.isfile(checkpoint_file):
    face_recognizer.read(checkpoint_file)
    face_recognizer.update(faces, np.array(labels))
else:
    face_recognizer.train(faces, np.array(labels))

face_recognizer.write(checkpoint_file)




