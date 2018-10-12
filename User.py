from Treasure import getTreasure
from Tools import update_treasure_file
from Tools import update_file
from Tools import remove_user

TODAYS_ROLLS_FILE = "./Data/TodaysRolls.txt"
SESSION_FILE = "./Data/SessionStats.ini"
ALLTIME_FILE = "./Data/AllTimeStats.ini"
USER_FILE = "./Data/Users.txt"
POINTS_FILE = "./Data/Points.txt"
ALLTIME_POINTS_FILE = "./Data/AllTimePoints.txt"
TREASURE_FILE = "./Data/Treasure.txt"
MODS_FILE = "./Data/Mods.txt"

levels = {'1': 100, '2': 250, '3': 750, '4': 1500, '5': 2500, '6': 4000, '7': 6000, '8': 10000, '9': 15000, '10': 25000, '11': 50000}

class User:
	def __init__(self, username):
		self.username = username
		self.xp = self.getXP()
		self.dollars = self.getDollars()
		#self.allDollars = self.getAllDollars()
		self.treasure = getTreasure(username)
		self.level = self.getLevel()
		self.remainder = self.getRemainingXP()
		self.sessionKappa = self.getSession()
		self.allKappa = self.getAllTime()
		self.mod = isMod(self.username)


	#
	# MAKE THESE LESS REDUNDANT! ONLY HAVE ONE GET WITH A STRING ARGUMENT
	#
	def getXP(self):
		File = open("./Data/Users.txt", "r")

		for line in File:
			if line == "\n":
				continue 

			username = line.split(":")[0]
			if username == self.username:
				xp = line.split(":")[1]
				return int(xp.strip("\n"))

		return 0

	def getDollars(self):
		File = open("./Data/Points.txt", "r")

		for line in File:
			if line == "\n":
				continue 

			username = line.split(":")[0]
			if username == self.username.lower():
				dollars = line.split(":")[1]
				return int(dollars.strip("\n"))

		return 0

	def getSession(self):
		File = open(SESSION_FILE, "r")
		return getStats(File, self.username)

	def getAllTime(self):
		File = open(ALLTIME_FILE, "r")
		return getStats(File, self.username)

	def getRemainingXP(self):
		levelUp = levels[str(self.level)]
		return str(levelUp - self.xp)



	#
	# Will return the current level the user is based on their total xp
	#
	def getLevel(self):
		xp = int(self.getXP())

		if xp < 100:
			return 1
		elif xp < 250:
			return 2
		elif xp < 750:
			return 3
		elif xp < 1500:
			return 4
		elif xp < 2500:
			return 5
		elif xp < 4000:
			return 6
		elif xp < 6000:
			return 7
		elif xp < 10000:
			return 8
		elif xp < 15000:
			return 9
		elif xp < 25000:
			return 10
		elif xp < 50000:
			return 11
		else:
			return 12


	def hasRolled(self):
		file = open(TODAYS_ROLLS_FILE, "r")

		for line in file:
			if line.split("\n")[0] == self.username:
				return True

		return False


#Finds the Kappa stats for a given user
def getStats(file, username):
	for line in file:
		if line == "[User]\n":
			continue

		if line.split(":")[0] == username:
			return float(line.split(":")[1])

	return 0


# Merges stats of curr with prev. 
# updates curr's stats
# removes prev's stats
# TODO: make it so curr stats are added with prev stats
def mergeUsers(curr, prev):
	for i in range(1,4):
		update_treasure_file(curr.username, i, int(prev.treasure[i-1]))
	
	update_file(POINTS_FILE, curr.username, prev.dollars)
	update_file(USER_FILE, curr.username, prev.xp)
	update_file(SESSION_FILE, curr.username, prev.sessionKappa)
	update_file(ALLTIME_FILE, curr.username, prev.allKappa)	

	#Must remove items when thats a thing.
	remove_user(TREASURE_FILE, prev.username)
	remove_user(USER_FILE, prev.username)
	remove_user(POINTS_FILE, prev.username)
	remove_user(SESSION_FILE, prev.username)
	remove_user(ALLTIME_FILE, prev.username)



#checks if username is a mod in the channel
def isMod(username):
	file = open(MODS_FILE, "r")

	for line in file:
		if line.strip("\n") == username:
			return True

	file.close()
	return False