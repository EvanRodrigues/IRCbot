import socket
import time
import threading
import datetime

from AutoPoints import AutoPoints
from SongList import SongList
from Mission import Mission
from Slots import Slots
from Raffle import Raffle
from Quote import Quote

from Tools import get_settings
from MessageHandler import get_game
from MessageHandler import message_handler
from MessageHandler import log


SETTINGS = get_settings()


class ircConnection:
    def __init__(self):
        self.HOST = "irc.twitch.tv"
        self.PORT = 6667
        self.NICK = SETTINGS["bot_name"]
        self.CHANNEL = SETTINGS["channel_name"]
        self.PASS = getPass()


# Just incase i stream some coding, i dont want the password out in the open.
def getPass():
    File = open("./Data/ConnectionVars.txt", "r")
    for line in File:
        return line


# Strips the fluff on the message when someone uses "/me" in chat.
def stripHighlight(message):
    if message.startswith("\\x01ACTION"):
        message = message[11:-4]

    return message


# Fixes issue if a user types a ':' in chat.
def combineParts(parts):
    output = ""
    for i in range(2, len(parts)):
        if i > 2:
            output += ":" + parts[i]
        else:
            output += parts[i]
    return output


# Connect to twitch's irc server
irc = ircConnection()
s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send(bytes("PASS " + irc.PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + irc.NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + irc.CHANNEL + "\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))


# Global mission/slots variable since there can only be one mission at a time.
mission = Mission(s, irc)
missionThread = threading.Thread(target=mission.initialize, args=())
missionThread.daemon = True
missionThread.start()

#slots = Slots(s, irc)


raffle = Raffle(s, irc, 2000000)
songList = SongList(s, irc)
quote = Quote()

ap = AutoPoints()
ap.run()

gameThread = threading.Thread(target=get_game, args=())
gameThread.daemon = True
gameThread.start()

# uptime
start_time = time.time()

while True:
    line = str(s.recv(524288))
    if "End of /NAMES list" in line:
        break


# TODO
# Points for new followers (Web hooks)
while True:
    for rawLine in str(s.recv(524288).decode("utf8")).split("\r\n"):
        message = str(rawLine.encode("utf8"))
        print("SERVER RESPONSE: " + message)

        if message.startswith("b'PING :tmi.twitch.tv"):
            s.send(bytes("PONG :tmi.twitch.tv \r\n", "UTF-8"))
            continue
        elif ("JOIN #" + SETTINGS["channel_name"]) in message or (
            "PART #" + SETTINGS["channel_name"]
        ) in message:
            ap.updateChatters(message)
            continue

        message = stripHighlight(message)
        message_handler(irc, s, rawLine, mission, raffle,
                        message, quote, songList, start_time)
