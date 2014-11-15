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


#
# GreedyBot always plays the highest scoring move
#
class GreedyBot(ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            return solutions[0]
        else:
            return None


#
# RandomBot always plays a random
#
class RandomBot(ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            return random.choice(solutions)
        else:
            return None


#
# CarefulGreedyBot always plays the highest scoring move, except when it opens
# up the triples on the border of the board for the opponent, in which case it
# apples penalties for every "opened up" field
#
class CarefulGreedyBot(ScrabbleAI):

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


#
# RadiusBot gives a little penalty to words that are off-center
#
class RadiusBot(ScrabbleAI):

    def make_move(self, board: list, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
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



