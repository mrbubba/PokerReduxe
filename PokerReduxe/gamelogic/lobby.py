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

    def get_lobby(self):
        payload = {}
        for table in self.tables:
            payload[table.table_name] = [table.seats, table.sb_amount, table.bb_amount, buy_in, ante]
        return payload

    def create_table(self, name, seats, sb_amount, bb_amount, buy_in, ante=0):
        table = Table(self, name, seats, sb_amount, bb_amount, buy_in, ante)
        self.tables.append(table)
        # TODO: Raise exception if table name is not unique

    def get_table(self, table_name):
        table = [table for table in self.tables if table.table_name == table_name]
        return table

# LobbyInstance = Lobby()
