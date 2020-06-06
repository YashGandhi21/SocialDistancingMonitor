from HeatmapModule import HeatMapAuto
import numpy as np
import matplotlib.pyplot as plt
import cv2
import io
from PIL import Image
from matplotlib.animation import FuncAnimation

for i in range(5):
    i=i*10
    list1=[(764+i,90+i),(620+i,103+i),(707+i,262+i)]

    plt=HeatMapAuto(list1)
    #print(fig)
    #plt.show(block=False)
    fig1 = plt.gcf()
    plt.show(block=False)
    #plt.draw()
    #fig1.savefig('tessstttyyy.png', dpi=100)
    plt.pause(0.75)
    plt.close()

def get_img_from_fig(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img_np_array = cv2.imdecode(img_arr, 1)
    img_np_array = cv2.cvtColor(img_np_array, cv2.COLOR_BGR2RGB)

    #Here we return the Image as numpy array
    return img_np_array



def numpy2pil(np_array: np.ndarray) -> Image:
    """
    Convert an HxWx3 numpy array into an RGB Image

    """
    img = Image.fromarray(np_array, 'RGB')
    return img

# Just trying for the last frame to get image from the numpy array
# plot_img_np = get_img_from_fig(fig1)
# #np.set_printoptions(threshold=np.inf)
# #print(plot_img_np)
# #print(type(plot_img_np))
# img = numpy2pil(plot_img_np)
# img.show()
