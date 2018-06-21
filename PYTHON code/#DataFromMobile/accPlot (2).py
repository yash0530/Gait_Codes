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

#---------------------------------------Plotting Data-------------------------------------------#

import matplotlib as mpl
import matplotlib.pyplot as plt

figAccX = plt.figure(1)
plt.plot(time, aX)
plt.xlabel('TIME')
plt.ylabel('Acc X')
figAccX.show()

figAccY = plt.figure(2)
plt.plot(time, aY)
plt.xlabel('TIME')
plt.ylabel('Acc Y')
figAccY.show()

figAccZ = plt.figure(3)
plt.plot(time, aZ)
plt.xlabel('TIME')
plt.ylabel('Acc Z')
figAccZ.show()

plt.show()