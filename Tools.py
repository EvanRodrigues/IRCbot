import datetime
import time
import sys
from os.path import exists


def send_message(socket, irc, message):
    socket.send(bytes("PRIVMSG #" + irc.CHANNEL +
                      " :" + message + "\r\n", "UTF-8"))
    try:
        print("doopbot: " + message)
    except UnicodeEncodeError:
        # handles emojis in the console.
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        print("doopbot: " + str(message.translate(non_bmp_map)))


def format_time(uptime):
    output = ""
    hours = 0
    minutes = 0

    if uptime < 60:
        output += str(uptime) + " secs btw"
        return output

    while uptime > 60:
        if uptime >= 3600:
            hours += 1
            uptime -= 3600
        elif uptime >= 60:
            minutes += 1
            uptime -= 60

    if hours > 0:
        if hours == 1:
            output += "1 hr "
        else:
            output += str(hours) + " hrs "
    if minutes > 0:
        if minutes == 1:
            output += "1 min "
        else:
            output += str(minutes) + " mins "

    return output + "btw"
