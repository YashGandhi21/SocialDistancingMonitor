#Author - CHETAN PATIL
'''
    Algorithm :

    Step 1] Convert the List of Tuples obtained from the Homography Module to give individual
            lists representing the x & y co-ordinates respectively .

    Step 2] Plot the Kernel Density Plot(KDE) wrt the x and y lists .

    Step 3] Set up scale for the axis over which KDE is to be plotted .

    Step 4] Conversion of plot to Figure Object .

    Step 5] Saving the figure in a memory buffer and hence convert the figure stored into the
            memory into H x W x 3 format which is represented by the nd-numpy array .
    Step 6] Return the nd-numpy array .

    Algorithm Terminates.
'''

from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from PIL import Image
import cv2

# Refrences:
# https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask
# https://matplotlib.org/3.2.1/gallery/misc/print_stdout_sgskip.html?highlight=matplotlib%20use%20agg

import matplotlib
matplotlib.use('Agg')


def HeatMapAuto(list1,max_x,max_y):
    # if there are no points return blank image
    if len(list1) < 3:
        plt.xlim(0, max_x)
        plt.ylim(0, max_y)
        plt.title("Heatmap")
        plt.xticks([])
        plt.yticks([])
        # plt.xlabel('X_MESH')
        # plt.ylabel('Y_MESH')
        fig2 = plt.gcf()

        buf1 = io.BytesIO()
        fig2.savefig(buf1, format="png", dpi=180)
        buf1.seek(0)
        img_arr1 = np.frombuffer(buf1.getvalue(), dtype=np.uint8)
        buf1.close()

        plt.clf()
        plt.cla()
        img1_np_array = cv2.imdecode(img_arr1, 1)
        # img_np_array = cv2.cvtColor(img_np_array, cv2.COLOR_BGR2RGB)
        # cv2.imshow("HeatMap", img_np_array)
        # Here we return the Image as numpy array
        return img1_np_array


    x, y = [coord[0] for coord in list1], [max_y-coord[1] for coord in list1]
    # call the kernel density estimator function
    ax = sns.kdeplot(x, y,cmap="coolwarm", shade=True, shade_lowest=False, cbar=False,gridsize=100)
    # the function has additional parameters we can play around with to fine-tune your heatmap, e.g.:
    # ax = sns.kdeplot(x, y, kernel="gau", bw = 25, cmap="Reds", n_levels = 50, shade=True, shade_lowest=False, gridsize=100)

    # plot your KDE

    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    plt.title("Heatmap")
    plt.xticks([])
    plt.yticks([])
    plt.plot(x, y, 'ro')
    fig1 = plt.gcf()

    buf = io.BytesIO()
    fig1.savefig(buf, format="png", dpi=180)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    plt.clf()
    plt.cla()
    img_np_array = cv2.imdecode(img_arr, 1)
    return img_np_array


