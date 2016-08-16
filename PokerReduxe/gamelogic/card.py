
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

