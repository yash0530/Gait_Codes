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

st = 0
sp = 20
# creating lists for displacements
dispX = [0]
dispY = [0]
dispZ = [0]

time0 = data[st, 0]

# creating aX aY aZ lists
aX = data[st : len(data) - sp, 14]
aX -= 0.0021751054852320677
aY = data[st : len(data) - sp, 15]
aY -= 0.00129957805907173
aZ = data[st : len(data) - sp, 16]
aZ -= 0.0005218002812939522
print

# creating time arr
time = data[st : len(data) - sp, 0]
time = (time - time0)

# creating arr for gyro
gRawX = data[st : len(data) - sp, 6]
gRawY = data[st : len(data) - sp, 7]
gRawZ = data[st : len(data) - sp, 8]

gX = []
gY = []
gZ = []

j = 1
for i in range(len(data) - (st + sp)):
    gX.append(simps(gRawX[0:i + 1], time[0 : i + 1]))
    x = aX[i]
    aX[i] = aX[i] * cos(gX[i])
    # print "Ax: " + str(aX[i] - x)

    gY.append(simps(gRawY[0:i + 1], time[0 : i + 1]))
    y = aY[i]
    aY[i] = aY[i] * cos(gY[i])
    # print "Ay: " + str(aY[i] - y)

    gZ.append(simps(gRawZ[0:i + 1], time[0 : i + 1]))
    z = aZ[i]
    aZ[i] = aZ[i] * cos(gZ[i])
    # print "Az: " + str(aZ[i] - z)

velX = [0]
velY = [0]
velZ = [0]

aX[0] = 0
aY[0] = 0
aZ[0] = 0

for i in range(1, len(data) - (st + sp)):
    velX.append(simps(aX[0:i + 1], time[0 : i + 1]))
    x = simps(velX[0:i + 1], time[0 : i + 1])
    dispX.append(x)

    velY.append(simps(aY[0:i + 1], time[0 : i + 1]))
    y = simps(velY[0:i + 1], time[0 : i + 1])
    dispY.append(y)

    velZ.append(simps(aZ[0:i + 1], time[0 : i + 1]))
    z = simps(velZ[0:i + 1], time[0 : i + 1])
    dispZ.append(z)


#---------------------------------------Plotting Data-------------------------------------------#

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
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
