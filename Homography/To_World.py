import numpy as np
import pickle



#Always call this function for this file
def map_points_to_homography_coordinates(people_coordinates_list):
    matrix = pickle.load(open("Homography matrix", "rb"))

    # Added by Ashish Surve
    # WHY : the points in new frames were appended and the global variable wasn't reset in multiple calls.
    # TODO : Remove the global variables.
    
    Original_Homographed_dict = {}
    for point in people_coordinates_list:
        imagepoint = [point[0], point[1], 1]
        worldpoint = np.array(np.dot(np.array(matrix), imagepoint))

        scalar = worldpoint[2]

        xworld = int(worldpoint[0] / scalar)
        yworld = int(worldpoint[1] / scalar)

    # store the pair in local dictionary for every function call
    Original_Homographed_dict[point] = (xworld, yworld)

    save_original_to_homgraphed_mapping(Original_Homographed_dict)

    return Original_Homographed_dict



def save_original_to_homgraphed_mapping(Original_Homographed_dict):
    for k, v in Original_Homographed_dict.items():
        print(k, " = ", v)

    #saving the pairs in pickle file
    dbfile = open("Original_to_homographed_points_dictionary", "ab")
    pickle.dump(Original_Homographed_dict, dbfile)
    dbfile.close()