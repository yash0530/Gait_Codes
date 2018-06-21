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
# creating lists for displacements
dispX = [0]
dispY = [0]
dispZ = [0]

time0 = data[st, 0]

# creating aX aY aZ lists
aX = data[st : len(data) - sp, 14]
aY = data[st : len(data) - sp, 15]
aZ = data[st : len(data) - sp, 16]

# creating time arr
time = data[st : len(data) - sp, 0]
time = (time - time0)

#----------------------------Filtering Acceleromter Raw Output---------------------------------#

from pykalman import KalmanFilter

AccX = np.array([list(a) for a in zip(aX, time)])

initial_state_mean_X = [AccX[0, 0],
                      0,
                      AccX[0, 1],
                      0]

transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_X)
kf1 = kf1.em(AccX, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(AccX)

kf2 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_X,
                  observation_covariance = 10*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])
kf2 = kf2.em(AccX, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf2.smooth(AccX)
fAccX = smoothed_state_means[:, 0]

AccY = np.array([list(a) for a in zip(aY, time)])

initial_state_mean_Y = [AccY[0, 0],
                      0,
                      AccY[0, 1],
                      0]

transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]

kf3 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Y)
kf3 = kf3.em(AccY, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf3.smooth(AccY)

kf4 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Y,
                  observation_covariance = 10*kf3.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])
kf4 = kf4.em(AccY, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf4.smooth(AccY)
fAccY = smoothed_state_means[:, 0]

AccZ = np.array([list(a) for a in zip(aZ, time)])

initial_state_mean_Z = [AccZ[0, 0],
                      0,
                      AccZ[0, 1],
                      0]

transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]                      

kf5 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Z)
kf5 = kf5.em(AccZ, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf5.smooth(AccZ)

kf6 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Z,
                  observation_covariance = 10*kf5.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])
kf6 = kf6.em(AccZ, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf6.smooth(AccZ)
fAccZ = smoothed_state_means[:, 0]

#----------------------------------------------------------------------------------------------#

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
    x = fAccX[i]
    fAccX[i] = fAccX[i] * cos(gX[i])
    # print "AX: " + str(fAccX[i] - x)

    gY.append(simps(gRawY[0:i + 1], time[0 : i + 1]))
    y = fAccY[i]
    fAccY[i] = fAccY[i] * cos(gY[i])
    # print "AY: " + str(fAccY[i] - y)

    gZ.append(simps(gRawZ[0:i + 1], time[0 : i + 1]))
    z = fAccZ[i]
    fAccZ[i] = fAccZ[i] * cos(gZ[i])
    # print "AZ: " + str(fAccZ[i] - z)

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
