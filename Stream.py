import threading
import requests
import time
import random
from Quote import Quote, get_quotes
from Settings import channel_name, CLIENT_ID, CLIENT_SECRET


thread_lock = threading.Lock()


def get_game(token, id):
    name = ""
    url = "https://api.twitch.tv/helix/games?id=" + id
    headers = {"Authorization": "Bearer " +
               token, "Client-ID": CLIENT_ID}

    response = requests.get(url, headers=headers)
    json = response.json()

    try:
        name = json["data"][0]["name"]
    except:
        name = ""

    return name


class Stream:
    def __init__(self):
        self.title = ""
        self.start_time = ""
        self.game_id = ""
        self.quotes = []

    # Add the ability to search by the user that said the quote
    def getQuote(self, key):
        try:
            key_int = int(key) - 1

            if key_int < 0 or key_int > len(self.quotes):
                return "Invalid quote number!"

            return self.quotes[key_int]

        except:
            return "Invalid quote number"

        return self.quotes[key]

    def getRandomQuote(self):
        index = random.randint(0, len(self.quotes) - 1)
        quote = self.quotes[index]
        return quote

    def get_token(self):
        url = "https://id.twitch.tv/oauth2/token?client_id=" + \
            CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&grant_type=client_credentials"

        response = requests.post(url)
        json = response.json()

        return json["access_token"]

    def get_info(self, channel):
        while True:
            thread_lock.acquire()
            token = self.get_token()

            url = "https://api.twitch.tv/helix/streams?user_login=" + channel
            headers = {"Authorization": "Bearer " +
                       token, "Client-ID": CLIENT_ID}

            response = requests.get(url, headers=headers)
            json = response.json()

            get_quotes(self.quotes)

            if(len(json["data"]) == 0):
                thread_lock.release()
                return "offline"

            self.start_time = json["data"][0]["started_at"]
            self.title = json["data"][0]["title"]
            self.game = get_game(token, json["data"][0]["game_id"])
            thread_lock.release()
            time.sleep(60)
