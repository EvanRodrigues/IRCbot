import random


QUOTE_FILE = "./Data/Quotes.txt"


def get_quotes(quotes):
    quote_file = open(QUOTE_FILE, 'r')

    for quote in quote_file:
        quote_parts = quote.split("=\"")

        quote_id = quote_parts[0]

        quote_value = quote_parts[1].split("\"=")[0][:-1]
        quoted_user = quote_parts[1].split("\"=")[1][:-1]

        quote = Quote(quote_id, quote_value, quoted_user)

        quotes.append(quote)

    quote_file.close()


class Quote:
    def __init__(self, id, value, user):
        self.id = id
        self.quote_value = value
        self.quoted_user = user
