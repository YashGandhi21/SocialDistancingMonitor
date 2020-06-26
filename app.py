# author: Aaditya Deshpande

'''
**************************************************
General Algorithm:

Step 1] start a camera and set its video_capture object global

Step 2] read frames from video_capture, encode into img and convert tobytes()

Step 3] while not released video_capture yield the frame

Algorithm Ends.

**************************************************
'''

#Import

from flask import Flask, render_template, Response,jsonify,make_response,request,redirect, url_for
from cameraApi.camera import webCamera_Stream,stopWebCamera_Stream,startWebCamera_Stream,openVideoFile_Stream
from cameraApi.camera import facedetection,playVideo,facedetecFromFrame,GetOnlyCamFrame,startipWebCam
import time
import cv2
import requests
import urllib
from main import integrated_social_distancing
from flask import flash , session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from cameraApi.streamer import Streamer
from view_db_contents import store_images
from PIL import Image

#Configuring flask
app = Flask(__name__)
app.config['DEBUG'] = True

#For adding the Login

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SECRET_KEY']='619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

# for first time commands to create db 
# from app import db
# db.create_all()

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    print("caught username is = ",username)
    print("caught password is = ",password)
    user = User.query.filter_by(username=username,password=password).first()

    if user is not None:
        session['logged_in'] = True
        session['username'] = username
        login_user(user)
        # flash("Login Successful")
        # return redirect(url_for('index'))
        return render_template('index.html',username = username)

    
    else:
        print("inCorrect credentials")
        flash("incorrect credentials")
        return render_template('login.html')

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    print("inserting in db is ,")
    print("username is = ",username)
    print("email is = ",email)
    print("password is = ",password)
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    session['logged_in'] = True
    session['username'] = username
    login_user(user)
    #return redirect(url_for('index'))
    return render_template('index.html',username = username)

@app.route('/logout',methods=['GET'])
def logout():
    if session.get('logged_in'):
        print("user log out")
        flash("logout successful")
        session.pop('logged_in', None)
        session.pop('username', None)
        logout_user()
    return redirect('/login')


@app.route('/index')
@login_required
def index():
    print("user in index page")
    return render_template('index.html',username=" ")





#global variables

#This data is fetched by website (by JavaScript)
jsonData = {}

#this is used to share a captured frame with multiple functions
globalFrame = None

#this is used to control any kind of video streames
global video_capture

#Workaround used to stop double cam feed...;)
StopAllFrames = False

#for handling HeatmapFrame
heatMapFrame = None

#for accessing same ip address in different functions
ip = None

#First function that gets invoked when visited home page.
@app.route('/')
def base():
    print("User in login page")
    return render_template('login.html')


#stop the stream, No matter who started.
@app.route('/stopCam',methods=['GET', 'POST'])
def stopCam():
    print("inside stop cam")
    #Resetting the double frame (Workaround)
    global globalFrame
    globalFrame = None

    global heatMapFrame
    heatMapFrame = None

    #used to break the double frame loop
    global StopAllFrames
    StopAllFrames = True

    #stopping the actual video stream object 
    global video_capture
    try:
        stopWebCamera_Stream(video_capture)
        cv2.destroyAllWindows()  #used to suppress the warning
    except NameError:
        print("caught nameError of video_Capture only for webcam, direclty hit to /stopCam")
        pass

    return render_template('stopCam.html')


#for local camera display (Camera view only option of index page)
@app.route('/camera')
def camera():
    return render_template('camera.html')

#generate frames and yield as it comes
def generate_camframe():
    global video_capture
    print("inside call start cam")
    video_capture = startWebCamera_Stream()
    while True:
        frame = webCamera_Stream(video_capture) #Comment this in case of different processing

        #frame = GetOnlyCamFrame(video_capture) # HERE WE CAN PROCESS FRAME

        if frame is None:
            print("found frame is none")
            break
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#this method gets invoked by <img src="url_for..."> 
@app.route('/cam_feed')
def cam_feed():
    print("inside cam_feed")
    #here response will be send frame by frame
    return Response(generate_camframe(), mimetype='multipart/x-mixed-replace; boundary=frame')


