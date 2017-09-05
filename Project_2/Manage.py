import sys, shutil

print "Welcome to the management console for your proxy server!\n\n"

#This function reads each line of the file into an array and strips each array of it EOL characters
def Read_in_blacklist():
	f = open("blacklist.txt", "r")				#Open the file to read
	site_list = f.readlines()				#Store each line in an array
	i = 0							#Initialise counter
	while i < len(site_list):				#While loop to iterate through array
   		site_list[i] = site_list[i].rstrip('\n')	#Strip EOL characters
   		i += 1						#Increment the counter
   	
   	f.close()						#Close the file 
	return site_list					#Return the array containing the stripped lines
	
def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
         # remove if exists
         shutil.rmtree(path)	

#This function adds a site to the blacklist	
def Add_to_blacklist(site):				
	f = open("blacklist.txt", "a")		#Open the blacklist file to be appended
	f.write(str(site) + "\n")		#Write the site assed in onto a new line and add a new line character
	f.close()				#Close the file
	
#This function takes in the blacklist and a site index to delete	
def Remove_from_blacklist(blacklist, site_index):	
	f = open("blacklist.txt", "w")			#Create a new blacklist file which overwrite the old one
	i = 0						#Initialise counter
	while (i < len(blacklist)):			#Step through the passed in array until you meet the index to delete
		if (i == site_index):			#If the index is the one to delete, just skip over it
			i+=1
		else:						
			f.write(str(blacklist[i]) + "\n")	#Write each line 
			i += 1
	f.close()						#Close the file

#This is the main loop
while True:
	try:	
		blacklist = Read_in_blacklist()									#Get a list of the sites in the blacklist
		print("\033c")											#Clear the terminal
		print "Here is the list of current sites which are blacklisted:"		
		i = 0												#Initialise counter
		while i < len(blacklist):									#Step through each index of the array
   			print "%i: %s" % (i+1, blacklist[i]) 							#Print each site on the blacklist with a unique index
   			i += 1											#Increment counter
   		
   		print "---------------------------------------------------\n"	
		choice = input("Press 1 to add a site to the list, press 2 to remove a site from the list: ")	#User chooses what to do
		
		if (choice == 1):										#User has selected to add a site to the blacklist
		
			while True:										#Will keep trying to add a site until correct format is entered
				site  = raw_input("Enter a site to blacklist: ")				#User input of the site
				www_find = site.find("www.")							#Won't accept it unless it had 'www.' in it 
				if(www_find == -1):				
					print "Invalid website, make sure you include 'www.'"
				else:
					Add_to_blacklist(site)							#Add site to blacklist 
					break									#break out of the adding site loop
			
		elif (choice == 2):										#User has selected to delete
			while True:										#Will keep trying to delete until one deleted or 0 pressed
				site_index = input("Enter the index number of the site above you want to remove from the blacklist or press 0 to cancel: ")
				if(site_index == 0):								#If 0 is pressed, cancel
					break
				elif((site_index < 1) or (site_index > len(blacklist))):			#If the index doesn't exist report it
					print "No website with that index. Try again or press 0 to cancel."
				else:										#If the index does exist
					Remove_from_blacklist(blacklist, site_index-1)				#Call the delete funciton
					break									#Break delete loop
					
		else:
			print "INVALID INPUT\n"
	
	except Exception, e:
		print "INVALID INPUT\n"
		
	except KeyboardInterrupt:
		print "\n\nClosing the management Console. Have a nice day!\n\n"
		sys.exit(1)
		
			
