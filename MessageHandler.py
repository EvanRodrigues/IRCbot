import socket
import threading
import time
import datetime

import SongList

from Mission import checkUser
from Mission import getLevel

from Quote import Quote

from Raffle import Raffle
from Raffle import getBet

from Tools import append
from Tools import update_file
from Tools import send_message
from Tools import clear_file
from Tools import create_log
from Tools import remove_user
from Tools import convert_file
from Tools import set_kappa
from Tools import sort_users
from Tools import format_five
from Tools import get_rank

from Tools import contact_api

from Treasure import reward
from User import User
from User import mergeUsers
from User import isMod
from Slots import Slots

ROLLS_FILE = "./Data/Rolls.txt"
KAPPA_FILE = "./Data/Kappa.txt"
TODAYS_ROLLS_FILE = "./Data/TodaysRolls.txt"
SESSION_FILE = "./Data/SessionStats.ini"
ALLTIME_FILE = "./Data/AllTimeStats.ini"
LOG_FILE = create_log()

KAPPA_FACES = set_kappa() 
TotalKappaMessages = 0
OneHand = False



def findKappa(message):
	for i in KAPPA_FACES:
		
		if i.strip("\n") in message:
			return True

	return False



def promote_links(s, irc):
	while True:
		time.sleep(2400)
		send_message(s, irc, "Feel free to join doopian's discord https://discord.gg/YBpfPQD")

		time.sleep(2400)
		send_message(s, irc, "Follow doopian on twitter for updates https://twitter.com/doopian")

		time.sleep(2400)
		send_message(s, irc, "Follow doopian on twitter for updates https://twitter.com/doopian")


# Initial timers and threads for when the stream starts
def start_stream(s, irc, mission, slots):
	clear_files()
	time.sleep(360)
	
	mission.joinable = True
	send_message(s, irc, getLevel(mission.level))

def clear_files():
	clear_file(KAPPA_FILE)
	clear_file(TODAYS_ROLLS_FILE)
	clear_file(SESSION_FILE)

def log(username, message):
	file_input = str(datetime.datetime.now().strftime('%H:%M:%S')) + " " + username + "=" + message + "\n\r"
	file = open(LOG_FILE, "a")
	file.write(file_input)
	file.close()


# Checks if a message contains a bad word.
# Punishes the user with a 3 strike rule
# The only exception is the n-word which results in an instant ban
def hasBadWord(message):
	file = open("./Data/BadWords.txt", "r")

	for line in file:
		if line.strip("\n") in message and "n" in line:
			return 2
		elif line.strip("\n") in message and "f" in line:
			return 1
	return 0
	


