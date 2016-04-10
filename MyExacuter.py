import ipgetter
import socket
import paho.mqtt.publish as publish
import datetime


now = datetime.datetime.now()
day = now.day


'''
Main Function - runs an enfinite loop publishing my local and global ip address.
'''
def Main():
    pubIp()
    curr=getAddress()
    while True:
        if curr != getAddress():
            pub()
            curr=getAddress()



'''
publishing a single (encrypted) message to the broker.
'''
def pubIp():
    #payload = getAddress()
    encPayload = encryptMessage(getAddress())
    publish.single("babykeeper/Rasp_Ip",encPayload, hostname="broker.mqttdashboard.com")

'''
getting my local and global ip address.
'''
def getAddress():
        
    # global ip address of device
    globalIp = ipgetter.myip()

    # local ip address of device
    localIp = socket.gethostbyname(socket.gethostname())

    output = 'Global_IP:'+globalIp+'//'+'Local_Ip:'+localIp
    return output

'''
encrypting a message by Cesar Cipher method with a uniqe key.
'''
def encryptMessage(message):
	message = message
	key = day
	letters = "8&YC9ZvMaxP@wOz|%*sf3QN0G/cp+U5$>gDorLmhE1l#eJ,*yWbdB_2KV(n=i?HSuX^{TI4;jq}'FA[:).t!<kR]67"
	letterslen = len(letters)
	translated = ""
	for m in message:
		if m in letters:
			myval = letters.find(m)
			myval = myval+key
		
			if myval >= letterslen:
				myval = myval-letterslen
			elif myval < 0:
				myval = myval+letterslen
			translated +=  letters[myval]
		else:
			translated +=  m	
	return translated



if __name__ == '__main__':
    Main()
