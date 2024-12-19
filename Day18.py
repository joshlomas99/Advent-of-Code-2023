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

def get_input(input_file: str='Inputs/Day18_Inputs.txt', expand: bool=False) -> list:
    """
    Extract the dig plan for a lagoon from an input file in the form (direction, distance, colour),
    where colours are given as hexidecimal digits. If the input is expanded, then each hexadecimal
    code (six hexadecimal digits long) is split into the first five hexadecimal digits, which
    encode the distance in meters as a five-digit hexadecimal number, and the last hexadecimal
    digit, which encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the dig plan.
        The default is 'Inputs/Day18_Inputs.txt'.
    expand : bool, optional
        Whether to expand the input.
        The default is False.

    Returns
    -------
    plan : list
        Extracted dig plan in the form (direction, distance, colour).

    """

    dir_dict = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    # Parse input file
    with open(input_file) as f:
        if expand:
            # Extract lines and format
            lines = [l.strip().split()[-1].strip('()#') for l in f.readlines()]
            # If expanding, split the hexadecimal and convert to base 10
            plan = [(dir_dict[l[-1]], int(l[:-1], base=16)) for l in lines]
        else:
            # Extract lines and format
            lines = [l.strip().split() for l in f.readlines()]
            plan = [(l[0], int(l[1]), l[2].strip('()')) for l in lines]

    return plan

# Map of direction symbols onto vectors
DIRECTIONS = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

import numpy as np

@time_function
def Day18_Part1(input_file: str='Inputs/Day18_Inputs.txt') -> int:
    """
    Determines how many cubic meters of lava could be held in a lagoon which is dug according
    to a plan given in an input file, where the lagoon boundary is given in the form (direction,
    distance, colour).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the dig plan.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    volume : int
        Volume of the lagoon.

    """
    # Parse input file to extract lagoon dig plan
    plan = get_input(input_file)

    # Find coordinates defining boundary of the lagoon
    outline = [(0, 0)]
    # Loop through dig plan
    for d, n, col in plan:
        for i in range(n):
            # Add each new coordinate
            outline.append((outline[-1][0]+DIRECTIONS[d][0], outline[-1][1]+DIRECTIONS[d][1]))

    # Find minimum coordinate of outline in both axis
    min_coords = [min(p[i] for p in outline) for i in range(2)]
    # Shift every coordinate so there is at least one row above the outline and one column to the
    # left (empty space all around the outline)
    outline = [(p[0] - min_coords[0] + 1, p[1] - min_coords[1] + 1) for p in outline]

    # Initialise grid of the area including the lagoon, starting as all ones
    grid = np.ones([max(p[i] for p in outline) + 2 for i in range(2)], dtype=int)
    # Set all outline points to 2
    for p in outline:
        grid[p] = 2

    # Set the top left corner (outside the grid) to 0
    grid[(0, 0)] = 0

    # Use breadth-first search to find all points outside the lagoon outline
    queue = [(0, 0)]
    # WHile there are points left to check
    while queue:
        # Remove oldest point in queue
        pos = queue.pop(0)
        # Check in each direction from the current point
        for d in DIRECTIONS.values():
            # Find the new coordinate
            new_pos = (pos[0]+d[0], pos[1]+d[1])
            # If this is outside the bounds of the area, skip
            if any(p < 0 for p in new_pos) or new_pos[0] >= len(grid) or new_pos[1] >= len(grid[0]):
                continue
            # Else if this point wasn't checked yet (still at 1), set to 0 and add pos to queue
            if grid[new_pos] == 1:
                grid[new_pos] = 0
                queue.append(new_pos)
    
    # Set all outline points to 1
    grid[grid == 2] = 1

    # Sum up all points still in the lagoon
    volume = np.sum(grid)
    
    return volume

@time_function
def Day18_Part2_Shoelace(input_file: str='Inputs/Day18_Inputs.txt') -> int:
    """
    Determines how many cubic meters of lava could be held in a lagoon which is dug according
    to a plan given in an input file, where the lagoon boundary is given in the form (direction,
    distance, colour), where colours are given as hexidecimal digits. However, now the input is
    expanded, such that each hexadecimal code (six hexadecimal digits long) is split into the
    first five hexadecimal digits, which encode the distance in meters as a five-digit hexadecimal
    number, and the last hexadecimal digit, which encodes the direction to dig: 0 means R, 1 means
    D, 2 means L, and 3 means U.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the dig plan.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    volume : int
        Volume of the lagoon.

    """
    # Parse input file to extract expanded lagoon dig plan
    plan = get_input(input_file, expand=True)
    
    # Find coordinates defining the corners of the lagoon boundary
    outline = [(0, 0)]
    # Loop through dig plan
    for d, n in plan:
        # Add each corner coordinate
        outline.append((outline[-1][0]+DIRECTIONS[d][0]*n, outline[-1][1]+DIRECTIONS[d][1]*n))

    # Use the shoelace theorem to find the area enclosed by the boundary
    left_sum = sum(outline[i][0]*outline[i+1][1] for i in range(len(outline)-1))
    right_sum = sum(outline[i][1]*outline[i+1][0] for i in range(len(outline)-1))
    
    area = abs(left_sum - right_sum)/2

    # Use Pick's theorem to find the number of points in the outline
    edge_points = sum(abs(outline[i][0] - outline[i+1][0]) + abs(outline[i][1] - outline[i+1][1]) \
                     for i in range(len(outline) - 1))

    # Combine values to find the volume of the lagoon
    total_internal_points = int(area + 1 - edge_points/2)
    volume = total_internal_points + edge_points

    return volume

