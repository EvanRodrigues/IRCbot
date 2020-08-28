import requests
import time
import datetime

from Settings import channel_name, CLIENT_ID, CLIENT_SECRET
from HaloGames import halo_games
from Tools import format_time
from Tools import send_message

start_time = ""
game = ""
stream_info = {}


class MessageHandler:
    socket = None
    irc = None

    def __init__(self, socket, irc, stream):
        self.socket = socket
        self.irc = irc
        self.stream = stream

    def get_token(self):
        url = "https://id.twitch.tv/oauth2/token?client_id=" + \
            CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&grant_type=client_credentials"

        response = requests.post(url)
        json = response.json()

        return json["access_token"]

    def get_uptime(self, start_time):
        if(start_time == "offline"):
            return channel_name + " is offline."

        start = datetime.datetime.strptime(
            start_time, '%Y-%m-%dT%H:%M:%SZ').timestamp()

        now = datetime.datetime.utcnow().timestamp()

        return format_time(int(now - start))

    def get_stream_info(self):
        token = self.get_token()

        url = "https://api.twitch.tv/helix/streams?user_login=asmongold"  # + channel_name
        headers = {"Authorization": "Bearer " + token, "Client-ID": CLIENT_ID}

        response = requests.get(url, headers=headers)
        json = response.json()

        if(len(json["data"]) == 0):
            return "offline"

        start_time = json["data"][0]["started_at"]
        title = json["data"][0]["title"]

        return {"start_time": start_time, "title": title}

    # Strips the fluff on the message when someone uses "/me" in chat.

    def strip_highlight(self, message):
        if message.startswith("\\x01ACTION"):
            message = message[11:-4]

        return message

    def get_tag_val(self, tag):
        return tag.split("=")[1]

    # Splits the server response into a python dict

    def get_message_data(self, server_response):
        message_data = {}
        response_tags = server_response.split(";")

        for tag in response_tags:
            if tag.startswith("display-name"):  # user name to lowercase
                message_data["display-name"] = self.get_tag_val(tag).lower()

            elif tag.startswith("badges"):
                message_data["broadcaster"] = (
                    True if "broadcaster" in self.get_tag_val(tag) else False
                )

            elif tag.startswith("mod"):
                message_data["mod"] = True if self.get_tag_val(
                    tag) == "1" else False

            elif tag.startswith("user-type"):  # what was typed
                message_parts = tag.split(channel_name + " :")
                message_data["message"] = message_parts[len(
                    message_parts) - 1][:-1]

        return message_data

    def get_world_record(self):
        game = self.stream.game
        # have stream info grabbed every minute
        # get game
        # if mcc -> get title of stream
        print(self.stream.game)

        if game == "Halo: The Master Chief Collection":
            print("Get title to determine sub-game")
        else:
            try:
                abbreviation = halo_games[game]
                print("Get record from haloruns")
            except:
                print("Get record from speedrun.com")

        # haloruns_url = "https://haloruns.com/api/"
        # url = "https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1"
        # runner_url = "https://www.speedrun.com/api/v1/users/"

        # response = requests.get(url)
        # json = response.json()
        # run_url = json["data"]["runs"][0]["run"]["videos"]["links"][0]["uri"]
        # run_time = json["data"]["runs"][0]["run"]["times"]["realtime"]
        # runner_id = json["data"]["runs"][0]["run"]["players"][0]["id"]

        # runner_response = requests.get(runner_url + runner_id)
        # json = runner_response.json()
        # runner = json["data"]["names"]["international"]
        # send_message(self.socket, self.irc, "SM64 70 Star WR by " + runner +
        #              " in " + run_time + " " + run_url)

        # TODO: Get the current game that I'm streaming
        # send a query to speedrun.com
        # could hardcode id of game and category also....
        # Flow: Get name from twitch -> get abbreviation from speedrun.com and category
        # url = "https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1"  # 70 star
        # need a haloruns url as well for halo games.
        # for random games ill go with Any% and do the flow listed above, but for games i regularly speedrun i will hardcode the speedrun.com api url and the haloruns url

    def message_handler(self, server_response):
        global start_time

        if "PRIVMSG" not in server_response:
            return

        message_data = self.get_message_data(server_response)
        print(message_data)

        # TODO: Test this while streaming.
        if(message_data["message"] == "!uptime"):
            uptime = ""

            if(start_time == ""):
                stream_info = self.get_stream_info()

            send_message(self.socket, self.irc,
                         (self.get_uptime(stream_info["start_time"])))

        elif(message_data["message"] == "!wr"):
            self. get_world_record()
            return 1


# import requests

# import time
# import datetime
# import math

# from Quote import Quote
# from Quote import add_quote
# import Tools
# import Treasure
# from User import User

# from ConnectionVars import CLIENT_ID


# SETTINGS = Tools.get_settings()
# channel_name = SETTINGS["channel_name"]
# bot_name = SETTINGS["bot_name"]
# currency = SETTINGS["currency_name"]


