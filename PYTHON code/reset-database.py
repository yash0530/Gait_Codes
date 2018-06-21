# import the MySQLdb and sys modules
import MySQLdb
import sys

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
db = MySQLdb.connect(host = "localhost", user = "yash", passwd = "qwerty123", db = "test")

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("DELETE FROM `imu_readings`;ALTER TABLE `imu_readings` DROP ID;ALTER TABLE `imu_readings` AUTO_INCREMENT = 1;ALTER TABLE `imu_readings` ADD ID int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")

# close the cursor object
cursor.close()

# close the connection
db.close()

sys.exit()