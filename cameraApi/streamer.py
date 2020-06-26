import cv2

class Streamer:
    def __init__(self):
        print("Object created")
        self.frame = None
        self.video_capture = None
        self.total_people = 1000
        self.num_follow = 1000
        self.num_dont_follow = 1000
        self.ip = None

    # Starting streamer
    def generateStream(self,VideoName = None):
        
        if VideoName is None:
            video_capture = cv2.VideoCapture('video1.mp4')
        else:
            video_capture = cv2.VideoCapture(VideoName)

        self.video_capture = video_capture
        
        return video_capture

    # API with loop
    def getFramesStream(self,video_capture):
        
        while True:

            ret ,frame = video_capture.read()

            if not ret:
                print("loop brokern")
                break
            
            self.frame = frame
        
            return frame
    
    # API should place inside a loop
    def getframe(self,video_capture):

        ret ,frame = video_capture.read()

        if not ret:
            print("loop brokern")
            return None
        
        self.frame = frame

        return frame

    # get the n'th frame
    def getCurrentFrame(self):
        frameToSend = self.frame
        if frameToSend is None:
            return None
        else:
            return frameToSend

    # Stop the started stream
    def stopStream(self):
        try:
            self.video_capture.release()
            cv2.destroyAllWindows()
        except NameError:
            print("caught name error")
            pass




        

    


        


    


