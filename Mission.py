from random import randint
from Tools import send_message
from Tools import isEmpty
from Tools import append
from Tools import clear_file
from Tools import update_file
from Tools import update_treasure_file
from User import User

import threading
import time

MISSION_FILE = "./Data/MissionUsers.txt"
MISSION_FILE_TEMP = "./Data/MissionUsersTemp.txt"
TREASURE_FILE = "./Data/Treasure.txt"
USER_FILE = "./Data/Users.txt"
POINTS_FILE = "./Data/Points.txt"
LEVEL_FILE = "./Data/Levels.txt"


class Mission:
    def __init__(self, s, irc):
        self.s = s
        self.irc = irc
        self.active = False
        self.joinable = False
        self.player_count = 0
        self.queue = []
        self.player_list = []
        self.success = False
        self.refresh = 5
        self.prev = 1
        self.level = getCurrentLevel()

    #
    # Starts the mission and sets up the timers
    #
    def start(self):
        send_message(self.s, self.irc, "mission starting!")
        self.active = True

        for i in range(0, 1):
            time.sleep(7)

            if len(self.queue) > 0:
                output = self.addQueue()
                send_message(self.s, self.irc, output)

        self.isSuccess(self.s, self.irc)
        self.player_list = []
        self.lock()
        self.initialize()

    def addUsers(self, username):
        if self.active == False and self.joinable == True:
            self.run()
        elif self.joinable == False:
            send_message(self.s, self.irc,
                         "There are no missions going on right now " + username)

        if not username in self.player_list and not username in self.queue:
            self.queue.append(username)

    #
    # Adds the users from self.queue to the player_list
    # This process is meant to reduce spam in the chat.
    #
    def addQueue(self):
        output = "Added to the mission: "

        for i in range(0, len(self.queue)):
            username = self.queue[i]
            self.player_list.append(username)

            if i == len(self.queue) - 1:
                output += username
            else:
                output += username + ", "

        self.queue = []
        return output

    #
    # Loops through the MissionUsers file and rolls each user against their individual RNG
    # Uses the current level to determine the difficulty of the level
    #

    def isSuccess(self, socket, irc):
        for i in range(0, len(self.player_list)):
            if self.levelRoll() == True:
                self.success = True
                outcome = self.getMissionOutcome()
                self.prev = self.level

                if self.level != 10:
                    self.level = self.level + 1
                else:
                    self.level = 1

                setCurrentLevel(self.level)
                self.reward(outcome)
                return

        self.success = False
        outcome = self.getMissionOutcome()
        self.prev = self.level
        self.level = 1
        setCurrentLevel(self.level)
        send_message(socket, irc, outcome)

    #
    # Returns the success or failure of the current level.
    # If @success is True, this returns a winning message.
    # If @success is False, this returns a losing message.
    #

    def getMissionOutcome(self):
        file = open(LEVEL_FILE, "r")

        for line in file:
            if self.success == True and line.startswith("Win"):
                level = int(line.split(":")[0].split(" ")[1])
                if level == self.level:
                    file.close()
                    output = line.split(":")[1].strip("\r\n")
                    return output

            elif self.success == False and line.startswith("Loss"):
                level = int(line.split(":")[0].split(" ")[1])
                if level == self.level:
                    file.close()
                    output = line.split(":")[1].strip("\r\n")
                    return output

    #
    # Rewards each user xp, and Doop Dollars. Chests are random
    #
    def reward(self, outcome):
        # Make this depend on the level
        rand = randint(5, 25)
        output = ""
        chestOutput = ""

        for i in range(0, len(self.player_list)):
            user = User(self.player_list[i])
            prevLvl = user.getLevel()

            chestOutput = chestOutput + self.rewardChest(user)
            update_file(POINTS_FILE, user.username, rand)
            update_file(USER_FILE, user.username, 25)
            updatedLvl = user.getLevel()

            if updatedLvl - prevLvl > 0:
                output = (
                    output
                    + user.username
                    + " has advanced to level "
                    + str(updatedLvl)
                    + "! "
                )

        if chestOutput != "":
            chestOutput = chestOutput[0:-2] + "."

        send_message(
            self.s,
            self.irc,
            outcome + " You each earn 25xp, and " +
            str(rand) + " Doop Dollars!",
        )
        send_message(self.s, self.irc, chestOutput)
        send_message(self.s, self.irc, output)

    #
    # Rewards treasure chests to the user
    #
    def rewardChest(self, user):
        rand = randint(0, 99)
        rewarded = self.treasureRoll()
        output = ""

        if rand < 10 and rewarded == True:
            update_treasure_file(user.username, 3, 1)
            output = user.username + " found Large Treasure, "
        elif rand < 40 and rewarded == True:
            update_treasure_file(user.username, 2, 1)
            output = user.username + " found Medium Treasure, "
        elif rand < 100 and rewarded == True:
            update_treasure_file(user.username, 1, 1)
            output = user.username + " found Small Treasure, "

        return output

    def levelRoll(self):
        rand = randint(0, 99)

        if self.level % 10 == 1 and rand < 100:
            return True
        elif self.level % 10 == 2 and rand < -1:
            return True
        elif self.level % 10 == 3 and rand < 40:
            return True
        elif self.level % 10 == 4 and rand < 35:
            return True
        elif self.level % 10 == 5 and rand < 30:
            return True
        elif self.level % 10 == 6 and rand < 25:
            return True
        elif self.level % 10 == 7 and rand < 20:
            return True
        elif self.level % 10 == 8 and rand < 15:
            return True
        elif self.level % 10 == 9 and rand < 10:
            return True
        elif self.level % 10 == 0 and rand < 5:
            return True

        return False

    def treasureRoll(self):
        rand = randint(0, 99)

        if self.level % 10 == 1 and rand < 5:
            return True
        elif self.level % 10 == 2 and rand < 10:
            return True
        elif self.level % 10 == 3 and rand < 15:
            return True
        elif self.level % 10 == 4 and rand < 20:
            return True
        elif self.level % 10 == 5 and rand < 25:
            return True
        elif self.level % 10 == 6 and rand < 30:
            return True
        elif self.level % 10 == 7 and rand < 35:
            return True
        elif self.level % 10 == 8 and rand < 45:
            return True
        elif self.level % 10 == 9 and rand < 55:
            return True
        elif self.level % 10 == 0 and rand < 75:
            return True

        return False

    def lock(self):
        self.joinable = False
        self.active = False

    def initialize(self):
        time.sleep(self.refresh)
        self.joinable = True
        send_message(self.s, self.irc, getLevel(self.level))

    #
    # Sets up the Thread so missions can work simultaneously with the rest of doopbot
    #
    def run(self):
        MissionThread = threading.Thread(target=self.start, args=())
        MissionThread.daemon = True
        MissionThread.start()


