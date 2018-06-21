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
fAX = smoothed_state_means[:, 0]

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

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Y)
kf1 = kf1.em(AccY, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(AccY)

kf2 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Y,
                  observation_covariance = 10*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])
kf2 = kf2.em(AccY, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf2.smooth(AccY)
fAY = smoothed_state_means[:, 0]

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

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Z)
kf1 = kf1.em(AccZ, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(AccZ)

kf2 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean_Z,
                  observation_covariance = 10*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])
kf2 = kf2.em(AccZ, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf2.smooth(AccZ)
fAZ = smoothed_state_means[:, 0]

#-------------------------Plotting Data-------------------------------------------#

import matplotlib as mpl
import matplotlib.pyplot as plt

figX = plt.figure(1)
plt.plot(time, aX, 'ro',
        time, fAX, 'b--')
plt.xlabel("TIME")
plt.ylabel("KALMAN FILTERED ACC X in Blue")
figX.show()

figY = plt.figure(2)
plt.plot(time, aY, 'ro',
        time, fAY, 'b--')
plt.xlabel("TIME")
plt.ylabel("KALMAN FILTERED ACC Y in Blue")
figY.show()

figZ = plt.figure(3)
plt.plot(time, aZ, 'ro',
        time, fAZ, 'b--')
plt.xlabel("TIME")
plt.ylabel("KALMAN FILTERED ACC Z in Blue")
figZ.show()

plt.show()