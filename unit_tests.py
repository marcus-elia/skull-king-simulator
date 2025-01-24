#!/usr/bin/env python3

import unittest

from card import *
from deck import *
from player import *
from trick import *

class TestCards(unittest.TestCase):
    def test_sorting_hand(self):
        green1 = SuitCard(Suit.Parrot, 1)
        yellow5 = SuitCard(Suit.TreasureMap, 5)
        purple14 = SuitCard(Suit.TreasureChest, 14)
        black1 = SuitCard(Suit.JollyRoger, 1)
        black14 = SuitCard(Suit.JollyRoger, 14)
        pirate = PirateCard()
        mermaid = MermaidCard()
        escape = EscapeCard()
        skull_king = SkullKingCard()
        tigress = TigressCard()
        hand = [yellow5, tigress, black1, green1, pirate, skull_king, purple14, mermaid, escape, black14]
        hand.sort(key=lambda x: x.power, reverse=False)
        self.assertEqual(hand[0], escape)
        self.assertEqual(hand[1], green1)
        self.assertEqual(hand[2], yellow5)
        self.assertEqual(hand[3], purple14)
        self.assertEqual(hand[4], black1)
        self.assertEqual(hand[5], black14)
        self.assertEqual(hand[6], mermaid)
        pirate_or_tigress_is_7th = (hand[7] == pirate or hand[7] == tigress)
        self.assertTrue(pirate_or_tigress_is_7th)
        pirate_or_tigress_is_8th = (hand[8] == pirate or hand[8] == tigress)
        self.assertTrue(pirate_or_tigress_is_8th)
        self.assertEqual(hand[9], skull_king)

        # Make sure escape tigress is sorted correctly
        tigress.escape()
        hand.sort(key=lambda x: x.power, reverse=False)
        tigress_is_0th_or_1st = (hand[0] == tigress or hand[1] == tigress)
        self.assertTrue(tigress_is_0th_or_1st)

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
        # Comparison without a trump suit
        self.assertTrue(green14.defeats_no_trump(EscapeCard()))
        self.assertTrue(black1.defeats_no_trump(green14))
        self.assertFalse(yellow5.defeats_no_trump(green14))

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
        self.assertEqual(player.make_bid(4), 0)
        # Round one with a winning card
        player.get_hand([PirateCard()])
        self.assertEqual(player.make_bid(4), 1)
        # Round 8 with 3 winners and 5 losers
        player.get_hand([PirateCard(), SkullKingCard(), MermaidCard(),\
                EscapeCard(), EscapeCard(), SuitCard(Suit.Parrot, 5), EscapeCard(), SuitCard(Suit.TreasureMap, 2)])
        self.assertEqual(player.make_bid(4), 3)
        # Round 8 with 1 winner and 3 maybes
        player.get_hand([SkullKingCard(), SuitCard(Suit.JollyRoger, 12), SuitCard(Suit.JollyRoger, 3), TigressCard(),\
                EscapeCard(), EscapeCard(), SuitCard(Suit.Parrot, 5), EscapeCard()])
        self.assertEqual(player.make_bid(4), 3)

    def test_play_card_at_index(self):
        player = Player()
        trick = Trick([Player(), player, Player(), Player()], 0)
        pirate = PirateCard()
        green5 = SuitCard(Suit.Parrot, 5)
        escape = EscapeCard()
        player.get_hand([pirate, green5, escape])
        player.determine_illegal_indices(trick)
        self.assertEqual(player.hand[0], escape)
        self.assertEqual(player.hand[1], green5)
        self.assertEqual(player.hand[2], pirate)
        player.play_card_at_index(1)
        self.assertEqual(len(player.hand), 2)
        self.assertEqual(player.hand[0], escape)
        self.assertEqual(player.hand[1], pirate)
        player.determine_illegal_indices(trick)
        player.play_card_at_index(0)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(player.hand[0], pirate)

    def test_contains_mermaid(self):
        player = Player()
        mermaid = MermaidCard()
        green5 = SuitCard(Suit.Parrot, 5)
        player.get_hand([mermaid, green5])
        self.assertTrue(player.contains_mermaid())
        player.get_hand([green5])
        self.assertFalse(player.contains_mermaid())

    def test_contains_pirate(self):
        player = Player()
        pirate = PirateCard()
        tigress = TigressCard()
        green5 = SuitCard(Suit.Parrot, 5)
        player.get_hand([pirate, green5, tigress])
        self.assertTrue(player.contains_pirate())
        player.get_hand([green5, tigress])
        self.assertTrue(player.contains_pirate())
        player.get_hand([green5])
        self.assertFalse(player.contains_pirate())

    def test_contains_skull_king(self):
        player = Player()
        skull_king = SkullKingCard()
        green5 = SuitCard(Suit.Parrot, 5)
        player.get_hand([skull_king, green5])
        self.assertTrue(player.contains_skull_king())
        player.get_hand([green5])
        self.assertFalse(player.contains_skull_king())

    def test_can_follow_trump_suit(self):
        player1 = Player()
        player1.get_hand([SuitCard(Suit.Parrot, 5), EscapeCard(), PirateCard()])
        # Can't follow suit due to not having trump suit
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(SuitCard(Suit.TreasureChest, 14))
        self.assertFalse(player1.can_follow_trump_suit(trick))
        # Can follow suit
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(SuitCard(Suit.Parrot, 14))
        self.assertTrue(player1.can_follow_trump_suit(trick))
        # Can't follow suit due to there not being a trump
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(EscapeCard())
        self.assertFalse(player1.can_follow_trump_suit(trick))

    def test_determine_illegal_indices(self):
        player1 = Player()
        player1.get_hand([SuitCard(Suit.Parrot, 5), EscapeCard(), SuitCard(Suit.TreasureChest, 2), PirateCard(), SuitCard(Suit.JollyRoger, 5)])
        # A yellow card is played, so can't play a green or black card
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(SuitCard(Suit.TreasureChest, 14))
        player1.determine_illegal_indices(trick)
        self.assertEqual(player1.legal_index_holder.indices, [0, 1, 4])
        # An escape is played, so any card is legal
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(EscapeCard())
        player1.determine_illegal_indices(trick)
        self.assertEqual(player1.legal_index_holder.indices, [0, 1, 2, 3, 4])
        # Black card is played, can't play green or yellow
        trick = Trick([Player(), player1, Player(), Player()], 0)
        trick.play_card(SuitCard(Suit.JollyRoger, 8))
        player1.determine_illegal_indices(trick)
        self.assertEqual(player1.legal_index_holder.indices, [0, 3, 4])

    def test_play_random_card(self):
        player1 = Player()
        player1.get_hand([SuitCard(Suit.Parrot, 5), EscapeCard(), SuitCard(Suit.TreasureChest, 2), PirateCard(), SuitCard(Suit.JollyRoger, 5)])
        trick = Trick([Player(), player1, Player(), Player()], 0)
        player1.determine_illegal_indices(trick)
        self.assertEqual(len(player1.hand), 5)
        player1.play_random_card()
        self.assertEqual(len(player1.hand), 4)

    def test_play_leading_card(self):
        player1 = Player()
        trick = Trick([Player(), player1, Player(), Player()], 0)
        green5 = SuitCard(Suit.Parrot, 5)
        escape = EscapeCard()
        yellow2 = SuitCard(Suit.TreasureChest, 2)
        pirate = PirateCard()
        black5 = SuitCard(Suit.JollyRoger, 5)
        player1.get_hand([green5, escape, yellow2, pirate, black5])
        player1.make_bid(4)
        self.assertEqual(player1.bid, 1)
        player1.determine_illegal_indices(trick)
        card = player1.choose_leading_card(4)
        self.assertEqual(card, green5)

    def test_indices_of_potential_winning_cards(self):
        player1 = Player()
        player1.get_hand([SuitCard(Suit.Parrot, 5), EscapeCard(), SuitCard(Suit.TreasureChest, 2), PirateCard(), SuitCard(Suit.JollyRoger, 5)])
        trick = Trick([Player(), player1, Player(), Player()], 3)
        trick.play_card(SuitCard(Suit.Parrot, 6))
        self.assertEqual(player1.indices_of_potential_winning_cards(trick), [3, 4])

