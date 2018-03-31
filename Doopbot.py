import socket
import threading
import time
import datetime


from AutoPoints import AutoPoints
from SongList import SongList
from Mission import Mission
from Slots import Slots
from Raffle import Raffle
from Quote import Quote
from MessageHandler import MessageHandler
from MessageHandler import log


class ircConnection:
	def __init__(self):
		self.HOST = "irc.twitch.tv"
		self.PORT = 6667
		self.NICK = "doopbot"
		self.CHANNEL = "doopian"
		self.PASS = getPass()


#Just incase i stream some coding, i dont want the password out in the open.
def getPass():
	File = open("./Data/ConnectionVars.txt", "r")
	for line in File:
		return line


#Strips the fluff on the message when someone uses "/me" in chat.
def stripHighlight(message):
	if message.startswith('\\x01ACTION'):
		message = message[11:-4]
		
	return message


#Fixes issue if a user types a ':' in chat.
def combineParts(parts):
	output = ""
	for i in range(2, len(parts)):
		if i > 2:
			output += ":" + parts[i]
		else:
			output += parts[i]
	return output



#Connect to twitch's irc server
irc = ircConnection()
s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send(bytes("PASS " + irc.PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + irc.NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + irc.CHANNEL + "\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))


#Global mission/slots variable since there can only be one mission at a time.
#mission = Mission()
#slots = Slots(s, irc)
#raffle = Raffle(s, irc, 0, False, None, 200)
#songList = SongList(s, irc)

quote = Quote()
mh = MessageHandler()
ap = AutoPoints()
ap.run()

gameThread = threading.Thread(target = mh.get_game , args = ())
gameThread.daemon = True
gameThread.start()

while True:
	line = str(s.recv(1024))
	if "End of /NAMES list" in line:
		break

#
# TODO
# Have doopbot Klappa for each month someone is subscribed
# Points for new followers (Web hooks)
# Make message handler NOT object oriented
# subbing/resubbing messages from chat not showing? can test with RAIDS
#
while True:
	for line in str(s.recv(1024)).split('\\r\\n'):
		log("twitch server", line)
		print(line)
		if line == "b'PING :tmi.twitch.tv":
			s.send(bytes("PONG :tmi.twitch.tv \r\n", "UTF-8"))
			continue
		elif "JOIN #doopian" in line or "PART #doopian" in line:
			ap.updateChatters(line)


		parts = line.split(':')
		if len(parts) < 3:
			continue

		if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
			message = combineParts(parts)
			message = stripHighlight(message)

		usernamesplit = parts[1].split("!")
		username = usernamesplit[0]
		print(username + ": " + message)
		mh.message_handler(irc, s, line, quote)