##################################################
#						 #		       
# 	####  ####    #####  #    #  #   #       #
#	#  #  #  #    #   #   #  #   #   #       #
#	#  #  #  #    #   #    ##    #   #	 #
#	####  ####    #   #    ##    #####	 #
#	#     #   #   #   #   #  #       #	 #
#	#     #    #  #####  #    #  #####       #
#						 #
##################################################


# Author: 		Donal Tuohy
# Student Number:	14313774
# Module:		3D3 - Computer Networks
# Assignment:		Project 2 - Build a proxy server

############        IMPORT LIBRARIES      ###################

from thread import *
import socket, sys, os, datetime

############        FUNCTION DEFINITIONS      ###################


#Creates a file with the data recieved from the host with the url as the file name
def create_cache(url,webserver, webserver_reply):

	try:				
		if(url[len(url)-1] == '/'):		#If there is a slash on the end of the url,
			url = url[:(len(url)-1)]	#take it off
		url = url[7:]				#get rid of the http://
		url = url.split('/')			#Split up the url by its slashes into a list
		
		if(webserver.find("www.") != -1):	#Take the www. off the webserver
			webserver = webserver[4:]
		
    		
    		filepath = 'cache'					#Start with the filepath as cache	
    		for i in range(0,len(url)-1):				#Do a for loop from 0 to 
    			filepath = os.path.join(filepath, url[i])	#Iterate through each part of the url, add the current part onto the file path
    			if (not os.path.exists(filepath)):		#If the directory doesnt exist in the cache
    				os.makedirs(filepath)			#Create the directory
    		
    		filepath = os.path.join(filepath, url[len(url)-1]) 	#Add the file name onto the end of the filepath
    			
		f = open("%s" %filepath, "a")		#Open a file named with the url get request
		f.write(webserver_reply)		#Write the data recieved froom the server
		f.close()				#Close the file
		
	except Exception, e:
		print("Could not cache part of " + webserver)

#This is called everytime a request is made with a unique thread for each request
def thread_request(BrowserClientSocket, info, addr):
	
	try:
		get_lines = info.splitlines()	#Splits the block of text into lines and set get_line to the first line which should look something like: GET http://example.com/ HTTP/1.1
		get_line = get_lines[0]
		url = get_line.split(' ')[1]	#Take the URL out of the line
	
		position_of_http = url.find('://')	#Find the end point of the http in the address
		if (position_of_http == -1):		#It will return -1 if there is no http in the address
			temporary_url = url
		else:
			temporary_url = url[(position_of_http+3):]
	
		type_of_site = url[:position_of_http]
		position_of_port = temporary_url.find(':')					#Finds a port postition if there is any	
		position_of_webserver = temporary_url.find('/')					#Find the postion of the end of the webserver

		if(position_of_webserver == -1):						#If nothing was found 
			position_of_webserver = len(temporary_url)				#Set the postion equal to the end of the url
			webserver = ""								#Webserver is nothing
		if(position_of_port == -1 or position_of_webserver < position_of_port):		#default port
			port = 80
			webserver = temporary_url[:position_of_webserver]
		else:
			port = int((temporary_url[(position_of_port+1):])[:position_of_webserver - position_of_port - 1])
			webserver = temporary_url[:position_of_port]
		
	except Exception, e:

			print("Could not parse GET request.")					#Will pass by the function if there is an error
			parsed = 0
			
	except KeyboardInterrupt:
			BrowserClientSocket.close()
			print(" Shutting down the server.")
			sys.exit(1)
	
		
		
