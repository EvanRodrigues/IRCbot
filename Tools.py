import datetime
from os.path import exists

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




def create_log():
	filepath = "B:/Streaming_Resources/Stream_Logs/"
	date = str(datetime.date.today()).split("-")
	year = date[0]
	month = get_month(date[1])
	day = date[2]
	
	filename = filepath + month + "_" + day + "_" + year + ".txt"
	count = 0
	while True:
		if exists(filename):
			count += 1
			filename = filepath + month + "_" + day + "_" + year + "(" + str(count) + ")" +".txt"
		else:
			file = open(filename, "a")
			file.write("File created \n\r")
			file.close()
			return filename
	





def get_month(month):
	months = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
	return months[month]


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
			newLine = target + ":" + str(value) + "\n" +"\n"
			temp = temp + newLine
			continue

		elif line == "\n":
			temp = temp + line
			continue

		#Change currentTier
		if line.startswith("*Tier"):
			currentTier = line.split(" ")[1][0]
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


def remove_top_line(filename):
	first_line = False
	file = open(filename, "r")
	output = ""

	for line in file:
		if first_line == False:
			first_line = True
			continue
		output += line

	file.close()

	file = open(filename, "w")
	file.write(output)


#
# Erases everything in a file
#
def clear_file(filename):
	open(filename, "w").close()