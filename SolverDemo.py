#
# This is only a demo file that can be used to debug/test the scrabble solver
# and see if packages are installed correctly.
#

__author__ = 'Sebastian Wernicke'

from ScrabbleBot import ScrabbleUtils
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleGame

from time import time

input_board = [[' ', 'P', 'A', 'C', 'I', 'F', 'Y', 'I', 'N', 'G', ' ', ' ', ' ', ' ', ' '],
               [' ', 'I', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['Y', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'R', 'E', 'Q', 'U', 'A', 'L', 'I', 'F', 'I', 'E', 'D', ' ', ' ', ' '],
               ['H', ' ', 'L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['E', 'D', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['N', 'O', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'R', 'A', 'I', 'N', 'W', 'A', 'S', 'H', 'I', 'N', 'G', ' ', ' ', ' '],
               ['U', 'M', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['T', ' ', ' ', 'E', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'W', 'A', 'K', 'E', 'N', 'E', 'R', 'S', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'O', 'N', 'E', 'T', 'I', 'M', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['O', 'O', 'T', ' ', ' ', 'E', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['N', ' ', ' ', ' ', ' ', ' ', ' ', 'U', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'J', 'A', 'C', 'U', 'L', 'A', 'T', 'I', 'N', 'G', ' ', ' ', ' ', ' ']]

my_letters = "**PBAZE"

# Load the Scrabble Dictionary
legal_words = ScrabbleUtils.load_word_set("OSPD4.txt")

# Build the Word Signatures
# (Needs my_letters to figure out if there are blank tiles)
num_blanks = my_letters.count('*')
word_signatures = ScrabbleUtils.build_word_signatures(legal_words, num_blanks)

# Get the board multiplier table
board_multipliers = ScrabbleBoard.get_board_multipliers()

# Get the letter value dictionary
letter_values = ScrabbleGame.get_letter_values()

# Calculate all possible solutions
start_time = time()
solutions = ScrabbleUtils.find_all_moves(input_board, my_letters, legal_words,
                                         board_multipliers, letter_values, word_signatures)
total_time = time() - start_time
print("Time (seconds): " + str(total_time))

# Print top 10 solutions
ScrabbleUtils.sort_and_print_solutions(solutions, 100)
