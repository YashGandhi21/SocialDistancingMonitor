import matplotlib.pyplot as plt
import numpy as np
import math

#POINT DATASET / PEOPLE COORDINATES
#x=[20,28,15,20,18,25,15,18,18,20,25,30,25,22,30,22,38,40,38,30,22,20,35,33,35]
#y=[20,14,15,20,15,20,32,33,45,50,20,20,20,25,30,38,20,28,33,50,48,40,30,35,36]


def HeatMapModule(x,y):
    #DEFINE GRID SIZE AND RADIUS(h)
    grid_size=1
    h=10
    #h is the bandwidth/ the radius of the kernel

    #GETTING X,Y MIN AND MAX to IDENTIFY THE VALID RANGE OF INPUT CO-ORDINATES
    x_min=min(x)
    x_max=max(x)
    y_min=min(y)
    y_max=max(y)
    print(x_min," ",x_max," ",y_min," ",y_max," ")

    #CONSTRUCT MESH GRID
    x_grid=np.arange(x_min-h,x_max+h,grid_size)
    y_grid=np.arange(y_min-h,y_max+h,grid_size)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)
    print("x_grid ",x_grid)
    print()
    print("y_grid ",y_grid)
    print()
    print("Shape of x_mesh :",x_mesh.shape)

    print()
    print("x_mesh ",x_mesh)
    print()
    print("Shape of y_mesh :",y_mesh.shape)


    print()
    print("y_mesh ", y_mesh)

    # GRID CENTER POINT - EACH MESH CELL CENTER POINT IS CREATED.
    # THIS TERMINOLOGY ACTS AS A POINT OF OF REFERENCE TO THE RESPECTIVE CO-ORDINATES OVER THE PLANE OF REFERENCE
    xc = x_mesh + (grid_size / 2)
    yc = y_mesh + (grid_size / 2)


    # FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
    def kde_quartic(d, h):
        dn = d / h
        P = (15 / 16) * (1 - dn ** 2) ** 2
        return P


    # PROCESSING

    # First loop is for mesh data list or grid
    # Second loop for each center point of those grids
    # Third loop to calculate the distance of the center point to each dataset point.
    # Here we only consider the point with a distance within the kernel radius.

    intensity_list = []
    for j in range(len(xc)):
        intensity_row = []
        for k in range(len(xc[0])):
            kde_value_list = []
            for i in range(len(x)):
                # CALCULATE DISTANCE
                d = math.sqrt((xc[j][k] - x[i]) ** 2 + (yc[j][k] - y[i]) ** 2)
                if d <= h:
                    p = kde_quartic(d, h)
                else:
                    p = 0
                kde_value_list.append(p)
            # SUM ALL INTENSITY VALUE
            p_total = sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    # HEATMAP OUTPUT
    intensity = np.array(intensity_list)
    print(intensity)

    # to show the heatmap along with the concerned points as person
    plt.pcolormesh(x_mesh, y_mesh, intensity)
    plot1 = plt.figure(1)
    plt.plot(x, y, 'ro')
    plt.xlabel('X_MESH')
    plt.ylabel('Y_MESH')
    plt.colorbar()
    plt.savefig('HeatmapWithPeopleCoordinates.png')

    # to show only the heatmap
    plot2 = plt.figure(2)
    plt.pcolormesh(x_mesh, y_mesh, intensity)
    plt.xlabel('X_MESH')
    plt.ylabel('Y_MESH')
    plt.savefig('HeatmapWithoutPeopleCoordinates.png')

    plt.show()


x=[10,20,30,15,30,20,30,10,27,15,20]
y=[10,20,30,15,25,10,5,30,27,13,40]
HeatMapModule(x,y)