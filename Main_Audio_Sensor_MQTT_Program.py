import sys
import pyaudio
import math
import struct
import time
import paho.mqtt.publish as publish

# Instantiate PyAudio
p = pyaudio.PyAudio()

# output file
#file = open("out.txt","w")

HOSTNAME = "test.mosquitto.org"
PORT = 1883

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
	if s > 60:
		publish.single("babykeeper/sound" ,s ,0 ,False ,HOSTNAME ,PORT)
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
