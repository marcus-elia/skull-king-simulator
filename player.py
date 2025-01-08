#!/usr/bin/env python3

from enum import Enum

from card import CardCategory, Suit

class WinningChances(Enum):
    High = 1
    Likely = 2
    Possible = 3
    Unlikely = 4
    Loser = 5

def evaluate_winning_chances(card):
    if card.card_category == CardCategory.SkullKing or card.card_category == CardCategory.Pirate or card.card_category == CardCategory.Tigress:
        return WinningChances.High
    elif card.card_category == CardCategory.Mermaid or (card.card_category == CardCategory.Suit and card.suit == Suit.JollyRoger and card.number >= 10):
        return WinningChances.Likely
    elif card.card_category == CardCategory.Suit and card.suit == Suit.JollyRoger and card.number < 10:
        return WinningChances.Possible
    elif card.card_category == CardCategory.Suit and card.suit != Suit.JollyRoger and card.number >= 10:
        return WinningChances.Unlikely
    else:
        return WinningChances.Loser

class Player():
    def __init__(self):
        self.score = 0
        self.hand = []
        self.bid = -1

    def get_hand(self, hand):
        self.hand = hand

    def make_bid(self, num_players, first_trick_order):
        num_tricks = len(self.hand)
        if num_tricks == 1:
            winning_chances = evaluate_winning_chances(self.hand[0])
            if winning_chances == WinningChances.High or winning_chances == WinningChances.Likely:
                return 1
            else:
                return 0
        expected_wins = 0
        for card in self.hand:
            winning_chances = evaluate_winning_chances(card)
            if winning_chances == WinningChances.High:
                expected_wins += 1
            elif winning_chances == WinningChances.Likely:
                expected_wins += 0.75
            elif winning_chances == WinningChances.Possible:
                expected_wins += 0.5
            elif winning_chances == WinningChances.Unlikely:
                expected_wins += 0.25
            else:
                expected_wins += 0
        tricks_per_player = num_tricks / num_players
        if round(expected_wins) - round(tricks_per_player) > 2:
            self.bid = int(round(expected_wins) - 1)
        self.bid = int(round(expected_wins))

        return self.bid

