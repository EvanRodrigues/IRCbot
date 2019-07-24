import datetime
import time
import sys
from os.path import exists


TREASURE_FILE = "./Data/Treasure.txt"
KAPPA_COUNT_FILE = "./Data/Kappa.txt"
KAPPA_FACES_FILE = "./Data/KappaFaces.txt"
POINTS_FILE = "./Data/Points.txt"
SONG_FILE = "B:/Clone Hero Stuff/Clone Hero/currentsong.txt"
CURRENT_SONG_FORMATTED = "./Data/CurrentSong.txt"
COMMANDS_FILE = "./Data/Commands.txt"


# KAPPAS = load_emotes()

KAPPAS = ["Kappa", "Keepo", "KappaRoss", "KappaPride", "KappaClaus", "doopKappa", "KappaWealth", "GoldenKappa", "KappaChief", "KappaG", "KappaHD", "KappaR", "KrappaW",  "Kapp", "Krap", "Krapp", "Krappa",
          "KrappaT", "KrappaPls", "KrappaPride", "KappaW", "KrappaRoss", "doopiaGrey", "doopBottle", "Kepapo", "Krepapo", "Krabpa", "doopiaXD", "YesHaha", "DarkMode", "doopKeepo", "doopiaGrey", "HolidayCookie"]


# TODO: Load emotes from a file and insert them into an array
def load_emotes():
    output = []
    file = open(EMOTE_FILE, "r")

    for line in file:
        output.append(line)

    return output


def contains_kappa(message):
    words = message.split(" ")

    for word in words:
        if word in KAPPAS:
            return True


def send_kappa_message(username, message, kappa_message_count):
    kappa_info = str(kappa_message_count) + "_" + \
        username + "=" + message + "\n\r"

    kappa_file = open(KAPPA_COUNT_FILE, "a")
    kappa_file.write(kappa_info)
    kappa_file.close()


# Goes through the commands file
# For each line, this function grabs the command and the output
# RETURNS: a dict of commands and outputs.
# GOAL: create an object to store simple commands. reduces boiler plate.
def set_commands():
    file = open(COMMANDS_FILE, "r")
    output = {}

    for line in file:
        split_index = line.find(":")
        command = line[0:split_index]
        command_output = line[split_index+1:]
        output[command] = command_output

    return output


# Puts settings into a dictionary
def get_settings():
    apply_line_breaks("./Data/Points.txt")
    File = open("./Data/Settings.txt", "r")
    output = {}

    for line in File:

        key = line.split(":")[0]
        val = line.split(":")[1].strip("\r\n")
        output[key] = val

    File.close()
    return output


def apply_line_breaks(file):
    File = open(file, "r")
    new_file = ""

    for line in File:
        if(line.endswith("\n") and not line.endswith("\r\n")):
            new_file += line.replace("\n", "\r\n")
        else:
            new_file += line

    File.close()
    File = open(file, "w")
    File.write(new_file)
    File.close()


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


def current_song():
    while True:
        file = open(SONG_FILE, "r")
        line = file.read()
        file.close()

        if line != "":
            song = line.split("\n")[0]
            artist = line.split("\n")[1]

            file = open(CURRENT_SONG_FORMATTED, "w")
            file.write(artist + " - " + song)
            file.close()
        else:
            file = open(CURRENT_SONG_FORMATTED, "w")
            file.write("NOTHING IS BEING PLAYED RIGHT NOW XD")
            file.close()

        time.sleep(1)


#
# Checks if a file is empty
# Returns True if file is empty. Returns False otherwise.
#
def isEmpty(filename):
    file = open(filename, "r")

    if file.read() == "":
        return True
    else:
        return False


def create_log(filepath):
    date = str(datetime.date.today()).split("-")
    year = date[0]
    month = get_month(date[1])
    day = date[2]

    filename = filepath + month + "_" + day + "_" + year + ".txt"
    count = 0
    while True:
        if exists(filename):
            count += 1
            filename = filepath + month + "_" + day + \
                "_" + year + "(" + str(count) + ")" + ".txt"
        else:
            file = open(filename, "a")
            file.write("File created")
            file.write("\r\n")
            file.close()
            return filename


def get_month(month):
    months = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
              "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    return months[month]


# Imports the points for each user from the points file.
def importPoints():
    users = []
    file = open(POINTS_FILE, "r")

    for line in file:
        username = line.split(":")[0]
        points = line.split(":")[1].strip("\n")
        temp = {'username': username, 'points': int(points)}
        users.append(temp)

    return users


def format_five(sortedUsers):
    totalUsers = 0
    count = 0
    output = ""
    while totalUsers < 5:
        if sortedUsers[count]['username'] != "doopian":
            output += "(" + str(totalUsers+1) + ") - " + \
                sortedUsers[count]['username'] + ": " + \
                str(sortedUsers[count]['points']) + " "
            totalUsers += 1
        count += 1

    return output


def get_rank(username, sortedUsers):
    count = 0

    for user in sortedUsers:
        if user["username"] == username:
            return "Your rank is " + str(count) + " out of " + str(len(sortedUsers)-1) + " with " + str(user["points"]) + " doop dollars " + username
        count += 1
    return "You are unranked " + username


