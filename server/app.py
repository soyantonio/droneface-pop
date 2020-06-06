# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response

from package.detector import detect_face
from LoadTrained import VideoCamera

# define application with constructor
app = Flask(__name__)


# define route of the server giving the current one
@app.route('/')
def index():
    return render_template('index.html')


def gen(detector):
    while True:
        frame = detect_face()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
