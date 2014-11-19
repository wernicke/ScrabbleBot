#
# QBot is greedy but careful about playing a Q if it
# doesn't gain a lot of points from the move
#

__author__ = 'John Bohannon'


from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class QBot(ScrabbleAI.ScrabbleAI):
    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            for i in solutions:
                if ('Q' in i.letters) and i.score < 20:
                    continue
                else:
                    return i
        else:
            return None
