#
# This file defines a ScrabbleBoard class on which games can be played.
#
# This is the main 'workhorse' for playing a game and has the following methods:
#  - Class initialization with an empty board
#  - Return all possible next moves as a list of ScrabbleMoves (including scores)
#  - Execute a ScrabbleMove
#  - Conversion to string
#  - Pretty printing
#

__author__ = 'Sebastian Wernicke'

from ScrabbleBot import ScrabbleUtils


#
# Returns an empty board
#
def get_empty_board() -> list:
    return [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


#
# Encoding of the scrabble board and it's special field properties
# 0 = blank   2 = double letter   3 = triple letter
# 4 = double word   6 = triple word
#
def get_board_multipliers() -> list:
    return [[6, 0, 0, 2, 0, 0, 0, 6, 0, 0, 0, 2, 0, 0, 6],
            [0, 4, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 4, 0],
            [0, 0, 4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 4, 0, 0],
            [2, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 2],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0],
            [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
            [6, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 6],
            [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
            [0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [2, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 2],
            [0, 0, 4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 4, 0, 0],
            [0, 4, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 4, 0],
            [6, 0, 0, 2, 0, 0, 0, 6, 0, 0, 0, 2, 0, 0, 6]]


class ScrabbleBoard:

    # Initialize an empty board
    def __init__(self):
        self._board = get_empty_board()
        self._multipliers = get_board_multipliers()
        self._blank_locations = get_empty_board()

    def get(self, row: int, col: int):
        return self._board[row][col]

    # Returns a list of possible ScrabbleMoves on the board for a given string of letters
    # Requires pointer to letter values, allowed words, and the word signature dictionary
    def possible_moves(self, letters: str, letter_values: dict,
                       legal_words: set, word_signatures: dict) -> list:
        if len(letters) > 7:
            TypeError("Letters must be a string no longer than 7 characters")
        return ScrabbleUtils.find_all_moves(self._board, letters, legal_words,
                                            self._multipliers, letter_values, word_signatures)

    def check_legal_and_score_move(self, move: ScrabbleUtils.ScrabbleMove, letter_values: dict, legal_words: set) -> int:
        if move.how == "across":
            if ScrabbleUtils.score_play_across(move.word, move.row, move.col, self._board, self._multipliers,
                                               letter_values, legal_words, False) > -1:
                tmp = list(move.word)
                for pos in move.blank_positions:
                    tmp[pos] = '*'
                word = "".join(tmp)
                return ScrabbleUtils.score_play_across(word, move.row, move.col, self._board, self._multipliers,
                                                       letter_values, legal_words, False)
            else:
                return -1
        elif move.how == "down":
            if ScrabbleUtils.score_play_down(move.word, move.row, move.col, self._board, self._multipliers,
                                             letter_values, legal_words, False) > -1:
                tmp = list(move.word)
                for pos in move.blank_positions:
                    tmp[pos] = '*'
                word = "".join(tmp)
                return ScrabbleUtils.score_play_down(word, move.row, move.col, self._board, self._multipliers,
                                                     letter_values, legal_words, False)
            else:
                return -1
        else:
            return -1

    # Execute a ScrabbleMove on the board (with some error checking)
    def execute_move(self, move: ScrabbleUtils.ScrabbleMove):
        if move.how == "down":
            for i in range(0, len(move.word)):
                letter_on_board = self._board[move.row + i][move.col]
                if letter_on_board != ' ' and letter_on_board != move.word[i]:
                    ValueError("Execution of move blocked at (" + str(move.row + i) + "," + str(move.col) + ")")
            for i in range(0, len(move.word)):
                self._board[move.row+i][move.col] = move.word[i]
            for pos in move.blank_positions:
                self._blank_locations[move.row+pos][move.col] = 'X'
        elif move.how == "across":
            for i in range(0, len(move.word)):
                letter_on_board = self._board[move.row][move.col + i]
                if letter_on_board != ' ' and letter_on_board != move.word[i]:
                    ValueError("Execution of move blocked at (" + str(move.row + i) + "," + str(move.col) + ")")
            for i in range(0, len(move.word)):
                self._board[move.row][move.col + i] = move.word[i]
            for pos in move.blank_positions:
                self._blank_locations[move.row][move.col+pos] = 'X'
        else:
            ValueError("Move does not correctly specify 'down' or ' across'")

    def play_blank(self, row, col):
        self._blank_locations[row][col] = "X"

    # Convert board to a nicely readable string
    def __str__(self) -> str:
        ret = " ------------------------------- \n"
        for i in range(0, len(self._board)):
            ret += "| "
            for j in range(0, len(self._board[i])):
                if self._blank_locations[i][j] == "X":
                    ret += str(self._board[i][j]).lower() + " "
                else:
                    ret += self._board[i][j] + " "
            ret += "|\n"
        ret += " ------------------------------- "
        return ret

    # Print the board
    def print(self):
        print(self.__str__())
