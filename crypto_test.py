from Crypto.Cipher import AES
import re
key = "0vUby9sjVX47pEz99HXs3ZqQUIff7YD7"
message = "my name is moshe malka i like to hang out"
cipher = AES.new(key)


def pad(s):
    return s + ((16-len(s) % 16 ) * '{')
                
def encrypt(text):
    global cipher, key
    return cipher.encrypt(pad(text))

def decrypt(text):
    global cipher
    dec = cipher.decrypt(text).decode('utf-8')
    l = dec.count('{')
    x = dec[:len(dec)-1]
    y = re.sub('[{]',"",x)
    return y



def encrypMytMessage(msg):
    return encrypt(msg)


def decrypMytMessage(msg):
    return decrypt(msg)

print("Message:",message)
print("\n")
print("Encrypted:",encrypMytMessage(message))
print("\n")
print("Decrypted:",decrypMytMessage(encrypMytMessage(message)))
