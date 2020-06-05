# author: Ashish Surve

# main module for social distancing monitor
import matplotlib.pyplot as plt
import PersonDetector as pd
import Homography as hg
import DistancingModule as dm
import Heatmap as hm
import cv2
import time
from PIL import Image
import numpy as np
def main():
    # change this hardcoded later
    source = "video1.mp4"

    # Demo on/off switch
    demo = True
    video = cv2.VideoCapture(source)

    while video.isOpened():
        start_time = time.time()
        # read frame from webcam/video
        status, frame = video.read()

        if not status:
            break

        # apply object detection
        bbox, label, conf = pd.detect_common_objects(frame, confidence=0.4, model='yolov3-tiny', enable_gpu=False)

        # get points
        points = pd.box_to_point(bbox)
        for point in points:
            frame = cv2.circle(frame, point, 4, (255, 0, 0), 3)

        # call to Homograph module
        homograph_calibrate = True

        # Call the first if only 1st frame then rest call to else
        # because that's how the module developer intended it to be called.
        if homograph_calibrate:
            mapped_points_dict = hg.Funct_Perform_Homography(frame, points)
            homograph_calibrate = False
        else:
            mapped_points_dict = hg.map_points_to_homography_coordinates(points)

        # call to distancing module
        # TODO : return frames.
        top_view_frame, _ = dm.red_coordinates_from_coordinates(mapped_points_dict)
        # top_view_frame = cv2.resize(top_view_frame, (frame.shape[1], frame.shape[0]))
        cv2.imshow("TopView", top_view_frame)

        # Heat-Map Module calls
        # convert list of tuple to 2 lists
        # x, y = hm.list_of_tuples_to_list_x_and_y(points)
        #imgo = hm.HeatMapAuto(points)
        #cv2.imshow("Heatmap",imgo)

        # draw bounding boxes
        frame = pd.draw_bbox(frame, bbox, label, conf, write_conf=True, colors=(0, 255, 0))
        cv2.putText(frame, "FPS: " + str(round(1.0 / (time.time() - start_time), 2)), (10, 50),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 3)

        # display output
        if demo:
            cv2.imshow("Real-time object detection", frame)
            print("FPS: ", 1.0 / (time.time() - start_time))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
