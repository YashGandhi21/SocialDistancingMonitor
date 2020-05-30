import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial import distance
import pickle

Original_Homographed_dict = {}

#Always call this function for this file
def map_points_to_homography_coordinates(people_coordinates_list):
    matrix = pickle.load(open("Homography matrix", "rb"))

    for point in people_coordinates_list:
        toworld(point, matrix)

    save_original_to_homgraphed_mapping()

    return Original_Homographed_dict

def toworld(o_point, matrix):
    imagepoint = [o_point[0], o_point[1], 1]
    worldpoint = np.array(np.dot(np.array(matrix), imagepoint))

    scalar = worldpoint[2]

    xworld = int(worldpoint[0] / scalar)
    yworld = int(worldpoint[1] / scalar)

    # store the pair in local dictionary for every function call
    Original_Homographed_dict[o_point] = (xworld, yworld)

    return xworld, yworld

def save_original_to_homgraphed_mapping():
    for k, v in Original_Homographed_dict.items():
        print(k, " = ", v)

    #saving the pairs in pickle file
    dbfile = open("Original_to_homographed_points_dictionary", "ab")
    pickle.dump(Original_Homographed_dict, dbfile)
    dbfile.close()