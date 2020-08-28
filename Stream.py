import threading
import requests
import time

from Settings import channel_name, CLIENT_ID, CLIENT_SECRET


def get_game(token, id):
    url = "https://api.twitch.tv/helix/games?id=" + id
    headers = {"Authorization": "Bearer " +
               token, "Client-ID": CLIENT_ID}

    response = requests.get(url, headers=headers)
    json = response.json()

    return json["data"][0]["name"]


class Stream:
    def __init__(self):
        self.title = ""
        self.start_time = ""
        self.game_id = ""

    def get_token(self):
        url = "https://id.twitch.tv/oauth2/token?client_id=" + \
            CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&grant_type=client_credentials"

        response = requests.post(url)
        json = response.json()

        return json["access_token"]

    def get_info(self, channel):
        while True:
            token = self.get_token()

            url = "https://api.twitch.tv/helix/streams?user_login=" + channel
            headers = {"Authorization": "Bearer " +
                       token, "Client-ID": CLIENT_ID}

            response = requests.get(url, headers=headers)
            json = response.json()

            if(len(json["data"]) == 0):
                return "offline"

            self.start_time = json["data"][0]["started_at"]
            self.title = json["data"][0]["title"]
            self.game = get_game(token, json["data"][0]["game_id"])

            time.sleep(60)
