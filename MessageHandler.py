import requests

import time
import datetime
import math

from Quote import Quote
from Quote import add_quote
import Tools
import Treasure
from User import User

from ConnectionVars import CLIENT_ID


SETTINGS = Tools.get_settings()
channel_name = SETTINGS["channel_name"]
bot_name = SETTINGS["bot_name"]
currency = SETTINGS["currency_name"]


kappa_message_count = 0
game = ""
startTime = None
id = {"Client-ID": CLIENT_ID}
q = "https://api.twitch.tv/helix/streams?user_login=" + channel_name
LOG_FILE = Tools.create_log("./Data/Stream_Logs/")
basic_commands = Tools.set_commands()


def get_game_name(gameID, HEADERS):
    game_query = "https://api.twitch.tv/helix/games?id=" + gameID

    r = requests.get(url=game_query, headers=HEADERS)
    data = r.json()

    r.close()

    return data["data"][0]["name"]


def get_game():
    global game
    while True:
        r = requests.get(url=q, headers=id)
        data = r.json()
        r.close()

        if data == None:
            time.sleep(60)
            continue

        if len(data["data"]) == 0:
            time.sleep(60)
            continue

        game = get_game_name(data["data"][0]["game_id"], id)
        time.sleep(60)


def log(username, message):
    file_input = (
        str(datetime.datetime.now().strftime("%H:%M:%S"))
        + " "
        + username
        + "="
        + message
        + "\n\r"
    )
    file = open(LOG_FILE, "a")
    file.write(file_input)
    file.close()


# TODO:
# Use speedrun.com API to get the time and video
def get_world_record():
    global game
    if game == "Super Mario 64":
        return "SM64 70 Star - 47min 34secs by Cheese05  https://www.youtube.com/watch?v=XQZfOHDlSQE"
    elif game == "Halo 2":
        return "Halo 2 Easy - 1:15:50 by Cryphon https://www.youtube.com/watch?v=Vb80nnrNyKk"
    elif game == "Halo: Combat Evolved":
        return "Halo CE Easy - 1:10:43 by GarishGoblin https://www.youtube.com/watch?v=6CmtXwFE43c"
    else:
        return (
            game
            + " (Any %) 5.51 seconds by Godd Rogers https://www.youtube.com/watch?v=z_9bvkaMI7k Krappa"
        )


def get_tag(target, line):
    tokens = line.split(";")

    for token in tokens:
        tokenName = token.split("=")[0]

        if tokenName == target:
            return token.split("=")[1]


# Gets the message portion of the server response
def getMessage(line):
    global channel_name
    # IRC channel is lower case
    channel = channel_name.lower()

    parts = line.split("#" + channel + " :")
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
        for i in range(0, count):
            output += "Kappa Clap "

    return output


