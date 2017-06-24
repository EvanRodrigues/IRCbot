def send_message(socket, irc, message):
	socket.send(bytes("PRIVMSG #" + irc.CHANNEL + " :" + message + "\r\n", "UTF-8"))



#
# Checks if a file is empty 
# Returns True if file is empty. Returns False otherwise.
#
def isEmpty(filename):
	file = open(filename, "r");

	if file.read() == "":
		return True
	else:
		return False



#
# Used to update the values of Points, XP, and Treasure  
# This function uses addition by default. 
# To use subtraction, input a negative value.
#
def update_file(filename, target, value):
	file = open(filename, "r")
	found = False
	temp = "" #saves the old file information to write to a new fresh file.

	for line in file:		
		if line == "\n":
			continue

		user = line.split(":")[0]
		oldPoints = int(line.split(":")[1])

		if user == target:
			newPoints = value + oldPoints
			newLine = user + ":" + str(newPoints) + "\n"
	
			temp = temp + newLine
			found = True
		else:
			temp = temp + line

	file.close()
	
	
	#No user to update, so appends the info to the file
	if found == False:
		file = open(filename, "a")
		file.write(target + ":" + str(value) + "\n")

	#Applies the changes to a fresh file
	else:
		file = open(filename, "w")
		file.write(temp)
	
	file.close()



#
# TODO: 
# Updates when they have treasure chest already
# Adds the user in the correct section if they have never had a chest of that tier.
#
def update_treasure_file(target, tier, value):
	file = open("Treasure.txt", "r")

	found = False
	notFound = False
	currentTier = 0
	temp = "" #saves the old file information to write to a new fresh file.

	for line in file:	
		#User has never had a chest of the tier being added.	
		if line == "\n" and tier == int(currentTier) and found == False:
			print("Gets Here")
			newLine = target + ":" + str(value) + "\n" +"\n"
			temp = temp + newLine
			continue

		elif line == "\n":
			temp = temp + line
			continue

		#Change currentTier
		if line.startswith("*Tier"):
			currentTier = line.split(" ")[1][0]
			print("tier: " + currentTier)
			temp = temp + line
			continue

		user = line.split(":")[0]
		oldPoints = int(line.split(":")[1])

		#User already has an entry for a chest of that tier.
		if user == target and tier == int(currentTier):
			newPoints = value + oldPoints
			newLine = user + ":" + str(newPoints) + "\n"
	
			temp = temp + newLine
			found = True
		else:
			temp = temp + line



	file.close() #close read-only mode
	file = open("Treasure.txt", "w") #open in write-only mode and update the file.
	file.write(temp)
	file.close()


#
# Appends the user to the end of the file
#
def append(filename, username):
	file = open(filename, "a")
	file.write(username + "\n")
	file.close()


#
# Erases everything in a file
#
def clear_file(filename):
	open(filename, "w").close()