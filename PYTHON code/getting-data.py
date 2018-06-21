# import the MySQLdb and sys modules
import MySQLdb
import sys

rows_prev = 0
while True:

    # open a database connection
    db = MySQLdb.connect (host = "localhost", user = "yash", passwd = "qwerty123", db = "test")

    # prepare a cursor object using cursor() method
    cursor = db.cursor ()

    rows = cursor.execute("SELECT * FROM `imu_readings`")
    if rows_prev != rows:
        print str(rows) + "\n\n"
    rows_prev = rows

# close the cursor object
cursor.close ()

# close the connection
db.close ()

# exit the program
sys.exit()