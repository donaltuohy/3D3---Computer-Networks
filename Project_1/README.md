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

<p>Once this was working I began to convert the large input data into binary. The client would read in the characters, split them into a list of 8 byte strings and then convert each char to their ASCII binary value.</p>
<p>The amount of items in the list is equal to the total number of frames to be sent and the current frame is equal to the current iteration on the sending for loop. These three parts are sent as joint binary string.</p>
<p>I then implemented the CRC function. This took in the string of data, appended 16 zeroes to the end of it and performed a long division using the CRC-16 algorithm. This function was in both the server and the client as it should return the same value if the data has remained the same. </p>
<p>Once the CRC was complete, the server knows whether or not it has received the frame correctly. If it has, it sends an acknowledgment back to the client along with the frame number. If not, it sends back a negative acknowledgment and waits for the client to send the frame again.</p>
<p>To test that this works, I implemented a gremlin that messes up the received data which should fail the CRC check. When this happens the frame is sent again as it should.
<p>Once a frame is received, it is written to an output file called “Output_data.txt”.    
</p>
