# author: Ashish Surve

# main module for social distancing monitor
import matplotlib.pyplot as plt
import PersonDetector as pd
import Homography as hg
import DistancingModule as dm
import Heatmap as hm

import cv2
import time
import traceback
from PIL import Image
import numpy as np


"""
Executes all modules and return top_view and people detector as  numpy BGR array
@frame : input frame from camera as a numpy BGR array.
"""
def integrated_social_distancing(frame):
    # reduce image resolution by half if width > 1000 pixels
    if frame.shape[:2][1] > 1000:
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    height, width = frame.shape[:2]

    # to calibrate set flag to True
    homograph_calibrate = False

    # apply object detection
    bbox, label, conf = pd.detect_common_objects(frame, confidence=0.4, model='yolov3-tiny', enable_gpu=False)

    # get points
    # TODO: change the code to get points nearest to legs instead of center
    points = pd.box_to_point(bbox)
    for point in points:
        frame = cv2.circle(frame, point, 4, (255, 0, 0), 3)

    # call to Homograph module

    # Funct_Perform_homography is for calibrating homograph by choosing points
    # mapped_points_dict is to get mapped points
    # TODO: show demo for 20 different frames.
    if homograph_calibrate:
        hg.caliberate_camera(frame)
        mapped_points_dict = hg.map_points_to_homography_coordinates(points)
        homograph_calibrate = False
    else:
        mapped_points_dict = hg.map_points_to_homography_coordinates(points)

    # find max height, width in homograph plane
    t_dict = list(hg.map_points_to_homography_coordinates([(width, height)]))
    # add 10 % padding
    mapped_width = t_dict[0][0] + int(0.1 * t_dict[0][0])
    mapped_height = t_dict[0][1] + int(0.1 * t_dict[0][1])

    # call to distancing module
    # TODO : return frames. Done.
    # TODO : Threshold add to function. Done
    # TODO : Keep width and height same as input image. Done
    #          pass it to module
    top_view_frame, red_coordinates = dm.fetchRedCoordinatesFromCoordinates(mapped_points_dict, 75, mapped_width, mapped_height)
    # top_view_frame = cv2.resize(top_view_frame, (frame.shape[1], frame.shape[0]))
    # cv2.imshow("TopView", top_view_frame)

    # Heat-Map Module calls
    # TODO: Make it work properly on BGR format.
    # TODO: not working for empty list.Done.
    # TODO: exclude until stable
    # TODO Axis OFF.Done.

    # heatMap_image = hm.HeatMapAuto(mapped_points_dict.keys(), mapped_width, mapped_height)
    # here 800x600 is the image window
    # imS = cv2.resize(heatMap_image, (800, 600))
    # cv2.imshow("HeatMap", imS)

    # draw bounding boxes


    frame = pd.draw_bbox(frame, bbox, label, conf, write_conf=True, colors=(0, 255, 0))
    # cv2.putText(frame, "FPS: " + str(round(1.0 / (time.time() - start_time), 2)), (10, 50),
    #            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 3)

    return frame, top_view_frame



def main():
    # change this hardcoded later
    source = "video1.mp4"

    # Demo on/off switch
    demo = True
    video = cv2.VideoCapture(source)

    # to calibrate homograph
    homograph_calibrate = False
    try:
        while video.isOpened():
            start_time = time.time()
            # read frame from webcam/video
            status, frame = video.read()
            if not status:
                break
            frame, top_view = integrated_social_distancing(frame)
            cv2.imshow("Person Detector", frame)
            cv2.imshow("Bird's Eye View", top_view)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception:
        print("Exception Occured")
        print(traceback.format_exc())
    finally:
        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


