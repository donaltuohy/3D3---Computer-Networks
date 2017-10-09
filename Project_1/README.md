<h1>A Data Link Protocol Simulation</h1>

<h2>The Client</h2>
<p>In the programs I have created, a string of 1024 alphanumeric characters is broken up into frames with 8 bytes of data. Each frame number is attached to the header along with the total number of frames. The payload data is run through a Cyclic Redundancy Check (CRC-16) and then the resulting checksum is appended to the end of the frame.
This frame is then sent as a binary string through the socket to the server. </p>

<h2>The Server</h2>  
<p>The server breaks the frame up into 8 byte segments. The payload is passed into the CRC function which is the same as client side and if no data was lost it will return a checksum equal to that of the checksum sent from the client. It then sends an acknowledgment to the client that it has received the frame. If the checksums do not equal, the server sends a negative acknowledgment.
The rest of the data is analysed so that the server can display what it has received.
</p>

<h2>Overall Process</h2>
<p>The first function I implemented was sending and receiving strings through the sockets. On the client side, the socket is called clientSocket and it's called serverSocket on serverSide. </p>
<p>To create the data, I wrote a python program called "data_creator.py" which selects 1024 random alphanumeric characters and writes them to a file called "Input_data.txt". </p>
<h3>data_creator.py</h3>

```python
from random import randint
f = open("Input_data.txt", "w+")
for i in range(0,1024):
	Selection_Int = randint(0,2)
	if Selection_Int == 0:
		f.write(str(chr(randint(48,57)))) #Numeric Characters
	elif Selection_Int == 1:
		f.write(str(chr(randint(65,90)))) #Uppercase Letters
	elif Selection_Int == 2:
		f.write(str(chr(randint(97,122)))) #Lowercase Letters
    f.close()
```

<p>Once this was working I began to convert the large input data into binary. The client would read in the characters, split them into a list of 8 byte strings and then convert each char to their ASCII binary value.</p>
<p>The amount of items in the list is equal to the total number of frames to be sent and the current frame is equal to the current iteration on the sending for loop. These three parts are sent as joint binary string.</p>
<p>I then implemented the CRC function. This took in the string of data, appended 16 zeroes to the end of it and performed a long division using the CRC-16 algorithm. This function was in both the server and the client as it should return the same value if the data has remained the same. </p>
<h3>Cyclic Redundancy Check Function</h3>

```python
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
```

<p>Once the CRC was complete, the server knows whether or not it has received the frame correctly. If it has, it sends an acknowledgment back to the client along with the frame number. If not, it sends back a negative acknowledgment and waits for the client to send the frame again.</p>
<p>To test that this works, I implemented a gremlin that messes up the received data which should fail the CRC check. When this happens the frame is sent again as it should.
<p>Once a frame is received, it is written to an output file called “Output_data.txt”.    
</p>
