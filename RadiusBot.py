#
# RadiusBot gives a little penalty to words that are off-center
#

__author__ = 'Sebastian Wernicke'

import random
import math
from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class RadiusBot(ScrabbleAI.ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        for s in solutions:
            penalty = 0
            col = s.col
            row = s.row
            length = len(s.word)
            if s.how == "across":
                for c in range(col, col+length):
                    penalty += math.sqrt((c - 7) ** 2 + (row - 7) ** 2)
                penalty /= length
                s.score -= penalty * 0.5
            if s.how == "down":
                for r in range(row, row+length):
                    penalty += math.sqrt((col - 7) ** 2 + (r - 7) ** 2)
                penalty /= length
                s.score -= penalty * 0.5
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            return solutions[0]
        else:
            return None





