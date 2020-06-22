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

homograph_calibrate = True
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


    # apply object detection
    # for faster execution
    bbox, label, conf = pd.detect_common_objects(frame, confidence=0.4, model='yolov3-tiny', enable_gpu=False)

    # for better accuracy
    # bbox, label, conf = pd.detect_common_objects(frame, confidence=0.4, model='yolov3', enable_gpu=False)

    # get points
    # TODO: change the code to get points nearest to legs instead of center
    points = pd.box_to_point(bbox)
    for point in points:
        frame = cv2.circle(frame, point, 4, (255, 0, 0), 3)

    # call to Homograph module

    # Funct_Perform_homography is for calibrating homograph by choosing points
    # mapped_points_dict is to get mapped points
    # TODO: show demo for 20 different frames.
    global homograph_calibrate
    if homograph_calibrate:
        hg.caliberate_camera(frame)
        mapped_points_dict = hg.map_points_to_homography_coordinates(points)
        homograph_calibrate = False
    else:
        mapped_points_dict = hg.map_points_to_homography_coordinates(points)

    # find max height, width in homograph plane11
    t_dict = list(hg.map_points_to_homography_coordinates([(width, height)]))
    # add 110 % padding
    mapped_width = int(1.15 * t_dict[0][0])
    mapped_height = int(1.15 * t_dict[0][1])

    # call to distancing module
    # TODO : return frames. Done.
    # TODO : Threshold add to function. Done
    # TODO : Keep width and height same as input image. Done
    #          pass it to module
    top_view_frame, red_coordinates = dm.fetchRedCoordinatesFromCoordinates(mapped_points_dict, 115, mapped_width, mapped_height)
    # top_view_frame = cv2.resize(top_view_frame, (frame.shape[1], frame.shape[0]))
    # cv2.imshow("TopView", top_view_frame)

    # Heat-Map Module calls
    # TODO: Make it work properly on BGR format.
    # TODO: not working for empty list.Done.
    # TODO: exclude until stable
    # TODO Axis OFF.Done.

    heatMap_image = hm.HeatMapAuto(mapped_points_dict.keys(), mapped_width, mapped_height)
    # here 800x600 is the image window
    imS = cv2.resize(heatMap_image, (800, 600))
    # cv2.imshow("HeatMap", imS)

    # draw bounding boxes
    red_bbox = []
    red_label = []
    red_conf = []
    green_bbox = []
    green_label = []
    green_conf = []

    for point, box, lab, con in zip(points, bbox, label, conf):
        if point in red_coordinates.values():
            red_bbox.append(box)
            red_label.append(lab)
            red_conf.append(con)
        else:
            green_bbox.append(box)
            green_label.append(lab)
            green_conf.append(con)

    # find no of people who arent following and people who are following social distancing
    num_follow, num_dont_follow = len(green_bbox), len(red_bbox)
    total_people = num_follow + num_dont_follow
    # print("follow = ",num_follow," dont follw = ",num_dont_follow)

    # draw green boxes
    frame = pd.draw_bbox(frame, green_bbox, green_label, green_conf, write_conf=False, colors=(0, 255, 0))
    if len(red_bbox) > 0:
        frame = pd.draw_bbox(frame, red_bbox, red_label, red_conf, write_conf=False, colors=(0, 0, 255))
    # cv2.putText(frame, "FPS: " + str(round(1.0 / (time.time() - start_time), 2)), (10, 50),
    #            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 3)

    frame = np.concatenate((frame, cv2.resize(heatMap_image, (width, height))), axis=1)
    return frame, top_view_frame, total_people, num_follow, num_dont_follow



def main():
    # change this hardcoded later
    source = "video1.mp4"

    # Demo on/off switch
    demo = True
    video = cv2.VideoCapture(source)

    writeVideo_flag = False

    if writeVideo_flag:
        w = int(video.get(3))
        h = int(video.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_yolov3.avi', fourcc, 30, (w, h))
        frame_index = -1


    try:
        while video.isOpened():
            start_time = time.time()
            # read frame from webcam/video
            status, frame = video.read()
            if not status:
                break
            frame, top_view, _, _, _ = integrated_social_distancing(frame)
            cv2.imshow("Person Detector", frame)
            cv2.imshow("Bird's Eye View", top_view)

            if writeVideo_flag:  # and not asyncVideo_flag:
                # save a frame
                out.write(frame)
                frame_index == frame_index + 1

            print("FPS: ", 1.0 / (time.time() - start_time))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception:
        print("Exception Occured")
        print(traceback.format_exc())
    finally:
        video.release()
        cv2.destroyAllWindows()
        if writeVideo_flag:
            out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


