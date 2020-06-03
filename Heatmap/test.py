from new import HeatMapAuto
from new import HeatMapAutoNext
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

for i in range(5):
    i=i*10
    list1=[(764+i,90+i),(620+i,103+i),(707+i,262+i)]
    print(i)
    if i==0:
        plt1=HeatMapAuto(list1)
        plt1.show()
    else:
        plt1=HeatMapAutoNext(list1,plt1)
        plt1.pause(0.1)
        plt1.show()