# kappa_message_count = 0
# game = ""
# startTime = None
# id = {"Client-ID": CLIENT_ID}
# q = "https://api.twitch.tv/helix/streams?user_login=" + channel_name
# # LOG_FILE = Tools.create_log("./Data/Stream_Logs/")
# basic_commands = Tools.set_commands()


# def get_game_name(gameID, HEADERS):
#     game_query = "https://api.twitch.tv/helix/games?id=" + gameID

#     r = requests.get(url=game_query, headers=HEADERS)
#     data = r.json()

#     r.close()

#     return data["data"][0]["name"]


# def get_game():
#     global game
#     while True:
#         r = requests.get(url=q, headers=id)
#         data = r.json()
#         r.close()

#         if data == None:
#             time.sleep(60)
#             continue

#         print(data)

#         # if len(data["data"]) == 0:
#         #     time.sleep(60)
#         #     continue

#         # game = get_game_name(data["data"][0]["game_id"], id)
#         time.sleep(60)


# # def log(username, message):
# #     file_input = (
# #         str(datetime.datetime.now().strftime("%H:%M:%S"))
# #         + " "
# #         + username
# #         + "="
# #         + message
# #         + "\n\r"
# #     )
# #     file = open(LOG_FILE, "a")
# #     file.write(file_input)
# #     file.close()


# # TODO:
# # Use speedrun.com API to get the time and video
# def get_world_record():
#     global game
#     if game == "Super Mario 64":
#         return "SM64 70 Star - 47min 34secs by Cheese05  https://www.youtube.com/watch?v=XQZfOHDlSQE"
#     elif game == "Halo 2":
#         return "Halo 2 Easy - 1:15:50 by Cryphon https://www.youtube.com/watch?v=Vb80nnrNyKk"
#     elif game == "Halo: Combat Evolved":
#         return "Halo CE Easy - 1:10:43 by GarishGoblin https://www.youtube.com/watch?v=6CmtXwFE43c"
#     else:
#         return (
#             game
#             + " (Any %) 5.51 seconds by Godd Rogers https://www.youtube.com/watch?v=z_9bvkaMI7k Krappa"
#         )


# def get_tag(target, line):
#     tokens = line.split(";")

#     for token in tokens:
#         tokenName = token.split("=")[0]

#         if tokenName == target:
#             return token.split("=")[1]


# # Gets the message portion of the server response
# def getMessage(line):
#     global channel_name
#     # IRC channel is lower case
#     channel = channel_name.lower()

#     parts = line.split("#" + channel + " :")
#     try:
#         message = parts[1]
#         return message
#     except:
#         return ""


# def add_klappas(count):
#     output = ""

#     if count > 25:
#         output = "Kappa Clap (x " + str(count) + ")"
#     else:
#         for i in range(0, count):
#             output += "Kappa Clap "

#     return output


# def message_handler(irc, s, utfLine, mission, raffle, line, quote, songList, start_time):
#     global game, kappa_message_count, bot_name, channel_name

#     try:
#         username = get_tag("display-name", line).lower()
#         bits = get_tag("bits", line)
#         sub = get_tag("msg-id", line)
#         gift_count = get_tag("msg-param-mass-gift-count", line)
#         gift_recipient = get_tag("msg-param-recipient-display-name", line)
#         months = get_tag("msg-param-cumulative-months", line)
#         mod = get_tag("mod", line)
#         message = getMessage(line).rstrip("'")  # .rstrip() strips new line.``
#     except AttributeError:
#         return

#     if message != "" and username != None:
#         print(username + ": " + message)
#         log(username, message)
#     else:
#         return

#     user = User(username)

#     if sub != None and username != bot_name:
#         output = ""
#         Klappas = ""

#         if sub == "resub":
#             Klappas = add_klappas(int(months))
#             output = "Thanks for resubbing for " + months + " months " + username + "! "
#         elif sub == "sub":
#             Klappas = "Kappa Clap"
#             output = "Thanks for subbing " + username + "! "

#         elif sub == "subgift":
#             Klappas = add_klappas(int(months))
#             if months == "1":
#                 output = (
#                     "Thanks for gifting a sub to "
#                     + gift_recipient
#                     + " "
#                     + username
#                     + "! "
#                 )
#             else:
#                 output = (
#                     "Thanks for gifting a sub to "
#                     + gift_recipient
#                     + " "
#                     + username
#                     + "! "
#                     + gift_recipient
#                     + " has subscribed for "
#                     + months
#                     + " months in a row! "
#                 )

#         elif sub == "submysterygift":
#             Klappas = add_klappas(int(gift_count))
#             output = (
#                 "Thanks for mass gifting "
#                 + gift_count
#                 + " subs to the channel "
#                 + username
#                 + "! "
#             )

#         Tools.send_message(s, irc, output + Klappas)

#     if bits != None:
#         output = "Thanks for the " + bits + " bits " + username + "! "
#         Klappas = add_klappas(math.ceil(int(bits) / 10))
#         Tools.send_message(s, irc, output + Klappas)

