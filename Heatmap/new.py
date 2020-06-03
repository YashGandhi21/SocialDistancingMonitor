from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def HeatMapAuto(list1):

    x, y = [coord[0] for coord in list1], [coord[1] for coord in list1]
    print(x)
    print(y)
    # call the kernel density estimator function
    ax = sns.kdeplot(x, y, cmap="coolwarm", shade=True, shade_lowest=False, cbar=True)
    # the function has additional parameters you can play around with to fine-tune your heatmap, e.g.:
    # ax = sns.kdeplot(x, y, kernel="gau", bw = 25, cmap="Reds", n_levels = 50, shade=True, shade_lowest=False, gridsize=100)

    # plot your KDE
    ax.set_frame_on(True)

    plt.xlim(min(x) - 10, max(x) + 10)
    plt.ylim(min(y) - 10, max(y) + 10)
    plt.axis('on')
    plt.plot(x, y, 'ro')
    plt.xlabel('X_MESH')
    plt.ylabel('Y_MESH')
    plt.pause(0.1)
    #plt.savefig('kde.png')
    #plt.show()
    return plt
def HeatMapAutoNext(list1,plt1):
    x, y = [coord[0] for coord in list1], [coord[1] for coord in list1]
    print(x)
    print(y)
    # call the kernel density estimator function
    ax = sns.kdeplot(x, y, cmap="coolwarm", shade=True, shade_lowest=False, cbar=True)
    # the function has additional parameters you can play around with to fine-tune your heatmap, e.g.:
    # ax = sns.kdeplot(x, y, kernel="gau", bw = 25, cmap="Reds", n_levels = 50, shade=True, shade_lowest=False, gridsize=100)

    # plot your KDE
    ax.set_frame_on(True)

    plt1.xlim(min(x) - 10, max(x) + 10)
    plt1.ylim(min(y) - 10, max(y) + 10)
    plt1.axis('on')
    plt1.plot(x, y, 'ro')
    plt1.xlabel('X_MESH')
    plt1.ylabel('Y_MESH')
    #plt1.pause(1000)
    #plt.savefig('kde.png')
    #plt.show()
    return plt


# load the coordinates file
#x = [10, 20, 30, 15, 30, 20, 30, 10, 27, 15, 20, 5, 30, 16]
#y = [10, 20, 30, 15, 25, 10, 5, 30, 27, 13, 40, 40, 27.5, 14]

#list1=[(764,90),(620,103),(707,262)]
#HeatMapAuto(list1)
#HeatMapAuto(x,y)