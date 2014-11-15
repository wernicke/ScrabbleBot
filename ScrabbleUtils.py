#
# This file contains a set of utility functions that are used to score moves on a scrabble board
# and generate a set of all allowed moves for a certain configuration
#
# There are also utility functions to pretty-print solutions and a move for debugging
# purposes or high verbosity
#

__author__ = 'Sebastian Wernicke'

from itertools import combinations, product


class ScrabbleMove:

    def __init__(self, row: int, col: int, how: str, word: str, letters: list, score: int):
        self.score = score
        self.row = row
        self.col = col
        self.how = how
        self.word = word
        self.letters = list(letters)
        self.blank_positions = []  # If the word played contains blanks, these are their positions

    def __lt__(self, other):
        return self.score < other.score


#
# Load Scrabble Word Set
#
def load_word_set(filename: str) -> set:
    print("Loading dictionary '" + filename + "'")
    return set(line.strip() for line in open(filename))


#
# Build utility dictionary with word signatures
# The keys of the dictionary are sorted letter sequences
# The entries are all words that match a given key
#
def build_word_signatures(legal_words: set, num_blanks: int) -> dict:

    if num_blanks > 2:
        print("Sorry, only up to 2 blank pieces allowed...")
        exit(1)
    sorted_letters = dict()

    print("Building word signatures with up to " + str(num_blanks) + " blank pieces")

    for word in legal_words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in sorted_letters.keys():
            sorted_letters[sorted_word].append(word)
        else:
            sorted_letters[sorted_word] = [word]

    if num_blanks == 1:
        for word in legal_words:
            sorted_word = ''.join(sorted(word))
            for i in range(0, len(word)):
                new_key_one = "*" + sorted_word[:i] + sorted_word[i+1:]
                if new_key_one in sorted_letters.keys():
                    sorted_letters[new_key_one].append(word)
                else:
                    sorted_letters[new_key_one] = [word]

    elif num_blanks == 2:
        for word in legal_words:
            #print("--"+word)
            sorted_word = ''.join(sorted(word))
            for i in range(0, len(word)):
                new_key_one = "*" + sorted_word[:i] + sorted_word[i+1:]
                if new_key_one in sorted_letters.keys():
                    sorted_letters[new_key_one].append(word)
                else:
                    sorted_letters[new_key_one] = [word]
                #print(new_key_one)
                for j in range(i + 1, len(word)):
                    new_key_two = "*" + new_key_one[:j] + new_key_one[j+1:]
                    if new_key_two in sorted_letters.keys():
                        sorted_letters[new_key_two].append(word)
                    else:
                        sorted_letters[new_key_two] = [word]
                    #print(new_key_two)
            #print("-------------")

    return sorted_letters


#
# Return the Scrabble for playing 'word' across, starting at
# coordinates (row, col) on the board.
# This function deliberately ignores any additional words that
# might be formed vertically, but does take into account that
# the actual word we're playing might start left of 'col'
#
def score_word_across(word: str, row: int, col: int, board: list, board_multipliers: list,
                      letter_values: dict, legal_words: set, legality_check: bool) -> int:

    base_score = 0
    word_multiplier = 1

    # Score the central word
    for i in range(0, len(word)):
        letter_on_board = board[row][col+i]
        if letter_on_board != ' ':  # Case 1: Current letter was already on the board
            if word[i] != letter_on_board:  # Check if we're trying to override a board letter
                return -1
            else:
                base_score += letter_values[letter_on_board]  # Score the letter
        else:  # Not clean but fast, uses 'magic constants' to decode special board fields
            if board_multipliers[row][col+i] == 0:
                base_score += letter_values[word[i]]
            elif board_multipliers[row][col+i] == 2:
                base_score += letter_values[word[i]] * 2
            elif board_multipliers[row][col+i] == 3:
                base_score += letter_values[word[i]] * 3
            elif board_multipliers[row][col+i] == 4:
                base_score += letter_values[word[i]]
                word_multiplier *= 2
            elif board_multipliers[row][col+i] == 6:
                base_score += letter_values[word[i]]
                word_multiplier *= 3

    # Score the prefix
    start_col = col
    prefix = ""
    while start_col > 0 and board[row][start_col-1] != ' ':
        start_col -= 1
        letter_on_board = board[row][start_col]
        prefix = letter_on_board + prefix
        base_score += letter_values[letter_on_board]

    # Score the postfix
    postfix = ""
    end_col = col + len(word) - 1
    while end_col < 14 and board[row][end_col+1] != ' ':
        end_col += 1
        letter_on_board = board[row][end_col]
        postfix += letter_on_board
        base_score += letter_values[letter_on_board]

    # Make sure the full word that is played is allowed
    if legality_check:
        if (prefix + word + postfix) not in legal_words:
            return -1

    return base_score * word_multiplier


