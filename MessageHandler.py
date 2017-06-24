import socket
import threading
import time

from Mission import checkUser
from Mission import getLevel
from Tools import append
from Tools import update_file
from Tools import send_message
from Treasure import reward
from User import User


def promoteLinks(s, irc, mission):
	time.sleep(60)
	mission.joinable = True
	send_message(s, irc, getLevel(mission.level))


def message_handler(irc, s, username, message, mission):
	if message == "!mission" and checkUser("MissionUsers.txt", username) == True and checkUser("MissionUsersTemp.txt", username) == True and mission.joinable == True:
		if mission.active == False:
			append("MissionUsers.txt", username)
			mission.run(s, irc)
		else:
			print("adding " +username +" to temp file")
			append("MissionUsersTemp.txt", username)

	elif mission.joinable == False:
		send_message(s, irc, "there are no missions active at the moment.")

	elif message == "!startstream" and username == "doopian":
		promoteThread = threading.Thread(target = promoteLinks , args = (s, irc, mission))
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
			send_message(s, irc, username + " has " + checking.getDollars() + " Doop Dollars!")
		

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