#For FACE DETECTION 


#on hitting this url, cam.html page will rander
@app.route('/cam')
def cam():
    return render_template('cam.html')

#generate frames and yield as it comes
def generate_frame():
    global video_capture
    print("inside call start cam")
    video_capture = startWebCamera_Stream()
    while True:
        frame , count = facedetection(video_capture) #might give warning when frame is none
        
        # HERE WE CAN PROCESS FRAME

        if frame is None:
            print("found frame is none")
            break
        
        #updating the JSON data so that client can fetch it
        global jsonData
        jsonData.update({"count":count})
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#for sending back response as image (it will be called by <img src="")
@app.route('/video_feed')
def video_feed():
    print("inside video_feed")
    #here response will be send frame by frame (called by html page)
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

#this will act like a REST-API, no matter state of server, client can fetch the data.
@app.route('/jsonData',methods=['GET', 'POST'])
def stream_json():
    global jsonData
    #print(jsonify(jsonData))
    return jsonify(jsonData)




#FOR playing DEMO DATA DISPLAY



@app.route('/demo')
def demo():
    return render_template('demo.html')

def generatedemo_frame():
    global video_capture
    print("inside call start demo")
    #video_capture = startWebCamera_Stream()
    #changed

    video_capture = openVideoFile_Stream()
    vidStartTime = time.time()

    print("ORIGINAL video Fps is ", video_capture.get(cv2.CAP_PROP_FPS))
    #print("Changes made status = ",video_capture.set(cv2.CAP_PROP_FPS,23))
    print("Total number of frames present is ",(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))
    origFPS = int(video_capture.get(cv2.CAP_PROP_FPS))
    frmcnt = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    wid = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    hei = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vidLen = frmcnt/origFPS
    print("video length is total {} sec ".format(vidLen))
    print("video resolution is {} X {} ".format(wid,hei))
    lpFlag = False

    #Dummy logic to set FPS
    if wid >= 1280 or hei >= 720:
        origFPS = origFPS + 11
    else:
        origFPS = origFPS + 1

    #origFPS = 70  #set this for manual fps

    while not frmcnt <= 0:
        
        t_end = time.time() + 1
        for _ in range(origFPS):

            time.sleep(1/origFPS)
            frame = playVideo(video_capture,wid,hei)
            # HERE WE CAN PROCESS FRAME
            frmcnt = frmcnt -1

            if frame is None:
                print("found frame is none")
                lpFlag = True
                vidBreakTime = time.time()
                print("total video time ", vidBreakTime - vidStartTime )
                break

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if lpFlag == True:
            #print("found frame is none")   
            print("broken upper loop")
            break

        if time.time() < t_end:
            print("inside time adjust")
            time.sleep(t_end - time.time())



    # Use this logic for maximum pumping of data

    # while True:
    #     #frame = webCamera_Stream(video_capture)

    #     #frame , count = facedetection(video_capture) #might give warning when frame is none
    #     frame = playVideo(video_capture,wid,hei) # HERE WE CAN PROCESS FRAME


    #     if frame is None:
    #         print("found frame is none")
    #         break
        
    #     #global jsonData
    #     #jsonData.update({"count":count})
        
    #     yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/demo_feed')
