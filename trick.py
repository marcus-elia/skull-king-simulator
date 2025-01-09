#!/usr/bin/env python3

from card import Suit

class Trick():
    def __init__(self, players, dealer_index):
        self.players = players
        self.num_players = len(players)
        self.dealer_index = dealer_index
        self.trump_suit = None
        self.current_winning_index = -1
        self.cards_played = []

    def card_index_to_player_index(self, i):
        """
        This figures out which player in the list of players
        played the ith card in the cards_played list.
        """
        return (i - self.dealer_index + 1) % self.num_players

    def card_is_played(self, card):
        pass
