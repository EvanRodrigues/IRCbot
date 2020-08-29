import socket
import time
import threading
import datetime

from Stream import Stream
from Settings import OAUTH, bot_name, channel_name
from MessageHandler import MessageHandler


class ircConnection:
    def __init__(self):
        self.HOST = "irc.twitch.tv"
        self.PORT = 6667
        self.NICK = bot_name
        self.CHANNEL = channel_name
        self.PASS = OAUTH


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


stream = Stream()
stream_thread = threading.Thread(target=stream.get_info, args=(channel_name,))
stream_thread.daemon = True
stream_thread.start()

mh = MessageHandler(s, irc, stream)

while True:
    for rawLine in str(s.recv(524288).decode("utf8")).split("\r\n"):
        server_response = str(rawLine.encode("utf8"))

        if server_response.startswith("b'PING :tmi.twitch.tv"):
            s.send(bytes("PONG :tmi.twitch.tv \r\n", "UTF-8"))
            continue

        mh.message_handler(server_response)
