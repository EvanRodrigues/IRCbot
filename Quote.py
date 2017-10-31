import time
import threading

from random import randint
from Tools import send_message

QUOTE_FILE = "./Data/Quotes.txt"



class Quote():
	def __init__(self):
		self.active = False



	def print_quote(self, socket, irc, index, username):
		self.active = True
		file = open(QUOTE_FILE, encoding="utf8")
		totalQuotes = count_quotes()

		if index == None:
			index = randint(1,totalQuotes)

		if totalQuotes < index or index < 1:
			send_message(socket, irc, "Please choose an integer between 1 and " + str(totalQuotes) + " " + username)
			self.active = False
			return

		for line in file:
			if line.startswith(str(index)):
				quote = line.split("=")[1].strip("\n")
				send_message(socket, irc, "Quote " + str(index) + " - " + quote)

		file.close()
		time.sleep(25)
		self.active = False

	def run(self, socket, irc, index, username):
		QuoteThread = threading.Thread(target = self.print_quote, args = (socket, irc, index, username))
		QuoteThread.start()



def count_quotes():
	file = open(QUOTE_FILE, encoding="utf8")
	count = 0

	for line in file:
		count += 1

	file.close()
	return count


def add_quote(message):
	totalQuotes = count_quotes()

	file = open(QUOTE_FILE, "a")
	file.write(str(totalQuotes+1) + "=" + message + "\n")
	file.close()

	return "Quote " + str(totalQuotes+1) + " has been added!"

