# import the MySQLdb and sys modules
import MySQLdb
import sys

# open a database connection
db = MySQLdb.connect(host = "localhost", user = "yash", passwd = "qwerty123", db = "test")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query
cursor.execute ("SELECT * FROM `imu_readings`;")

# fetch all of the rows from the query
data = cursor.fetchall()

# writing the data-set to database.txt file\
from pprint import pprint
with open('data.txt', 'wt') as out:
    pprint(data, stream=out)

# close the cursor object
cursor.close()

# close the connection
db.close()

# exit the program
sys.exit()