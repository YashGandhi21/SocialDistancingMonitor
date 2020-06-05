import cv2

import numpy as np
import pickle


def get_camera_perspective(img, inner_points):
    IMAGE_H = img.shape[0]
    IMAGE_W = img.shape[1]

    src = np.float32(np.array(inner_points))
    dst = np.float32([[0, 0], [IMAGE_W, 0], [IMAGE_W, IMAGE_H], [0, IMAGE_H]])

    matrix, status = cv2.findHomography(src, dst, cv2.RANSAC)

    P = np.array([[0, IMAGE_W, IMAGE_W, 0], [0, 0, IMAGE_H, IMAGE_H], [1, 1, 1, 1]])
    h_ = matrix.dot(P)

    min_x, min_y = np.min(h_[0] / h_[2]), np.min(h_[1] / h_[2])
    if (min_x < 0 and min_y > 0):
        trans_mat = np.array([[1, 0, -min_x], [0, 1, min_y], [0, 0, 1]])
    elif (min_x > 0 and min_y < 0):
        trans_mat = np.array([[1, 0, min_x], [0, 1, -min_y], [0, 0, 1]])
    elif (min_x < 0 and min_y < 0):
        trans_mat = np.array([[1, 0, -min_x], [0, 1, -min_y], [0, 0, 1]])
    else:
        trans_mat = np.array([[1, 0, min_x], [0, 1, min_y], [0, 0, 1]])

    F = trans_mat.dot(matrix)

    h__ = F.dot(P)
    max_x, max_y = int(np.max(h__[0] / h__[2])), int(np.max(h__[1] / h__[2]))

    #As soon as matrix is generated it is saved in pickle file
    save_homography_matrix(matrix, max_x, max_y)

    return F, max_x, max_y


def save_homography_matrix(matrix, max_x, max_y):
    # saving the homography matrix in pickle file
    dbfile = open("Homography matrix", "ab")
    pickle.dump(matrix, dbfile)
    dbfile.close()
    #save max_x & max_y
    dbfiles = open("Image Size", "ab")
    pickle.dump([max_x, max_y], dbfiles)
    dbfile.close()