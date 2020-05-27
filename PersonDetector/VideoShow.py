from threading import Thread
import cv2
import time

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.counter=0

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            self.counter += 1
            #print("VideoShower", (self.counter))
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True


# def threadVideoShow(source=0):
#     """
#     Dedicated thread for showing video frames with VideoShow object.
#     Main thread grabs video frames.
#     """
#
#     cap = cv2.VideoCapture(source)
#     (grabbed, frame) = cap.read()
#     video_shower = VideoShow(frame).start()
#
#     while True:
#         (grabbed, frame) = cap.read()
#         if not grabbed or video_shower.stopped:
#             video_shower.stop()
#             break
#
#         video_shower.frame = frame
#
# threadVideoShow(0)