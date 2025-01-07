#!/usr/bin/env python3

import unittest

from card import *
from deck import *


class TestCards(unittest.TestCase):
    def test_suit_card_defeats(self):
        green2 = SuitCard(Suit.Parrot, 2)
        # Compare to special cards
        self.assertFalse(green2.defeats(PirateCard(), Suit.Parrot))
        self.assertFalse(green2.defeats(MermaidCard(), Suit.Parrot))
        self.assertFalse(green2.defeats(SkullKingCard(), Suit.Parrot))
        self.assertTrue(green2.defeats(EscapeCard(), Suit.TreasureMap))
        tigress = TigressCard()
        self.assertFalse(green2.defeats(tigress, Suit.Parrot))
        tigress.escape()
        self.assertTrue(green2.defeats(tigress, Suit.JollyRoger))
        # Compare to other suit cards
        green14 = SuitCard(Suit.Parrot, 14)
        yellow5 = SuitCard(Suit.TreasureChest, 5)
        black1 = SuitCard(Suit.JollyRoger, 1)
        self.assertTrue(green14.defeats(green2, Suit.TreasureMap))
        self.assertTrue(green14.defeats(green2, Suit.Parrot))
        self.assertFalse(green2.defeats(green14, Suit.TreasureMap))
        self.assertFalse(green2.defeats(green14, Suit.Parrot))
        self.assertFalse(yellow5.defeats(green14, Suit.Parrot))
        self.assertTrue(yellow5.defeats(green14, Suit.TreasureChest))
        self.assertTrue(black1.defeats(green14, Suit.Parrot))
        self.assertTrue(black1.defeats(green14, Suit.TreasureMap))
        self.assertTrue(black1.defeats(green14, Suit.JollyRoger))
        self.assertFalse(yellow5.defeats(black1, Suit.Parrot))
        self.assertFalse(yellow5.defeats(black1, Suit.TreasureChest))
        self.assertFalse(yellow5.defeats(black1, Suit.JollyRoger))

    def test_pirate_defeats(self):
        self.assertTrue(PirateCard().defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertTrue(PirateCard().defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertTrue(PirateCard().defeats(MermaidCard(), Suit.TreasureMap))
        self.assertFalse(PirateCard().defeats(PirateCard(), Suit.TreasureMap))
        self.assertTrue(PirateCard().defeats(EscapeCard(), Suit.TreasureMap))
        self.assertFalse(PirateCard().defeats(SkullKingCard(), Suit.TreasureMap))
        tigress = TigressCard()
        self.assertFalse(PirateCard().defeats(tigress, Suit.TreasureMap))
        tigress.escape()
        self.assertTrue(PirateCard().defeats(tigress, Suit.TreasureMap))

    def test_mermaid_defeats(self):
        self.assertTrue(MermaidCard().defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertTrue(MermaidCard().defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertFalse(MermaidCard().defeats(MermaidCard(), Suit.TreasureMap))
        self.assertFalse(MermaidCard().defeats(PirateCard(), Suit.TreasureMap))
        self.assertTrue(MermaidCard().defeats(EscapeCard(), Suit.TreasureMap))
        self.assertTrue(MermaidCard().defeats(SkullKingCard(), Suit.TreasureMap))
        tigress = TigressCard()
        self.assertFalse(MermaidCard().defeats(tigress, Suit.TreasureMap))
        tigress.escape()
        self.assertTrue(MermaidCard().defeats(tigress, Suit.TreasureMap))

    def test_skull_king_defeats(self):
        self.assertTrue(SkullKingCard().defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertTrue(SkullKingCard().defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertFalse(SkullKingCard().defeats(MermaidCard(), Suit.TreasureMap))
        self.assertTrue(SkullKingCard().defeats(PirateCard(), Suit.TreasureMap))
        self.assertTrue(SkullKingCard().defeats(EscapeCard(), Suit.TreasureMap))
        tigress = TigressCard()
        self.assertTrue(SkullKingCard().defeats(tigress, Suit.TreasureMap))
        tigress.escape()
        self.assertTrue(SkullKingCard().defeats(tigress, Suit.TreasureMap))

    def test_escape_defeats(self):
        self.assertFalse(EscapeCard().defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertFalse(EscapeCard().defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertFalse(EscapeCard().defeats(MermaidCard(), Suit.TreasureMap))
        self.assertFalse(EscapeCard().defeats(PirateCard(), Suit.TreasureMap))
        self.assertFalse(EscapeCard().defeats(EscapeCard(), Suit.TreasureMap))
        self.assertFalse(EscapeCard().defeats(SkullKingCard(), Suit.TreasureMap))
        tigress = TigressCard()
        self.assertFalse(EscapeCard().defeats(tigress, Suit.TreasureMap))
        tigress.escape()
        self.assertFalse(EscapeCard().defeats(tigress, Suit.TreasureMap))

    def test_tigress_defeats(self):
        # First test Tigress as Pirate
        tigress = TigressCard()
        self.assertTrue(tigress.defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertTrue(tigress.defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertTrue(tigress.defeats(MermaidCard(), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(PirateCard(), Suit.TreasureMap))
        self.assertTrue(tigress.defeats(EscapeCard(), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(SkullKingCard(), Suit.TreasureMap))
        # Test Tigress as Escape
        tigress.escape()
        self.assertFalse(tigress.defeats(SuitCard(Suit.Parrot, 14), Suit.Parrot))
        self.assertFalse(tigress.defeats(SuitCard(Suit.JollyRoger, 8), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(MermaidCard(), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(PirateCard(), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(EscapeCard(), Suit.TreasureMap))
        self.assertFalse(tigress.defeats(SkullKingCard(), Suit.TreasureMap))

class TestDeck(unittest.TestCase):
    def test_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), DECK_SIZE)

    def test_shuffle(self):
        deck = Deck()
        unshuffled = list(deck.cards)
        deck.shuffle()
        num_same = 0
        for i in range(DECK_SIZE):
            if unshuffled[i] == deck.cards[i]:
                num_same += 1
        MAX_SHUFFLE_SIMILARITY = 0.10
        self.assertLess(num_same / DECK_SIZE, MAX_SHUFFLE_SIMILARITY)

if __name__ == '__main__':
    unittest.main()
