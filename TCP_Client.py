#
# TCP Client
#
from socket import *
from ctypes import *
import time

#CRC Correction function
def CRC(s):

	#Defining values needed to perform CRC
	generator = '10001000000100001'
	padding ='0000000000000000'
	padded_string_set = [s,padding]
	padded_string = ''.join(padded_string_set)
	
	generator_length = len(generator)
	input_length = len(padded_string)
	
	current = padded_string[0:generator_length-1]
	temp = split_str_into_len(current, 1)
	

	#print(padded_string)
	
	for i in range (0, input_length - generator_length):
	
		if current[0] == '1':
			current = int(current, 2) ^ int(generator, 2)
			current = '{0:0{1}b}'.format(current,generator_length)
			
		for x in range(0,generator_length-2):
			temp[x] = current[x+1]
		
		index = len(temp)-1 
		temp[index] = padded_string[i + generator_length]
		current = ''.join(temp)
		
	return current
	
	
#This breaks the string up into 8 chars
def split_str_into_len(s, l=2):
    """ Split a string into chunks of length l """
    return [s[i:i+l] for i in range(0, len(s), l)]


#######   MAIN PART    #######


#Setting up the socket
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#Opening the premade data file
f = open("Input_data.txt","r")
data = f.read()

#Using the function to split the file in to 8 byte strings
data = split_str_into_len(data, 8)
Number_of_frames = len(data)



for i in range(0, Number_of_frames-1):
	
	#print(data[i])

	
	#Converting each ascii char into 8 bit binary
	data[i] = (''.join('{0:08b}'.format(ord(x), 'b') for x in data[i]))
	
	#Making the ACK frame
	ACK_string = "00000110"
	ACK_num = '{0:08b}'.format(i)
	ACK = [ACK_string, ACK_num]
	ACK = ''.join(ACK)
	
	#Joining each part into a frame
	frame_string = ['{0:08b}'.format(i), '{0:08b}'.format(Number_of_frames -1), data[i], CRC(data[i]), ACK]
	Binary_frame = ''.join(frame_string)
	data[i] = Binary_frame
	print(Binary_frame)


for i in range(0, Number_of_frames-1):
	ACK_recieved = 0
	
	while ACK_recieved == 0:
		clientSocket.send(data[i])
		print "Frame %d sent" % (i +1)
		time.sleep(0.001)
		reply = clientSocket.recv(2048)
		reply = split_str_into_len(reply, 8)
		if reply[0] == '00000110':  
			ACK_recieved = 1 
			ACK_num = int(reply[1],2) +1
			print "ACK for frame %d recieved.\n" % (ACK_num)
		elif reply[0] == '0000':
			print"NAK for frame %d recieved.\n"% (ACK_num)
			clientSocket.send(data[i])
			ACK_recieved = 0
			
			
			
	
	
print 'Data sent to server.'

clientSocket.close()
