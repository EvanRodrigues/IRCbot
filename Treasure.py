from random import randint
from Tools import update_file
from Tools import update_treasure_file
from Tools import send_message

TREASURE_FILE = "./Data/Treasure.txt"
POINTS_FILE = "./Data/Points.txt"

# Opens up and rewards the user with the Doop Dollars in the treasure chest.
# Returns "You have no treasure chests" if there is none to open.


def reward(socket, irc, username):
    totalChests = getTreasure(username)
    if totalChests == ("0", "0", "0"):
        send_message(socket, irc, "You have no treasure chests " + username)
        return
    reward = 0

    for i in range(1, 4):
        reward = reward + openChests(username, i, int(totalChests[i-1]))
        update_treasure_file(username, i, (int(totalChests[i-1]) * -1))

    update_file(POINTS_FILE, username, reward)
    send_message(socket, irc, username + " found " +
                 str(reward) + " Doop Dollars from their chests!")


# Opens up every chest of the given tier that the user has.
# Can be easier if tier was the entire tuple.
def openChests(username, tier, totalChests):
    reward = 0

    for i in range(0, totalChests):
        if tier == 1:
            reward = reward + randint(5, 25)
        elif tier == 2:
            reward = reward + randint(25, 75)
        else:
            reward = reward + randint(75, 250)

    return reward


def treasure_to_message(username):
    chests = getTreasure(username)
    output = "You have "
    output += chests[0] + " small, "
    output += chests[1] + " medium, and "
    output += chests[2] + " large treasure chests " + username

    return output


#
# Creates a tuple of the amount of chests the user has at each tier.
# If the user doesn't have a chest of that tier, a tuple of 0 is added to the output.
#
def getTreasure(target):
    file = open(TREASURE_FILE)
    treasure = ()  # a tuple that will output the total chest for each tier
    found = False

    for line in file:
        if line.startswith("*Tier"):
            continue
        elif line == "\n" and found == True:  # Found user in the last tier
            found = False
            continue
        # User did not have a chest of the last tier .. adding a tuple of 0 to output
        elif line == "\n" and found == False:
            treasure = treasure + tuple("0")
            continue

        username = line.split(":")[0]
        temp_tuple = tuple(line.split(":")[1][0])

        if username == target:
            found = True
            treasure = treasure + temp_tuple

    return treasure
