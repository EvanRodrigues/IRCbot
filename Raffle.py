from random import randint

from Tools import send_message
from Tools import update_file
from Tools import clear_file

import threading
import time


RAFFLE_FILE = "./Data/Raffle.txt"
POINTS_FILE = "./Data/Points.txt"


class Raffle:
	def __init__(self, s, irc, pot, on, users, limit):
		self.socket = s
		self.irc = irc
		self.pot = pot
		self.on = on
		self.users = users
		self.limit = limit

	def run(self, socket, irc):
		RaffleThread = threading.Thread(target = self.start, args = (socket, irc))
		RaffleThread.start()

	def start(self, s, irc):
		for i in range(0, 60):
			time.sleep(15)
			if i == 20:
				send_message(s, irc, "Raffle is ending in 10 minutes!")
			elif i == 40:
				send_message(s, irc, "Raffle is ending in 5 minutes!")
			elif i == 56:
				send_message(s, irc, "Raffle is ending in 1 minute!")
			elif i == 58:
				send_message(s, irc, "Raffle is ending in 30 seconds!")


		self.on = False
		winner = self.getWinner()
		clear_file(RAFFLE_FILE)
		send_message(s, irc, "Winner is " + winner)


	

	#updates the bet if user previously bet.
	#if the user hasn't bet, adds the user to the end of the file.
	def bet(self, username, bet):
		file = open(RAFFLE_FILE, "r")

		self.pot += bet
		update_file(POINTS_FILE, username, bet * -1)

		for line in file:
			if line.split(":")[0] == username:
				update_file(RAFFLE_FILE, username, bet)
				file.close()
				return

		addUser(username, bet)
		file.close()


	def getWinner(self):
		file = open(RAFFLE_FILE, "r")
		
		winningTicket = randint(1, self.pot)
		ticketLocation = 0

		for line in file:
			username = line.split(":")[0]
			bet = line.split(":")[1].strip("\n")
			ticketLocation += int(bet)

			if ticketLocation >= winningTicket:
				return username



#If user has not placed a bet yet
def addUser(username, bet):
	file = open(RAFFLE_FILE, "a")
	file.write(username + ":" + str(bet) + "\n")
	file.close()



#Checks to see if the user is:
#1. Betting over the limit
#2. Betting more dd than they have
#3. Will have a negative bet
def canWager(username, bet):
	
	return False





def getBet(username):
	file = open(RAFFLE_FILE, "r")

	for line in file:
		if line.split(":")[0] == username:
			return int(line.split(":")[1].strip("\n"))

	return 0