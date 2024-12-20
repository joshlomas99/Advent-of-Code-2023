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

def get_input(input_file: str='Inputs/Day21_Inputs.txt') -> tuple:
    """
    Extract the layout of a garden consisting of plots (.), rocks (#) and a starting position (S)
    from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden layout.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    rocks : set(tuple(int))
        Set of (x, y) coordinates of every rock.
    pos : tuple(int)
        Starting (x, y) coordinates.
    bounds : tuple(int)
        Boundaries of the garden in each dimension.

    """
    # Parse input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
    
    rocks = set()
    # Loop through garden
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            # Record rock coordinates and starting position
            if lines[r][c] == '#':
                rocks.add((r, c))
            elif lines[r][c] == 'S':
                pos = (r, c)

    # Found boundaries
    bounds = (len(lines), len(lines[0]))

    return rocks, pos, bounds

# Four orthogonal directions
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

@time_function
def Day21_Part1(input_file: str='Inputs/Day21_Inputs.txt') -> int:
    """
    Determines how many garden plots, laid out according to an input file, can be reached in
    exactly 64 steps from the starting point. The garden contains rocks which cannot be passed
    through.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden layout.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    num_reachable : int
        Number of reachable points in exactly 64 steps.

    """
    # Parse input gile to extract rock positions and starting point
    rocks, pos, bounds = get_input(input_file)

    # Track all reachable points on even numbered steps (all reachable after 64 steps)
    reachable = {pos}
    # Track new positions reached on the last step
    last_reached = {pos}
    # Track all reached points
    all_reached = {pos}
    # Take 64 steps
    for steps in range(1, 64+1):
        new_last_reached = set()
        # For each new position reached in the last step
        for pos in last_reached:
            # Test each direction
            for d in DIRECTIONS:
                new_pos = (pos[0]+d[0], pos[1]+d[1])
                # If we are outside the garden boundaries, skip
                if not (0 <= new_pos[0] < bounds[0] and 0 <= new_pos[1] < bounds[1]):
                    continue
                # If we have hit a rock or found this position before, skip
                if new_pos in rocks or new_pos in all_reached:
                    continue
                # Add point to sets
                all_reached.add(new_pos)
                new_last_reached.add(new_pos)
                # If we are on an even step, add to reachable set
                if not steps%2:
                    reachable.add(new_pos)
        last_reached = new_last_reached.copy()

    # Count number of unique positions reached in an even number of steps up to 64
    num_reachable = len(reachable)

    return num_reachable

import numpy as np

@time_function
def Day21_Part2(input_file: str='Inputs/Day21_Inputs.txt') -> int:
    """
    Determines how many garden plots, laid out according to an input file, can be reached in
    exactly 26501365 steps from the starting point. The garden contains rocks which cannot be
    passed through. The garden plots and rocks are set up so that the given map repeats infinitely
    in every direction, with the layout wrapping around at the map boundaries.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden layout.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    num_reachable : int
        Number of reachable points in exactly 26501365 steps around the infinite garden.

    """
    # Parse input gile to extract rock positions and starting point
    rocks, pos, bounds = get_input(input_file)

    # Track unique points reachable in even and odd numbers of steps (every position enters exactly
    # one of these, and the reachable positions flip every step between all points reached on an
    # even number of steps and all those reached on an odd number of steps)
    reachable_even, reachable_odd = {pos}, set()
    # Take enough steps for a repeating pattern to be found, based on the width of the garden map
    # of 131 steps in both axis, every 131 steps the map wraps so the pattern of discovered points
    # should repeat, after an initial 65 steps due to starting from the centre of the first map
    steps = np.arange(0, 131*2 + 66, 1)
    # Track number of reachable points after each step
    num_reachable = [len(reachable_even)]
    #
    # Track new positions reached on the last step
    last_reached = {pos}
    # Track all reached points
    all_reached = {pos}
    # Loop through steps
    for step in steps[1:]:
        new_last_reached = set()
        # For each new position reached in the last step
        for pos in last_reached:
            # Test each direction
            for d in DIRECTIONS:
                new_pos = (pos[0]+d[0], pos[1]+d[1])
                # If we hit a rock (found by wrapping coordinates onto original map) or we have
                # already found this position, skip
                if (new_pos[0]%bounds[0], new_pos[1]%bounds[1]) in rocks or new_pos in all_reached:
                    continue
                # Add point to sets
                all_reached.add(new_pos)
                new_last_reached.add(new_pos)
                # Depending on if we are on an even or odd step, add to corresponding reachable set
                if step%2:
                    reachable_odd.add(new_pos)
                else:
                    reachable_even.add(new_pos)
        # Add relevant number of reachable points to list
        if step%2:
            num_reachable.append(len(reachable_odd))
        else:
            num_reachable.append(len(reachable_even))
        last_reached = new_last_reached.copy()

    # Now extract the sequence of number of reachable points at each point the map wraps around
    # again by the size of the original map, this should form a quadratic sequence (2D space)
    mod_f = [num_reachable[65 + 131*i] for i in range(3)]

    # Find general form of the sequence a*n**2 + b*n + c:
    # Find difference between each element
    diff = [mod_f[i+1] - mod_f[i] for i in range(len(mod_f)-1)]
    # Find second derivative
    diff2 = {diff[i+1] - diff[i] for i in range(len(diff)-1)}
    # For a quadratic sequence, the second derivative should be constant
    assert len(diff2) == 1
    # If so, this is 2a - twice the coefficient of n**2
    a = diff2.pop()//2

    # Find array of a*n**2
    squares = np.array([a*i**2 for i in range(len(mod_f))])
    # And subtract from sequence to leave a linear sequence
    linear = mod_f - squares
    # Find derivative
    diff = set(linear[1:] - linear[:-1])
    # For a linear sequence, the first derivative should be constant
    assert len(diff) == 1
    # If so, this is b - the coefficient of n
    b = diff.pop()
    # The constant c is the first element in the sequence (n = 0)
    c = mod_f[0]

    # Find value of n corresponding to the desired number of steps
    n = (26501365 - 65)/131
    # Input into sequence to find number of reachable points
    steps = int(a*n**2 + b*n + c)

    return steps
