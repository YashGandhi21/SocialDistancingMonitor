import cv2
import requests
import numpy as np
import platform
# cascPath = 'static\\haarcascade_frontalface_dataset.xml'
# faceCascade = cv2.CascadeClassifier(cascPath)

#global video_capture

def startWebCamera_Stream():
    print("Starting web camera")
    video_capture = cv2.VideoCapture(0)
    return video_capture

def openVideoFile_Stream():
    print("open file stream")
    if platform.system()=='Windows':
        video_capture = cv2.VideoCapture('videos\\video.mp4')
    elif platform.system()=='Linux':
        video_capture = cv2.VideoCapture('videos/video.mp4')
    #video_capture.set(cv2.CAP_PROP_FPS, 10)
    #print("Changes applied are res = ",video_capture.set(cv2.CAP_PROP_FPS, 30))
    return video_capture

def webCamera_Stream(video_capture):
    ret, frame = video_capture.read()
    if not ret :
        #video_capture = cv2.VideoCapture(0)   
        print("Camera can not be opened, some other process using it")
        return None 
    frame = cv2.resize(frame, (480,320))
    return cv2.imencode('.jpg', frame)[1].tobytes()

def stopWebCamera_Stream(video_capture):
    try:
        video_capture.release()
    except NameError:
        print("caught nameError, direclty hit to /stopCam")
        pass
    print("webCamera Stopped")


def playVideo(video_capture,wid,hei):
    ret, frame = video_capture.read()
    if not ret :
        print("videocapture reaturened ",ret)   
        print("Camera can not be opened")
        return None
    
    #frame = cv2.resize(frame,(1280,720))
    #frame = cv2.resize(frame, (720,480))
    #frame = cv2.resize(frame, (wid,hei))
    #frame = cv2.resize(frame, (600,480))
    frame = cv2.resize(frame, (480,320))

    #frame , _ = facedetecFromFrame(frame)

    frame = cv2.imencode('.jpg', frame)[1].tobytes()

    return frame
    


def facedetection(video_capture):
    if platform.system()=='Windows':
        cascPath = 'static\\haarcascade_frontalface_dataset.xml'
    elif platform.system()=='Linux':
        cascPath = 'static/haarcascade_frontalface_dataset.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    ret, frame = video_capture.read()
    
    if not ret :
        print("videocapture reaturened ",ret)   
        print("Camera can not be opened")
        return (None , 0)

    frame = cv2.resize(frame, (480,320))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    #count number of faces found in frame
    count = len(faces)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    frame = cv2.imencode('.jpg', frame)[1].tobytes()
    
    return (frame , count)


def facedetecFromFrame(frame):
    if platform.system()=='Windows':
        cascPath = 'static\\haarcascade_frontalface_dataset.xml'
    elif platform.system()=='Linux':
        cascPath = 'static/haarcascade_frontalface_dataset.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    frame = cv2.resize(frame, (480,320))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    count = len(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    frame = cv2.imencode('.jpg', frame)[1].tobytes()
    return (frame, count)


def GetOnlyCamFrame(video_capture):
    ret, frame = video_capture.read()
    if not ret :   
        print("Camera can not be opened, some other process using it")
        return None

    frame = cv2.resize(frame, (480,320))

    return frame


def startipWebCam(ip):
    if ip is not None:
        camIP = "http://"+ip+"/shot.jpg"
        img_res = requests.get(camIP)
        #print("found = ",img_res)
        img_arr = np.array(bytearray(img_res.content), dtype = np.uint8)
        try:
            frame = cv2.imdecode(img_arr,-1)
            frame = cv2.resize(frame, (480,320))
            return frame
        except cv2.error as e:
            print("IP web Cam is Stopped")
            return None

        
    else:
        return None


