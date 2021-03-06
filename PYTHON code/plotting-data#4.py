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
dispX = [0]
dispY = [0]
dispZ = [0]

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

velX = [0]
velY = [0]
velZ = [0]

for i in range(1, len(data)):
    velX.append(aX[i-1]*(time[i] - time[i-1]) + velX[i-1])
    x = velX[i-1]*(time[i] - time[i-1]) + dispX[i-1]
    dispX.append(round(x, 3))

    velY.append(aY[i-1]*(time[i] - time[i-1]) + velY[i-1])
    y = velY[i-1]*(time[i] - time[i-1]) + dispY[i-1]
    dispY.append(round(y, 3))


    velZ.append(aZ[i-1]*(time[i] - time[i-1]) + velZ[i-1])
    z = velZ[i-1]*(time[i] - time[i-1]) + dispZ[i-1]
    dispZ.append(round(z, 3))

    print dispX[i]
    print dispY[i]
    print dispZ[i]
    print "\n\n"




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