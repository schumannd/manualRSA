#!/usr/bin/python
import random
import sys
import cProfile
from random import shuffle
from copy import copy
from fractions import gcd


def main():
	if len(sys.argv) < 3:
		writeUsageInfo()
	elif sys.argv[1] == "-key":
		encryptAndGenerateKey(readParameterFile(3), int(sys.argv[2]))
	elif sys.argv[1] == "-d":
		decrypt(readParameterFile(2), long(readParameterFile(3)), long(readParameterFile(4)))
	elif sys.argv[1] == "-e":
		encrypt(readParameterFile(2), readParameterFile(3), readParameterFile(4))
	else:
		writeUsageInfo()
def writeUsageInfo():
	print """
		create key and encrypt:
		python manualRSA.py -key [keySize] [/path/to/clearTextFile]

		decryption:
		python manualRSA.py -d [/path/to/cypherFile] [/path/to/privateKeyD] [/path/to/publicKeyN]

		encrypt with existing key:
		python manualRSA.py -e [/path/to/clearTextFile] [/path/to/publicKeyE] [/path/to/publicKeyN]
		"""

def encryptAndGenerateKey(text, bitsize):
	keyPair = createRSAKeyPair(bitsize)
	writeKeysToFile(keyPair)
	encrypt(text, keyPair[1], keyPair[0])

def encrypt(text, e, n):
	cypher = applyEncryption(text, e, n)
	f = open("cypher.txt",'w')
	f.write(cypher)

def decrypt(cypher, d, n):
	clearText = applyDecryption(cypher, d, n)
	f = open("clearText.txt",'w')
	f.write(clearText)

def applyEncryption(text, e, n):
	cypher = ""
	for char in text:
		cypher += str(pow(ord(char), e, n))+"\n"
	return cypher

def applyDecryption(cypher, d, n):
	clearText = ""
	for number in cypher.strip().split('\n'):
		num = long(number)
		clearText += chr(pow(num, d, n))
	return clearText

########## Prime calculation helper

def fermat(n, security):
	if n < 4:
		return False
	for i in range(security):
		a = random.randrange(2,n-1)
		if not pow(a, n-1, n) == 1:
			return False
	return True
# def millerRabinForBigNumbers(n):
# 	d = n-1
# 	while d % 2 == 0:
# 		d /= 2

# 	for i in range(5):
# 		a = random.randint(1, n-1)
# 		r = d
# 		x = pow(a,r,n)
# 		while (r != n-1 and x != 1 and x != n-1):
# 			x = (x * x) % N
# 			r *= 2

# 		if (x != n-1 and r % 2 == 0):
# 			return False
# 	return True

def pulverizer(a, b): # a > b
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b != 0:
    	q, r = a//b, a%b
    	x, y = x2 - q*x1, y2 - q*y1
    	a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y
    return a, x2, y2

def modularInverse(e, phi):
    g, x, y = pulverizer(e, phi)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % phi

def createPrimeOfSize(bitSize):
	primeToBe = 4
	while not fermat(primeToBe, 10):
		primeToBe = random.getrandbits(bitSize)
	return primeToBe

def createRSAKeyPair(bitSize):
	p = createPrimeOfSize(bitSize/2)
	q = createPrimeOfSize(bitSize/2)
	n = p * q
	phi = (p - 1) * (q - 1)
	e = coprimeTo(phi)
	d = modularInverse(e, phi)
	return [n, e, d]

def coprimeTo(num):
	while True:
		z = random.randrange(2, num)
		if gcd(z, num) == 1:
			return z

###########  IO helper 

def writeKeysToFile(keyPair):
	f = open('pubkeyN.txt','w')
	f.write(str(keyPair[0]))
	f = open('pubkeyE.txt','w')
	f.write(str(keyPair[1]))
	f = open('privkeyD.txt','w')
	f.write(str(keyPair[2]))

def readParameterFile(num):
	with open(sys.argv[num], "r") as textFile:
		return textFile.read()
##########################
if __name__ == "__main__":
	sys.exit(main())