def message_handler(irc, s, utfLine, mission, raffle, line, quote, songList, start_time):
    global game, kappa_message_count, bot_name, channel_name

    try:
        username = get_tag("display-name", line).lower()
        bits = get_tag("bits", line)
        sub = get_tag("msg-id", line)
        gift_count = get_tag("msg-param-mass-gift-count", line)
        gift_recipient = get_tag("msg-param-recipient-display-name", line)
        months = get_tag("msg-param-cumulative-months", line)
        mod = get_tag("mod", line)
        message = getMessage(line).rstrip("'")  # .rstrip() strips new line.
    except AttributeError:
        return

    if message != "" and username != None:
        print(username + ": " + message)
        log(username, message)
    else:
        return

    user = User(username)

    if sub != None and username != bot_name:
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
                output = (
                    "Thanks for gifting a sub to "
                    + gift_recipient
                    + " "
                    + username
                    + "! "
                )
            else:
                output = (
                    "Thanks for gifting a sub to "
                    + gift_recipient
                    + " "
                    + username
                    + "! "
                    + gift_recipient
                    + " has subscribed for "
                    + months
                    + " months in a row! "
                )

        elif sub == "submysterygift":
            Klappas = add_klappas(int(gift_count))
            output = (
                "Thanks for mass gifting "
                + gift_count
                + " subs to the channel "
                + username
                + "! "
            )

        Tools.send_message(s, irc, output + Klappas)

    if bits != None:
        output = "Thanks for the " + bits + " bits " + username + "! "
        Klappas = add_klappas(math.ceil(int(bits) / 10))
        Tools.send_message(s, irc, output + Klappas)

    # quote section
    if message == "!quote" and quote.active == False:
        quote.run(s, irc, None, username)
    elif message.startswith("!quote ") and quote.active == False:
        quoteIndex = None

        try:
            quoteIndex = int(message.split(" ")[1].strip("\n"))
        except ValueError:
            Tools.send_message(
                s,
                irc,
                "Please use a positive integer when searching quotes " + username,
            )
            return

        quote.run(s, irc, quoteIndex, username)

    # For some reason, the broadcaster is not listed as a mod.
    elif message.startswith("!addquote "):
        if mod == "1" or username == channel_name:
            Tools.send_message(s, irc, add_quote(utfLine))

    # Song Request Section
    if message == "!requests on" and username == channel_name:
        if songList.on == True:
            Tools.send_message(s, irc, "Song requests are already on")
        else:
            songList.on = True
            Tools.send_message(s, irc, "Song requests are now on")
    elif message == "!requests off" and username == channel_name:
        if songList.on == False:
            Tools.send_message(s, irc, "Song requests are already off")
        else:
            songList.on = False
            Tools.send_message(s, irc, "Song requests are now off")

    # Mod only command to remove a song from the SongList.
    elif message.startswith("!remove "):
        if mod == "1" or username == channel_name:
            index_start = message.find(" ")
            index = message[index_start + 1:]
            if index.isnumeric():
                index_int = int(index)
                songList.removeSong(index_int)
            else:
                Tools.send_message(
                    s, irc, "Please use a positive integer " + username)

    # Mod only command to update a song on the SongList.
    elif message.startswith("!update "):
        if mod == "1" or username == channel_name:
            message_parts = message.split(" ")
            index = message_parts[1]
            new_title = " "
            new_title = new_title.join(message_parts[2:])

            if index.isnumeric():
                index_int = int(index)
                songList.updateSong(index_int, new_title)
            else:
                Tools.send_message(
                    s, irc, "Please use a positive integer " + username)

    elif message.startswith("!request "):
        if songList.on == False:
            Tools.send_message(s, irc, "Song requests are off " + username)
            return

        song_start = message.find(" ")
        song = message[song_start + 1:]

        if len(song) < 55:
            songList.addSong(song, username)
        else:
            Tools.send_message(
                s, irc, "That song name is too long " + username)

    elif message == "!songs":
        Tools.send_message(
            s,
            irc,
            channel_name
            + "'s songs can be found here: https://doop-songs.000webhostapp.com",
        )
    elif message == "!currentsong":
        songList.currentSong()
    elif message == "!nextsong":
        songList.nextSong()
    elif message == "!list":
        songList.printList()
    elif message == "!mysong":
        songList.mySong(username)
    elif message == "!pop" and username == channel_name:
        songList.pop()

    # Mission commands
    elif message == "!mission":
        mission.addUsers(username)

    # Treasure Chest commands
    elif message == "!mytreasure":
        Tools.send_message(s, irc, Treasure.treasure_to_message(username))
    elif message == "!loot":
        Treasure.reward(s, irc, username)

    # Raffle commands
    elif message == "!raffle" and username == channel_name:
        raffle.run()
    elif message == "!mytickets":
        print(raffle.getBet(username))
    elif message.startswith("!addtickets "):
        bet = message.split(" ")[1]

        if raffle.canBet(user, bet):
            raffle.bet(user, int(bet))

    elif message.startswith("!removetickets"):
        remove = message.split(" ")[1]

        if raffle.canRemove(user, remove):
            raffle.remove(user, int(remove))

    # Misc commands
    elif Tools.contains_kappa(message):
        Tools.send_kappa_message(username, message, kappa_message_count)
        kappa_message_count += 1

    # Doop Dollars
    elif message == "!dd":
        Tools.send_message(
            s,
            irc,
            "You have " + str(user.getDollars()) + " " +
            currency + " " + username,
        )

    # Uptime command
    elif message == "!uptime":
        elapsed_time = int(time.time() - start_time)
        Tools.send_message(
            s,
            irc,
            channel_name + " has been streaming for " +
            Tools.format_time(elapsed_time),
        )

    elif message == "!wr":
        Tools.send_message(s, irc, get_world_record())

    elif message == "!doyourememberme":
        Tools.send_message(
            s, irc, channel_name + " does not remember you " + username + " Krappa"
        )

    elif message == "!motivation":
        Tools.send_message(
            s, irc, ":ok_hand: SeriousSloth you got this " + username)

    # All basic commands, (this used to be like 30 lines)
    try:
        if basic_commands[message] != None:
            Tools.send_message(s, irc, basic_commands[message])
    except KeyError:
        pass
