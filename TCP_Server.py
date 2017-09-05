#
# TCP Server
#
from socket import *
import binascii
import threading



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

#This takes in a frame in binary and takes the header and then the payload.
#It then returns a set with 3 elements, 1st = frame number, 2nd = No. Frames, 3rd = payload in a string
#It also calls th CRC function and compares the result with the checksum
def convert_frame_into_readable(s ,gremlin_count):

	#Splits the frame into bytes
	data = split_str_into_len(s, 8)
	
	
	#Takes out the data from the header
	frame_number = int(data[0], 2)
	number_of_frames = int(data[1], 2)

	#Take the payload and put it into a set of 8 bytes
	payload = [data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]]
	
	#Gremlin Function
	
	if (frame_number == 124) :
		if gremlin_count != 0:
		
			payload = [data[4], data[3], data[4], data[5], data[5], data[2], data[4]]
			
		   
	
	#Take out the CRC checksum form the trailer
	checksum = [data[10],data[11]]
	checksum = ''.join(checksum)
	checksum = checksum[0:16]
	
	
	#Finding the ACK
	ACK = [data[12], data[13]]
	ACK = ''.join(ACK)
	
	payload_check = ''.join(payload)
	CRC_from_function = CRC(payload_check)

	
	if (CRC_from_function == checksum):
		print('CRC correct')
	else:
		print('CRC Error')
		error = 'ERROR'
		broken_frame = [frame_number, number_of_frames, error, '0000']
		return broken_frame
		
	#Convert each byte into its ascii char
	for x in range(0,8):
		payload[x] = ''.join(chr(int(payload[x], 2)))
	
	#Join the payload set into one string
	payload = ''.join(payload)

	#Set of the data in the frame which has been sorted
	converted_frame = [frame_number, number_of_frames, payload, ACK]

	return converted_frame
	

f = open("Output_data.txt", "a")	
	
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print 'The server is ready to receive'


	


while True:
	connectionSocket, addr = serverSocket.accept()
	gremlin_count = 2
	while True:
		sentence = connectionSocket.recv(12288)
		if not sentence:
			break
		
		Converted_frame = convert_frame_into_readable(sentence, gremlin_count)
		print "Frame %d of %d.\nPayload: %s." % (Converted_frame[0] + 1, Converted_frame[1], Converted_frame[2])
		

		if Converted_frame[3] != '0000': 
			f.write(str(Converted_frame[2]))
			connectionSocket.send(Converted_frame[3])
			print "Ack for %d sent.\n" % (Converted_frame[0]+1)
		else:
			print "Bad frame recieved.\n"
			connectionSocket.send(Converted_frame[3])
			gremlin_count = gremlin_count-1	
			

		if (Converted_frame[0]+1) == (Converted_frame[1]):
			break
	print 'Data recieved written to "Output_data.txt".'
	f.close()	
	connectionSocket.close()
	
	