# Sorts the users by their points.
# The user with the most points will be at the start of the array
def sort_users():
    users = importPoints()
    mid = int(len(users) / 2)
    left = users[0:mid]
    right = users[mid:]

    return mergeSort(left, right)


def mergeSort(left, right):
    # default to left and right incase they have length 1
    sortedL = left
    sortedR = right

    if len(left) > 1:
        midL = int(len(left) / 2)
        leftL = left[0:midL]
        leftR = left[midL:]
        sortedL = mergeSort(leftL, leftR)

    if len(right) > 1:
        midR = int(len(right) / 2)
        rightL = right[0:midR]
        rightR = right[midR:]
        sortedR = mergeSort(rightL, rightR)

    return merge(sortedL, sortedR)


def merge(left, right):
    output = []
    countL = 0
    countR = 0

    while True:
        # add right because there is nothing in left anymore
        if countL == len(left):
            output.append(right[countR])
            countR += 1
        elif countR == len(right):
            output.append(left[countL])
            countL += 1
        elif left[countL]['points'] >= right[countR]['points']:
            output.append(left[countL])
            countL += 1
        elif right[countR]['points'] >= left[countL]['points']:
            output.append(right[countR])
            countR += 1

        if countL == len(left) and countR == len(right):
            break

    return output


#
# Used to update the values of Points, XP, and Treasure
# This function uses addition by default.
# To use subtraction, input a negative value.
#
def update_file(filename, target, value):
    file = open(filename, "r")
    found = False
    temp = ""  # saves the old file information to write to a new fresh file.

    for line in file:
        if line == "\r\n":
            continue

        user = line.split(":")[0]
        oldPoints = 0.0

        try:
            oldPoints = int(line.split(":")[1])
        except ValueError:
            oldPoints = float(line.split(":")[1])
        except IndexError:
            continue

        if user == target:
            newPoints = value + oldPoints
            newLine = user + ":" + str(newPoints) + "\r\n"

            temp = temp + newLine
            found = True
        else:
            if(line.endswith("\n") and not line.endswith("\r\n")):
                temp += line.replace("\n", "\r\n")
            else:
                temp += line

    file.close()

    # No user to update, so appends the info to the file
    if found == False:
        file = open(filename, "a")
        file.write(target + ":" + str(value) + "\r\n")

    # Applies the changes to a fresh file
    else:
        file = open(filename, "w")
        file.write(temp)

    file.close()


#
# Removes the target's stats in the file. Used for the merge command.
#
def remove_user(filename, target):
    output = ""
    file = open(filename, "r")

    for line in file:
        if line.startswith("*Tier"):
            output += line
            continue

        if line.split(":")[0] != target:
            output += line

    file.close()

    newFile = open(filename, "w")
    newFile.write(output)
    newFile.close()

    return


#
# TODO:
# Replace @tier with a tuple so there doesn't need to be extra iterations of the file.
#
def update_treasure_file(target, tier, value):
    file = open(TREASURE_FILE, "r")
    found = False
    currentTier = 0
    temp = ""  # saves the old file information to write to a new fresh file.

    for line in file:
        # User has never had a chest of the tier being added.
        if line == "\n" and tier == int(currentTier) and found == False:
            newLine = target + ":" + str(value) + "\r\n" + "\r\n"
            temp += newLine
            continue

        elif line == "\n":
            temp += "\r\n"
            continue

        # Change currentTier
        if line.startswith("*Tier"):
            currentTier = line.split(" ")[1][0]
            temp += line.rstrip("\n") + "\r\n"
            continue

        user = line.split(":")[0]
        oldPoints = int(line.split(":")[1])

        # User already has an entry for a chest of that tier.
        if user == target and tier == int(currentTier):
            newPoints = value + oldPoints
            newLine = user + ":" + str(newPoints) + "\r\n"

            temp += newLine
            found = True
        else:
            if(line.endswith("\n") and not line.endswith("\r\n")):
                temp += line.replace("\n", "\r\n")
            else:
                temp += line

    file.close()  # close read-only mode
    # open in write-only mode and update the file.
    file = open(TREASURE_FILE, "w")
    file.write(temp)
    file.close()


#
# Appends the user to the end of the file
#
def append(filename, username):
    file = open(filename, "a")
    file.write(username + "\r\n")
    file.close()


def remove_top_line(filename):
    first_line = False
    file = open(filename, "r")
    output = ""

    for line in file:
        if first_line == False:
            first_line = True
            continue
        output += line

    file.close()

    file = open(filename, "w")
    file.write(output)


#
# Erases everything in a file
#
def clear_file(filename):
    open(filename, "w").close()


def convert_file(filename):
    file = open(filename, "r")
    output = ""

    for line in file:
        if line.startswith("[User]"):
            continue

        info = line.split("=")
        output += ":".join(info)

    file.close()

    file = open(filename, "w")
    file.write(output)
    file.close()


def set_kappa():
    file = open(KAPPA_FACES_FILE, "r")
    output = []

    for line in file:
        output.append(line.strip("\r\n"))

    return output
