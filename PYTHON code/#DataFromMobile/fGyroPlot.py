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

st = 30
sp = 30

# # creating lists for displacements
# dispX = [0]
# dispY = [0]
# dispZ = [0]

time0 = data[st, 0]

# # creating aX aY aZ lists
# aX = data[st : len(data) - sp, 14]
# aX -= 0.0021751054852320677
# aY = data[st : len(data) - sp, 15]
# aY -= 0.00129957805907173
# aZ = data[st : len(data) - sp, 16]
# aZ -= 0.0005218002812939522
# print

# creating time arr
time = data[st : len(data) - sp, 0]
time = (time - time0)

# creating arr for gyro
gRawX = data[st : len(data) - sp, 6]
gRawY = data[st : len(data) - sp, 7]
gRawZ = data[st : len(data) - sp, 8]

# ramp-speed - play with this value until satisfied
kFilteringFactor = 0.33

# last result storage - keep definition outside of this function, eg. in wrapping object
gyros = [0.0, 0.0, 0.0]

# filtered Gyro data
fGyroX = []
fGyroY = []
fgyroZ = []

for i in range(0, len(data) - (sp+st)):
    gyros[0] = gRawX[i] * kFilteringFactor + gyros[0] * (1.0 - kFilteringFactor)
    gyros[1] = gRawY[i] * kFilteringFactor + gyros[1] * (1.0 - kFilteringFactor)
    gyros[2] = gRawZ[i] * kFilteringFactor + gyros[2] * (1.0 - kFilteringFactor)
    fGyroX.append(gRawX[i] - gyros[0])
    fGyroY.append(gRawY[i] - gyros[1])
    fgyroZ.append(gRawZ[i] - gyros[2])

# gX = []
# gY = []
# gZ = []

# for i in range(len(data) - (st + sp)):
#     gX.append(simps(fGyroX[0:i + 1], time[0 : i + 1]))
#     gY.append(simps(fGyroY[0:i + 1], time[0 : i + 1]))
#     gZ.append(simps(fgyroZ[0:i + 1], time[0 : i + 1]))

import matplotlib as mpl
import matplotlib.pyplot as plt

figAccX = plt.figure(1)
plt.plot(time, gRawX, 'ro',
        time, fGyroX, 'b--')
plt.xlabel('TIME')
plt.ylabel('GYRO FILTERED X in Blue')
figAccX.show()

figAccY = plt.figure(2)
plt.plot(time, gRawY, 'ro',
        time, fGyroY, 'b--')
plt.xlabel('TIME')
plt.ylabel('GYRO FILTERED Y in Blue')
figAccY.show()

figAccZ = plt.figure(3)
plt.plot(time, gRawZ, 'ro',
        time, fgyroZ, 'b--')
plt.xlabel('TIME')
plt.ylabel('GYRO FILTERED Z in Blue')
figAccZ.show()

plt.show()