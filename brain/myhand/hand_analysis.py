from gameserver.gamelogic.card import Card
from gameserver.gamelogic.player import Player


deck = []


def create_deck():
    """ Creates a deck """
    # Make a standard poker deck (14 represents an ace)

    for value in range(2, 15):

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

        deck.append(Card(name + "_Diamonds", value, "d"))
        deck.append(Card(name + "_Hearts", value, "h"))
        deck.append(Card(name + "_Spades", value, "s"))
        deck.append(Card(name + "_Clubs", value, "c"))


def hand_order(community_cards):
    """Orders every possible permutation of hole cards, and sorts them. Returns a list from best to worst."""

    create_deck()

    for card in community_cards:
        for i, o in enumerate(deck):
            if o.name == card.name:
                del deck[i]







__all__ = ['deck', 'create_deck', 'hand_order']