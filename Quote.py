import random


QUOTE_FILE = "./Data/Quotes.txt"


def add_to_quote_file(quote):
    file = open(QUOTE_FILE, 'a')
    file.write(quote + "\r\n")
    file.close()


def get_quotes(quotes):
    quote_file = open(QUOTE_FILE, 'r')

    for quote in quote_file:
        quote_parts = quote.split("=\"")

        value = quote_parts[1].split("\"=")[0][:-1]
        user = quote_parts[1].split("\"=")[1][:-1]

        quote = Quote(value, user)

        quotes.append(quote)

    quote_file.close()


class Quote:
    def __init__(self, value, user):
        self.value = value
        self.user = user
