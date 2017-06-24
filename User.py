from Treasure import getTreasure

class User:
	def __init__(self, username):
		self.username = username
		self.xp = self.getXP()
		self.dollars = self.getDollars()
		self.treasure = getTreasure(username)
		self.level = self.getLevel()

	#
	# MAKE THESE LESS REDUNDANT! ONLY HAVE ONE GET WITH A STRING ARGUMENT
	#
	def getXP(self):
		File = open("Users.txt", "r")

		for line in File:
			if line == "\n":
				continue 

			username = line.split(":")[0]
			if username == self.username:
				xp = line.split(":")[1]
				return xp.strip("\n")

		return 0

	def getDollars(self):
		File = open("Points.txt", "r")

		for line in File:
			if line == "\n":
				continue 

			username = line.split(":")[0]
			if username == self.username:
				dollars = line.split(":")[1]
				return dollars.strip("\n")


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




