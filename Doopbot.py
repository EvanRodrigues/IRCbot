import socket

from Mission import Mission
from MessageHandler import message_handler

class ircConnection:
	def __init__(self):
		self.HOST = "irc.twitch.tv"
		self.PORT = 6667
		self.NICK = "doopbot"
		self.CHANNEL = "doopian"
		self.PASS = getPass()


#Just incase i stream some coding, i dont want the password out in the open.
def getPass():
	File = open("ConnectionVars.txt", "r")
	for line in File:
		return line


#Strips the fluff on the message when someone uses "/me" in chat.
def stripHighlight(message):
	if message.startswith('\\x01ACTION'):
		message = message[11:-4]
		
	return message



#Connect to twitch's irc server
irc = ircConnection()
s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send(bytes("PASS " + irc.PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + irc.NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + irc.CHANNEL + "\r\n", "UTF-8"))

#Global mission variable since there can only be one mission at a time.
mission = Mission()

while True:
	line = str(s.recv(1024))
	if "End of /NAMES list" in line:
		break

while True:
	for line in str(s.recv(1024)).split('\\r\\n'):
		parts = line.split(':')
		if len(parts) < 3:
			continue

		if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
		 	message = parts[2][:len(parts[2])]
		 	message = stripHighlight(message)

		usernamesplit = parts[1].split("!")
		username = usernamesplit[0]
		print(username + ": " + message)
		message_handler(irc, s, username, message, mission)
	
		
