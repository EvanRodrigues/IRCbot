from random import randint

QUOTE_FILE = "./Data/Quotes.txt"


#add a timer
def print_quote(index, username):
	totalQuotes = count_quotes()
	file = open(QUOTE_FILE, encoding="utf8")

	if index == None:
		index = randint(1,totalQuotes)

	if totalQuotes < index or index < 1:
		return "Please choose an integer between 1 and " + str(totalQuotes) + " " + username

	for line in file:
		if line.startswith(str(index)):
			quote = line.split("=")[1].strip("\n")
			file.close()
			return "Quote " + str(index) + " - " + quote

	file.close()

def count_quotes():
	file = open(QUOTE_FILE, encoding="utf8")
	count = 0

	for line in file:
		count += 1

	return count


def add_quote(message):
	totalQuotes = count_quotes()

	file = open(QUOTE_FILE, "a")
	file.write(str(totalQuotes+1) + "=" + message + "\n")
	file.close()

	return "Quote " + str(totalQuotes+1) + " has been added!"