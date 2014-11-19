#
# QU Bot is greedy but careful about playing a Q if it
# doesn't have a U and can't gain a lot of points from the move
#

__author__ = 'John Bohannon'


from ScrabbleBot import ScrabbleAI
from ScrabbleBot import ScrabbleBoard
from ScrabbleBot import ScrabbleUtils


class QUBot(ScrabbleAI.ScrabbleAI):

    def make_move(self, board: ScrabbleBoard, letters: list, solutions: list) -> ScrabbleUtils.ScrabbleMove:
        if len(solutions) > 0:
            solutions.sort(reverse=True)
            for i in solutions:
                if ('Q' in i.letters) and ('U' not in i.letters) and (i.score < 30):
                    continue
                else:
                    return i
        else:
            return None






