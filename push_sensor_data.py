import mysql.connector
import sys
import time
from raspberry_pi_unique_product_key import getRaspberryPiID

#table = "users_login"
#time = datetime
#value = temperature / humidity / sound value
#rpi_id = raspberry pi unique product key 


# This function inserts received data into mysql database - Adjust parameters for your server
def insert_data(table,value):
    my_time = time.strftime('%Y-%m-%d %H:%M:%S')
    rpi_id = getRaspberryPiID()
    conn = mysql.connector.connect(
        host='sql7.freesqldatabase.com', # Enter your Mysql Server ip
        user='sql7118146', # Enter your mysql username
        password='rmWVntI87f', # Enter your mysql password
        database='sql7118146')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO %s VALUES( '%s','%d','%s')"""
                   % (table,my_time,value,rpi_id))
    conn.commit()
    cursor.close()
    conn.close()
    #sys.exit()
    #exit()

