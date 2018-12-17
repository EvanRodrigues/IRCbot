import requests

import time
import datetime
import math

from Quote import Quote
from Quote import add_quote
from Tools import send_message
from Tools import create_log
from Tools import contains_kappa
from Tools import send_kappa_message
from Tools import format_time
from Tools import set_commands
from User import User

from ConnectionVars import CLIENT_ID

kappa_message_count = 0
game = ""
startTime = None
id = {'Client-ID': CLIENT_ID}
q = "https://api.twitch.tv/helix/streams?user_login=doopian"
LOG_FILE = create_log()
basic_commands = set_commands()



def get_game_name(gameID, HEADERS):
	game_query = "https://api.twitch.tv/helix/games?id=" + gameID

	r = requests.get(url = game_query, headers = HEADERS)
	data = r.json()

	r.close()

	return data['data'][0]['name']



def get_game():
	global game
	while True:
		r = requests.get(url = q, headers = id)
		data = r.json()
		r.close()

		if data == None:
			time.sleep(60)
			continue

		if len(data['data']) == 0:
			time.sleep(60)
			continue

		game = get_game_name(data['data'][0]['game_id'], id)
		startTime = data['data'][0]['started_at']
		time.sleep(60)



def log(username, message):
	file_input = str(datetime.datetime.now().strftime('%H:%M:%S')) + " " + username + "=" + message + "\n\r"
	file = open(LOG_FILE, "a")
	file.write(file_input)
	file.close()



def get_world_record():
	global game
	if game == "Super Mario 64":
		return "SM64 70 Star - 47min 34secs by Cheese05  https://www.youtube.com/watch?v=XQZfOHDlSQE"
	elif game == "Halo 2":
		return "Halo 2 Easy - 1:15:50 by Cryphon https://www.youtube.com/watch?v=Vb80nnrNyKk"
	elif game == "Halo: Combat Evolved":
		return "Halo CE Easy - 1:10:43 by GarishGoblin https://www.youtube.com/watch?v=6CmtXwFE43c"
	else:
		return game + " (Any %) 5.51 seconds by Godd Rogers https://www.youtube.com/watch?v=z_9bvkaMI7k Krappa"


def get_tag(target, line):
	tokens = line.split(';')

	for token in tokens:
		tokenName = token.split('=')[0]

		if tokenName == target:
			return token.split('=')[1]


def getMessage(line):
	parts = line.split("#doopian :")
	try:
		message = parts[1]
		return message
	except:
		return ""



def add_klappas(count):
	output = ""

	if count > 25:
		output = "Kappa Clap (x " + str(count) + ")"
	else:
		for	i in range (0, count):
			output += "Kappa Clap "

	return output


def message_handler(irc, s, utfLine, line, quote, start_time):
	global game, kappa_message_count

	username = get_tag("display-name", line)
	bits = get_tag("bits", line)
	sub = get_tag("msg-id", line)
	gift_count = get_tag("msg-param-mass-gift-count", line)
	gift_recipient = get_tag("msg-param-recipient-display-name", line)
	months = get_tag("msg-param-months", line)
	mod = get_tag("mod", line)
	message = getMessage(line)



	if message != "" and username != None:
		print(username + ": " + message)
		log(username, message)
	else:
		return

	user = User(username)


	if sub != None and username != "doopbot":
		output = ""
		Klappas = ""

		if sub == "resub":
			Klappas = add_klappas(int(months))
			output = "Thanks for resubbing for " + months + " months " + username + "! "

		elif sub == "sub":
			Klappas = "Kappa Clap"
			output = "Thanks for subbing " + username + "! "

		elif sub == "subgift":
			Klappas = add_klappas(int(months))
			if months == "1":
				output = "Thanks for gifting a sub to " + gift_recipient + " " + username + "! "
			else:
				output = "Thanks for gifting a sub to " + gift_recipient + " " + username + "! " + gift_recipient + " has subscribed for " + months + " months in a row! "

		elif sub == "submysterygift":
			Klappas = add_klappas(int(gift_count))
			output = "Thanks for mass gifting " + gift_count + " subs to the channel " + username + "! "

		send_message(s, irc, output + Klappas)


	if bits != None:
		count = 0
		output = "Thanks for the " + bits + " bits " + username + "! "
		Klappas = add_klappas(math.ceil(int(bits) / 10))
		send_message(s, irc, output + Klappas)


	#quote section
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
	

	#For some reason, the broadcaster is not listed as a mod.
	elif message.startswith("!addquote "):
		if mod == "1" or username == "Doopian":
			send_message(s, irc, add_quote(utfLine))

	#Misc commands
	elif message == "!commands":
		send_message(s, irc, "https://pastebin.com/k9cPVTdS")

	elif contains_kappa(message):
		send_kappa_message(username, message, kappa_message_count)
		kappa_message_count += 1

	#Doop Dollars
	elif message == "!dd":
		send_message(s, irc, "You have " + str(user.getDollars()) + " Doop Dollars " + username)

    #Uptime command
	elif message == "!uptime":
		elapsed_time = int(time.time() - start_time)
		send_message(s, irc, "Doopian has been streaming for " + format_time(elapsed_time))

	elif message == "!wr":
		send_message(s, irc, get_world_record())

	elif message == "!doyourememberme":
		send_message(s, irc, "Doopian does not remember you " + username  + " Krappa")

	elif message == "!motivation":
		send_message(s, irc, ":ok_hand: SeriousSloth you got this " + username)

	#Social media dump
	elif message == "!social" and username == "Doopian":
		send_message(s, irc, "Join Doopian's discord server https://discord.gg/YBpfPQD")
		send_message(s, irc, "Follow Doopian at https://twitter.com/doopian")
		send_message(s, irc, "Subscribe to Doopian's YouTube channel at https://youtube.com/doopian")
		send_message(s, irc, "Follow Doopian on instagram https://www.instagram.com/the_kappa_fan_club")

	#All basic commands, (this used to be like 30 lines)
	try:
		if basic_commands[message] != None:
			send_message(s, irc, basic_commands[message])
	except KeyError:
		pass