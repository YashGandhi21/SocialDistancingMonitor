#!/usr/bin/env python
# coding: utf-8

# In[12]:


import cv2
import numpy as np
import pickle
import Homography.Perform_Homography as ph
from Homography.To_World import map_points_to_homography_coordinates


mouse_pts = []



#call this function for this file
def Funct_Perform_Homography(input_image):
    # In[211]:
    cap = input_image
    print(cap.shape)
    def get_mouse_points(event, x, y, flags, param):
        # Used to mark 4 points on the frame zero of the video that will be warped
        # Used to mark 2 points on the frame zero of the video that are 6 feet away
        global mouseX, mouseY, mouse_pts
        if event == cv2.EVENT_LBUTTONDOWN:
            mouseX, mouseY = x, y
            cv2.circle(cap, (x, y), 5, (0, 255, 255), 10)
            if "mouse_pts" not in globals():
                mouse_pts = []
        mouse_pts.append((x, y))
        print("Point detected")
        print(mouse_pts)

    #social_distance = 6912  # 1feet = 1152 pixels, hence 6 feet is 6912 pixels

    

    try:
        matrix = pickle.load(open("Homography matrix", "rb"))
        size = pickle.load(open("Image Size", "rb"))
        max_x, max_y = size[0], size[1]
    except:
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", get_mouse_points)
        # Ask user to mark parallel points. Order tl, tr, br, bl
        while True:
            cv2.imshow("image", cap)
            cv2.waitKey(1)
            if len(mouse_pts) >= 4:
                cv2.destroyWindow("image")
                break
            four_points = mouse_pts
        pts = np.array([four_points[0], four_points[1], four_points[2], four_points[3]], np.int32)
        cv2.polylines(cap, [pts.reshape((-1, 1, 2))], True, (255, 255, 0), 3)
        matrix, max_x, max_y = ph.get_camera_perspective(cap, four_points[0:4])


    #warped_pt = cv2.warpPerspective(cap, matrix, (max_x, max_y))
    #Original_Homographed_dict = map_points_to_homography_coordinates(people_coordinates_list)


    #return matrix, max_x, max_y
    #returning name of pickle file or return "Original_Homographed_dict" dictionary
    #return Original_Homographed_dict