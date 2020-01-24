from random import randint

from Tools import send_message
from Tools import update_file
from Tools import clear_file

import threading
import time


POINTS_FILE = "./Data/Points.txt"


class Raffle:
    def __init__(self, s, irc, limit):
        self.s = s
        self.irc = irc
        self.pot = 33
        self.on = False
        self.bets = {"user1": 21, "user2": 12}
        self.limit = limit

    def run(self):
        RaffleThread = threading.Thread(target=self.start, args=())
        RaffleThread.start()

    # Starts the raffle, sets the timers for reminders in chat.
    def start(self):
        send_message(self.s, self.irc, "RAFFLE STARTING!!!")
        self.on = True

        for i in range(59, 60):
            time.sleep(40)
            if i == 20:
                send_message(self.s, self.irc,
                             "Raffle is ending in 10 minutes!")
            elif i == 40:
                send_message(self.s, self.irc,
                             "Raffle is ending in 5 minutes!")
            elif i == 56:
                send_message(self.s, self.irc, "Raffle is ending in 1 minute!")
            elif i == 58:
                send_message(self.s, self.irc,
                             "Raffle is ending in 30 seconds!")

        self.getWinner()
        self.reset()

    # Checks to see if the user is:
    # 1. Trying a combined bet over the limit
    # 2. Betting more dd than they have left
    # 3. Betting a negative integer
    # 4. Betting a non-integer value
    def canBet(self, user, bet_str):
        if self.on == False:
            return False

        try:
            bet = int(bet_str)
        except ValueError:
            send_message(self.s, self.irc,
                         "Please bet a positive integer " + user.username)
            return False

        try:
            total_bet = self.bets[user.username] + bet
        except KeyError:
            total_bet = bet

        if total_bet > self.limit:
            send_message(self.s, self.irc, "Please bet less than the limit (" +
                         str(self.limit) + "dd) " + user.username)
            return False
        elif bet > user.dollars:
            send_message(
                self.s, self.irc, "You don't have that many Doop Dollars " + user.username)
            return False
        elif bet <= 0:
            send_message(self.s, self.irc,
                         "Please bet a positive integer " + user.username)
            return False

        return True

    # Adds the bet to the self.bets dictionary
    # Updates points file to new amount
    def bet(self, user, bet):
        username = user.username

        try:
            self.bets[username] += bet
        except KeyError:
            self.bets[username] = bet

        self.pot += bet

        send_message(self.s, self.irc, "You have added " + str(bet) + " tickets to the raffle. You have " +
                     str(self.bets[username]) + " tickets in the raffle " + username)

        update_file(POINTS_FILE, username, bet * -1)

    # Gets the users bet, and odds of winning.
    # Sends this info in the chatroom.
    def getBet(self, username):
        try:
            odds = self.getWinPercentage(username)

            send_message(self.s, self.irc, "You have " +
                         str(self.bets[username]) + " tickets in the raffle  with a " + odds + "% chance of winning " + username)
        except KeyError:
            send_message(self.s, self.irc,
                         "You have not entered the raffle " + username)

    # Checks to see if the user is:
    # 1. Removing more than they've bet
    # 2. Using a non-integer value
    def canRemove(self, user, remove_str):
        if self.on == False:
            return False

        try:
            remove = int(remove_str)
        except ValueError:
            send_message(self.s, self.irc,
                         "Please use a positive integer " + user.username)
            return False

        try:
            tickets = self.bets[user.username]
        except KeyError:
            send_message(self.s, self.irc,
                         "You didn't bet that much " + user.username)
            return False

        if remove > tickets:
            send_message(self.s, self.irc,
                         "You didn't bet that much " + user.username)
            return False

        return True

    # Removes the @amount tickets from the raffle for the user.
    # Updates the pot and the points file.
    def remove(self, user, amount):
        self.bets[user.username] -= amount
        self.pot -= amount
        update_file(POINTS_FILE, user.username, amount)
        send_message(self.s, self.irc, "You have removed " + str(amount) +
                     " tickets from the raffle. You have " + str(self.bets[user.username]) + " tickets left in the raffle.")

    # Finds the winner of the raffle
    # Rewards the winner with the pot
    #
    def getWinner(self):
        winningTicket = randint(1, self.pot)
        bet_total = 0

        for user in self.bets:
            bet_total += self.bets[user]

            if bet_total >= winningTicket:
                odds = self.getWinPercentage(user)
                update_file(POINTS_FILE, user, self.pot)
                send_message(self.s, self.irc, "Winner is " + user +
                             " with a bet of " + str(self.bets[user]) + " dd and a win percentage of " + odds + "%")
                return

    # Calculates the win percentage of the user for the raffle
    # Returns a formatted string of their win percentage
    def getWinPercentage(self, username):
        percentage = (self.bets[username] / self.pot) * 100
        odds_float = float("{0:.2f}".format(percentage))
        odds = str(odds_float)

        return odds

    # Resets the raffle to default values
    def reset(self):
        self.on = False
        self.pot = 0
        self.bets = {}
