#
# This file defines the ScrabbleMatch class
#
# A ScrabbleMatch consists of a list of players (each one must be of type ScrabbleAI)
# and must also be initialized with a dictionary file that specifies the words that
# are allowed to be played
#

__author__ = 'Sebastian Wernicke'

from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleGame
from ScrabbleBot import ScrabbleUtils

import random

class ScrabbleMatch:

    def __init__(self, dictionary_file: str, player_list: list):

        self._total_scores = dict()
        self._total_matchwins = dict()
        self._player_names = set()

        self._players = []
        for p in player_list:
            if type(p) is not ScrabbleAI:
                TypeError("Player list may only contain ScrabbleAI objects")
            if p.name in self._player_names:
                ValueError("A player by the name '" + p.name + "' already exists. Each player must have a unique name")
            self._players.append(p)
            self._total_scores[p.name] = 0
            self._total_matchwins[p.name] = 0

        print("Welcome to a new Scrabble match!")

        # Load the set of allowed words
        self._legal_words = ScrabbleUtils.load_word_set(dictionary_file)

        # Build the Word Signatures, assuming 2 blanks
        # (since we only build this once, this is the most efficient)
        self._word_signatures = ScrabbleUtils.build_word_signatures(self._legal_words, 2)

    #
    # Let the players play against each other for a specified number of rounds
    # the randomize_order flag signals if player order is to be randomized for each round
    #
    def play_match(self, num_rounds: int, randomize_order: bool, verbosity: int):

        if verbosity > 0:
            print("Match is starting!")

        # Play the rounds
        for i in range(0, num_rounds):

            if randomize_order:
                random.shuffle(self._players)

            # Initialize game
            game = ScrabbleGame.ScrabbleGame(self._players, self._legal_words, self._word_signatures)

            # Play game
            tmp_result = game.play_until_finished(verbosity)

            # Keep score
            max_score = max(tmp_result)
            for j in range(0, len(tmp_result)):
                player_name = self._players[j].name
                self._total_scores[player_name] += tmp_result[j]
                if tmp_result[j] == max_score:
                    if verbosity > 0:
                        print("Player '" + player_name + "' (" + str(j) + ") wins!")
                    self._total_matchwins[player_name] += 1

            print("Round " + str(i) + " |  game score: " + str(tmp_result) +
                  "   total matchwins:" + str(self._total_matchwins))

    def get_total_scores(self):
        return self._total_scores

    def get_total_matchwins(self):
        return self._total_matchwins