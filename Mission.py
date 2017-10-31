from random import randint
from Tools import send_message
from Tools import isEmpty
from Tools import append
from Tools import clear_file
from Tools import update_file
from Tools import update_treasure_file
from User import User

import threading
import time

MISSION_FILE = "./Data/MissionUsers.txt"
MISSION_FILE_TEMP = "./Data/MissionUsersTemp.txt"
TREASURE_FILE = "./Data/Treasure.txt"
USER_FILE = "./Data/Users.txt"
POINTS_FILE = "./Data/Points.txt"
LEVEL_FILE = "./Data/Levels.txt"


#TODO: Replace all "file.txt" to one of these FINAL variables ^^^^^^^^^^^^^^

class Mission:
	def __init__(self):
		self.active = False
		self.joinable = False
		self.players = 0
		self.success = False
		self.prev = 1
		self.level = getCurrentLevel()


	#
	# Starts the mission and sets up the timers
	#
	def start(self, socket, irc):
		send_message(socket, irc, "mission starting!")
		self.active = True

		output = "Added to the mission: "
		count = 0
		while count < 6:
			time.sleep(15)
			if isEmpty(MISSION_FILE_TEMP) == False:
				output = addUsers(output)
				send_message(socket, irc, output)

			output = "Added to the mission: "
			count = count + 1

		self.active = False
		self.joinable = False
		success(self, socket, irc)
		clear_file(MISSION_FILE)

		time.sleep(360)
		send_message(socket, irc, getLevel(self.level))
		self.joinable = True

	#
	# Returns the success or failure of the current level. 
	# If @success is True, this returns a winning message.
	# If @success is False, this returns a losing message.
	#
	def getMissionOutcome(self):
		file = open(LEVEL_FILE, "r")

		for line in file:
			if self.success == True and line.startswith("Win"):
				level = int(line.split(":")[0].split(" ")[1])
				if level == self.level:
					file.close()
					output = line.split(":")[1].strip('\n')
					return output

			elif self.success == False and line.startswith("Loss"):
				level = int(line.split(":")[0].split(" ")[1])
				if level == self.level:
					file.close()
					output = line.split(":")[1].strip('\n')
					return output


	#
	# Rewards each user xp, and Doop Dollars. Chests are random
	#
	def reward(self, socket, irc, outcome):
		file = open(MISSION_FILE, "r")
		rand = randint(1, 10)
		output = ""
		chestOutput = ""

		for line in file:
			user = User(line.strip('\n'))
			prevLvl = user.getLevel()

			chestOutput = chestOutput + self.rewardChest(user)
			update_file(POINTS_FILE, user.username, rand)
			update_file(USER_FILE, user.username, 25)
			updatedLvl = user.getLevel()

			if updatedLvl - prevLvl > 0:
				output = output + user.username + " has advanced to level " + str(updatedLvl) + "! "


		chestOutput = chestOutput[0:-2] + '.'

		file.close()
		send_message(socket, irc, outcome + " You each earn 25xp, and " + str(rand) + " Doop Dollars!")
		send_message(socket, irc, chestOutput)
		send_message(socket, irc, output)
		return



	#
	# Rewards treasure chests to the user
	#
	def rewardChest(self, user):
		rand = randint(0, 99)
		rewarded = self.treasureRoll()
		output = ""

		if rand < 10 and rewarded == True:
			update_treasure_file(user.username, 3, 1)
			output = user.username + " found Large Treasure, "
		elif rand < 40 and rewarded == True:
			update_treasure_file(user.username, 2, 1)
			output = user.username + " found Medium Treasure, "
		elif rand < 100 and rewarded == True:
			update_treasure_file(user.username, 1, 1)
			output = user.username + " found Small Treasure, "

		return output



	def levelRoll(self):
		rand = randint(0, 99)

		print("level roll: " + str(rand))

		if self.level % 10 == 1 and rand < 50:
			return True
		elif self.level % 10 == 2 and rand < 45:
			return True
		elif self.level % 10 == 3 and rand < 40:
			return True
		elif self.level % 10 == 4 and rand < 35:
			return True
		elif self.level % 10 == 5 and rand < 30:
			return True
		elif self.level % 10 == 6 and rand < 25:
			return True
		elif self.level % 10 == 7 and rand < 20:
			return True
		elif self.level % 10 == 8 and rand < 15:
			return True
		elif self.level % 10 == 9 and rand < 10:
			return True
		elif self.level % 10 == 0 and rand < 5:
			return True

		return False



	def treasureRoll(self):
		rand = randint(0, 99)

		if self.level % 10 == 1 and rand < 5:
			return True
		elif self.level % 10 == 2 and rand < 10:
			return True
		elif self.level % 10 == 3 and rand < 15:
			return True
		elif self.level % 10 == 4 and rand < 20:
			return True
		elif self.level % 10 == 5 and rand < 25:
			return True
		elif self.level % 10 == 6 and rand < 30:
			return True
		elif self.level % 10 == 7 and rand < 35:
			return True
		elif self.level % 10 == 8 and rand < 45:
			return True
		elif self.level % 10 == 9 and rand < 55:
			return True
		elif self.level % 10 == 0 and rand < 75:
			return True

		return False



	#
	# Sets up the Thread so missions can work simultaneously with the rest of doopbot
	#
	def run(self, socket, irc):
		MissionThread = threading.Thread(target = self.start, args = (socket, irc))
		MissionThread.start()



