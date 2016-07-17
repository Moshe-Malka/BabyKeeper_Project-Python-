#!/usr/bin/python

'''
this program gets your device local and global ip
and sends in via MQTT protocol every hour OR every time the ip changes
'''

# import suppurting libs    
import paho.mqtt.publish as publish
import ipgetter
import socket
import datetime
import time
from raspberry_pi_unique_product_key import getRaspberryPiID

HOSTNAME = "test.mosquitto.org"
PORT = 1883

'''
getting my local and global ip address.
'''
def getAddress():
    # global ip address of device
    globalIp = ipgetter.myip()
    # local ip address of device
    localIp = socket.gethostbyname(socket.gethostname())
    my_time = time.strftime('%Y-%m-%d %H:%M:%S')
    output = 'Global_IP:' + globalIp + '//Local_Ip:' + localIp + '//Time:' + my_time + '//Raspberry_Product_Key:' + getRaspberryPiID()
    return output

'''
publishing a single (encrypted) message to the broker with thee device IP.
'''
def pubIp():
    pubMsg('babykeeper/Ras_Pi', getAddress())
    #encPayload = encryptMessage(getAddress())
    #pubMsg('babykeeper/Ras_Pi', encPayload)

'''
publishing a single message to the broker.
'''
def pubMsg(topic, msg):
    publish.single(topic, msg, 0, False, HOSTNAME, PORT)


'''
encrypting a message using Ceaser Cypher and a unique key.
'''
def encryptMessage(message):
    key = 16   # give's '16' as a key.
    letters = "8&YC9ZvMaxP@wOz|%*sf3QN0G/cp+U5$>gDorLmhE1l#eJ,*yWbdB_2KV(n=i?HSuX^{TI4;jq}'FA[:).t!<kR]67"
    letterslen = len(letters)
    translated = ""
    for m in message:
        if m in letters:
            myval = letters.find(m)
            myval = myval + key

            if myval >= letterslen:
                myval -= letterslen
            elif myval < 0:
                myval += letterslen
            translated += letters[myval]
        else:
            translated += m
    return translated

def main():
    currentAddress = getAddress()
    currentHour = time.localtime()[3]
    pubIp()
    # main loop to check if address changed, and if so - publish them again.
    while True:
        if currentAddress != getAddress() or time.localtime()[3] != currentHour:
                pubIp()
                currentAddress = getAddress()
                currentHour = time.localtime()[3]

        #else: publish.single("babykeeper/Rasp_Ip","same Ip", hostname="broker.mqttdashboard.com")

if __name__ == "__main__":
    main()
    
