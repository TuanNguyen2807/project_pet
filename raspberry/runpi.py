import socketio, cv2, pickle, struct
import imutils 
import requests
import numpy as np
import base64
import os , io , sys
from PIL import Image

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[2]

if int(minor_ver) < 3:
    tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()



video = cv2.VideoCapture(0)

ok, frame = video.read()

# Define an initial bounding box
bbox = cv2.selectROI(frame, False)

ok = tracker.init(frame, bbox)

flag = True

socketIO = socketio.Client()

@socketIO.event
def connect_error(data):
    print("The connection failed!")

@socketIO.event
def disconnect():
    print(" disconnected!")

@socketIO.event
def connect():
    print('connection established')
    while (video.isOpened()):
        global flag
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Update tracker
        ok, bbox = tracker.update(frame)

        # # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            socketIO.emit('send flag', "True")
        else :
        #     # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            socketIO.emit('send flag', "False")
        ## converting RGB to BGR, as opencv standards
        # frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

        # Process the image frame
        frame = cv2.flip(frame, 1)

        # Encode the frame
        imgencode = cv2.imencode('.jpg', frame)[1]
        stringData = imgencode.tobytes()
    
        # emit the frame back
        socketIO.emit('send data', stringData)
        

socketIO.connect('http://localhost:3456')
socketIO.wait()