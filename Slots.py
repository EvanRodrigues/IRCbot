from User import User
from Tools import send_message
from Tools import update_file
from Tools import clear_file
from Tools import remove_top_line

import threading
import time

POINTS_FILE = "./Data/Points.txt"
ROLLS_FILE = "./Data/Rolls.txt"
JACKPOT_FILE = "./Data/Jackpot.txt"
WINNER_FILE = "./Data/Winnings.txt"
TODAYS_ROLLS_FILE = "./Data/TodaysRolls.txt"


class Slots:
	def __init__(self, s, irc):
		self.roller = None
		self.wager = 0
		self.can_roll = False
		self.on = True
		startTimer(s, irc)

	def setRoller(self, username):
		self.roller = User(username)
		self.can_roll = self.canRoll()

	#rolls the slot machine for self.roller
	def roll(self, s, irc, username, wager):
		moreRolls = True
		self.roller = User(username)
		self.wager = wager
		update_file(ROLLS_FILE, username, wager)	
		self.on = False

		while moreRolls == True:
			file = open(ROLLS_FILE, "r")
			line = file.readline()

			if line == "":
				moreRolls = False
				continue
			else:
				self.roller = User(line.split(":")[0])
				self.wager = int(line.split(":")[1].strip("\n"))

			user = self.roller.username
			send_message(s, irc, "Rolling for " + user)

			#read the winner file, get the winnings, update users points
			time.sleep(1)

			winnings = (self.wager * -1) + find_winnings(user)
			update_file(POINTS_FILE, user, winnings)
			add_recent_roll(user)
			remove_top_line(ROLLS_FILE)

			time.sleep(18)

			if winnings < 0:
				winnings = winnings * -1
				send_message(s, irc, "The roll is finished! " +user + " has loserino'd " +str(winnings) + " OneHand Clap")
			elif winnings == 0:
				send_message(s, irc, "The roll is finished! " +user + " gets their money back KrappaW b")
			else:
				send_message(s, irc, "The roll is finished! " +user + " has wonned " +str(winnings) + " Kappa Clap")


		self.on = True

	#Checks if user has rolled recently
	def canRoll(self):
		if self.on == False:
			return False

		file = open("Rolls.txt", "r")

		for line in file:
			if line == self.roller.username:
				return False

		return True

	#starts the thread for the slot machine
	def start(self, socket, irc, username, wager):
		slotsThread = threading.Thread(target =  self.roll, args = (socket, irc, username, wager))
		slotsThread.daemon = True
		slotsThread.start()


def find_winnings(target):
	file = open(WINNER_FILE, "r")

	for line in file:
		user = line.split(":")[0]
		winnings = line.split(":")[1]
		
		if user == target:
			return int(winnings)

	return 0


def add_recent_roll(username):
	file = open(TODAYS_ROLLS_FILE, "a")
	file.write(username + "\n")



def startTimer(s, irc):
	resetThread = threading.Thread(target =  resetTimer, args = (s, irc))
	resetThread.daemon = True
	resetThread.start()


#Resets the ability for viewers to use the slot machine again
def resetTimer(s, irc):
	while True:
		time.sleep(300)
		clear_file(TODAYS_ROLLS_FILE)
		send_message(s, irc, "The slot machine has been reset!")

	