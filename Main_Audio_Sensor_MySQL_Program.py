import sys
import pyaudio
import math
import struct
import mysql.connector
import time
from raspberry_pi_unique_product_key import getRaspberryPiID

# MySQL Variables
MYSQL_HOST = 'sql7.freesqldatabase.com'
MYSQL_USERNAME = 'sql7118146'
MYSQL_PASSWORD = 'rmWVntI87f'
MYSQL_DB = 'sql7118146'

# Instantiate PyAudio
p = pyaudio.PyAudio()

# output file
#file = open("out.txt","w")

HOSTNAME = "test.mosquitto.org"
PORT = 1883

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

# Define callback
def callback(in_data, frame_count, time_info, status):
    floatLevels = []
    for _i in range(1024):
        floatLevels.append(struct.unpack('<h', in_data[_i:_i + 2])[0])
    avgChunk = sum(floatLevels)/len(floatLevels)
    print_audio_level(avgChunk, time_info['current_time'])
    return (in_data, pyaudio.paContinue)


time_difference = [0, 0]
def print_audio_level(in_data, callback_time):
    time_difference [1] = callback_time
    if time_difference [1] - time_difference [0] > 0.1:
    	time_difference [0] = time_difference [1]
        level = get_level_dB(in_data)
        sys.stdout.write('Audio level' + str(level) + '\r')
        sys.stdout.flush()

	s = abs(level)
        insert_data('sound_log',s)

	#file.write(str(s)+"\n")
	
	
def get_level_dB(sample_value):
    MAX_SAMPLE_VALUE = 32768
    try:
        level = (20 * math.log10(float(abs(sample_value)) / MAX_SAMPLE_VALUE))
    except ValueError:
        level = - 96.32
    return int(level)

# Open stream using callback
stream = p.open(format=pyaudio.paInt16,
                channels = 1,
                rate=48000,
		input_device_index=2,
                frames_per_buffer=1024,
                input=True,
                stream_callback=callback)

# Start the stream
stream.start_stream()

# endless loop          later on - wait for system event.
while True:
    time.sleep(1)


stream.stop_stream()
stream.close()
p.terminate()
file.close()