#     # quote section
#     if message == "!quote" and quote.active == False:
#         quote.run(s, irc, None, username)
#     elif message.startswith("!quote ") and quote.active == False:
#         quoteIndex = None

#         try:
#             quoteIndex = int(message.split(" ")[1].strip("\n"))
#         except ValueError:
#             Tools.send_message(
#                 s,
#                 irc,
#                 "Please use a positive integer when searching quotes " + username,
#             )
#             return

#         quote.run(s, irc, quoteIndex, username)

#     # For some reason, the broadcaster is not listed as a mod.
#     elif message.startswith("!addquote "):
#         if mod == "1" or username == channel_name:
#             Tools.send_message(s, irc, add_quote(utfLine))

#     # Song Request Section
#     if message == "!requests on" and username == channel_name:
#         if songList.on == True:
#             Tools.send_message(s, irc, "Song requests are already on")
#         else:
#             songList.on = True
#             Tools.send_message(s, irc, "Song requests are now on")
#     elif message == "!requests off" and username == channel_name:
#         if songList.on == False:
#             Tools.send_message(s, irc, "Song requests are already off")
#         else:
#             songList.on = False
#             Tools.send_message(s, irc, "Song requests are now off")

#     # Mod only command to remove a song from the SongList.
#     elif message.startswith("!remove "):
#         if mod == "1" or username == channel_name:
#             index_start = message.find(" ")
#             index = message[index_start + 1:]
#             if index.isnumeric():
#                 index_int = int(index)
#                 songList.removeSong(index_int)
#             else:
#                 Tools.send_message(
#                     s, irc, "Please use a positive integer " + username)

#     # Mod only command to update a song on the SongList.
#     elif message.startswith("!update "):
#         if mod == "1" or username == channel_name:
#             message_parts = message.split(" ")
#             index = message_parts[1]
#             new_title = " "
#             new_title = new_title.join(message_parts[2:])

#             if index.isnumeric():
#                 index_int = int(index)
#                 songList.updateSong(index_int, new_title)
#             else:
#                 Tools.send_message(
#                     s, irc, "Please use a positive integer " + username)

#     elif message.startswith("!request "):
#         if songList.on == False:
#             Tools.send_message(s, irc, "Song requests are off " + username)
#             return

#         song_start = message.find(" ")
#         song = message[song_start + 1:]

#         if len(song) < 55:
#             songList.addSong(song, username)
#         else:
#             Tools.send_message(
#                 s, irc, "That song name is too long " + username)

#     elif message == "!songs":
#         Tools.send_message(
#             s,
#             irc,
#             channel_name
#             + "'s songs can be found here: https://doop-songs.000webhostapp.com",
#         )
#     elif message == "!currentsong":
#         songList.currentSong()
#     elif message == "!nextsong":
#         songList.nextSong()
#     elif message == "!list":
#         songList.printList()
#     elif message == "!mysong":
#         songList.mySong(username)
#     elif message == "!pop" and username == channel_name:
#         songList.pop()

#     # Mission commands
#     elif message == "!mission":
#         mission.addUsers(username)

#     # Treasure Chest commands
#     elif message == "!mytreasure":
#         Tools.send_message(s, irc, Treasure.treasure_to_message(username))
#     elif message == "!loot":
#         Treasure.reward(s, irc, username)

#     # Raffle commands
#     elif message == "!raffle" and username == channel_name:
#         raffle.run()
#     elif message == "!mytickets":
#         print(raffle.getBet(username))
#     elif message.startswith("!addtickets "):
#         bet = message.split(" ")[1]

#         if raffle.canBet(user, bet):
#             raffle.bet(user, int(bet))

#     elif message.startswith("!removetickets"):
#         remove = message.split(" ")[1]

#         if raffle.canRemove(user, remove):
#             raffle.remove(user, int(remove))

#     # Misc commands
#     elif Tools.contains_kappa(message):
#         Tools.send_kappa_message(username, message, kappa_message_count)
#         kappa_message_count += 1

#     # Doop Dollars
#     elif message == "!dd":
#         Tools.send_message(
#             s,
#             irc,
#             "You have " + str(user.getDollars()) + " " +
#             currency + " " + username,
#         )

#     # Uptime command
#     elif message == "!uptime":
#         elapsed_time = int(time.time() - start_time)
#         Tools.send_message(
#             s,
#             irc,
#             channel_name + " has been streaming for " +
#             Tools.format_time(elapsed_time),
#         )

#     elif message == "!wr":
#         Tools.send_message(s, irc, get_world_record())

#     elif message == "!doyourememberme":
#         Tools.send_message(
#             s, irc, channel_name + " does not remember you " + username + " Krappa"
#         )

#     elif message == "!motivation":
#         Tools.send_message(
#             s, irc, ":ok_hand: SeriousSloth you got this " + username)

#     # All basic commands, (this used to be like 30 lines)
#     try:
#         if basic_commands[message] != None:
#             Tools.send_message(s, irc, basic_commands[message])
#     except KeyError:
#         pass
