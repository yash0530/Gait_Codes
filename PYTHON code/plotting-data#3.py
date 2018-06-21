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


#-----------------------------------------Data Pre-Processing---------------------------------------#

# importing libraries
import sympy
import numpy as np

# creating lists for displacements
dispX = []
dispY = []
dispZ = []

data = np.array(data)
time0 = data[0, -1]

# creating aX aY aZ lists
aX = data[:, 1]
aY = data[:, 2]
aZ = data[:, 3]

# creating time arr
time = data[:, -1]
time = np.array(time)
time = (time - time0) * 0.001

# creating functions for aX aY aZ
t = sympy.symbols('t')
interpolatedAccX = sympy.interpolating_poly(5, t, time, aX)
interpolatedAccY = sympy.interpolating_poly(12, t, time, aY)
interpolatedAccZ = sympy.interpolating_poly(25, t, time, aZ)

# creating functions for calculating disp
def fDispX(tX):
    return sympy.integrate(interpolatedAccX, (t, 0, t), (t, 0, tX))
def fDispY(tY):
    return sympy.integrate(interpolatedAccY, (t, 0, t), (t, 0, tY))
def fDispZ(tZ):
    return sympy.integrate(interpolatedAccZ, (t, 0, t), (t, 0, tZ))


i = 0
# populating the displacements lists
for T in time:
    dispX.append(fDispX(T))
    dispY.append(fDispY(T))
    dispZ.append(fDispZ(T))
    print i
    i += 1


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