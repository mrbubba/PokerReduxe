import unittest

from table import Table


class TestTable(unittest.TestCase):
    """ Do we have a working table object? """

    def test_seats_dict(self):
        """ Is seats dict properly created on instantiation """


        table = Table(6,1,2)

        self.assertEqual(len(table.seats), 6)


    def test_





if __name__ == '__main__':
    unittest.main()
