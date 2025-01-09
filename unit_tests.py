#!/usr/bin/env python3

import unittest

from card import *
from deck import *
from player import *
from trick import *

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

    def test_choose_num_cards(self):
        self.assertEqual(choose_num_cards(4, 2, 100), 2)
        self.assertEqual(choose_num_cards(4, 25, 100), 25)
        self.assertEqual(choose_num_cards(4, 26, 100), 25)
        self.assertEqual(choose_num_cards(8, 10, 70), 8)

    def test_deal(self):
        deck = Deck(shuffle=True)
        # Using all the cards
        NUM_PLAYERS = 7
        ROUND_NUMBER = 10
        hands = deck.deal(NUM_PLAYERS, ROUND_NUMBER)
        self.assertEqual(len(hands), NUM_PLAYERS)
        for i in range(NUM_PLAYERS):
            self.assertEqual(len(hands[i]), ROUND_NUMBER)
            for j in range(ROUND_NUMBER):
                self.assertEqual(deck.cards[j * NUM_PLAYERS + i], hands[i][j])
        # There are extra cards
        NUM_PLAYERS = 7
        ROUND_NUMBER = 3
        hands = deck.deal(NUM_PLAYERS, ROUND_NUMBER)
        self.assertEqual(len(hands), NUM_PLAYERS)
        for i in range(NUM_PLAYERS):
            self.assertEqual(len(hands[i]), ROUND_NUMBER)
            for j in range(ROUND_NUMBER):
                self.assertEqual(deck.cards[j * NUM_PLAYERS + i], hands[i][j])

        # Not enough cards
        NUM_PLAYERS = 8
        ROUND_NUMBER = 10
        num_cards = choose_num_cards(NUM_PLAYERS, ROUND_NUMBER, DECK_SIZE)
        self.assertNotEqual(ROUND_NUMBER, num_cards)
        hands = deck.deal(NUM_PLAYERS, ROUND_NUMBER)
        self.assertEqual(len(hands), NUM_PLAYERS)
        for i in range(NUM_PLAYERS):
            self.assertEqual(len(hands[i]), num_cards)
            for j in range(num_cards):
                self.assertEqual(deck.cards[j * NUM_PLAYERS + i], hands[i][j])

class TestPlayer(unittest.TestCase):
    def test_make_bid(self):
        player = Player()
        # Round one with a non-winning card
        player.get_hand([SuitCard(Suit.Parrot, 12)])
        self.assertEqual(player.make_bid(4, 1), 0)
        # Round one with a winning card
        player.get_hand([PirateCard()])
        self.assertEqual(player.make_bid(4, 1), 1)
        # Round 8 with 3 winners and 5 losers
        player.get_hand([PirateCard(), SkullKingCard(), MermaidCard(),\
                EscapeCard(), EscapeCard(), SuitCard(Suit.Parrot, 5), EscapeCard(), SuitCard(Suit.TreasureMap, 2)])
        self.assertEqual(player.make_bid(4, 8), 3)
        # Round 8 with 1 winner and 3 maybes
        player.get_hand([SkullKingCard(), SuitCard(Suit.JollyRoger, 12), SuitCard(Suit.JollyRoger, 3), TigressCard(),\
                EscapeCard(), EscapeCard(), SuitCard(Suit.Parrot, 5), EscapeCard()])
        self.assertEqual(player.make_bid(4, 8), 3)

class TestTrick(unittest.TestCase):
    def test_card_index_to_player_index(self):
         trick = Trick([Player(), Player(), Player(), Player()], 2)
         self.assertEqual(trick.card_index_to_player_index(0), 3)
         self.assertEqual(trick.card_index_to_player_index(1), 0)
         self.assertEqual(trick.card_index_to_player_index(2), 1)
         self.assertEqual(trick.card_index_to_player_index(3), 2)

if __name__ == '__main__':
    unittest.main()
