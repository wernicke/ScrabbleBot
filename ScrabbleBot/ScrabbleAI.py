#
# This file defines the Scrabble AI class
#
# Any player in a scrabble tournament must descend from this class
#
# The class must implement a function called "make_move" that takes as input
# a ScrabbleBoard, a list of the letters it has available, and a list
# of valid moves that can be played on the given board with the current
# letters (this is provided as a courtesy and does not have to be used
# of course)
#

__author__ = 'Sebastian Wernicke'

import random
import math
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


#
# Class structure of a scrabble bot
#
class ScrabbleAI:

    def __init__(self, name):
        self.name = name

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        raise NotImplementedError("Subclass must implement abstract method")






