import mysql.connector
import sys
import time
from raspberry_pi_unique_product_key import getRaspberryPiID

#table = "users_login"
#time = datetime
#value = temperature / humidity / sound value
#rpi_id = raspberry pi unique product key

MYSQL_HOST = ''
MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_DB = ''


# This function inserts received data into mysql database - Adjust parameters for your server
def insert_data(table,value):
    my_time = time.strftime('%Y-%m-%d %H:%M:%S')
    rpi_id = getRaspberryPiID()
    conn = mysql.connector.connect(
        host=MYSQL_HOST, # Enter your Mysql Server ip
        user=MYSQL_USERNAME, # Enter your mysql username
        password=MYSQL_PASSWORD, # Enter your mysql password
        database=MYSQL_DB)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO %s VALUES( '%s','%d','%s')"""
                   % (table,my_time,value,rpi_id))
    conn.commit()
    cursor.close()
    conn.close()
    #sys.exit()
    #exit()
    
