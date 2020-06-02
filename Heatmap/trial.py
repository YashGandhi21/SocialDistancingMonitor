#from scipy import stats, integrate
import numpy as np
import matplotlib.pyplot as plt

def ScatterPlot(x,y):
    plt.xlim(min(x) - 10, max(x) + 10)
    plt.ylim(min(y) - 10, max(y) + 10)
    plt.axis('on')
    plt.plot(x, y, 'ro')
    plt.xlabel('X_MESH')
    plt.ylabel('Y_MESH')
    plt.savefig('kde1.png')
    plt.show()

# load the coordinates file
x = [10, 20, 30, 15, 30, 20, 30, 10, 27, 15, 20, 5, 30, 16]
y = [10, 20, 30, 15, 25, 10, 5, 30, 27, 13, 40, 40, 27.5, 14]
ScatterPlot(x,y)
