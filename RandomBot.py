#
# RandomBot always plays a random
#

__author__ = 'Sebastian Wernicke'

import random
import math
from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class RandomBot(ScrabbleAI.ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            return random.choice(solutions)
        else:
            return None
