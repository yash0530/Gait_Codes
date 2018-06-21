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
    gX.append(simps(gRawX[0:i + 1], time[0 : i + 1]) * 180 / 3.1415926536)
    gY.append(simps(gRawY[0:i + 1], time[0 : i + 1]) * 180 / 3.1415926536)
    gZ.append(simps(gRawZ[0:i + 1], time[0 : i + 1]) * 180 / 3.1415926536)


import matplotlib as mpl
import matplotlib.pyplot as plt

plt.plot(time, gZ)

plt.xlabel('TIME')
plt.ylabel('GYRO INTEGRATED FILTERED Z')

plt.show()