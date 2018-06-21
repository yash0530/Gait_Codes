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
sp = 0

time0 = data[0][0]
# creating aX aY aZ lists
aX = data[st : len(data) - sp, 14]
aY = data[st : len(data) - sp, 15]
aZ = data[st : len(data) - sp, 16]

# creating time arr
time = data[st : len(data) - sp, 0]
time = (time - time0)

#----------------------------Filtering Acceleromter Raw Output---------------------------------#

# ramp-speed - play with this value until satisfied
kFilteringFactor = 0.33

# last result storage - keep definition outside of this function, eg. in wrapping object
accel = [0.0, 0.0, 0.0]

# filtered Accelerations
fAccX = []
fAccY = []
fAccZ = []

for i in range(0, len(data) - (sp+st)):
    accel[0] = aX[i] * kFilteringFactor + accel[0] * (1.0 - kFilteringFactor)
    accel[1] = aY[i] * kFilteringFactor + accel[1] * (1.0 - kFilteringFactor)
    accel[2] = aZ[i] * kFilteringFactor + accel[2] * (1.0 - kFilteringFactor)
    fAccX.append(aX[i] - accel[0])
    fAccY.append(aY[i] - accel[1])
    fAccZ.append(aZ[i] - accel[2])

#------------------------------------- --Plotting Data-------------------------------------------#

import matplotlib as mpl
import matplotlib.pyplot as plt

figAccX = plt.figure(1)
plt.plot(time, aX, 'ro',
        time, fAccX, 'b--')
plt.xlabel('TIME')
plt.ylabel('Acc X')
figAccX.show()

figAccY = plt.figure(2)
plt.plot(time, aY, 'ro',
        time, fAccY, 'b--')
plt.xlabel('TIME')
plt.ylabel('Acc Y')
figAccY.show()

figAccZ = plt.figure(3)
plt.plot(time, aZ, 'ro',
        time, fAccZ, 'b--')
plt.xlabel('TIME')
plt.ylabel('Acc Z')
figAccZ.show()

plt.show()
