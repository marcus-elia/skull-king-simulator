#!/usr/bin/env python3

import argparse
import json

from deck import *
from game_writer import GameWriter
from player import *
from trick import *

def points_from_round(players, bids, tricks_won, round_number):
    """
    These 3 lists need to be in sync.
    """
    points_per_player = []
    for i in range(len(players)):
        if bids[i] == 0:
            if len(tricks_won[i]) == 0:
                points = 10 * round_number
            else:
                points = -10 * round_number
        elif bids[i] != len(tricks_won[i]):
            points = -20 * abs(bids[i] - len(tricks_won[i]))
        else:
            points = 20 * bids[i]
            for (cards, winning_card) in tricks_won[i]:
                points += bonus_points(cards, winning_card)
        points_per_player.append(points)
        players[i].score += points
    return points_per_player

class Game():
    def __init__(self, num_players, print_bids, print_trick_results, print_dealer, print_scores_each_round, print_played_cards, print_hands_before_playing):
        self.deck = Deck(shuffle=True)
        self.num_players = num_players
        self.players = [Player() for _ in range(num_players)]
        self.dealer_index = 0
        self.scores = [0 for _ in range(num_players)]
        self.print_bids = print_bids
        self.print_trick_results = print_trick_results
        self.print_dealer = print_dealer
        self.print_scores_each_round = print_scores_each_round
        self.print_played_cards = print_played_cards
        self.print_hands_before_playing = print_hands_before_playing
        self.game_writer = GameWriter()

    def play_round(self, round_number):
        # Deal the cards and have players make bids
        if self.print_dealer:
            print("Player %d is dealing round %d." % (self.dealer_index, round_number))
        self.deck.shuffle()
        hands = self.deck.deal(self.num_players, round_number)
        self.game_writer.add_hands(round_number, hands)
        for i in range(self.num_players):
            self.players[i].get_hand(hands[i])
            self.players[i].make_bid(self.num_players)
        bids = [player.bid for player in self.players]
        self.game_writer.add_bids(round_number, bids)
        if self.print_bids:
            for i in range(len(bids)):
                print("Player %d bids %d (%s)." % (i, bids[i], self.players[i].print_hand()))
        # Corresponding to each player, we have a list of tuples (trick, winning card) representing tricks that player won
        tricks_won = [[] for _ in range(self.num_players)]

        # Do all of the tricks
        leading_player_index = (self.dealer_index + 1) % self.num_players # who leads each trick
        for trick_number in range(1, round_number + 1):
            hands_before_trick = [player.hand for player in self.players]
            if self.print_trick_results:
                print("Player %d is leading the trick." % (leading_player_index))
            trick = Trick(self.players, leading_player_index)
            for i in range(self.num_players):
                player_index = trick.card_index_to_player_index(i)
                if self.print_hands_before_playing:
                    print("Player %d's hand: %s." % (player_index, self.players[player_index].print_hand())) 
                self.players[player_index].determine_illegal_indices(trick)
                played_card = self.players[player_index].choose_and_play_card(trick, self.num_players)
                trick.play_card(played_card)
                if self.print_played_cards:
                    print("Player %d plays %s." % (player_index, str(played_card)))
            winning_player_index = trick.card_index_to_player_index(trick.current_winning_index)
            self.players[winning_player_index].win_trick()
            if self.print_trick_results:
                print("Player %d wins trick %d." % (winning_player_index, trick_number))
                print("-------------------------------")
            tricks_won[winning_player_index].append((trick.cards_played, trick.current_winning_card))
            self.game_writer.add_trick(round_number, leading_player_index, hands_before_trick, trick.cards_played, winning_player_index)
            leading_player_index = winning_player_index # update who leads the next trick

        # Give out points
        points = points_from_round(self.players, bids, tricks_won, round_number)
        for i in range(self.num_players):
            self.scores[i] += points[i]
            if self.print_scores_each_round:
                print("Player %d won %d tricks, scoring %d points, and now has %d." % (i, len(tricks_won[i]), points[i], self.players[i].score))
                print("======================================")
        self.game_writer.add_scores(round_number, list(self.scores))

        # Update the dealer
        self.dealer_index += 1
        self.dealer_index = self.dealer_index % self.num_players

    def run_game(self, output_filepath):
        for i in range(1, 11):
            self.play_round(i)
        if output_filepath:
            f = open(output_filepath, 'w')
            f.write(json.dumps(self.game_writer.data))
            f.close()

def main():
    parser = argparse.ArgumentParser(description="Run a full 10-round skull king with only computer players.")
    parser.add_argument("-n", "--num-players", type=int, required=True, help="How many players the game has")
    parser.add_argument("--print-all", action='store_true', help="Print all of the following")
    parser.add_argument("--print-bids", action='store_true', help="Print the bids at the start of each trick")
    parser.add_argument("--print-trick-results", action='store_true', help="Print the results of each trick")
    parser.add_argument("--print-dealer", action='store_true', help="Print the dealer at the start of each round")
    parser.add_argument("--print-scores-each-round", action='store_true', help="Print each player's score after each round")
    parser.add_argument("--print-played-cards", action='store_true', help="Print the card every time a card is played")
    parser.add_argument("--print-hands-before-playing", action='store_true', help="Print the player's hand right before the player chooses a card")
    parser.add_argument("--output-filepath", required=False, help="Output json path")

    args = parser.parse_args()

    game = Game(args.num_players,\
            args.print_bids or args.print_all,\
            args.print_trick_results or args.print_all,\
            args.print_dealer or args.print_all,\
            args.print_scores_each_round or args.print_all,\
            args.print_played_cards or args.print_all,\
            args.print_hands_before_playing or args.print_all)
    game.run_game(args.output_filepath)

if __name__ == "__main__":
    main() 
