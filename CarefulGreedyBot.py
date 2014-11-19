#
# CarefulGreedyBot always plays the highest scoring move, except when it opens
# up the triples on the border of the board for the opponent, in which case it
# apples penalties for every "opened up" field
#

__author__ = 'Sebastian Wernicke'

import random
import math
from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class CarefulGreedyBot(ScrabbleAI.ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        for s in solutions:
            penalty = 0
            col = s.col
            row = s.row
            length = len(s.word)
            if s.how == "across":
                penalty = 0
                if col == 0:
                    if row == 0 or row == 7 or row == 14:
                        penalty = 0
                    elif 0 < row < 7:
                        if board.get(0, 0) == ' ':
                            penalty += 15
                        if board.get(7, 0) == ' ':
                            penalty += 25
                    else:
                        if board.get(7, 0) == ' ':
                            penalty += 25
                        if board.get(14, 0) == ' ':
                            penalty += 15
                s.score -= penalty
                if col + length == 14:
                    if row == 0 or row == 7 or row == 14:
                        penalty = 0
                    elif 0 < row < 7:
                        if board.get(0, 14) == ' ':
                            penalty += 15
                        if board.get(7, 14) == ' ':
                            penalty += 25
                    else:
                        if board.get(7, 14) == ' ':
                            penalty += 25
                        if board.get(14, 14) == ' ':
                            penalty += 15
                s.score -= penalty
            if s.how == "down":
                #if row == 0 or row + length == 14:
                #    penalty = -4
                #if row == 1 or row + length == 13:
                ##    penalty = -1
                s.score += penalty
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            return solutions[0]
        else:
            return None
