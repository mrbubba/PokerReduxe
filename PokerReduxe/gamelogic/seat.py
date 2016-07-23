__author__ = 'mark'


class Seat(object):
    """  Seat object up to nine max

    Attributes:

        name(str): name of seat (ie seat 1, seat 2, etc)
        active(boolean):  is this seat currently in the game?
        player(obj):  player  currently occupying seat
    """
    def __init__(self, name):
        name = name
        active = False
        player = None
