# importing libraries
from scipy.integrate import simps
import pprint as pp
from math import cos
import numpy as np
import csv
import sys

filename = sys.argv[1]
data = []
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)

l = len(data)
i = 0
for _ in range(l):
    if len(data[i]) < 17 or data[i][15] == '':
        data.remove(data[i])
        i -= 1
    i += 1


for i in range(len(data)):
    for j in range(17):
        data[i][j] = float(data[i][j])
data = np.array(data)


#-----------------------------------------Data Pre-Processing---------------------------------------#
k = 0.05
for _ in range (10):
    st = 0
    sp = 0
    # creating lists for displacements
    dispX = [0]
    dispY = [0]
    dispZ = [0]

    time0 = data[st, 0]

    # creating aX aY aZ lists
    aX = data[st : len(data) - sp, 14]
    aY = data[st : len(data) - sp, 15]
    aZ = data[st : len(data) - sp, 16]

    # creating arr for gyro
    gRawX = data[st : len(data) - sp, 6]
    gRawY = data[st : len(data) - sp, 7]
    gRawZ = data[st : len(data) - sp, 8]

    # creating time arr
    time = data[st : len(data) - sp, 0]
    time = (time - time0)

    #----------------------------Filtering Acceleromter and Gyroscope Raw Output---------------------------------#

    # ramp-speed - play with this value until satisfied
    kFilteringFactor = k
    k += 0.05

    # last result storage - keep definition outside of this function, eg. in wrapping object
    accel = [0.0, 0.0, 0.0]
    gyros = [0.0, 0.0, 0.0]

    # filtered Accelerations
    fAccX = []
    fAccY = []
    fAccZ = []

    # filtered Gyro data
    fGyroX = []
    fGyroY = []
    fgyroZ = []

    for i in range(0, len(data) - (sp+st)):
        accel[0] = aX[i] * kFilteringFactor + accel[0] * (1.0 - kFilteringFactor)
        accel[1] = aY[i] * kFilteringFactor + accel[1] * (1.0 - kFilteringFactor)
        accel[2] = aZ[i] * kFilteringFactor + accel[2] * (1.0 - kFilteringFactor)
        fAccX.append(aX[i] - accel[0])
        fAccY.append(aY[i] - accel[1])
        fAccZ.append(aZ[i] - accel[2])

        gyros[0] = gRawX[i] * kFilteringFactor + gyros[0] * (1.0 - kFilteringFactor)
        gyros[1] = gRawY[i] * kFilteringFactor + gyros[1] * (1.0 - kFilteringFactor)
        gyros[2] = gRawZ[i] * kFilteringFactor + gyros[2] * (1.0 - kFilteringFactor)
        fGyroX.append(gRawX[i] - gyros[0])
        fGyroY.append(gRawY[i] - gyros[1])
        fgyroZ.append(gRawZ[i] - gyros[2])

    gX = []
    gY = []
    gZ = []

    j = 1
    for i in range(len(data) - (st + sp)):
        gX.append(simps(fGyroX[0:i + 1], time[0 : i + 1]))
        x = aX[i]
        fAccX[i] = fAccX[i] * cos(gX[i])
        # print "Ax: " + str(aX[i] - x)

        gY.append(simps(fGyroY[0:i + 1], time[0 : i + 1]))
        y = aY[i]
        fAccY[i] = fAccY[i] * cos(gY[i])
        # print "Ay: " + str(aY[i] - y)

        gZ.append(simps(fgyroZ[0:i + 1], time[0 : i + 1]))
        z = aZ[i]
        fAccZ[i] = fAccZ[i] * cos(gZ[i])
        # print "Az: " + str(aZ[i] - z)

    velX = [simps(fAccX[0:1], time[0:1])]
    velY = [simps(fAccY[0:1], time[0:1])]
    velZ = [simps(fAccZ[0:1], time[0:1])]

    for i in range(1, len(data) - (st + sp)):
        velX.append(simps(fAccX[0:i + 1], time[0 : i + 1]))
        x = simps(velX[0:i + 1], time[0 : i + 1])
        dispX.append(x)

        velY.append(simps(fAccY[0:i + 1], time[0 : i + 1]))
        y = simps(velY[0:i + 1], time[0 : i + 1])
        dispY.append(y)

        velZ.append(simps(fAccZ[0:i + 1], time[0 : i + 1]))
        z = simps(velZ[0:i + 1], time[0 : i + 1])
        dispZ.append(z)


    #---------------------------------------Plotting Data-------------------------------------------#

    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure(_)
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    dispX = np.array(dispX)
    dispY = np.array(dispY)
    dispZ = np.array(dispZ)

    max_range = np.array([dispX.max() - dispX.min(), dispY.max() - dispY.min(), dispZ.max() - dispZ.min()]).max() / 2.0
    mid_x = (dispX.max() + dispX.min()) * 0.5
    mid_y = (dispY.max() + dispY.min()) * 0.5
    mid_z = (dispZ.max() + dispZ.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)


    ax.plot(dispX, dispY, dispZ)
    ax.legend()

    plt.xlabel('X axis')
    plt.ylabel('Y axis')

plt.show()