#
# Return the Scrabble for playing 'word' down, starting at
# coordinates (row, col) on the board.
# This function deliberately ignores any additional words that
# might be formed horizontally, but does take into account that
# the actual word we're playing might start above of 'row'
#
def score_word_down(word: str, row: int, col: int, board: list, board_multipliers: list,
                    letter_values: dict, legal_words: set, legality_check: bool) -> int:

    base_score = 0
    word_multiplier = 1

    # Score the central word
    for i in range(0, len(word)):
        letter_on_board = board[row+i][col]
        if letter_on_board != ' ':  # Case 1: Current letter was already on the board
            if word[i] != letter_on_board:  # Check if we're trying to override a board letter
                return -1
            else:
                base_score += letter_values[letter_on_board]  # Score the letter
        else:  # Not clean but fast, uses 'magic constants' to decode special board fields
            if board_multipliers[row+i][col] == 0:
                base_score += letter_values[word[i]]
            elif board_multipliers[row+i][col] == 2:
                base_score += letter_values[word[i]] * 2
            elif board_multipliers[row+i][col] == 3:
                base_score += letter_values[word[i]] * 3
            elif board_multipliers[row+i][col] == 4:
                base_score += letter_values[word[i]]
                word_multiplier *= 2
            elif board_multipliers[row+i][col] == 6:
                base_score += letter_values[word[i]]
                word_multiplier *= 3

    # Score the prefix
    start_row = row
    prefix = ""
    while start_row > 0 and board[start_row-1][col] != ' ':
        start_row -= 1
        letter_on_board = board[start_row][col]
        prefix = letter_on_board + prefix
        base_score += letter_values[letter_on_board]

    # Find the extension of the word
    postfix = ""
    end_row = row + len(word) - 1
    while end_row < 14 and board[end_row+1][col] != ' ':
        end_row += 1
        letter_on_board = board[end_row][col]
        postfix += letter_on_board
        base_score += letter_values[letter_on_board]

    # Make sure the full word that is played is allowed
    if legality_check:
        if (prefix + word + postfix) not in legal_words:
            return -1

    return base_score * word_multiplier


#
# Return the Scrabble score if I play 'word' across, starting at
# coordinates (row, col) on the board. Note that the input word
# is given in full, not just the letters we are adding.
# Function returns -1 if it detects anything illegal
#
def score_play_across(word: str, row: int, col: int, board: list,
                      board_multipliers: list, letter_values: dict, legal_words: set,
                      legality_check: bool) -> int:

    # Check if word is too long
    if col + len(word) > 15:
        return -1

    # Score the word we're about to play across
    score = score_word_across(word, row, col, board, board_multipliers, letter_values, legal_words, legality_check)
    if score == - 1:
        return -1

    # Score any additional words that are formed vertically and check
    # if the word can actually be played given what's on the board already
    # Additionally, account for scrabble bonus
    letters_used = 0
    for letter_pos in range(0, len(word)):
        working_col = col + letter_pos
        letter_on_board = board[row][working_col]
        if letter_on_board == ' ':  # Placing new letter might generate additional words
            letters_used += 1
            if (row > 0 and board[row-1][working_col] != ' ') or \
               (row < 14 and board[row+1][working_col] != ' '):  # Check if new word is generated
                add_score = score_word_down(word[letter_pos], row, working_col,
                                            board, board_multipliers, letter_values, legal_words, legality_check)
                if add_score == -1:
                    return -1
                else:
                    score += add_score
        else:  # Check if the letter of the word and what's on the board match
            if letter_on_board != word[letter_pos]:
                return -1

    if letters_used == 7:
        score += 50

    return score