def message_handler(irc, s, username, message, mission, slots, raffle, songList, quote):
	log(username, message)
	ban = hasBadWord(message)
	global TotalKappaMessages, OneHand, Raffle, Quote

	if ban != 0:
		if ban == 1:
			send_message(s, irc, "/timeout " + username + " 1 ")
		else:
			send_message(s, irc, "/ban " + username)

	
	
	if findKappa(message) == True and username != "doopbot":
		KappaMsg = str(TotalKappaMessages) + "_" + username + "=" + message + "\r\n"
		file = open(KAPPA_FILE, "a")
		file.write(KappaMsg)
		TotalKappaMessages += 1

	if "OneHand" in message and OneHand == True:
		tokens = message.split(" ")
		for word in tokens:
			if word == "OneHand"  or word == "OneHandWeen" and OneHand == True:
				send_message(s, irc, "/timeout " + username + " 1")
				break

	




	#song request code
	if message.startswith("!request ") and username == "doopian":
		song = message[9:] #super hard-coded, but the command is not likely to change
		songList.addSong(False, song, username)

	if message.startswith("!vipRequest ") and username == "doopian":
		song = message[12:]
		songList.addSong(True, song, username)

	if message.startswith("!remove ") and username == "doopian":
		target = message[8:]
		songList.removeSong(False, target)

	if message.startswith("!vipRemove ") and username == "doopian":
		target = message[11:]
		songList.removeSong(True, target)


	if message == ("!list") and username == "doopian":
		send_message(s, irc, songList.getList())






	#quote commands
	if quote.active == True:
		print("QUOTE IS True")

	if message == ("!quotelist"):
		send_message(s, irc, "All of the quotes for the bot can be found here https://pastebin.com/k6ke3pfB")
	
	elif message == "!quote" and quote.active == False:
		quote.run(s, irc, None, username)
	
	elif message.startswith("!quote ") and quote.active == False:
		quoteIndex = None

		try:
			quoteIndex = int(message.split(" ")[1].strip("\n"))
		except ValueError:
			send_message(s, irc, "Please use a positive integer when searching quotes " + username)
			return
		
		quote.run(s, irc, quoteIndex, username)
		

	elif message.startswith("!addquote "):
		modCheck = User(username)

		if modCheck.mod == False:
			return

		print("message before: " + message)
		message = message.split("!addquote ")[1].strip("\n")
		print("message after: " + message)
		send_message(s, irc, add_quote(message))






	

	# merge command
	if message.startswith("!merge ") and username == "doopian":
		curr = User(message.split(" ")[1])
		prev = User(message.split(" ")[2].strip("\n"))
		mergeUsers(curr, prev)
		send_message(s, irc, "Finished merging " + curr.username + " with " + prev.username)


	if message == "!test" and username == "doopian":
		contact_api()


	

	message = message.lower()

	#raffle commands
	if message == "!raffle" and username == "doopian" and raffle.on == False:
		raffle.on = True
		raffle.run(s, irc)

	#TODO:
	#TODO:
	#TODO:make this into a function Krappa
	elif message.startswith("!addtickets ") and raffle.on == True:
		try:
			bet = int(message.split(" ")[1].strip("\n"))

			user = User(username)
			if bet <= 0:
				send_message(s, irc, "Please enter a positive integer " + username)
				return
			elif bet > user.dollars:
				send_message(s, irc, "You dont have that many Doop Dollars " + username)
				return
		except ValueError:
			send_message(s, irc, "Please enter an integer " + username)
			return
		
		raffle.bet(username, bet)
		send_message(s, irc, username + " has bet " + str(bet) + " and now has " + str(getBet(username)) + " doop dollars in the raffle")

	#TODO:
	#TODO:
	#TODO:make this into a function Krappa
	elif message.startswith("!removetickets ") and raffle.on == True and username == "doopian":
		try:
			bet = int(message.split(" ")[1].strip("\n"))

			user = User(username)
			if bet <= 0:
				send_message(s, irc, "Please enter a positive integer " + username)
				return
			elif bet > getBet(username):#FIND THE USER'S DOLLARS IN THE RAFFLE
				send_message(s, irc, "You dont have that many dollars in the raffle " + username)
				return
		except ValueError:
			send_message(s, irc, "Please enter an integer " + username)
			return

		raffle.bet(username, bet * -1)
		send_message(s, irc, username + " has removed " + str(bet) + " and now has " + str(getBet(username)) + " doop dollars in the raffle")



	elif message == "!topfive":
		output = format_five(sort_users())
		send_message(s, irc, output)


	elif message == "!myrank":
		output = get_rank(username, sort_users())
		send_message(s, irc, output)
		




	if message == "!mission" and checkUser("./Data/MissionUsers.txt", username) == True and checkUser("./Data/MissionUsersTemp.txt", username) == True and mission.joinable == True:
		if mission.active == False:
			append("./Data/MissionUsers.txt", username)
			mission.run(s, irc)
		else:
			print("adding " +username +" to temp file")
			append("./Data/MissionUsersTemp.txt", username)


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
		promoteThread = threading.Thread(target = promote_links , args = (s, irc))
		promoteThread.daemon = True
		promoteThread.start()

		startThread = threading.Thread(target = start_stream, args = (s, irc, mission, slots))
		startThread.daemon = True
		startThread.start()


	#TODO: make an !add function for anyone to use.
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




	#############Kappa Stuff#############
	elif message == "!firstkappa":
		file = open("./Data/FirstKappa.ini", "r")

		for line in file:
			if line != "[First]\n":
				username = line.split("=")[1].strip("\n")
				send_message(s, irc, "Today's first Kappa was posted by: " +username)
				file.close()
				return

		send_message(s, irc, "No one has posted a Kappa today!")
		file.close()

	elif message == "!mystats":
		user = User(username)

		if user.allKappa == 0:
			send_message(s, irc, username + " has not written a Kappa in chat yet! WUTFACE")
		elif user.allKappa > 0 and user.sessionKappa == 0:
			send_message(s, irc, username + " has written " + str(user.allKappa) + " Kappa faces all time, but has not written one today.")
		else:
			send_message(s, irc, username + " has written " + str(user.allKappa) + " Kappa all time and " + str(user.sessionKappa) + " Kappa today.")





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
			send_message(s, irc, username + " is level " + str(checking.level) + " with " + str(checking.xp) + " total xp! " + username + " needs " + checking.remainder + " xp to level up!")

	elif message == "!mytreasure":
		checking = User(username)

		if checking.treasure == None:
			send_message(s, irc, username + " has no treasure chests. Do some missions!")
		else:
			send_message(s, irc, username + ": " + checking.treasure[0] + " Small, " + checking.treasure[1] + " Medium, and " + checking.treasure[2] + " Large treasure chests!")
	

	elif message == "!songs":
		send_message(s, irc, "A full list of doopian's customs can be found here https://doop-songs.000webhostapp.com (please dont use internet explorer for now)")







	### RANDOM COMMANDS ###
	elif message == "!commands":
		send_message(s, irc, "The commands for doopbot are found here: https://pastebin.com/k9cPVTdS")
	elif message == "!protoss":
		send_message(s, irc, "Protoss are Love, Protoss are Life, for Aiur!!")
	elif message == "!zerg":
		send_message(s, irc, "PvZ is Doopian's best matchup. You will probably lose if you are zerg versus Doopian Kappa")
	elif message == "!terran":
		send_message(s, irc, "Terran is a delicate race, be sure to a-move frequently into Doopian's storms.")
	elif message == "!random":
		send_message(s, irc, "Playing random is like a box of chocolates. Only 1 of the chocolates is your favorite ~ Kappa ~")
	elif message == "!top5":
		send_message(s, irc, "1. Kappa 2. Krappa 3. Krabpa 4. Krepapo 5. Kapp")
	elif message == "!doyourememberme":
		send_message(s, irc, "Doopian does not remember you " + username  + " Krappa")
	elif message == "!pranked":		
		send_message(s, irc, "YOU HAVE BEEN COAXED INTO A SNAFU! LUL")
	elif message == "!vapenation":
		send_message(s, irc, "http://sketchtoy.com/67098968")
	elif message == "!fc":
		send_message(s, irc, "A fan club (or fc for short) is a group of like minded individuals that congregate over the same topic.")
	elif message == "!cf":
		send_message(s, irc, "A combo full (or cf for short) is when you get a 100% in a guitar hero song without breaking your combo.")
	elif message == "!cheer":
		send_message(s, irc, "*\ Kappa /* GO DOOP GO *\ Kappa /*")
	elif message == "!rigged":
		send_message(s, irc, "BabyRage NEVER LUCKY BabyRage")
	elif message == "!Klappa":
		send_message(s, irc, "Kappa Clap Kappa Clap Kappa Clap")
	elif message == "!thumbsup":
		send_message(s, irc, "Kappa b Kappa b Kappa b")
	elif message == "!thumbsdown":
		send_message(s, irc, "Krappa p Krappa p Krappa p")
	elif message == "!schedule":
		send_message(s, irc, "Doopian streams randomly Krappa")
	elif message == "!plugdj":
		send_message(s, irc, "request songs here -> https://plug.dj/doopian-song-requests")
	elif message == "!customs":
		send_message(s, irc, "Download clonehero.")
	elif message == "!motivation":
		send_message(s, irc, ":ok_hand: OSsloth you got this " + username)
	elif message == "!prime":
		send_message(s, irc, "https://i.imgur.com/fBf3v1r.png")
	elif message == "!freeshit":
		send_message(s, irc, "All of doopian's sub emotes are free. Just download better twitch tv AND frankerfaceZ (which are also free!) Hooray free shit! \ Krappa /")
	elif message == "!gentlebob":
		send_message(s, irc, "http://i.imgur.com/AkTtU0c.jpg")
	elif message == "!marble":
		send_message(s, irc, "This is not marble racing. This will never be marble racing. You are in the wrong chat room. Stop using the !marble command please. Thanks!")
	elif message == "!twitter":
		send_message(s, irc, "Follow Doopian at http://twitter.com/doopian")
	elif message == "!youtube":
		send_message(s, irc, "Subscribe to Doopian's channel for Guitar Hero related videos at http://youtube.com/doopian")
	elif message == "!facebook":
		send_message(s, irc, "Like Doopian's facebook here http://www.facebook.com/doopian")
	elif message == "!discord":
		send_message(s, irc, "Here is Doopian's discord server https://discord.gg/YBpfPQD")
	elif message == "!social" and isMod(username):
		send_message(s, irc, "Join Doopian's discord server https://discord.gg/YBpfPQD")
		send_message(s, irc, "Follow Doopian at http://twitter.com/doopian")
		send_message(s, irc, "Subscribe to Doopian's YouTube channel at http://youtube.com/doopian")
		send_message(s, irc, "Like Doopian's facebook here http://www.facebook.com/doopian")