from PokerReduxe.gamelogic.table import Table


class Lobby(object):
    """  The lobby is the container object that instantiates and holds the table objects

    Attributes:
        tables(lst):  A list of all the active tables

    Methods:
        create_table:  creates a table object and adds it to the tables list

        TODO:  remove_table:   needs to remove inactive tables (tables with 0 players)"""

    def __init__(self):
        self.tables = []

    def create_table(self, player_name, stack, table_name, seats,
                     sb_amount, bb_amount, buy_in, ante=0):
        if self.tables:
            for table in self.tables:
                if table_name == table.table_name:
                    raise Exception("Table Names must be unique.")
        table = Table(table_name, seats, sb_amount, bb_amount, buy_in, ante)
        table.join(1, player_name, stack)
        self.tables.append(table)

LobbyInstance = Lobby()
