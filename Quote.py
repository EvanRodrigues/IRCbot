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
				break

		file.close()
		time.sleep(25)
		self.active = False

	def run(self, socket, irc, index, username):
		QuoteThread = threading.Thread(target = self.print_quote, args = (socket, irc, index, username))
		QuoteThread.start()


#Needs to find the quote in the messy server response from twitch :)
def getQuote(line):
	parts = line.split(":!addquote ")
	quote = parts[1].strip("\n\r")
	return quote


def count_quotes():
	file = open(QUOTE_FILE, encoding="utf8")
	count = 0

	for line in file:
		count += 1

	file.close()
	return count


#takes the quote and author from message handler and adds them to the quote file.
def add_quote(message):
	totalQuotes = count_quotes()
	quote = getQuote(message)

	print("utf8 quote start")
	print(quote.encode("utf8"))
	print("utf8 quote over")

	file = open(QUOTE_FILE, "a", encoding="utf8")
	file.write(str(totalQuotes+1) + "=" + quote.replace('\\', '') + "\n")
	file.close()

	return "Quote " + str(totalQuotes+1) + " has been added!"