#
# Return the Scrabble score if I play 'word' down, starting at
# coordinates (row, col) on the board. Note that the input word
# is given in full, not just the letters we are adding.
# Function returns -1 if it detects anything illegal
#
def score_play_down(word: str, row: int, col: int, board: list,
                    board_multipliers: list, letter_values: dict, legal_words: set,
                    legality_check: bool) -> int:

    # Check if word is too long
    if row + len(word) > 15:
        return -1

    # Score the word we're about to play down
    score = score_word_down(word, row, col, board, board_multipliers, letter_values, legal_words, legality_check)
    if score == - 1:
        return -1

    # Score any additional words that are formed vertically and check
    # if the word can actually be played given what's on the board already
    # Additionally, account for scrabble bonus
    letters_used = 0
    for letter_pos in range(0, len(word)):
        working_row = row + letter_pos
        letter_on_board = board[working_row][col]
        if letter_on_board == ' ':  # Placing new letter might generate additional words
            letters_used += 1
            if (col > 0 and board[working_row][col-1] != ' ') or \
               (col < 14 and board[working_row][col+1] != ' '):  # Check if new word is generated
                add_score = score_word_across(word[letter_pos], working_row, col,
                                              board, board_multipliers, letter_values, legal_words, legality_check)
                if add_score == -1:
                    return -1
                else:
                    score += add_score
        else:  # Check if the letter of the word and what's on the board match
            if letter_on_board != word[letter_pos]:
                return -1

    if letters_used == 7:
        score += 50

    return score


#
# Function to generate all unique non-empty subsets of a given iterable
#
def non_empty_powerset(iterable):
    xs = list(iterable)
    ls = set()
    for n in range(1, len(xs)+1):
        for el in combinations(xs, n):
            ls.add(tuple(sorted(el)))
    return ls


#
# Small utility function that tests if all elements of a list are unique
#
def all_unique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