#ALL THE DATA HAS NOW BEEN PARSED SO START SENDING THE REQUEST TO THE HOST

	try:	
		webserver = temporary_url[:position_of_webserver]
		f = open("blacklist.txt", "r")								#Open the blacklist file
		site_list = f.readlines()								#Store each line in an array called site_list		
		SITE_OK = 1										#Initialise variable to say if th esite is blacklisted or not
		host_list = site_list	
		for i in range(0, len(site_list)):							#Step through each member of the list
			site_list[i] = site_list[i].rstrip('\n')					#Strip the EOL characters
			host_list[i] = (site_list[i])[4:]
			if (webserver == site_list[i] or webserver == host_list[i]):			#If the current website is on the blacklist	
				SITE_OK = 0 
				break								#Site is on the blacklist
		f.close()
		if (SITE_OK == 0):
			f =open("blocked.html", "r")
			blocked_site = f.read()
			f.close()
			BrowserClientSocket.send(blocked_site)	#This should be displayed on the browser if you are trying to access a blocked site
			BrowserClientSocket.close()	
			
		else:
		
			if(webserver.find("www.") != -1):
				webserver = webserver[4:]	
			
			#This if is just parsing the url into a filepath	
			if(url.find("http://") != -1):
				filepath = os.path.join("cache", url[7:])
			else:
				filepath = os.path.join("cache", url)
			
			#Initialise two variables one to check if the cache exists and then one to say if it's up to date	
			SITE_CACHED = 0
			SITE_CACHE_OK = 0
			
			#check if the filepath exists
			if (os.path.exists(filepath)):
				SITE_CACHED = 1
					
			if(SITE_CACHED == 1):
				cached_file = open("%s" % filepath, "r")
				cached_data = cached_file.read()
				cached_lines = cached_data.split('\n')
				cached_file.close()
				i = 0
				x = 0
				for i in range(0,len(cached_lines)-1):
					x = cached_lines[i].find("Date:")
					if(x!= -1):
						break
								
				date_line = cached_lines[i]
				date_line_split = date_line.split(" ")
				time = date_line_split[5]
				time_split = time.split(':')
				minutes = time_split[1]
				
				current_time = str(datetime.datetime.now())
				current_minutes = (current_time.split(':'))[1]
				
				if(minutes == current_minutes ):
					SITE_CACHE_OK = 1
					#print(SITE_CACHE_OK)		

			if(SITE_CACHED == 0 ):
				HostSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Connect to the host
				HostSocket.connect((webserver, port))
				HostSocket.settimeout(0.5)	
			
				if(type_of_site == "https"):
					print("HTTPS ALERT")
					HostSocket.connect((addr[0], port))
					HostSocket.send("200 OK")	#Send the CONNECT request to the internet
					BrowserClientSocket.send("200 OK")
				else:
					HostSocket.send(info)		#Send the GET request to the internet
				
			while 1:
				if(SITE_CACHED == 0):
							
					webserver_reply = HostSocket.recv(4096)		#Recieve the reply from the internet which needs to be sent back to the browser
					
					if(len(webserver_reply) > 0):
						
						#Create a cache of the data
						create_cache(url,webserver, webserver_reply)
						#print("Cache created")
						
						#Send reply back to application
						BrowserClientSocket.settimeout(1)
						BrowserClientSocket.send(webserver_reply) 		
						
						#Show what has happened on the server
						print "** Request Processed: %s taken from webserver"  %  url
			
					else: 	#Break the connection when recieving data failed
						#print "NO REPLY FROM WEBSERVER"
						HostSocket.close()
						break
				
				else: 
					BrowserClientSocket.settimeout(1)
					BrowserClientSocket.send(cached_data)
					print "** Request Processed: %s taken from cache."  %  url
					break
				 			
			BrowserClientSocket.close()
	except Exception, e:
		#print "Get was invalid."
		HostSocket.close()
		BrowserClientSocket.close()
			
	except socket.error, v:
		#print("Could not get reply request. ")
		HostSocket.close()
		BrowserClientSocket.close()

	
	#This exception will just give a neat exit message rather than looking like there was an error
	except KeyboardInterrupt:
		HostSocket.close()
		BrowserClientSocket.close()
		print(" \nShutting down the server.")
		sys.exit(1)
		
				

############        INITIALISATION       ###################	


#This part sets up the socket
try:	
	serverPort = 8888								#Choosing the port to use
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)			#Create Socket
	serverSocket.bind(('', serverPort))						#Bind Socket so its ready to listen
	serverSocket.listen(1)								#Start listening for request with a limit of five connections to the server
	print "The server is set up and ready to receive on port %i ." % serverPort 

#If the program fails to set up a socket it will run this exception code
except Exception, e:
	print("Failed to set up the socket, exiting program.")
	sys.exit(2)
	
	
############        MAIN LOOP       ###################
while 1:

	#Loops throught this until control-C is pressed to exit. 
	try:
		BrowserClientSocket, addr = serverSocket.accept()				#Accept connection from the browser
		info = BrowserClientSocket.recv(4096)					#Recieve data from the socket and store it in the variable info
		start_new_thread(thread_request, (BrowserClientSocket, info, addr)) 	#This starts a thread which calls the thread_request function
	
	#This exception will just give a neat exit message rather than looking like there was an error
	except KeyboardInterrupt:
		BrowserClientSocket.close()
		serverSocket.close()
		print(" \nShutting down the server.")
		sys.exit(1)
		
	
	












