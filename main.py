# author: Ashish Surve

# main module for social distancing monitor

import PersonDetector as pd
import cv2
import time


def main():
    # change this hardcoded later
    source = "video1.mp4"

    video = cv2.VideoCapture(source)

    while video.isOpened():
        start_time = time.time()
        # read frame from webcam/video
        status, frame = video.read()

        if not status:
            break

        # apply object detection
        bbox, label, conf = pd.detect_common_objects(frame, confidence=0.4, model='yolov3-tiny', enable_gpu=False)

        # draw points
        points = pd.box_to_point(bbox)
        for point in points:
            frame = cv2.circle(frame, point, 4, (255, 0, 0), 3)

        # draw bounding boxes
        frame = pd.draw_bbox(frame, bbox, label, conf, write_conf=True, colors=(0, 255, 0))
        cv2.putText(frame, "FPS: " + str(round(1.0 / (time.time() - start_time), 2)), (10, 50),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 3)

        # display output
        cv2.imshow("Real-time object detection", frame)

        print("FPS: ", 1.0 / (time.time() - start_time))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
