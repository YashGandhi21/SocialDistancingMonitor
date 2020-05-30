# author: Ashish Surve

# person detection video example using tiny yolo model.
# demo file for person detector.
# import necessary packages
from PersonDetector import person_detection as od
import cv2
import time
import acapture


# open file or webcam
source = "video.mp4"

# video_getter = VG.VideoGet(source).start()

writeVideo_flag = True
asyncVideo_flag = False

if asyncVideo_flag:
    video = acapture.open(source)
else:
    video = cv2.VideoCapture(source)

if writeVideo_flag:
    w = int(video.get(3))
    h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_yolov3.avi', fourcc, 30, (w, h))
    frame_index = -1

if not video.isOpened():
    print("Could not open video")
    exit()

# video_shower = VS.VideoShow(frame).start()
while video.isOpened():
    start_time = time.time()
    # read frame from webcam/video
    status, frame = video.read()

    if not status:
        break

    # apply object detection
    bbox, label, conf = od.detect_common_objects(frame, confidence=0.4, model='yolov3-tiny', enable_gpu=False)

    frame = od.draw_bbox(frame, bbox, label, conf, write_conf=True)
    cv2.putText(frame, "FPS: " + str(round(1.0 / (time.time() - start_time), 2)), (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)

    if writeVideo_flag:  # and not asyncVideo_flag:
        # save a frame
        out.write(frame)
        frame_index == frame_index + 1

    # display output
    #cv2.imshow("Real-time object detection", out)
    # video_shower.frame = frame
    print("FPS: ", 1.0 / (time.time() - start_time))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Time: ", time.time()-start_time)
# release resources
if asyncVideo_flag:
    video.stop()
else:
    video.release()

if writeVideo_flag:
    out.release()

cv2.destroyAllWindows()
