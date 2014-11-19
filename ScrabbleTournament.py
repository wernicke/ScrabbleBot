#
# This script can be used to set up and start ScrabbleBot tournaments
# Use the players, num_rounds, and verbosity parameters to tweak
#

__author__ = 'Sebastian Wernicke'

# Import utilities
from ScrabbleBot import ScrabbleMatch
from ScrabbleBot import ScrabbleAI

# Import robots
from QUBot import QUBot
from GreedyBot import GreedyBot
from RandomBot import RandomBot
from CarefulGreedyBot import CarefulGreedyBot
from QBot import QBot


# Specify the set of players
players = [QBot("Q-Bert"), GreedyBot("Greedy")]

# Number of match rounds
num_rounds = 100

# Specify volume of output, verbosity levels are 0, 1, and 2
verbosity = 0

# Play it out
sm = ScrabbleMatch.ScrabbleMatch("OSPD4.txt", players)
sm.play_match(num_rounds, True, verbosity)

# Print results
print("\nResults:")
print(sm.get_total_scores())
print(sm.get_total_matchwins())
