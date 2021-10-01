from flask_socketio import SocketIO
from flask import Flask, render_template, redirect, url_for, request, Response
import cv2
import json
import numpy as np
import os , io , sys
from PIL import Image
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image')
def image():
    return Response(generate_images(),mimetype='multipart/x-mixed-replace; boundary=frame')

frame = b'\xff'
image1 = b'\xff'
flag = False
trackFlag = "True"

def generate_frames():
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_images():
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image1 + b'\r\n')

@sio.on('send data')
def image(stringData):
    global frame
    frame = stringData

@sio.on('send flag')
def recvFlag(data):
    global trackFlag
    if(data == "False"):
        trackFlag = "False"
    else:
        trackFlag = "True"
    
@app.route('/saveimg', methods=['POST'])
def saveImg():
    if request.method == 'POST':
        global frame
        nparr = np.fromstring(frame, np.uint8)
        imgdecode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        now = datetime.now()
        dt_string = now.strftime("%d%m%Y-%H%M%S")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + '/lib'

        filename = dt_string + '.jpg'
        cv2.imwrite(os.path.join(path , filename), imgdecode)

@app.route('/getlib', methods=['POST'])
def getLib():
    if request.method == 'POST':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + '/lib'
        abc = ""
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                abc += name
                abc += ","
        list = "{}".format(abc)
        return list;

@app.route('/getimg', methods=['POST'])
def getImg():
    global flag
    global image1
    if request.method == 'POST':
        flag = True
        name = request.data
        name = name.decode('ascii')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + '/lib/'
        path = path + name
        img = cv2.imread(path)
        img_encode = cv2.imencode('.jpg', img)[1]
        image1 = img_encode.tobytes()
    return render_template('index.html')

@app.route('/getflag')
def getFlag():
    global trackFlag
    def getData():
        msg = f"data:{trackFlag}\n\n"
        yield msg
    for msg in getData():
        return Response(msg, mimetype='text/event-stream')
                   
if __name__ == "__main__":
    app.debug = True
    print('[INFO] Starting server at http://localhost:3456')
    sio.run(app=app, host='localhost', port=3456)