#
# Checks to see if the user is already on the mission
# Returns False if they are already on the mission, and True if they aren't
#
def checkUser(filename, username):
    file = open(filename, "r")

    for line in file:
        tempName = line.replace("\n", "")

        if tempName == username:
            file.close()
            return False

    file.close()
    return True


#
# Used to figure out the chat's current progress in the story.
#
def getCurrentLevel():
    file = open(LEVEL_FILE, "r")

    line = file.readline()
    line.split(" ")

    file.close()
    return int(line[15:].replace("\n", ""))


#
# Updates the current level. If the stream resets, progress wont be lost.
#
def setCurrentLevel(level):
    file = open(LEVEL_FILE, "r")
    first = False
    output = ""

    for line in file:
        if first == False:
            output = "Current Level: " + str(level) + "\r\n"
            first = True
        else:
            if(line.endswith("\n") and not line.endswith("\r\n")):
                output += line.replace("\n", "\r\n")
            else:
                output += line

    file.close()
    file = open(LEVEL_FILE, "w")
    file.write(output)
    file.close()
    return


#
# Sets the Mission's scenario to the index'th line in the
#
def getLevel(index):
    file = open(LEVEL_FILE, "r")
    count = 0

    for line in file:
        if count == index:
            file.close
            return line.replace("\n", "")
        count += 1

    file.close()
    return None
