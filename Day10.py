import numpy as np

def get_input(input_file: str='Inputs/Day10_Inputs.txt', pad: bool=False) -> list:
    """
    Extracts 2D grid of pipes from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid.
        The default is 'Inputs/Day10_Inputs.txt'.

    pad : bool, optional
        Whether or not to apply padding to every side of the grid with '.' representing empty space.
        Default is False.

    Returns
    -------
    pipes : numpy.2darray(char)
        2D numpy array of characters representing the grid.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract grid and separate characters
        pipes = [[c for c in l.strip()] for l in f.readlines()]
        # Pad the grid on all sides if that option is selected
        if pad:
            pipes = [['.']*len(pipes[0])] + pipes
            pipes += [['.']*len(pipes[0])]
            pipes = [['.'] + r + ['.'] for r in pipes]
    # Convert to numpy array on return for simpler indexing
    return np.array(pipes)

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

# Define all orthogonal directions
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
# Define directions which can be moved in from all types of pipe
PIPE_DIRS = {'|': [(-1, 0), (1, 0)], '-': [(0, 1), (0, -1)], 'L': [(-1, 0), (0, 1)],
              'J': [(-1, 0), (0, -1)], '7': [(1, 0), (0, -1)], 'F': [(1, 0), (0, 1)]}

def Day10_Part1(input_file: str='Inputs/Day10_Inputs.txt') -> int:
    """
    Determines how many steps along a loop of pipes it takes to get from a given starting position
    to the point farthest from the starting position. The pipes are laid out on a 2D grid which
    is given in an input file, and contains exactly one loop of pipes.

    ``|`` is a vertical pipe connecting north and south.

    ``-`` is a horizontal pipe connecting east and west.

    ``L`` is a 90-degree bend connecting north and east.

    ``J`` is a 90-degree bend connecting north and west.

    ``7`` is a 90-degree bend connecting south and west.

    ``F`` is a 90-degree bend connecting south and east.

    ``.`` is ground; there is no pipe in this tile.

    ``S`` is the starting position; there is a pipe on this tile, but the shape is not given.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid of pipes.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    furthest_point : int
        The number of steps required to get from the starting position on the loop to the point
        farthest from the starting position.

    """
    # Parse input file and extract grid of pipes
    pipes = get_input(input_file)

    # Find coordinates of the 'S' tile - the start point
    start_point = tuple(i[0] for i in np.where(pipes == 'S'))
    # Start the loop at the start point
    loop = [start_point]
    # Find which direction can be moved from the start point based on which pipes are connected
    for next_dir in DIRECTIONS:
        # If there is a pipe in a given direction
        if pipes[(next_pos := add_tuple(start_point, next_dir))] in PIPE_DIRS:
            # If the start point can be reached from that pipe, this is a valid direction to start
            # moving in
            if start_point in [add_tuple(next_pos, pipe_dir)\
                               for pipe_dir in PIPE_DIRS[pipes[next_pos]]]:
                break

    # Until the start point is reached again (full loop)
    while next_pos != loop[0]:
        # Add the next point to the loop
        loop.append(next_pos)
        # Store the last direction moved in to avoid going backwards
        last_dir = (-next_dir[0], -next_dir[1])
        # Find possible directions from the current pipe
        possible_dirs = PIPE_DIRS[pipes[loop[-1]]]
        # Find the previous direction travelled in the list of two possible directions
        last_dir_loc = possible_dirs.index(last_dir)
        # And choose the other one (don't go backwards)
        next_dir = possible_dirs[(last_dir_loc + 1)%2]
        # Set this next position and repeat
        next_pos = add_tuple(loop[-1], next_dir)

    # The furthest point is just the length of the loop divided by 2
    furthest_point = len(loop)//2
    
    return furthest_point

def Day10_Part2(input_file: str='Inputs/Day10_Inputs.txt') -> int:
    """
    Finds the total area enclosed by a loop of pipes on a 2D grid which is given in an input file,
    and contains exactly one loop of pipes.

    ``|`` is a vertical pipe connecting north and south.

    ``-`` is a horizontal pipe connecting east and west.

    ``L`` is a 90-degree bend connecting north and east.

    ``J`` is a 90-degree bend connecting north and west.

    ``7`` is a 90-degree bend connecting south and west.

    ``F`` is a 90-degree bend connecting south and east.

    ``.`` is ground; there is no pipe in this tile.

    ``S`` is the starting position; there is a pipe on this tile, but the shape is not given.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid of pipes.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    enclosed_tiles : int
        The number of tiles enclosed by the loop.

    """
    # Parse input file and extract grid of pipes, and add padding of empty ground '.' on every side
    pipes = get_input(input_file, pad=True)

    #### FIND THE LOOP ####
        
    # Find coordinates of the 'S' tile - the start point
    start_point = tuple(i[0] for i in np.where(pipes == 'S'))
    # Start the loop at the start point
    loop = [start_point]
    # Find which direction can be moved from the start point based on which pipes are connected
    for next_dir in DIRECTIONS:
        # If there is a pipe in a given direction
        if pipes[(next_pos := add_tuple(start_point, next_dir))] in PIPE_DIRS:
            # If the start point can be reached from that pipe, this is a valid direction to start
            # moving in
            if start_point in [add_tuple(next_pos, pipe_dir)\
                               for pipe_dir in PIPE_DIRS[pipes[next_pos]]]:
                break

    # Until the start point is reached again (full loop)
    while next_pos != loop[0]:
        # Add the next point to the loop
        loop.append(next_pos)
        # Store the last direction moved in to avoid going backwards
        last_dir = (-next_dir[0], -next_dir[1])
        # Find possible directions from the current pipe
        possible_dirs = PIPE_DIRS[pipes[loop[-1]]]
        # Replace all given pipe symbols with the corresponding box drawing symbols, both for
        # easier visualisation but more importantly to differentiate pipes in the loop from other
        # pipes, which could be enclosed
        pipes[next_pos] = pipes[next_pos].replace('|', '│').replace('-', '─').replace('L', '└')\
            .replace('J', '┘').replace('7', '┐').replace('F', '┌')
        # Find the previous direction travelled in the list of two possible directions
        last_dir_loc = possible_dirs.index(last_dir)
        # And choose the other one (don't go backwards)
        next_dir = possible_dirs[(last_dir_loc + 1)%2]
        # Set this next position and repeat
        next_pos = add_tuple(loop[-1], next_dir)

    #### SEARCH FOR ENCLOSED TILES ####

    # Starting in the top left corner
    pos = (0, 0)
    # Start outside the loop and not on a row of the loop
    inside, row_type = 0, 0
    # Count enclosed tiles
    enclosed_tiles = 0
    # While there are rows left to search
    while pos[0] < len(pipes):
        # While there are positions on the current row left to search
        while pos[1] < len(pipes[0]):
            # If the current tile is not part of the loop and we are inside the loop, count it
            # as an enclosed tile
            if pipes[pos] in {'.', '|', '-', 'L', '7', 'J', 'F'} and inside:
                enclosed_tiles += 1
            # Else if the current tile is a vertical section of the loop, switch between
            # inside/outside depending on the current state
            elif pipes[pos] == '│':
                inside = (inside + 1)%2
            # Else if the current tile is a corner section of the loop, if we are already on a row
            # then depending on the previous corner tile crossed this one may or may not invert
            # the inside/outside state
            elif pipes[pos] in {'┌', '┐', '└', '┘'}:
                # If the current tile is a south-east corner, it must be starting a row which
                # comes from below, corresponding to row_type -1
                if pipes[pos] == '┌':
                    row_type = -1
                # Else if the current tile is a north-east corner, it must be starting a row which
                # comes from above, corresponding to row_type 1
                elif pipes[pos] == '└':
                    row_type = 1
                # Else if the current tile is a south-west corner, it must be ending a row by
                # moving down
                elif pipes[pos] == '┐':
                    # If the row_type is 1, i.e. the previous corner came from above, then
                    # together they act like a vertical loop section, inverting the inside/outside
                    # state, if row_type is -1 then the state doesn't change
                    if row_type == 1:
                        inside = (inside + 1)%2
                    # Set row_type back to zero as we have left the row
                    row_type = 0
                # Else if the current tile is a north-west corner, it must be ending a row by
                # moving up
                elif pipes[pos] == '┘':
                    # If the row_type is -1, i.e. the previous corner came from below, then
                    # together they act like a vertical loop section, inverting the inside/outside
                    # state, if row_type is 1 then the state doesn't change
                    if row_type == -1:
                        inside = (inside + 1)%2
                    # Set row_type back to zero as we have left the row
                    row_type = 0
            # Move to the next position to the right
            pos = add_tuple(pos, (0, 1))
        # Move to the beginning of the next row
        pos = (pos[0] + 1, 0)
    
    return enclosed_tiles
