'''

>>> msg='79.181.9.160'
>>> msg
'79.181.9.160'
>>> newstr = msg.replace(".", "P")
>>> newstr
'79P181P9P160'
>>> encryptMessage(newstr)
'bdT5c5TdT5a4'
>>> decryptMessage('bdT5c5TdT5a4')
'79P181P9P160'
>>> newstr = msg.replace("P", ".")
>>> newstr
'79.181.9.160'
>>> 

'''


# Caesar Cipher Encryption and Decryption
import datetime

dayOfMonth = datetime.datetime.now()

def encryptMessage(message):
	message = message
	key = dayOfMonth.day
	letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
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
			translated = translated + letters[myval]
		else:
			translated = translated + m	
	return translated
	
def decryptMessage(message):
	message = message
	key = dayOfMonth.day
	letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	letterslen = len(letters)
	translated = ""
	for m in message:
		if m in letters:
			myval = letters.find(m)
			myval = myval-key
		
			if myval >= letterslen:
				myval = myval-letterslen
			elif myval < 0:
				myval = myval+letterslen
			translated = translated + letters[myval]
		else:
			translated = translated + m	
	return translated
