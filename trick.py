#!/usr/bin/env python3

from card import CardCategory, Suit, TigressMode

def card_is_escape(card):
    return card.card_category == CardCategory.Escape or (card.card_category == CardCategory.Tigress and card.tigress_mode == TigressMode.Escape)

def card_forces_no_trump(card):
    """
    Return true if the card does not set a trump suit if it is either
    the first card played or the first non-escape card played.
    """
    return card.card_category == CardCategory.Pirate or card.card_category == CardCategory.Mermaid or card.card_category == CardCategory.SkullKing\
            or (card.card_category == CardCategory.Tigress and card.tigress_mode == TigressMode.Pirate)

def determine_winning_index(cards):
    num_cards = len(cards)
    if num_cards == 0:
        raise ValueError("Cannot determine winner of empty set of cards.")
    elif num_cards == 1:
        return 0
    else:
        no_trump = False
        trump_suit = None
        seen_non_escape = False
        winning_index_so_far = 0
        winning_card_so_far = cards[0]
        for i in range(num_cards):
            if not seen_non_escape:
                if card_forces_no_trump(cards[i]):
                    no_trump = True
                    seen_non_escape = True
                    winning_index_so_far = i
                    winning_card_so_far = cards[i]
                elif card_is_escape(cards[i]):
                    pass
                else:
                    trump_suit = cards[i].suit
                    no_trump = False
                    seen_non_escape = True
                    winning_index_so_far = i
                    winning_card_so_far = cards[i]

            if cards[i].card_category == CardCategory.Suit:
                trump_suit
    trump_suit = None


class Trick():
    def __init__(self, players, dealer_index):
        self.players = players
        self.num_players = len(players)
        self.dealer_index = dealer_index
        self.trump_suit = None
        self.no_trump = False # If a special card is the first non-escape played
        self.non_escape_has_been_played = False
        self.current_winning_index = -1
        self.current_winning_card = None
        self.cards_played = []

    def card_index_to_player_index(self, i):
        """
        This figures out which player in the list of players
        played the ith card in the cards_played list.
        """
        return (i - self.dealer_index + 1) % self.num_players

    def play_card(self, card):
        self.cards_played.append(card)
        num_cards_played = len(self.cards_played)
        if num_cards_played == 1:
            self.current_winning_index = 0
            self.current_winning_card = card
            if card_is_escape(card):
                pass
            else:
                self.non_escape_has_been_played = True
                if card_forces_no_trump(card):
                    self.no_trump = True
                else:
                    self.trump_suit = card.suit
        else:
            if not self.non_escape_has_been_played:
                if card_is_escape(card):
                    pass
                else:
                    self.non_escape_has_been_played = True
                    self.current_winning_index = num_cards_played - 1
                    self.current_winning_card = card
                    if card_forces_no_trump(card):
                        self.no_trump = True
                    else:
                        self.trump_suit = card.suit
            elif self.no_trump:
                if card.defeats_no_trump(self.current_winning_card):
                    self.current_winning_index = num_cards_played - 1
                    self.current_winning_card = card
            else:
                # Finally, the normal case when there is a trump suit.
                if card.defeats(self.current_winning_card, self.trump_suit):
                    self.current_winning_index = num_cards_played - 1
                    self.current_winning_card = card