def demo_feed():
    print("inside demo_feed")
    #here response will be send frame by frame (called by html page)
    return Response(generatedemo_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')




#FOR DOUBLE STREAMING



@app.route('/double')
def double():
    global StopAllFrames
    StopAllFrames = False
    return render_template('double.html')

def generatefirst_camframe():
    global video_capture
    print("inside call start cam")
    video_capture = startWebCamera_Stream()
    while True:
        #frame = webCamera_Stream(video_capture)

        frame = GetOnlyCamFrame(video_capture) # HERE WE CAN PROCESS FRAME

        if frame is None:
            print("found frame is none")
            break        
        
        global globalFrame
        globalFrame = frame

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generateSecond_camframe():
    print("i am inside Double frame")
    global globalFrame
    global StopAllFrames
    #count = 0
    #time.sleep(100)
    #better use a loop than time, coz it depends upon time to load
    while True:
        if globalFrame is None and StopAllFrames == False:
            #count = count + 1
            #print("NO second frame count= ",count)
            continue
        
        if StopAllFrames == True:
            print("Double Frame Loop Broken")
            break

        FaceFrame = None

        FaceFrame , count = facedetecFromFrame(globalFrame)

        global jsonData
        jsonData.update({"count":count})

        global heatMapFrame

        heatMapFrame = FaceFrame

        #FaceFrame = cv2.imencode('.jpg', globalFrame)[1].tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + FaceFrame + b'\r\n')


'''
@app.route('/first') and @app.route('/second') called one after another by html page...(depends)

first and second these driver functions call their respective generate frames

'''


@app.route('/first')
def first():
    print("inside first feed")
    #here response will be send frame by frame (called by html page)
    return Response(generatefirst_camframe(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/second')
def second():
    print("received call for double frame")
    #global globalFaceFrame
    return Response(generateSecond_camframe(),mimetype='multipart/x-mixed-replace; boundary=frame')



# adding feature pause video
# idea is to, on demand send that perticular single frame
# on demand means called by JS
# perticular frame is global face Frame

@app.route('/pauseFirst')
def pauseFirst():
    print("paused First frame sent ")
    pausedFrame = None
    global globalFrame
    img = globalFrame
    img = img[:,:,::-1]	# The data has 3 dimensions: width, height, and color. ::-1 effectively reverses the order of the colors. The width and height are not affected
    img = Image.fromarray(img, 'RGB')
    
    store_images(img)
    pausedFrame = cv2.imencode('.jpg', globalFrame)[1].tobytes()

    res = make_response(pausedFrame)
    res.mimetype= "image/jpg; boundary=frame"

    #No cache to store other wise image will not change.
    res.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    res.headers['Pragma'] = 'no-cache'

    return res

    #return Response(pausedFrame,mimetype="image/jpg; boundary=frame",)

#ISSUE if global frame is None handle it and cv2.errors as e
# Issue will be when encoding that image simply redirect to double page

@app.route('/pauseSecond')
def pauseSecond():
    print("paused Heatmap frame")
    global heatMapFrame
    res1 = make_response(heatMapFrame)
    res1.mimetype= "image/jpg; boundary=frame"

    #No cache to store other wise image will not change.
    res1.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    res1.headers['Pragma'] = 'no-cache'

    return res1

@app.route('/pausebirdseye')
def pausebirdseye():
    print("paused birdseye frame")
    global heatMapFrame
    pausedFrame = cv2.imencode('.jpg', heatMapFrame)[1].tobytes()

    res1 = make_response(pausedFrame)
    res1.mimetype= "image/jpg; boundary=frame"

    #No cache to store other wise image will not change.
    res1.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    res1.headers['Pragma'] = 'no-cache'

    return res1



#FOR SAMPLE VIDEO

@app.route('/sample')
@login_required
def sample():
    global StopAllFrames
    StopAllFrames = False
    return render_template('sample.html')

def generatefirst_sampleframe():
    # global video_capture
    streamer_obj = Streamer()
    video_capture = streamer_obj.generateStream(VideoName=None)

    print("inside call start cam")
    # video_capture = startWebCamera_Stream()
    # video_capture = openVideoFile_Stream()
    while True:
        #frame = webCamera_Stream(video_capture)

        #frame = GetOnlyCamFrame(video_capture) # HERE WE CAN PROCESS FRAME
        # ret, frame = video_capture.read()
        frame = streamer_obj.getframe(video_capture)

        if frame is None:
            print("found frame is none")
            break        
        
        global globalFrame
        global heatMapFrame

        globalFrame, heatMapFrame, total_people, num_follow, num_dont_follow =  integrated_social_distancing(frame)

        global jsonData
        jsonData.update({"total_people":total_people})
        jsonData.update({"num_follow":num_follow})
        jsonData.update({"num_dont_follow":num_dont_follow})

        
        #frame = globalFrame

        #global heatMapFrame
        #heatMapFrame = cv2.imencode('.jpg', frame)[1].tobytes()


        frame = cv2.imencode('.jpg', globalFrame)[1].tobytes()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generateSecond_sampleframe():
    print("i am inside Sample frame")
    global globalFrame
    global StopAllFrames
    global heatMapFrame
    #count = 0
    #time.sleep(100)
    #better use a loop than time, coz it depends upon time to load
    while True:
        if globalFrame is None and StopAllFrames == False:
            #count = count + 1
            #print("NO second frame count= ",count)
            continue
        
        if StopAllFrames == True:
            print("Double Sample Frame Loop Broken")
            break

        if heatMapFrame is None:
            print("Birds eye view found null")
            continue

        FaceFrame = None

        #FaceFrame , count = facedetecFromFrame(globalFrame)

        #global jsonData
        #jsonData.update({"count":count})

        #global globalFrame

        #FaceFrame = globalFrame

        #heatMapFrame = cv2.imencode('.jpg', heatMapFrame)[1].tobytes()

        #heatMapFrame = FaceFrame


        FaceFrame = cv2.imencode('.jpg', heatMapFrame)[1].tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + FaceFrame + b'\r\n')


'''
@app.route('/first') and @app.route('/second') called one after another by html page...(depends)

first and second these driver functions call their respective generate frames

'''


@app.route('/firstsample')
def firstsample():
    print("inside first feed")
    #here response will be send frame by frame (called by html page)
    return Response(generatefirst_sampleframe(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/secondsample')
def secondsample():
    print("received call for double frame")
    #global globalFaceFrame
    return Response(generateSecond_sampleframe(),mimetype='multipart/x-mixed-replace; boundary=frame')







# FOR IP WEB CAMERA ACCESS


# take input ip from the web browser and fetch shots from that ip
# 
@app.route('/getip',methods=['GET', 'POST'])
@login_required
def getip():
    global ip
    ip = request.form.get("ip")
    print("Found ip is ",ip)
    print("type is " , type(ip))

    if ip is None:
        print("inside nonde")
        #print("sending back to ipcam")
        return render_template("getip.html",message=" ")
        #return redirect(url_for("ipcam"))
    
    ip = str(request.form.get("ip"))

    try:
        if urllib.request.urlopen("http://"+ip+"/shot.jpg").getcode() == 200:
            return redirect(url_for("ipcam"))
    except urllib.error.URLError:
        print("Wrong URl entered")
        return render_template("getip.html",message="Wrong Url Entered")
    


    return redirect(url_for("ipcam"))
    #return render_template("getip.html")



@app.route('/ipcam',methods=['GET', 'POST'])
@login_required
def ipcam():
    global ip
    global StopAllFrames
    StopAllFrames = False
    #print("req form get ip")
    #ip = str(request.form.get("ip"))
    
    #if ip is None:
    #    while ip is None:
    #        continue
    #print("sending to ipcam template ip is ",ip)
    return render_template('ipcam.html')

def getIpFrame():
    global ip
    #ip = str(request.form.get("ip"))

    if ip is None:
        print("IP found is none in frame")
        while ip is None:
            continue

    print("IP Found inside getipFrame  is = ",ip)
    while True:
        #frame = webCamera_Stream(video_capture)

        frame = startipWebCam(ip)
        global globalFrame
        global heatMapFrame

                

        if frame is None:
            print("found frame is none from IP cam")
            #Stop the second frame
            break        
        
        #global globalFrame
        #globalFrame = frame
        #so that automatically second frame we can stream

        globalFrame,heatMapFrame, _, _, _ =  integrated_social_distancing(frame)

        frame = cv2.imencode('.jpg', globalFrame)[1].tobytes()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/ipstream')
def ipstream():
    #print("inside first feed")
    #here response will be send frame by frame (called by html page)
    return Response(getIpFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000, threaded=True)
