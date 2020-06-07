from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from PIL import Image
import cv2


def HeatMapAuto(list1,max_x,max_y):
    # if there are no points return blank image
    if len(list1) < 3:
        plt.xlim(0, max_x)
        plt.ylim(0, max_y)
        plt.xlabel('X_MESH')
        plt.ylabel('Y_MESH')
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


    x, y = [coord[0] for coord in list1], [coord[1] for coord in list1]
    print(x)
    print(y)
    # call the kernel density estimator function
    ax = sns.kdeplot(x, y,cmap="coolwarm", shade=True, shade_lowest=False, cbar=False,gridsize=100)
    # the function has additional parameters you can play around with to fine-tune your heatmap, e.g.:
    # ax = sns.kdeplot(x, y, kernel="gau", bw = 25, cmap="Reds", n_levels = 50, shade=True, shade_lowest=False, gridsize=100)

    # plot your KDE
    #ax.set_frame_on(True)

    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    #plt.axis('on')
    plt.plot(x, y, 'ro')
    plt.xlabel('X_MESH')
    plt.ylabel('Y_MESH')
    #plt.pause(0.01)
    # plt.savefig('kde.png')
    # plt.show
    fig1 = plt.gcf()
    # plt.show(block=False)
    # plt.draw()
    # fig1.savefig('tessstttyyy.png', dpi=100)
    # plt.pause(0.02)
    # plt.close()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png", dpi=180)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    plt.clf()
    plt.cla()
    img_np_array = cv2.imdecode(img_arr, 1)
    # img_np_array = cv2.cvtColor(img_np_array, cv2.COLOR_BGR2RGB)
    # cv2.imshow("HeatMap", img_np_array)
    # Here we return the Image as numpy array
    return img_np_array


# def get_img_from_fig(plot, dpi=180):
#     fig1 = plot.gcf()
#     plot.show(block=False)
#     # plt.draw()
#     # fig1.savefig('tessstttyyy.png', dpi=100)
#     plot.pause(0.75)
#     plot.close()
#     buf = io.BytesIO()
#     fig1.savefig(buf, format="png", dpi=dpi)
#     buf.seek(0)
#     img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
#     buf.close()
#     img_np_array = cv2.imdecode(img_arr, 1)
#     # img_np_array = cv2.cvtColor(img_np_array, cv2.COLOR_BGR2RGB)
#     cv2.imshow("LOLSS", img_np_array)
#     # Here we return the Image as numpy array
#     return img_np_array
#
#
# def numpy2pil(np_array: np.ndarray) -> Image:
#     """
#     Convert an HxWx3 numpy array into an RGB Image
#
#     """
#     img = Image.fromarray(np_array, 'RGB')
#     return img

# For Testing this module
# load the coordinates file
# x = [10, 20, 30, 15, 30, 20, 30, 10, 27, 15, 20, 5, 30, 16]
# y = [10, 20, 30, 15, 25, 10, 5, 30, 27, 13, 40, 40, 27.5, 14]

# list1=[(764,90),(620,103),(707,262)]
# HeatMapAuto(list1)
# HeatMapAuto(x,y)
