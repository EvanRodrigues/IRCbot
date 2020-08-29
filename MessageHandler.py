import requests
import time
import datetime
import functools
import isodate
import random
from Settings import channel_name, CLIENT_ID, CLIENT_SECRET
from HaloGames import halo_games, halo_tags
from RandomInfo import videos, runners
from Tools import format_time
from Tools import send_message


start_time = ""
game = ""
stream_info = {}


# Gets the world record information for the abbreviated halo game
# NOTE: World records are tracked on haloruns.com not speedrun.com
def get_halo_run(abbreviation, category):
    halo_runs_url = "https://haloruns.com/api/records/" + \
        abbreviation + "/fullgame/solo/" + category

    response = requests.get(halo_runs_url)
    json = response.json()

    time = json["time"]
    game = json["game_name"]
    runner = json["runners"][0]
    video = json["vid"]

    return game + " " + category + " difficulty world record in " + time + " by " + runner + " " + video


# Generates a random time for the random world record.
def get_random_time():
    hours = "0"
    minutes = "00"
    seconds = "00"

    while hours == "0" and minutes == "00" and seconds == "00":
        hours = str(random.randrange(3))
        minutes = str(random.randrange(60)).zfill(2)
        seconds = str(random.randrange(60)).zfill(2)

    return hours + ":" + minutes + ":" + seconds


# Generates a random world record for the current game the channel is playing.
def get_random_world_record(game, category):
    video = random.choice(videos)
    runner = random.choice(runners)
    run_time = remove_leading_zeroes(get_random_time())

    return game + " " + category + " world record in " + run_time + " by " + runner + " " + video


# Removes the leading 0s for times that don't contain hours or minutes
# Example 0:12:13 -> 12:13
def remove_leading_zeroes(time):
    durations = time.split(":")

    for duration in durations:
        if duration == "0" or duration == "00":
            durations.pop(0)
        else:
            break

    return ":".join(durations)


# Removes the trailing zeroes for runs with milliseconds
# Example 4:59.656000 -> 4:59.656
def remove_trailing_zeroes(time):
    if "." not in time:
        return time

    time_split = time.split(".")
    milliseconds = time_split[1]

    for digit in reversed(milliseconds):
        if digit == "0":
            milliseconds = milliseconds[:-1]
        else:
            break

    time_split[1] = milliseconds

    return ".".join(time_split)


# Formats the run time based on total seconds
# Removes trailing zeroes and leading zeroes from time then converts the timedelta to a string
def format_run_time(seconds):
    return remove_trailing_zeroes(remove_leading_zeroes(str(datetime.timedelta(seconds=seconds))))


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

        url = "https://api.twitch.tv/helix/streams?user_login=" + channel_name
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

    # Gets the title and category of the game from the !wr command
    def get_wr_args(self, message):
        if len(message) == 4:
            return ""

        message_parts = message[4:].split(",")

        title = message_parts[0]

        try:
            category = message_parts[1].strip()
            return {"title": title, "category": category}
        except:
            return {"title": title, "category": ""}

    # Gets the world record speedrun for the game_title
    # If there is no game_title, the streamer's current directory is looked up

    def get_world_record(self, game_title, category):
        game = game_title

        print(game)
        print(category)

        if game == "":
            try:
                game = self.stream.game
            except:
                return

        if game == "Halo: The Master Chief Collection":
            title = self.stream.title
            game_tag = title.split("]")[0]
            game = game_tag[1:]
            abbreviation = halo_tags[game]
            send_message(self.socket, self.irc,
                         get_halo_run(abbreviation, category))
        else:
            try:
                abbreviation = halo_games[game]
                get_halo_run(abbreviation, category)
                send_message(self.socket, self.irc,
                             get_halo_run(abbreviation, category))
            except:
                games_url = "https://www.speedrun.com/api/v1/games?name=" + game

                response = requests.get(games_url)
                json = response.json()

                target_game = list(filter(
                    lambda g: g["names"]["international"].lower() == game.lower(), json["data"]))
                game_id = target_game[0]["id"]

                categories_url = "https://www.speedrun.com/api/v1/games/" + game_id + "/categories"
                category_response = requests.get(categories_url)
                category_json = category_response.json()

                if category == "":
                    title = self.stream.title

                    if "]" in title:
                        category = title.split("]")[0][1:]
                    else:
                        category = "Any%"

                target_category = list(
                    filter(lambda cat: cat["name"].lower() == category.lower(), category_json["data"]))
                category_id = ""

                if len(target_category) != 0:  # found category
                    category_id = target_category[0]["id"]
                else:  # did not find category
                    send_message(self.socket, self.irc,
                                 get_random_world_record(game, category))
                    return

                run_url = "https://www.speedrun.com/api/v1/leaderboards/" + \
                    game_id + "/category/" + category_id + "?top=1"
                run_response = requests.get(run_url)
                run_json = run_response.json()

                run_video = run_json["data"]["runs"][0]["run"]["videos"]["links"][0]["uri"]
                run_time = run_json["data"]["runs"][0]["run"]["times"]["primary_t"]
                runner_id = run_json["data"]["runs"][0]["run"]["players"][0]["id"]

                formatted_time = format_run_time(run_time)

                runner_url = "https://www.speedrun.com/api/v1/users/"

                runner_response = requests.get(runner_url + runner_id)
                runner_json = runner_response.json()
                runner = runner_json["data"]["names"]["international"]
                send_message(self.socket, self.irc, game + " " + category + " world record in " + formatted_time +
                             " by " + runner + " " + run_video)

    def message_handler(self, server_response):
        global start_time

        if "PRIVMSG" not in server_response:
            return

        message_data = self.get_message_data(server_response)
        print(message_data)

        if(message_data["message"] == "!uptime"):
            uptime = ""

            if(start_time == ""):
                stream_info = self.get_stream_info()

            if stream_info == "offline":
                send_message(self.socket, self.irc,
                             channel_name + " is offline")
            else:
                send_message(self.socket, self.irc,
                             (self.get_uptime(stream_info["start_time"])))

        elif(message_data["message"] == "!wr"):
            self.get_world_record("", "")
        elif(message_data["message"].startswith("!wr ")):
            args = self.get_wr_args(message_data["message"])
            self.get_world_record(args["title"], args["category"])

        elif(message_data["message"] == "!emotes"):
            send_message(self.socket, self.irc,
                         "https://akakrypt.me/projects/emotes?channel=doopian")
