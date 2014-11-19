#
# GreedyBot always plays the highest scoring move
#

__author__ = 'Sebastian Wernicke'

import random
import math
from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class GreedyBot(ScrabbleAI.ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            return solutions[0]
        else:
            return None
