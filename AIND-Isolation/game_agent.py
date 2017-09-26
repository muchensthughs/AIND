"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from math import exp

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()
    if len(blank_spaces) < 15:
        my_loc = game.get_player_location(player)
        opp_loc = game.get_player_location(game.get_opponent(player))
        return 1/2*(float(_longest_path(game, blank_spaces, my_loc)) - float(
            _longest_path(game, blank_spaces, opp_loc)))

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if not 0.4 * my_moves == 0.6 * opp_moves:
        return float(0.4 * my_moves - 0.6 * opp_moves)
    # Calculate the Manhattan distance to the center of the board
    # The closer a player is to the center, the larger probability that the player would win
    center_y, center_x = int(game.height / 2), int(game.width / 2)
    my_y, my_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    my_dist = abs(my_y - center_y) + abs(my_x - center_x)
    opp_dist = abs(opp_y - center_y) + abs(opp_x - center_x)

    # Divide the distance by 10 since positional advantage is less effective than the difference in number of moves left
    return float(opp_dist - my_dist)/10 * (1/2)





def _longest_path(game, blank_spaces, loc):
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]

    r, c = loc
    if blank_spaces == None or blank_spaces == []:
        return 0
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if (r + dr, c + dc) in blank_spaces]
    if len(valid_moves) == 0 or valid_moves == [None] or valid_moves == None or valid_moves[0] == None:
        return 0

    blank_spaces_left_group = []
    for i in range(len(valid_moves)):
        blank_spaces_copy = blank_spaces
        new_blanks = blank_spaces_copy.remove(valid_moves[i])
        blank_spaces_left_group.append(new_blanks)

    if len(valid_moves) == 1:
        return _longest_path(game, blank_spaces_left_group, valid_moves[0]) + 1
    return max([_longest_path(game, blank_spaces_left, new_loc)
                for blank_spaces_left, new_loc in zip(blank_spaces_left_group, valid_moves)])+1



def _num_of_nearby_spaces(game, player):
    #computes the number of nearby empty spaces whose distance are less than 3 from current player position in both x and y direction
    spaces = game.get_blank_spaces()
    player_y, player_x = game.get_player_location(player)
    score = 0
    for space in spaces:
        dist_y = abs(player_y - space[0])
        dist_x = abs(player_x - space[1])
        if dist_y + dist_x < 3:
            score += 1
    return score

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()
    if len(blank_spaces) < 15:
        my_loc = game.get_player_location(player)
        opp_loc = game.get_player_location(game.get_opponent(player))
        return 1 / 2 * (float(_longest_path(game, blank_spaces, my_loc)) - float(
            _longest_path(game, blank_spaces, opp_loc)))
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if not 0.4*my_moves == 0.6*opp_moves:
        return float(0.4*my_moves - 0.6*opp_moves)
    #Use number of blank spaces in the surrounding as a measurement
    #The larger the number of blank spaces around, the greater the advantage
    my_space = _num_of_nearby_spaces(game, player)
    opp_space = _num_of_nearby_spaces(game, game.get_opponent(player))

    return float(my_space - opp_space)/30 * (1/2)



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()
    if len(blank_spaces) < 15:
        my_loc = game.get_player_location(player)
        opp_loc = game.get_player_location(game.get_opponent(player))
        return 1 / 2 * (float(_longest_path(game, blank_spaces, my_loc)) - float(
            _longest_path(game, blank_spaces, opp_loc)))


    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if not 0.4*my_moves == 0.6*opp_moves:
        return float(0.4*my_moves - 0.6*opp_moves)
    # A mixture of positional advantage and spacial advantage
    c_y, c_x = int(game.height / 2), int(game.width / 2)
    my_y, my_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    my_dist = abs(my_y - c_y) + abs(my_x - c_x)
    opp_dist = abs(opp_y - c_y) + abs(opp_x - c_x)

    my_space = _num_of_nearby_spaces(game, player)
    opp_space = _num_of_nearby_spaces(game, game.get_opponent(player))

    return 1/2 * (float(my_space - opp_space)/30 + float(opp_dist - my_dist)/10)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=15.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def _minimax(self, game, depth, maximizing):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)
        if depth == 0:
            return self.score(game, self), legal_moves[0]

        if maximizing:
            best_score, best_move = float("-inf"), legal_moves[0]
            for move in legal_moves:
                new_game = game.forecast_move(move)
                v, _ = self._minimax(new_game, depth - 1, False)
                if best_score < v:
                    best_move = move
                    best_score = v
            return best_score, best_move

        else:
            best_score, best_move = float("inf"), legal_moves[0]
            for move in legal_moves:
                new_game = game.forecast_move(move)
                v, _ = self._minimax(new_game, depth - 1, True)
                if best_score > v:
                    best_move = move
                    best_score = v
            return best_score, best_move


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        _, best_move = self._minimax(game, depth, True)

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        # in case the search fails due to timeout

        best_move = (-1, -1)


        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def _minimax_pruning(self, game, depth, alpha, beta, maximizing):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)
        if depth == 0:
            return self.score(game, self), legal_moves[0]

        if maximizing:
            best_score, best_move = float("-inf"), legal_moves[0]

            for move in legal_moves:
                new_game = game.forecast_move(move)
                v, _ = self._minimax_pruning(new_game, depth - 1, alpha, beta, False)
                if v >= beta:
                    return v, move
                if best_score < v:
                    best_move = move
                    best_score = v
                alpha = max(alpha, v)
            return best_score, best_move

        else:
            best_score, best_move = float("inf"), legal_moves[0]

            for move in legal_moves:
                new_game = game.forecast_move(move)
                v, _ = self._minimax_pruning(new_game, depth - 1, alpha, beta, True)
                if v <= alpha:
                    return v, move
                if best_score > v:
                    best_move = move
                    best_score = v
                beta = min(beta, v)
            return best_score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        _, best_move = self._minimax_pruning(game, depth, alpha, beta, True)
        return best_move



