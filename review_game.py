#!/usr/bin/env python3

import argparse
import json

from game_writer import BIDS_KEY, HANDS_KEY, TRICKS_KEY

def main():
    parser = argparse.ArgumentParser(description="Read a saved game's JSON and go through the steps one at a time.")
    parser.add_argument("-f", "--json-filepath", required=True, help="Path to JSON file of the game you want to review")

    args = parser.parse_args()
    f = open(args.json_filepath, 'r')
    json_data = json.loads(f.read())
    f.close()

    num_players = len(json_data[0][BIDS_KEY])
    dealer_index = 0
    for round_index in range(10):
        round_number = round_index + 1
        print("\n===== Round %d ======" % (round_number))
        # Display each player's hand
        for player_index in range(num_players):
            player_number = player_index + 1
            print("Player %d's hand: " % (player_number) + str(json_data[round_index][HANDS_KEY][player_index]))
        
        # State who is dealing
        dealer_number = dealer_index + 1
        print("Player %d is dealing." % (dealer_number))

        # Display the bids
        for player_index in range(num_players):
            player_number = player_index + 1
            print("Player %d bids %d." % (player_number, json_data[round_index][BIDS_KEY][player_index]))

        # Iterate over the tricks
        leader_index = dealer_index + 1
        for trick_index in range(round_number):
            trick_number = trick_index + 1
            leader_number = leader_index + 1
            print("\t----- Trick %d -----" % (trick_number))

            # State who is leading the trick
            print("\tPlayer %d is leading." % (leader_number))
            current_player_index = leader_index
            for card in json_data[round_index][TRICKS_KEY][trick_index]["cards_played"]:

                # Display each player's card that is played
                current_player_number = current_player_index + 1
                print("\t\tPlayer %d plays %s." % (current_player_number, card))
                current_player_index += 1
                current_player_index = current_player_index % num_players

            # State who won the trick
            winner_index = json_data[round_index][TRICKS_KEY][trick_index]["winner_index"]
            winner_number = winner_index + 1
            print("\tPlayer %d won trick %d." % (winner_number, trick_number))
            leader_index = winner_index

        # Display the scores
        print("After round %d, the scores are:" % (round_number))
        for player_index in range(num_players):
            player_number = player_index + 1
            print("Player %d: %d" % (player_number, json_data[round_index]["scores"][player_index])) 

        dealer_index = dealer_index + 1
        dealer_index = dealer_index % num_players

if __name__ == "__main__":
    main() 