#
# Adds the users from the temp mission file to the mission file
#
def addUsers(output):
	file = open(MISSION_FILE_TEMP, "r")
	
	for line in file:
		username = line.strip('\n')
		output = output + username + ", "
		append(MISSION_FILE, username)
	
	lastComma = output.rfind(",")
	output = output[:lastComma] 

	file.close()
	clear_file(MISSION_FILE_TEMP)	
	return output



#
# Loops through the MissionUsers file and rolls each user against their individual RNG
# Uses the current level to determine the difficulty of the level
#
def success(self, socket, irc):
	file = open(MISSION_FILE, "r")
	output = ""

	for line in file:
		if self.levelRoll() == True:
			self.success = True
			outcome = self.getMissionOutcome()
			self.prev = self.level

			if self.level != 10:
				self.level = self.level + 1
			else:
				self.level = 1

			setCurrentLevel(self.level)
			self.reward(socket, irc, outcome)
			file.close()
			return
	

	self.success = False
	outcome = self.getMissionOutcome()
	self.prev = self.level
	self.level = 1
	setCurrentLevel(self.level)
	send_message(socket, irc, outcome)
	file.close()
	return


#
# Checks to see if the user is already on the mission
# Returns False if they are already on the mission, and True if they aren't
#
def checkUser(filename, username):
	file = open(filename, "r");

	for line in file:		
		tempName = line.replace('\n', '')

		if tempName == username:
			file.close()
			return False

	file.close()
	return True



#
# Used to figure out the chat's current progress in the story.
#
def getCurrentLevel():
	file = open(LEVEL_FILE, "r")
	
	line = file.readline()
	line.split(" ")

	file.close()
	return int(line[15:].replace("\n", ""))



#
# Updates the current level. If the stream resets, progress wont be lost.
#
def setCurrentLevel(level):
	file = open(LEVEL_FILE, "r")
	first = False
	output = ""

	for line in file:
		if first == False:
			output = "Current Level: " + str(level) + "\n"
			first = True	
		else:
			output = output + line


	file.close()
	file = open(LEVEL_FILE, "w")
	file.write(output)
	file.close()
	return



#
# Sets the Mission's scenario to a the index'th line in the 
#
def getLevel(index):
	file = open(LEVEL_FILE, "r")
	count = 0

	for line in file:
		if count == index:
			file.close
			return line.replace('\n', '')
		count += 1

	file.close()
	return None