#>>> msg='79.181.9.160'
#>>> msg
#'79.181.9.160'
#>>> newstr = msg.replace(".", "P")
#>>> newstr
#'79P181P9P160'
#>>> encryptMessage(newstr)
#'bdT5c5TdT5a4'
#>>> decryptMessage('bdT5c5TdT5a4')
#'79P181P9P160'
#>>> newstr = msg.replace("P", ".")
#>>> newstr
#'79.181.9.160'
#>>> 

# Caesar Cipher Encryption and Decryption
import datetime

dayOfMonth = datetime.datetime.now()

def encryptMessage(message):
	message = message
	key = dayOfMonth.day
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
			translated = translated + letters[myval]
		else:
			translated = translated + m	
	return translated
	
