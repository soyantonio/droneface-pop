# -*- coding: utf-8 -*-

import time
from flask import Flask, render_template, Response
from model_web import VideoCamera
import numpy as np

# define application with constructor
app = Flask(__name__)
subjects = ["", "Rolando", "Cristian", "Antonio"]


# define route of the server giving the current one
@app.route('/')
def index():
    return render_template('index.html')


def reset_present(present):
    return np.zeros([len(present)])


def gen(camera):
    max_samples = 25
    samples = 0
    accepted_samples = (max_samples+1)//2
    prev_subject = 0
    start_time = time.time()
    face_timeout = 5
    pr = np.zeros([4])
    index = 0
    header = b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n'

    while True:
        current_time = time.time()
        label, frame = camera.get_frame()
        if current_time - start_time > face_timeout:
            prev_subject = 0
            start_time = current_time

        if samples > max_samples:
            samples = 0
            index = np.argmax(pr)
            print(pr)
            if pr[index] > accepted_samples and prev_subject != index:
                yield header + b'end' + b'\r\n'
                break
            pr = reset_present(pr)

        if label is not None:
            pr[label] = pr[label] + 1
            samples += 1

        stream = header + frame + b'\r\n'

        yield stream


@app.route('/video_feed')
def video_feed():
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    goal = gen(VideoCamera())

    response = Response(goal, mimetype=mimetype)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)
