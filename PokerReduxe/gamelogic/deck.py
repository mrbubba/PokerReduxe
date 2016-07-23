import random


class Card(object):
    """card objects
    attributes:

        name(str): human readable name (i.e. ten of clubs)
        value(int): a number from 2 to 14 representing the cards rank (aces are 14)
        suit(str): one letter suit designator (c, s, d, or h)
   """

    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit

    def __str__(self):
        return "Card {0} {1} {2}".format(self.name, self.suit, self.value)


class Deck(object):
    """ a collection compromising a full deck of playing card objects

    Attributes:

        deck(list):  a list of all playing card objects that remian in the deck

    Methods:

        create:  creates and instantiates all 52 unique playing card objects and appends them

                (after clearing Deck.deck) to Deck.deck then randomizes the order

        deal:  returns and erases the first card in Deck.deck (i.e. Deck.deck[0])
    """

    def __init__(self):

        self.deck = []

    def create(self):

        for value in range(2, 15):

            if value > 10:
                if value == 11:
                    name = 'Jack'
                elif value == 12:
                    name = 'Queen'
                elif value == 13:
                    name = 'King'
                elif value == 14:
                    name = 'Ace'
            else:
                name = str(value)

            self.deck.append(Card(name + " of Diamonds", value, "d"))
            self.deck.append(Card(name + " of Hearts", value, "h"))
            self.deck.append(Card(name + " of Spades", value, "s"))
            self.deck.append(Card(name + " of Clubs", value, "c"))

        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

