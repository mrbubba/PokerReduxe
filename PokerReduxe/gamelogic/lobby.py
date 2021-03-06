from table import Table


class Lobby(object):
    """  The lobby is the container object that instantiates and holds the table objects

    Attributes:
        tables(lst):  A list of all the active tables

    Methods:
        create_table:  creates a table object and adds it to the tables list

        TODO:  remove_table:   needs to remove inactive tables (tables with 0 players)"""

    def __init__(self):
        self.tables = []

    def create_table(self, seats, sb_amount, bb_amount, buy_in, ante=0):
        table = Table(self, seats, sb_amount, bb_amount, buy_in, ante)
        self.tables.append(table)
