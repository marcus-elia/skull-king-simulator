#!/usr/bin/env python3

from enum import Enum
import random

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

class LegalIndexHolder():
    def __init__(self):
        self.indices = []
        self.up_to_date = False

    def update(self, illegal_indices, num_cards):
        if len(illegal_indices) == num_cards:
            # If every card is illegal, then all are legal
            self.indices = illegal_indices
        else:
            self.indices = [i for i in range(num_cards) if not i in illegal_indices]
        self.up_to_date = True

    def get_random_legal_index(self):
        index_of_legal_index = random.randint(0, len(self.indices) - 1)
        return self.indices[index_of_legal_index]

class Player():
    def __init__(self):
        self.score = 0
        self.hand = []
        self.bid = -1
        self.tricks_won = 0
        self.legal_index_holder = LegalIndexHolder()

    def get_hand(self, hand):
        self.tricks_won = 0
        self.hand = hand
        self.sort_hand()

    def sort_hand(self):
        self.hand.sort(key=lambda x: x.power, reverse=False)

    def make_bid(self, num_players):
        num_tricks = len(self.hand)
        if num_tricks == 1:
            winning_chances = evaluate_winning_chances(self.hand[0])
            if winning_chances == WinningChances.High or winning_chances == WinningChances.Likely:
                self.bid = 1
                return 1
            else:
                self.bid = 0
                return 0
        else:
            expected_wins = 0
            for card in self.hand:
                winning_chances = evaluate_winning_chances(card)
                if winning_chances == WinningChances.High:
                    expected_wins += 1
                elif winning_chances == WinningChances.Likely:
                    expected_wins += 0.7
                elif winning_chances == WinningChances.Possible:
                    expected_wins += 0.4
                elif winning_chances == WinningChances.Unlikely:
                    expected_wins += 0.2
                else:
                    expected_wins += 0
            tricks_per_player = num_tricks / num_players
            if round(expected_wins) - round(tricks_per_player) > 2:
                self.bid = int(round(expected_wins) - 1)
            self.bid = int(round(expected_wins))
        
        if self.bid == 0:
            self.make_tigress_escape()
        return self.bid

    def win_trick(self):
        self.tricks_won += 1
        if self.tricks_won >= self.bid:
            self.make_tigress_escape()

    def make_tigress_escape(self):
        for card in self.hand:
            if card.card_category == CardCategory.Tigress:
                card.escape()

    def contains_mermaid(self):
        for card in self.hand:
            if card.card_category == CardCategory.Mermaid:
                return True
        return False

    def contains_pirate(self):
        for card in self.hand:
            if card.is_pirate():
                return True
        return False

    def contains_skull_king(self):
        for card in self.hand:
            if card.card_category == CardCategory.SkullKing:
                return True
        return False

    def play_card_at_index(self, i):
        if not self.legal_index_holder.up_to_date:
            raise ValueError("Developer error: Must call `determine_illegal_indices()` before playing a card.")
        card = self.hand[i]
        del self.hand[i]
        self.legal_index_holder.up_to_date = False
        return card

    def can_follow_trump_suit(self, trick):
        if trick.trump_suit == None:
            return False
        for card in self.hand:
            if card.card_category == CardCategory.Suit and card.suit == trick.trump_suit:
                return True
        return False

    def determine_illegal_indices(self, trick):
        illegal_indices = []
        if trick.trump_suit == None:
            pass
        else:
            for i in range(len(self.hand)):
                if self.hand[i].card_category == CardCategory.Suit and self.hand[i].suit != trick.trump_suit:
                    illegal_indices.append(i)
        self.legal_index_holder.update(illegal_indices, len(self.hand))

    def play_random_card(self):
        card_index = self.legal_index_holder.get_random_legal_index()
        return self.play_card_at_index(card_index)

    def play_pirate(self):
        for i in range(len(self.hand)):
            if self.hand[i].is_pirate():
                return self.play_card_at_index(i)
        return self.play_random_card()

    def play_mermaid(self):
        for i in range(len(self.hand)):
            if self.hand[i].card_category == CardCategory.Mermaid:
                return self.play_card_at_index(i)
        return self.play_random_card()

    def play_skull_king(self):
        for i in range(len(self.hand)):
            if self.hand[i].card_category == CardCategory.SkullKing:
                return self.play_card_at_index(i)
        return self.play_random_card()

    def play_weakest_card(self):
        return self.play_card_at_index(self.legal_index_holder.indices[0])

    def play_weakest_winning_card(self, trick):
        indices_of_winning_cards = self.indices_of_potential_winning_cards(trick)
        if len(indices_of_winning_cards) == 0:
            return self.play_random_card()
        else:
            index = indices_of_winning_cards[0]
            return self.play_card_at_index(index)

    def play_strongest_losing_card(self):
        indices_of_winning_cards = self.indices_of_potential_winning_cards(trick)
        for i in range(len(self.legal_index_holder.indices) - 1, -1, -1):
            if not i in indices_of_winning_cards:
                return self.play_card_at_index(self.legal_index_holder.indices[i])
        return self.play_random_card()

    def play_strongest_non_special_card(self):
        for i in range(len(self.legal_index_holder.indices) - 1, -1, -1):
            if self.hand[self.legal_index_holder.indices[i]].card_category == CardCategory.Suit:
                return self.play_card_at_index(self.legal_index_holder.indices[i])
        return self.play_random_card()

    def play_strongest_plain_suit_card(self):
        for i in range(len(self.legal_index_holder.indices) - 1, -1, -1):
            index = self.legal_index_holder.indices[i]
            card = self.hand[index]
            if card.card_category == CardCategory.Suit and card.suit != Suit.JollyRoger:
                return self.play_card_at_index(index)
        return self.play_random_card()

    def choose_leading_card(self, num_players):
        expected_bid = round(len(self.hand) / num_players)
        if self.bid == 0 or self.bid < expected_bid:
            return self.play_weakest_card()
        elif self.bid > expected_bid:
            return self.play_strongest_plain_suit_card()
        else:
            return self.play_strongest_plain_suit_card()

    def indices_of_potential_winning_cards(self, trick):
        indices = []
        for i in range(len(self.hand)):
            if trick.would_win(self.hand[i]):
                indices.append(i)
        return indices

    def can_win(self, trick):
        return len(self.indices_of_potential_winning_cards(trick)) > 0

    def choose_closing_card(self, trick):
        if self.tricks_won >= self.bid:
            return self.play_weakest_card()
        winning_indices = self.indices_of_potential_winning_cards(trick)
        if len(winning_indices) > 0:
            return self.play_weakest_winning_card(trick)
        else:
            return self.play_weakest_card()

    def choose_and_play_card(self, trick, num_players):
        if self.tricks_won >= self.bid:
            return self.play_weakest_card()
        elif trick.contains_mermaid() and self.contains_pirate():
            return self.play_pirate()
        elif trick.contains_pirate() and self.contains_skull_king():
            return self.play_skull_king()
        elif trick.contains_skull_king() and self.contains_mermaid():
            return self.play_mermaid()
        elif self.can_win(trick):
            return self.play_weakest_winning_card(trick)
        else:
            return self.play_weakest_card()

    def print_hand(self):
        s = '['
        for card in self.hand:
            s += str(card)
            s += ', '
        return s[:(len(s) - 2)] + ']'
