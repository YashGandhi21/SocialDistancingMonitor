# Author - Ashish Surve

# Python code for converting the bounding box to a point for Homograph generation


def box_to_point(bbox):
    points_list = []
    for single_box in bbox:  # (x, y, w, h)
        center_x = single_box[0] + int((single_box[2] - single_box[0]) / 2)
        center_y = single_box[1] + int((single_box[3] - single_box[1]) / 2)
        points_list.append((center_x, center_y))
    return points_list
