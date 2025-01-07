#!/usr/bin/env python3

import numpy as np
import time

from card import *

ALL_SUITS = (Suit.JollyRoger, Suit.Parrot, Suit.TreasureChest, Suit.TreasureMap)
MAX_SUIT_NUMBER = 14
NUM_PIRATE_CARDS = 5
NUM_MERMAID_CARDS = 2
NUM_SKULL_KING_CARDS = 1
NUM_ESCAPE_CARDS = 5
NUM_TIGRESS_CARDS = 1
DECK_SIZE = len(ALL_SUITS) * MAX_SUIT_NUMBER + NUM_PIRATE_CARDS + NUM_MERMAID_CARDS + NUM_SKULL_KING_CARDS + NUM_ESCAPE_CARDS + NUM_TIGRESS_CARDS

def choose_num_cards(num_players, round_number, deck_size):
    if num_players * round_number <= deck_size:
        return round_number
    return int(deck_size / num_players)

class Deck():
    def __init__(self, shuffle=False):
        self.cards = []
        for i in range(1, MAX_SUIT_NUMBER + 1):
            for suit in ALL_SUITS:
                self.cards.append(SuitCard(suit, i))
        self.cards = self.cards + [PirateCard() for _ in range(NUM_PIRATE_CARDS)]
        self.cards = self.cards + [MermaidCard() for _ in range(NUM_MERMAID_CARDS)]
        self.cards = self.cards + [SkullKingCard() for _ in range(NUM_SKULL_KING_CARDS)]
        self.cards = self.cards + [EscapeCard() for _ in range(NUM_ESCAPE_CARDS)]
        self.cards = self.cards + [TigressCard() for _ in range(NUM_TIGRESS_CARDS)]

        if shuffle:
            self.shuffle()
        self.shuffled = shuffle

    def shuffle(self):
        rng_seed = int(time.time() * 10000)
        rng = np.random.default_rng(seed=rng_seed)
        rng.shuffle(self.cards)
        self.shuffled = True

    def print_deck(self):
        for card in self.cards:
            print(str(card))

    def deal(self, num_players, round_number):
        if not self.shuffled:
            raise ValueError("Cannot deal unshuffled deck.")
        num_cards = choose_num_cards(num_players, round_number, DECK_SIZE)
        return [[self.cards[num_players * i + j] for i in range(num_cards)] for j in range(num_players)]
