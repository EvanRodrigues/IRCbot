import socket
import threading
import time
import datetime

from Mission import checkUser
from Mission import getLevel
from Tools import append
from Tools import update_file
from Tools import send_message
from Tools import clear_file
from Tools import create_log
from Treasure import reward
from User import User
from Slots import Slots

ROLLS_FILE = "Rolls.txt"
KAPPA_FILE = "Kappa.txt"
LOG_FILE = create_log()
TotalKappaMessages = 0
OneHand = False

def promoteLinks(s, irc, mission, slots):
	clear_file(KAPPA_FILE)
	time.sleep(360)
	mission.joinable = True
	send_message(s, irc, getLevel(mission.level))

def log(username, message):
	file_input = str(datetime.datetime.now().strftime('%H:%M:%S')) + " " + username + "=" + message + "\n\r"
	file = open(LOG_FILE, "a")
	file.write(file_input)
	file.close()
	


def message_handler(irc, s, username, message, mission, slots):
	log(username, message)
	global TotalKappaMessages, OneHand
	
	if "Kapp" in message or "Keepo" in message or "Krappa" in message or "kappa" in message and username != "doopbot":
		KappaMsg = str(TotalKappaMessages) + "_" + username + "=" + message + "\r\n"
		file = open(KAPPA_FILE, "a")
		file.write(KappaMsg)
		TotalKappaMessages += 1

	if "OneHand" in message:
		tokens = message.split(" ")
		for word in tokens:
			if word == "OneHand"  and OneHand == True:
				send_message(s, irc, "/timeout " + username + " 1")
				break

	message = message.lower()

	if message == "!mission" and checkUser("MissionUsers.txt", username) == True and checkUser("MissionUsersTemp.txt", username) == True and mission.joinable == True:
		if mission.active == False:
			append("MissionUsers.txt", username)
			mission.run(s, irc)
		else:
			print("adding " +username +" to temp file")
			append("MissionUsersTemp.txt", username)


	elif message == "!mission" and mission.joinable == False:
		send_message(s, irc, "there are no missions active at the moment.")

	elif message == "!onehand" and username == "doopian":
		if OneHand == False:
			OneHand = True
			send_message(s, irc, "OneHand nuke on!")
		else:
			OneHand = False
			send_message(s, irc, "OneHand nuke off!")

	elif message == "!startstream" and username == "doopian":
		promoteThread = threading.Thread(target = promoteLinks , args = (s, irc, mission, slots))
		promoteThread.daemon = True
		promoteThread.start()

	elif message == "!add":
		update_file("Users.txt", "doopian", 10)
		update_file("Users.txt", "doopian1", 10)

	elif message == "!loot":
		reward(s, irc, username)

	elif message == "!dd":
		checking = User(username)

		if checking.dollars == None:
			send_message(s, irc, username + " has no Doop Dollars! Do some missions!")
		else:
			send_message(s, irc, username + " has " + str(checking.getDollars()) + " Doop Dollars!")



	#checks if message BEGINS WITH !slots
	elif message.startswith("!slots "):
		if "." in message[7:]:
			send_message(s, irc, "Don't use decimals " +username)
			return

		try:
			num = int(message[7:])
		except:
			send_message(s, irc, "Please bet a number " +username)
			return
	
		if num <= 0:
			send_message(s, irc, "Please bet a positive number " +username)
			return

		wager = num
		user = User(username)

		if wager > int(user.getDollars()):
			send_message(s, irc, "You don't have enough Doop Dollars " +username)
			return

		elif num > 100 or num < 0:
			send_message(s, irc, "Please bet a number between 1 and 100 " +username)
			return


		if user.hasRolled() == True:
			send_message(s, irc, "You have rolled recently " +username)
			return 
		else:
			if slots.on == False:
				update_file(ROLLS_FILE, username, wager)	
				send_message(s, irc, "You have been added to the slot queue " +username)
			else:
				slots.start(s, irc, username, wager)


	elif message == "!xp":
		checking = User(username)

		if checking.xp == None:
			send_message(s, irc, username + " has no xp! Do some missions!")
		else:
			send_message(s, irc, username + " has " + str(checking.xp) + " xp!")

	elif message == "!mytreasure":
		checking = User(username)

		if checking.treasure == None:
			send_message(s, irc, username + " has no treasure chests. Do some missions!")
		else:
			send_message(s, irc, username + ": " + checking.treasure[0] + " Small, " + checking.treasure[1] + " Medium, and " + checking.treasure[2] + " Large treasure chests!")
		
	return