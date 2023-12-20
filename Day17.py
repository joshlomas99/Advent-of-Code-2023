from time import perf_counter

def time_function(func):
    """
    Decorator function to measure runtime of given function.

    Parameters
    ----------
    func : func
        Function to time.

    """
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        out = func(*args, **kwargs)
        t2 = perf_counter() - t1
        print(f'{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

import operator

def add_tuple(a, b):
    """
    Adds two tuples elementwise.

    Parameters
    ----------
    a : tuple(int)
        First tuple.
    b : tuple(int)
        Second tuple.

    Returns
    -------
    tuple(int)
        Result of elementwise addition of given tuples.

    """
    # Map addition operator onto tuples
    return tuple(map(operator.add, a, b))

import numpy as np

def get_input(input_file: str='Inputs/Day17_Inputs.txt') -> list:
    """
    Extracts a 2D heat loss map from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the heat loss map.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    grid : numpy.2darray(int)
        2D numpy array of integers giving the heat loss at each position on the map.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines and convert to numpy array of ints
        grid = np.array([[int(n) for n in l.strip()] for l in f.readlines()])

    return grid

from heapq import heappop, heappush

# Define all orthogonal directions
DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}

@time_function
def Day17_Part1(input_file: str='Inputs/Day17_Inputs.txt') -> int:
    """
    Finds the optimal path with minimal heat loss which can be taken through a grid, where the
    heat loss from passing through each point is given in a heat loss map in an input file. The
    movement cannot continue in the same direction for more than 3 consecutive moves. The path
    must start at the top left of the grid and end at the bottom right, and cannot go immediately
    backwards on itself at any point.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the heat loss map.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    min_heatloss : int
        The minimum possible heat loss.

    """
    # Parse input file and extract heat loss map
    grid = get_input(input_file)

    # Start at top left corner of the grid
    pos = (0, 0)
    # Initialise dict of minimum heat loss to reach each position in each state, where each state
    # is in the form (position, last_direction, number_of_straight_moves). Account for both
    # possible directions entering the grid at this point (right and down)
    min_heatlosses = {(pos, (0, 1), 0): 0, (pos, (1, 0), 0): 0}

    # Initialise queue using heap module to prioritise the shortest path still not searched
    queue = [(0, (pos, (0, 1), 0)), (0, (pos, (1, 0), 0))]
    # While there are unsearched states
    while queue:
        # Remove the highest priority unsearched state and extract parameters
        hl, state = heappop(queue)
        pos, last_dir, num_straight = state
        # Start with all possible directions
        possible_dirs = DIRECTIONS.copy()
        # Remove the opposite of the last direction travelled in (can't go backwards)
        possible_dirs.discard((-last_dir[0], -last_dir[1]))
        # If we have moved at least 3 moves in the same direction, remove this direction as well
        if num_straight >= 3:
            possible_dirs.discard(last_dir)
        # For each possible direction of travel
        for direction in possible_dirs:
            # Find new position
            new_pos = add_tuple(pos, direction)
            # If the new position is outside the grid, ignore it and move on
            if any(p < 0 for p in new_pos) or new_pos[0] >= len(grid) or new_pos[1] >= len(grid[0]):
                continue
            # If we are travelling in the same direction as last time, add 1 to num_straight
            if direction == last_dir:
                new_num_straight = num_straight + 1
            # Else reset to 1
            else:
                new_num_straight = 1
            # If the corresponding new state has not been found yet (in min_heatlosses), set its
            # minimum heat loss to the current value and add it to the queue to search
            if (new_state := (new_pos, direction, new_num_straight)) not in min_heatlosses:
                min_heatlosses[new_state] = min_heatlosses[state] + grid[new_state[0]]
                heappush(queue, (min_heatlosses[new_state], new_state))
            # Else if it is already in min_heatlosses so has already been searched, but this path
            # gives lower heat loss than the recorded value, set it to the new value
            elif min_heatlosses[state] + grid[new_state[0]] < min_heatlosses[new_state]:
                min_heatlosses[new_state] = min_heatlosses[state] + grid[new_state[0]]

    # Extract the heat loss to every end state at the bottom right corner
    possible_heatloss = [d for state, d in min_heatlosses.items()\
                      if state[0] == (len(grid)-1, len(grid[0])-1)]

    # Find minimum heat loss
    min_heatloss = min(possible_heatloss)

    return min_heatloss


@time_function
def Day17_Part2(input_file: str='Inputs/Day17_Inputs.txt') -> int:
    """
    Finds the optimal path with minimal heat loss which can be taken through a grid, where the
    heat loss from passing through each point is given in a heat loss map in an input file. Any
    movement must continue for a minimum of four blocks in a given direction before it can turn
    (or before it can stop at the end), but can only move a maximum of ten consecutive blocks
    without turning. The path must start at the top left of the grid and end at the bottom right,
    and cannot go immediately backwards on itself at any point.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the heat loss map.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    min_heatloss : int
        The minimum possible heat loss.

    """
    # Parse input file and extract heat loss map
    grid = get_input(input_file)

    # Start at top left corner of the grid
    pos = (0, 0)
    # Initialise dict of minimum heat loss to reach each position in each state, where each state
    # is in the form (position, last_direction, number_of_straight_moves). Account for both
    # possible directions entering the grid at this point (right and down)
    min_heatlosses = {(pos, (0, 1), 0): 0, (pos, (1, 0), 0): 0}

    # Initialise queue using heap module to prioritise the shortest path still not searched
    queue = [(0, (pos, (0, 1), 0)), (0, (pos, (1, 0), 0))]
    # While there are unsearched states
    while queue:
        # Remove the highest priority unsearched state and extract parameters
        hl, state = heappop(queue)
        pos, last_dir, num_straight = state
        # If the number of straight moves is less than 4, have to continue in the same direction
        if num_straight < 4:
            possible_dirs = {last_dir}
        else:
            # Else start with all possible directions
            possible_dirs = DIRECTIONS.copy()
            # Remove the opposite of the last direction travelled in (can't go backwards)
            possible_dirs.discard((-last_dir[0], -last_dir[1]))
            # If we have moved at least 10 moves in the same direction, remove this direction too
            if num_straight >= 10:
                possible_dirs.discard(last_dir)
        # For each possible direction of travel
        for direction in possible_dirs:
            # Find new position
            new_pos = add_tuple(pos, direction)
            # If the new position is outside the grid, ignore it and move on
            if any(p < 0 for p in new_pos) or new_pos[0] >= len(grid) or new_pos[1] >= len(grid[0]):
                continue
            # If we are travelling in the same direction as last time, add 1 to num_straight
            if direction == last_dir:
                new_num_straight = num_straight + 1
            # Else reset to 1
            else:
                new_num_straight = 1
            # If the corresponding new state has not been found yet (in min_heatlosses), set its
            # minimum heat loss to the current value and add it to the queue to search
            if (new_state := (new_pos, direction, new_num_straight)) not in min_heatlosses:
                min_heatlosses[new_state] = min_heatlosses[state] + grid[new_state[0]]
                heappush(queue, (min_heatlosses[new_state], new_state))
            # Else if it is already in min_heatlosses so has already been searched, but this path
            # gives lower heat loss than the recorded value, set it to the new value
            elif min_heatlosses[state] + grid[new_state[0]] < min_heatlosses[new_state]:
                min_heatlosses[new_state] = min_heatlosses[state] + grid[new_state[0]]

    # Extract the heat loss to every end state at the bottom right corner, with at least 4 moves in
    # the same direction before stopping
    possible_heatloss = [d for state, d in min_heatlosses.items()\
                      if state[0] == (len(grid)-1, len(grid[0])-1)\
                          and state[2] >= 4]

    # Find minimum heat loss
    min_heatloss = min(possible_heatloss)

    return min_heatloss
