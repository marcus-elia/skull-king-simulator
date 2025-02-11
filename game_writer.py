#!/usr/bin/env python3

"""
A class to store every detail about a game as it is played in a
dictionary, with the intent to write the dictionary to JSON so
the game can be analyzed and replayed.
It should work like this
[ array of dictionaries of round data
"bids" : [array of bids],
"hands" : [array of hands],
"tricks" : [array of trick info maps {"starting_index" : _, "hands" : [array of hands], "cards_played" : [array of cards], "winner_index" : _}]
"scores" : [array of scores at end of round]
]
"""

BIDS_KEY = "bids"
HANDS_KEY = "hands"
TRICKS_KEY = "tricks"

class GameWriter():
    def __init__(self):
        self.data = [{TRICKS_KEY : []} for _ in range(1, 11)]

    def add_bids(self, round_number, bids):
        self.data[round_number - 1][BIDS_KEY] = bids

    def add_hands(self, round_number, hands):
        self.data[round_number - 1][HANDS_KEY] = hands

    def add_trick(self, round_number, starting_index, hands, cards_played, winner_index):
        self.data[round_number - 1][TRICKS_KEY].append({"starting_index" : starting_index, "hands" : hands, "cards_played" : cards_played, "winner_index" : winner_index})

    def add_scores(self, round_number, scores):
        self.data[round_number - 1]["scores"] = scores
