#	Donal Tuohy
#	3D3 Computer Networks
#	Project 1
#	Program to create the input data


from random import randint

f = open("Input_data.txt", "w+")



for i in range(0,1024):

	Number =   randint(48,57)	#Numeric Values
	UpLetter = randint(65,90)	#Uppercase Alphabet
	LowLetter = randint(97,122)	#Lowercase Alphabet

	Selection_Int = randint(0,2)

	if Selection_Int == 0:
		f.write(str(chr(Number)))
	elif Selection_Int == 1:
		f.write(str(chr(UpLetter)))
	elif Selection_Int == 2:
		f.write(str(chr(LowLetter)))

f.close
