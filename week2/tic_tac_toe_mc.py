"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 20    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def max_element(board, matrix):
    """
    Find the maximum value in score matrix. The number of row and 
    col value are returned. 
    """
    row_num = len(matrix)
    col_num = len(matrix[0])
    maximum = -99999
    for dummy_i in range(row_num):
        for dummy_j in range(col_num):
            if maximum < matrix[dummy_i][dummy_j] and board.square(dummy_i, dummy_j) == provided.EMPTY:
                maximum = matrix[dummy_i][dummy_j]
                row = dummy_i
                col = dummy_j
    return row, col

def mc_trial(board, player):
    """
    This function takes a current board and 
    the next player to move. The function 
    should play a game starting with the 
    given player by making random moves, 
    alternating between players. The function 
    should return when the game is over. 
    The modified board will contain the 
    state of the game, so the function does 
    not return anything.
    """
    cur_player = player
    winner = None
    while winner == None:
        empty_squares = board.get_empty_squares()
        pos = random.randrange(len(empty_squares))
        row, col = empty_squares[pos]
        board.move(row, col, cur_player)
        winner = board.check_win()
        cur_player = provided.switch_player(cur_player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores 
    (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a 
    completed game, and which player the machine 
    player is. The function should score the 
    completed board and update the scores grid. 
    As the function updates the scores grid 
    directly, it does not return anything. 
    """
    game_res = board.check_win()
    if game_res == provided.DRAW:
        return
    dim = board.get_dim()
    if game_res == player:
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == player: 
                    scores[row][col] += MCMATCH
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += -MCOTHER 
    else:
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == player: 
                    scores[row][col] += -MCMATCH
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += MCOTHER 
    return scores

def get_best_move(board, scores):
    """
    This function takes a current board 
    and a grid of scores. The function 
    should find all of the empty squares 
    with the maximum score and randomly 
    return one of them as a (row, column) tuple. 
    It is an error to call this function 
    with a board that has no empty squares 
    (there is no possible next move), so 
    your function may do whatever it wants 
    in that case. The case where the board 
    is full will not be tested.
    """
    if len(board.get_empty_squares()) == 0:
        return
    row, col = max_element(board, scores)
    return (row, col)

def mc_move(board, player, trials):
    """
    This function takes a current board, 
    which player the machine player is, 
    and the number of trials to run. 
    The function should use the Monte Carlo 
    simulation described above to return a move 
    for the machine player in the form of 
    a (row, column) tuple. Be sure to use 
    the other functions you have written!
    """
    dim = board.get_dim()
    score_grid = [[0 for dummy_j in range(dim)] for dummy_k in range(dim)]
    for dummy_i in range(trials):
        board_cp = board.clone()
        mc_trial(board_cp, player)
        mc_update_scores(score_grid, board_cp, player)
    row, col = get_best_move(board, score_grid)
    return row, col

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)