@time_function
def Day18_Part2(input_file: str='Inputs/Day18_Inputs.txt') -> int:
    """
    Determines how many cubic meters of lava could be held in a lagoon which is dug according
    to a plan given in an input file, where the lagoon boundary is given in the form (direction,
    distance, colour), where colours are given as hexidecimal digits. However, now the input is
    expanded, such that each hexadecimal code (six hexadecimal digits long) is split into the
    first five hexadecimal digits, which encode the distance in meters as a five-digit hexadecimal
    number, and the last hexadecimal digit, which encodes the direction to dig: 0 means R, 1 means
    D, 2 means L, and 3 means U.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the dig plan.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    volume : int
        Volume of the lagoon.

    """
    # Parse input file to extract expanded lagoon dig plan
    plan = get_input(input_file, expand=True)
    
    # Find coordinates defining the corners of the lagoon boundary
    outline = [(0, 0)]
    # Loop through dig plan
    for d, n in plan:
        # Add each corner coordinate
        outline.append((outline[-1][0]+DIRECTIONS[d][0]*n, outline[-1][1]+DIRECTIONS[d][1]*n))

    # Old method - I forgot how it works, but it does
    v_divs = {p[0] for p in outline}
    v_divs.add(min(v_divs)-1)
    v_divs.add(max(v_divs)+1)
    h_divs = {p[1] for p in outline}
    h_divs.add(min(h_divs)-1)
    h_divs.add(max(h_divs)+1)
    
    v_divs = sorted(list(v_divs))
    h_divs = sorted(list(h_divs))
    
    outline_set = set()
    for i in range(len(outline) - 1):
        # Horizontal line
        if outline[i][0] == outline[i+1][0]:
            first_ind = h_divs.index(outline[i][1])
            last_ind = h_divs.index(outline[i+1][1])
            for j in range(min(first_ind, last_ind), max(first_ind, last_ind)):
                outline_set.add(((outline[i][0], h_divs[j]), (outline[i][0], h_divs[j+1])))
    
        # Vertical line
        if outline[i][1] == outline[i+1][1]:
            first_ind = v_divs.index(outline[i][0])
            last_ind = v_divs.index(outline[i+1][0])
            for j in range(min(first_ind, last_ind), max(first_ind, last_ind)):
                outline_set.add(((v_divs[j], outline[i][1]), (v_divs[j+1], outline[i][1])))
        
    outside = {(0, 0)}

    queue = [(0, 0)]
    while queue:
        section = queue.pop(0)
        top_left = (v_divs[section[0]], h_divs[section[1]])
        top_right = (v_divs[section[0]], h_divs[section[1]+1])
        bottom_left = (v_divs[section[0]+1], h_divs[section[1]])
        bottom_right = (v_divs[section[0]+1], h_divs[section[1]+1])
        outside_dirs = []
        if not (top_right, bottom_right) in outline_set:
            outside_dirs.append('R')
        if not (bottom_left, bottom_right) in outline_set:
            outside_dirs.append('D')
        if not (top_left, bottom_left) in outline_set:
            outside_dirs.append('L')
        if not (top_left, top_right) in outline_set:
            outside_dirs.append('U')
        for d in outside_dirs:
            new_section = (section[0]+DIRECTIONS[d][0], section[1]+DIRECTIONS[d][1])
            if any(p < 0 for p in new_section)\
                or new_section[0] >= len(v_divs) - 1 or new_section[1] >= len(h_divs) - 1:
                continue
            if new_section not in outside:
                outside.add(new_section)
                queue.append(new_section)
    
    volume = 0
    for v in range(len(v_divs) - 1):
        for h in range(len(h_divs) - 1):
            section = (v, h)
            top_left = (v_divs[section[0]], h_divs[section[1]])
            top_right = (v_divs[section[0]], h_divs[section[1]+1])
            bottom_left = (v_divs[section[0]+1], h_divs[section[1]])
            bottom_right = (v_divs[section[0]+1], h_divs[section[1]+1])
            # right side
            if (top_right, bottom_right) in outline_set:
                h_side = h_divs[h+1] - h_divs[h] + 1
            else:
                h_side = h_divs[h+1] - h_divs[h]
            # bottom side
            if (bottom_left, bottom_right) in outline_set:
                v_side = v_divs[v+1] - v_divs[v] + 1
            else:
                v_side = v_divs[v+1] - v_divs[v]
            if (v, h) not in outside:
                volume += v_side*h_side
                # bottom right
                if (top_right, bottom_right) in outline_set and (bottom_left, bottom_right) in outline_set:
                    volume -= 1
    
    volume += 1
    
    return volume
