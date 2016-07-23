__author__ = 'mark'
from table import Table
from deck import Card


class HandUnit(object):
    """
    List of Lists denoting every conceivable combination of made hands
    """

    def __init__(self):
        self.strFlush = {"face_value": type(int), "hole": []}
        self.quads = {"face_value": type(int), "hole": type(int),
                      "kicker": type(int), "hole_kicker": type(bool)}
        self.flush = {
            "face_value1": type(int), "face_value2": type(int),
            "face_value3": type(int), "face_value4": type(int), "face_value5": type(int),
            "hole": []}  # hole will be 1 or 2 card values

        self.straight = {"face_value": type(int), "hole": []}  # hole will be 1 or 2 card values

        self.trips = {"face_value": type(int), "hole": type(int),
                      "first_kicker": type(int), "first_hole_kicker": type(bool),
                      "second_kicker": type(int), "second_hole_kicker": type(bool)}

        self.trips2 = {"face_value": type(int), "hole": type(int),
                       "first_kicker": type(int), "first_hole_kicker": type(bool),
                       "second_kicker": type(int), "second_hole_kicker": type(bool)}

        self.pair = {"face_value": type(int), "hole": type(int),
                     "first_kicker": type(int), "first_hole_kicker": type(bool),
                     "second_kicker": type(int), "second_hole_kicker": type(bool),
                     "third_kicker": type(int), "third_hole_kicker": type(bool)}

        self.pair2 = {"face_value": type(int), "hole": type(int),
                     "first_kicker": type(int), "first_hole_kicker": type(bool),
                     "second_kicker": type(int), "second_hole_kicker": type(bool),
                     "third_kicker": type(int), "third_hole_kicker": type(bool)}

        self.pair3 = {"face_value": type(int), "hole": type(int),
                     "first_kicker": type(int), "first_hole_kicker": type(bool),
                     "second_kicker": type(int), "second_hole_kicker": type(bool),
                     "third_kicker": type(int), "third_hole_kicker": type(bool)}


class MadeHand(object):
    """
    Defines MadeHands for the AI
    Attributes:

        table(obj): The Table object
        player(obj): A Player object
        cc(List): list of the community cards
        hole(List): list of the hole cards

        The following are the MadeHand lists and their formats

        Quads(List):  [face value, kicker( if applicable),
                    boolean value which True if the kicker in the hole
        Trips(List):  [face value, number of trip cards in hole, first kicker,
                    boolean value True if the Kicker in the hole, second kicker bool if in hole]



    """

    def __init__(self, table, player):
        self.player = player
        self.table = table
        self.cc = self.table.community_cards
        self.hole = self.player.hole
        self.hand = []
        self.hand_unit = player.handunit

    def _matching_values(self):
        for x in self.cc:
            self.hand.append(x)

        for x in self.hole:
            self.hand.append(x)

        seen = {}
        for card in self.hand:
            if card.value in seen:
                seen[card.value] += 1
            else:
                seen[card.value] = 1

        return seen

    def _is_quads(self, seen):
        """check for 4 of a kind in hand"""

        for card in seen:
            if seen[card] == 4:
                self.hand_unit.quads["face_value"] = card

        # how many of the quad cards are in the whole
        # if self.hand_unit.quads['face_value']:


        # are these board quads? If not then add the Kicker to the self.quad list
        # first, find the highest Kicker
        if self.hand_unit.quads['face_value']:
            kicker = -1
            for card in self.hand:
                if card.value != self.hand_unit.quads and card.value > kicker:
                    kicker = card.value
            self.hand_unit.quads.append(kicker)
            # Is the Kicker a community card? If so self.quads.append(False) else True
            for c in self.table.community_cards:
                if kicker == c.value:
                    self.hand_unit.quads['hole_kicker'] = False
            if not self.hand_unit.quads['hole_kicker']:
                self.hand_unit.quads['hole_kicker'] = True

    def _is_trips(self, seen):
        """Check for trips"""
        tmp_trips = []
        for card in seen:
            if seen[card] == 3:
                tmp_trips.append(card)

        if len(tmp_trips) == 1:
            self.hand_unit.trips['face_value'] = [tmp_trips[0]]

        if len(tmp_trips) == 2:
            first_trip = tmp_trips[0]
            second_trip = tmp_trips[1]
            if first_trip > second_trip:
                self.hand_unit.trips['face_value'] = first_trip
                self.hand_unit.trips2['face_value'] = second_trip
            else:
                self.hand_unit.trips['face_value'] = second_trip
                self.hand_unit.trips2['face_value'] = first_trip







                # are these boards trips? If not then add the Kicker to the self.trips list
                # first, find the highest Kicker
