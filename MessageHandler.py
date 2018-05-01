import requests

import time
import datetime

from Quote import Quote
from Quote import add_quote
from Tools import send_message
from Tools import create_log

from ConnectionVars import CLIENT_ID


game = ""
startTime = None
id = {'Client-ID': CLIENT_ID}
q = "https://api.twitch.tv/helix/streams?user_login=doopian"
LOG_FILE = create_log()



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
	message = parts[1]

	return message



def message_handler(irc, s, utfLine, line, quote):
	global game

	username = get_tag("display-name", line)
	bits = get_tag("bits", line)
	message = getMessage(line)
	print(username + ": " + message)

	if username != None:
		log(username, message)	
		

	if bits != None:
		count = 0
		output = "Thanks for the " + bits + " bits " + username + "! "
		Klappas = ""

		if int(bits) > 2500:
			Klappas = "Kappa Clap (x " + bits[:-2] + ")"
		else:
			while count < int(bits):
				Klappas += "Kappa Clap "
				count += 100

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
	elif message.startswith("!addquote ") and username == "Doopian":
		message = message.split("!addquote ")[1].strip("\n")
		send_message(s, irc, add_quote(utfLine))



	elif message == "!songs":
		send_message(s, irc, "https://doop-songs.000webhostapp.com/")



	elif message == "!commands":
		send_message(s, irc, "https://pastebin.com/k9cPVTdS")


	#TODO:
	#Put these commands in an array to save lines of code. 
	#Store them in a file and load them in?


	#random commands
	elif  message == "!subscribe":
		send_message(s, irc, "Here's a link to subscribe if you're on mobile: https://subs.twitch.tv/doopian")
	elif message == "!wr":
		send_message(s, irc, get_world_record())
	elif message == "!protoss":
		send_message(s, irc, "Protoss are Love, Protoss are Life, for Aiur!!")
	elif message == "!cuck":
		send_message(s, irc, "TheDoc213")
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
		send_message(s, irc, "Check in doopian's panels to see the current schedule.")
	elif message == "!plugdj":
		send_message(s, irc, "request songs here -> https://plug.dj/doopian-song-requests")
	elif message == "!customs":
		send_message(s, irc, "Download clonehero.")
	elif message == "!motivation":
		send_message(s, irc, ":ok_hand: SeriousSloth you got this " + username)
	elif message == "!prime":
		send_message(s, irc, "https://i.imgur.com/fBf3v1r.png")
	elif message == "!gentlebob":
		send_message(s, irc, "http://i.imgur.com/AkTtU0c.jpg")
	elif message == "!marble":
		send_message(s, irc, "This is not marble racing. This will never be marble racing. You are in the wrong chat room. Stop using the !marble command please. Thanks!")
	elif message == "!twitter":
		send_message(s, irc, "Follow Doopian at http://twitter.com/doopian")
	elif message == "!youtube":
		send_message(s, irc, "Subscribe to Doopian's channel for Guitar Hero related videos at https://youtube.com/doopian")
	elif message == "!facebook":
		send_message(s, irc, "Like Doopian's facebook here https://www.facebook.com/doopian")
	elif message == "!instagram":
		send_message(s, irc, "https://www.instagram.com/the_kappa_fan_club")
	elif message == "!discord":
		send_message(s, irc, "Here is Doopian's discord server https://discord.gg/YBpfPQD")
	elif message == "!social" and username == "Doopian":
		send_message(s, irc, "Join Doopian's discord server https://discord.gg/YBpfPQD")
		send_message(s, irc, "Follow Doopian at https://twitter.com/doopian")
		send_message(s, irc, "Subscribe to Doopian's YouTube channel at https://youtube.com/doopian")
		send_message(s, irc, "Follow Doopian on instagram https://www.instagram.com/the_kappa_fan_club")
		send_message(s, irc, "Like Doopian's facebook here http://www.facebook.com/doopian")