class TestTrick(unittest.TestCase):
    def test_card_index_to_player_index(self):
         trick = Trick([Player(), Player(), Player(), Player()], 2)
         self.assertEqual(trick.card_index_to_player_index(0), 3)
         self.assertEqual(trick.card_index_to_player_index(1), 0)
         self.assertEqual(trick.card_index_to_player_index(2), 1)
         self.assertEqual(trick.card_index_to_player_index(3), 2)

    def test_violates_trump_suit(self):
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        green2 = SuitCard(Suit.Parrot, 2)
        yellow8 = SuitCard(Suit.TreasureChest, 8)
        black1 = SuitCard(Suit.JollyRoger, 1)
        pirate = PirateCard()
        escape = EscapeCard()
        self.assertFalse(trick.violates_trump_suit(green2))
        self.assertFalse(trick.violates_trump_suit(yellow8))
        self.assertFalse(trick.violates_trump_suit(black1))
        self.assertFalse(trick.violates_trump_suit(pirate))
        self.assertFalse(trick.violates_trump_suit(escape))
        trick.play_card(escape)
        self.assertFalse(trick.violates_trump_suit(green2))
        self.assertFalse(trick.violates_trump_suit(yellow8))
        self.assertFalse(trick.violates_trump_suit(black1))
        self.assertFalse(trick.violates_trump_suit(pirate))
        self.assertFalse(trick.violates_trump_suit(escape))
        trick.play_card(green2)
        self.assertFalse(trick.violates_trump_suit(green2))
        self.assertTrue(trick.violates_trump_suit(yellow8))
        self.assertTrue(trick.violates_trump_suit(black1))
        self.assertFalse(trick.violates_trump_suit(pirate))
        self.assertFalse(trick.violates_trump_suit(escape))

    def test_would_win(self):
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        green14 = SuitCard(Suit.Parrot, 14)
        green10 = SuitCard(Suit.Parrot, 10)
        green6 = SuitCard(Suit.Parrot, 6)
        green2 = SuitCard(Suit.Parrot, 2)
        yellow8 = SuitCard(Suit.TreasureChest, 8)
        black1 = SuitCard(Suit.JollyRoger, 1)
        trick.play_card(green6)
        self.assertFalse(trick.would_win(green2))
        self.assertFalse(trick.would_win(yellow8))
        self.assertTrue(trick.would_win(green10))
        self.assertTrue(trick.would_win(green14))
        self.assertTrue(trick.would_win(black1))
        trick.play_card(green14)
        self.assertFalse(trick.would_win(green10))

    def test_play_card(self):
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        green14 = SuitCard(Suit.Parrot, 14)
        green10 = SuitCard(Suit.Parrot, 10)
        green6 = SuitCard(Suit.Parrot, 6)
        green2 = SuitCard(Suit.Parrot, 2)
        black1 = SuitCard(Suit.JollyRoger, 1)
        black14 = SuitCard(Suit.JollyRoger, 14)
        yellow5 = SuitCard(Suit.TreasureChest, 5)
        pirate1 = PirateCard()
        pirate2 = PirateCard()
        mermaid = MermaidCard()
        tigress = TigressCard()
        skull_king = SkullKingCard()
        escape1 = EscapeCard()
        escape2 = EscapeCard()

        # Simple test. The dealer is the first player. The person left of the dealer plays a high parrot.
        # Everyone else plays a low parrot.
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green10)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green6)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)

        # The same thing in reverse order
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green6)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green6)
        self.assertEqual(trick.current_winning_index, 1)
        trick.play_card(green10)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green10)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 3)

        # Parrot gets trumped by jolly roger
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green6)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(black1)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, black1)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, black1)
        self.assertEqual(trick.current_winning_index, 2)

        # Starting with escape cards
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(escape1)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, escape1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(escape2)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, escape1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(yellow5)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 2)

        # Pirate takes trick
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(black1)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, black1)
        self.assertEqual(trick.current_winning_index, 1)
        trick.play_card(mermaid)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, mermaid)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(pirate1)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 3)

        # Pirate starts trick, so no trump
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(pirate1)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green2)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(mermaid)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(pirate2)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 0)

        # Mermaid is first non-escape, so no trump
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(escape1)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, escape1)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(mermaid)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, mermaid)
        self.assertEqual(trick.current_winning_index, 1)
        trick.play_card(black1)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, mermaid)
        self.assertEqual(trick.current_winning_index, 1)
        trick.play_card(green14)
        self.assertIsNone(trick.trump_suit)
        self.assertEqual(trick.current_winning_card, mermaid)
        self.assertEqual(trick.current_winning_index, 1)

        # Tigress as pirate
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green6)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(tigress)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, tigress)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, tigress)
        self.assertEqual(trick.current_winning_index, 2)

        # Tigress as escape
        tigress.escape()
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green14)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green6)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(tigress)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green14)
        self.assertEqual(trick.current_winning_index, 0)

        # Skull king wins
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(yellow5)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(pirate1)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, pirate1)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(skull_king)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, skull_king)
        self.assertEqual(trick.current_winning_index, 3)

        # Skull king doesn't win
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(green2)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(yellow5)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, green2)
        self.assertEqual(trick.current_winning_index, 0)
        trick.play_card(skull_king)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, skull_king)
        self.assertEqual(trick.current_winning_index, 2)
        trick.play_card(mermaid)
        self.assertEqual(trick.trump_suit, Suit.Parrot)
        self.assertEqual(trick.current_winning_card, mermaid)
        self.assertEqual(trick.current_winning_index, 3)

    def test_bonus_points(self):
        trick = Trick([Player(), Player(), Player(), Player()], 0)
        trick.play_card(SuitCard(Suit.Parrot, 2))
        trick.play_card(SuitCard(Suit.TreasureChest, 13))
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 0)
        trick.play_card(SuitCard(Suit.Parrot, 14))
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 10)
        trick.play_card(SuitCard(Suit.JollyRoger, 14))
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 30)
        trick.play_card(MermaidCard())
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 30)
        trick.play_card(PirateCard())
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 50)
        trick.play_card(SkullKingCard())
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 60)
        trick.play_card(MermaidCard())
        self.assertEqual(bonus_points(trick.cards_played, trick.current_winning_card), 70)

if __name__ == '__main__':
    unittest.main()
