#-----------------------------------------Fetching Data----------------------------------------------#

# import the MySQLdb and sys modules
import MySQLdb
import sys

# open a database connection
db = MySQLdb.connect(host = "localhost", user = "yash", passwd = "qwerty123", db = "test")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query
cursor.execute("SELECT * FROM `imu_readings`")

# fetch all of the rows from query
data = cursor.fetchall()


#-----------------------------------------Data Pre Processing---------------------------------------#

# importing libraries
from scipy.integrate import dblquad
from scipy import interpolate as inp
import numpy as np

# creating aX aY aZ lists
data = np.array(data)
aX = data[:, 1]
aY = data[:, 2]
aZ = data[:, 3]

# creating time arr
time = data[:, -1]
time = np.array(time)
time = (time - time0) * 0.001

# creating lists for displacements
dispX = []
dispY = []
dispZ = []

# creating functions for aX aY aZ
interpolatedAccX = inp.interp1d(time, aX, kind='cubic')
interpolatedAccY = inp.interp1d(time, aY, kind='cubic')
interpolatedAccZ = inp.interp1d(time, aZ, kind='cubic')

def accX(t1, t2):
    return interpolatedAccX(t1)
def accY(t1, t2):
    return interpolatedAccY(t1)
def accZ(t1, t2):
    return interpolatedAccZ(t1)


# creating functions for calculating disp
def fDispX(t):
    return dblquad(accX, 0, t, lambda t1: 0, lambda t1: t1)
def fDispY(t):
    return dblquad(accY, 0, t, lambda t1: 0, lambda t1: t1)
def fDispZ(t):
    return dblquad(accZ, 0, t, lambda t1: 0, lambda t1: t1)


# populating the displacements lists
for t in time:
    dispX.append(fDispX(t)[0])
    dispY.append(fDispY(t)[0])
    dispZ.append(fDispZ(t)[0])


#---------------------------------------Plotting Data-------------------------------------------#

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(dispX, dispY, dispZ)
ax.legend()
plt.show()


#--------------------------------------Closing Connection---------------------------------------#

# close the cursor object
cursor.close()

# close the connection
db.close()

# exit the program
sys.exit()