#
# Given a Scrabble board and a string of letters, this function calculates a list of
# tuples that represent all possible Scrabble moves.
# The tuples are structured
#   (score, starting row, starting column, "down"/"across", word, letters used)
#
def find_all_moves(board: list, letters: str, legal_words: set,
                   board_multipliers: list, letter_values: dict, word_signatures: dict) -> list:

    # The following part is a pre-calculation that significantly speeds up the solution
    # finding. It generates two nested lists of the structure
    #    list -> num_letters -> (rows cols letterset)
    # that is to be interpreted as follows:
    #  - If I place num_letters on the board, in which (row,col) coordinates can I do that
    #    to generate a legal move?
    #  - Assuming I play num_letters letters in a given row and column, what letters
    #    would need to be incorporated (because they are already on the board)?
    # We generate two nested lists, one for playing words across and one for
    # playing words down

    max_num_letters = len(letters)
    potential_plays_across = []
    potential_plays_down = []
    for i in range(0, max_num_letters+1):
        potential_plays_across.append([])
        potential_plays_down.append([])

    for row in range(0, 15):
        for col in range(0, 15):
            if board[row][col] == ' ':  # We can skip positions where there's already a letter
                                        # because we always attempt prefix-expansion

                #
                # Check across
                #
                letterset = []
                legal_move = False
                start_col = col
                # Check extension to the left
                while start_col > 0 and board[row][start_col-1] != ' ':
                    start_col -= 1
                    legal_move = True
                    letterset.append(board[row][start_col])
                # Now extend to the right
                letters_placed = 0
                working_col = col
                while letters_placed < max_num_letters and working_col < 15:
                    if not legal_move:
                        if board[row][working_col] != ' ':
                            legal_move = True
                        elif row > 0 and board[row-1][working_col] != ' ':
                            legal_move = True
                        elif row < 14 and board[row+1][working_col] != ' ':
                            legal_move = True
                        elif working_col < 14 and board[row][working_col+1] != ' ':
                            legal_move = True
                        elif row == 7 and working_col == 7:
                            legal_move = True
                    if board[row][working_col] == ' ':
                        letters_placed += 1
                        working_col += 1
                        while working_col < 15 and board[row][working_col] != ' ':
                            letterset.append(board[row][working_col])
                            working_col += 1
                        if legal_move:
                            potential_plays_across[letters_placed].append((row, start_col, list(letterset)))
                    else:
                        letterset.append(board[row][working_col])
                        working_col += 1

                #
                # Check down
                #
                letterset = []
                legal_move = False
                start_row = row
                # Check extension upwards
                while start_row > 0 and board[start_row-1][col] != ' ':
                    start_row -= 1
                    legal_move = True
                    letterset.append(board[start_row][col])
                # Now extend downward
                letters_placed = 0
                working_row = row
                while letters_placed < max_num_letters and working_row < 15:
                    if not legal_move:
                        if board[working_row][col] != ' ':
                            legal_move = True
                        elif col > 0 and board[working_row][col-1] != ' ':
                            legal_move = True
                        elif col < 14 and board[working_row][col+1] != ' ':
                            legal_move = True
                        elif working_row < 14 and board[working_row+1][col] != ' ':
                            legal_move = True
                        elif working_row == 7 and col == 7:
                            legal_move = True
                    if board[working_row][col] == ' ':
                        letters_placed += 1
                        working_row += 1
                        while working_row < 15 and board[working_row][col] != ' ':
                            letterset.append(board[working_row][col])
                            working_row += 1
                        if legal_move:
                            potential_plays_down[letters_placed].append((start_row, col, list(letterset)))
                    else:
                        letterset.append(board[working_row][col])
                        working_row += 1

    # Now that the pre-computation is complete, we can iterate over all
    # non-empty subset of letters that we have ('letterset') and see, for
    # each subset, if there are valid plays using those letters
    solutions = []
    for letterset in non_empty_powerset(letters):
        letters_to_place = list(letterset)
        num_letters = len(letterset)
        num_blanks = letterset.count('*')
        #Across_eval
        for placement_tuple in potential_plays_across[num_letters]:
            row = placement_tuple[0]
            col = placement_tuple[1]
            additional_letters = list(placement_tuple[2])
            letters_to_use = "".join(sorted(letters_to_place + additional_letters))
            if letters_to_use in word_signatures.keys():
                for potential_word in word_signatures[letters_to_use]:
                    score = score_play_across(potential_word, row, col, board,
                                              board_multipliers, letter_values, legal_words, True)
                    if score > -1:
                        if num_blanks == 0:
                            new_move = ScrabbleMove(row, col, "across", potential_word, letters_to_place, score)
                            solutions.append(new_move)
                        else:
                            #If we have blanks, we need to re-evaluate the score
                            #We'll assume that the player always wants to place the
                            #blanks score-optimally (as there's no advantage to doing it
                            # any other way)
                            #Steps:
                            # 1) What letters do the blanks represent?
                            blank_meaning = list(potential_word)
                            for char in additional_letters:
                                blank_meaning.remove(char)
                            for char in letters_to_place:
                                if char != '*':
                                    blank_meaning.remove(char)
                            # 2) In which position could I play the blanks?
                            blank_positions = []
                            for i in range(0, len(blank_meaning)):
                                blank_positions.append([])
                                for j in range(0, len(potential_word)):
                                    if potential_word[j] == blank_meaning[i] and board[row][col + j] == ' ':
                                        blank_positions[i].append(j)
                            # 3) evaluate each position to find the optimal one
                            best_penalty = 100000
                            best_placement = []
                            old_across_score = score_word_across(potential_word, row, col, board, board_multipliers,
                                                                 letter_values, legal_words, False)
                            for blank_placement in product(*blank_positions):
                                if all_unique(blank_placement):

                                    word_with_blanks = list(potential_word)
                                    for pos in blank_placement:
                                        word_with_blanks[pos] = '*'
                                    new_across_score = score_word_across(''.join(word_with_blanks), row, col,
                                                                         board, board_multipliers,
                                                                         letter_values, legal_words, False)

                                    current_penalty = old_across_score - new_across_score

                                    if current_penalty < best_penalty:
                                        for pos in blank_placement:
                                            current_penalty += score_word_down(potential_word[pos], row, col,
                                                                               board, board_multipliers,
                                                                               letter_values, legal_words, False) \
                                                - score_word_down('*', row, col,
                                                                  board, board_multipliers,
                                                                  letter_values, legal_words, False)

                                    if current_penalty < best_penalty:
                                        best_penalty = current_penalty
                                        best_placement = list(blank_placement)
                            # Done, now add the move
                            new_move = ScrabbleMove(row, col, "across", potential_word, letters_to_place,
                                                    score - best_penalty)
                            new_move.blank_positions = list(best_placement)
                            solutions.append(new_move)

        #Down_eval
        for placement_tuple in potential_plays_down[num_letters]:
            #if num_letters == 7:
            #    print(str(len(letterset)) + " down: " + str(placement_tuple))
            row = placement_tuple[0]
            col = placement_tuple[1]
            additional_letters = list(placement_tuple[2])
            letters_to_use = "".join(sorted(letters_to_place + additional_letters))
            if letters_to_use in word_signatures.keys():
                for potential_word in word_signatures[letters_to_use]:
                    score = score_play_down(potential_word, row, col, board,
                                            board_multipliers, letter_values, legal_words, True)
                    if score > -1:
                        if num_blanks == 0:
                            new_move = ScrabbleMove(row, col, "down", potential_word, letters_to_place, score)
                            solutions.append(new_move)
                        else:
                            #If we have blanks, we need to re-evaluate the score
                            #We'll assume that the player always wants to place the
                            #blanks score-optimally (as there's no advantage to doing it
                            # any other way)
                            #Steps:
                            # 1) What letters do the blanks represent?
                            blank_meaning = list(potential_word)
                            for char in additional_letters:
                                blank_meaning.remove(char)
                            for char in letters_to_place:
                                if char != '*':
                                    blank_meaning.remove(char)
                            # 2) In which position could I play the blanks?
                            blank_positions = []
                            for i in range(0, len(blank_meaning)):
                                blank_positions.append([])
                                for j in range(0, len(potential_word)):
                                    if potential_word[j] == blank_meaning[i] and board[row + j][col] == ' ':
                                        blank_positions[i].append(j)
                            # 3) evaluate each position to find the optimal one
                            best_penalty = 100000
                            best_placement = []
                            old_down_score = score_word_down(potential_word, row, col, board, board_multipliers,
                                                             letter_values, legal_words, False)
                            for blank_placement in product(*blank_positions):
                                if all_unique(blank_placement):
                                    word_with_blanks = list(potential_word)

                                    for pos in blank_placement:
                                        word_with_blanks[pos] = '*'
                                    new_down_score = score_word_down(''.join(word_with_blanks), row, col,
                                                                     board, board_multipliers,
                                                                     letter_values, legal_words, False)

                                    current_penalty = old_down_score - new_down_score

                                    if current_penalty < best_penalty:
                                        for pos in blank_placement:
                                            current_penalty += score_word_across(potential_word[pos], row, col,
                                                                                 board, board_multipliers,
                                                                                 letter_values, legal_words, False) \
                                                - score_word_across('*', row, col,
                                                                    board, board_multipliers,
                                                                    letter_values, legal_words, False)

                                    if current_penalty < best_penalty:
                                        best_penalty = current_penalty
                                        best_placement = list(blank_placement)
                            # Done, now add the move
                            new_move = ScrabbleMove(row, col, "down", potential_word, letters_to_place,
                                                    score - best_penalty)
                            new_move.blank_positions = list(best_placement)
                            solutions.append(new_move)

    return solutions


#
# Format word for signifying blanks
#
def format_with_blanks(word: str, blanks: list):
    tmp = list(word.upper())
    for pos in blanks:
        tmp[pos] = tmp[pos].lower()
    return "".join(tmp)


#
# Utility function to print a list of ScrabbleMoves, sorted by score and with cutoff
#
def sort_and_print_solutions(solutions: list, max_results: int):
    print("SCORE\tROW\tCOL\tHOW\tWORD\tUSED LETTERS".expandtabs(7))
    solutions.sort(reverse=True)
    res = 0
    for solution in solutions:
        print((str(solution.score) + "\t" + str(solution.row) + "\t" + str(solution.col)
              + "\t" + str(solution.how)
              + "\t" + format_with_blanks(str(solution.word), solution.blank_positions)
              + "\t" + str(solution.letters)).expandtabs(7))
        res += 1
        if res == max_results:
            return


#
# Utility function to print a move
#
def print_move(move: ScrabbleMove):
    print("At row " + str(move.row) + " and column " + str(move.col) + ", " +
          "play word '" + format_with_blanks(move.word, move.blank_positions) +
          "' using letters " + str(move.letters))
    #print("For " + str(move.score) + " points.")
