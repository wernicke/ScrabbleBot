#
# This file defines the ScrabbleGame class
#
# The idea here is that a ScrabbleMatch will initiate a set
# of ScrabbleGames
#
#
# TODO: The option for bots to exchange letters has yet to be implemented
#

__author__ = 'Sebastian Wernicke'

from ScrabbleBot import ScrabbleUtils
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleAI

from random import shuffle


#
# List of all English Scrabble pieces with duplicates
#
def get_letter_pieces() -> list:
    return ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B',
            'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E',
            'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F',
            'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I',
            'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L',
            'L', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O',
            'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q',
            'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S',
            'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U',
            'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z', '*', '*']


#
# Values of al Scrabble letters.
# '*' represents a blank piece
#
def get_letter_values() -> dict:
    return {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
            'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
            'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
            'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10, '*': 0}


#
# Class to draw random tiles from until they are out
#
class LetterSet:

    def __init__(self):
        self._remaining_letters = get_letter_pieces()
        shuffle(self._remaining_letters)

    def draw(self, num_letters: int) -> list:
        count = 0
        ret = []
        while count < num_letters and len(self._remaining_letters) > 0:
            ret.append(self._remaining_letters.pop())
            count += 1
        return ret

    def empty(self) -> bool:
        return len(self._remaining_letters) == 0

    def exchange_letters(self, old_letters: list) -> list:
        if len(old_letters) > len(self._remaining_letters):
            print("Warning: Not enough letters to exchange, will give back less")
        ret = []
        while len(self._remaining_letters) > 0 and len(ret) < len(old_letters):
            ret.append(self._remaining_letters.pop())
        self._remaining_letters.append(old_letters)
        shuffle(self._remaining_letters)
        return ret


class ScrabbleGame:

    def __init__(self, players: list, legal_words: set, word_signatures: dict):
        self._board = ScrabbleBoard.ScrabbleBoard()
        self._legal_words = legal_words
        self._word_signatures = word_signatures
        self._players = []
        self._move_history = []
        self._scores = []
        self._player_letters = []
        self._current_player = 0
        self._letter_values = get_letter_values()
        self._game_finished = False
        self._letter_bag = LetterSet()
        self._numplayers = len(players)
        self._rounds_without_move = 0
        if self._numplayers > 4:
            TypeError("Maximum number of players is 4")
        for p in players:
            if type(p) != ScrabbleAI:
                TypeError("All players must be of type 'ScrabbleAI'")
            self._players.append(p)
            self._scores.append(0)
            self._player_letters.append(self._letter_bag.draw(7))

    def game_started(self) -> bool:
        return len(self._move_history) > 0

    def game_finished(self) -> bool:
        return self._game_finished

    def finish_game(self):
        self._game_finished = True
        # Subtract penalties for leftover letters
        for i in range(0, self._numplayers):
            for l in self._player_letters[i]:
                self._scores[i] -= self._letter_values[l]

    def play_one_move(self, verbosity: int) -> ScrabbleUtils.ScrabbleMove:

        if verbosity >= 1:
            print("\nPlayer " + str(self._current_player) + "'s turn:")

        # As a service to the AI, we pre-calculate the legal moves
        current_letters = "".join(self._player_letters[self._current_player])
        solutions = self._board.possible_moves(current_letters, self._letter_values,
                                               self._legal_words, self._word_signatures)

        # Let the player tell us what they want to play
        next_move = self._players[self._current_player].make_move(self._board, current_letters, solutions)

        # Play the move (if it's possible)
        if next_move is not None:

            #TODO: Implement possibility for bots to trigger a letter exchange

            # Score the move (implicitly checks whether it's legal, too)
            move_score = self._board.check_legal_and_score_move(next_move, self._letter_values, self._legal_words)

            if move_score == -1:
                ValueError("Illegal move detected!")

            self._scores[self._current_player] += move_score

            # Play the move
            self._board.execute_move(next_move)
            if verbosity >= 1:
                ScrabbleUtils.print_move(next_move)
                print("For " + str(move_score) + " points.")
            if verbosity >= 2:
                self._board.print()

            # Remove old letters and draw new letters
            current_letterset = self._player_letters[self._current_player]
            #print(current_letterset)
            num_letters = len(next_move.letters)
            for char in next_move.letters:
                current_letterset.remove(char)
                #print(current_letterset)
            current_letterset.extend(self._letter_bag.draw(num_letters))
            #print(current_letterset)
            self._rounds_without_move = 0
        else:
            self._rounds_without_move += 1

        if verbosity > 0:
            print("Scores: " + str(self._scores))

        # Game ends when there are no moves left for anyone
        if self._rounds_without_move == self._numplayers:
            self.finish_game()
            return

        # Game ends when all letters have been drawn and someone uses last letter
        if self._letter_bag.empty() and len(self._player_letters[self._current_player]) == 0:
            self.finish_game()
            return

        # Switch to next player
        self._current_player = (self._current_player + 1) % self._numplayers

    def play_until_finished(self, verbosity: int) -> list:
        while not self.game_finished():
            self.play_one_move(verbosity)
        if verbosity >= 1:
            print("Final scores: " + str(self._scores))
        return self._scores
