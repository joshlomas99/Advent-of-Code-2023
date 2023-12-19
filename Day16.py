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

import numpy as np

def get_input(input_file: str='Inputs/Day16_Inputs.txt') -> list:
    """
    Extracts the layout of a square grid of mirrors and beam splitters from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid layout.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    grid : numpy.2darray(char)
        2D numpy array of characters representing the contents of each grid position.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines and convert to numpy array
        grid = np.array([[c for c in l.strip()] for l in f.readlines()])

    return grid

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

@time_function
def Day16_Part1(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Determines the number of energised tiles in a 2D grid containing a series of mirrors and beam
    splitters, the layout of which is given in an input file, when a light beam enters the grid
    from the top left corner travelling to the right, and bounces around the grid.

    - If the beam encounters empty space (.), it continues in the same direction.
    - If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the
    angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would
    continue upward in the mirror's column, while a rightward-moving beam that encounters a \
    mirror would continue downward from the mirror's column.
    - If the beam encounters the pointy end of a splitter (| or -), the beam passes through the
    splitter as if the splitter were empty space. For instance, a rightward-moving beam that
    encounters a - splitter would continue in the same direction.
    - If the beam encounters the flat side of a splitter (| or -), the beam is split into two
    beams going in each of the two directions the splitter's pointy ends are pointing. For
    instance, a rightward-moving beam that encounters a | splitter would split into two beams:
    one that continues upward from the splitter's column and one that continues downward from
    the splitter's column.

    Beams do not interact with other beams; a tile can have many beams passing through it at the
    same time. A tile is energized if that tile has at least one beam pass through it, reflect in
    it, or split in it. Beams that reach the edges of the grid travelling outwards do not travel
    any further.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid layout.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    num_energised : int
        The number of energised tiles after the beam has bounced around every part of its path.

    """
    # Parse input file and extract grid layout
    grid = get_input(input_file)
    # Start with the beam entering the top right corner of the grid from the left
    beams = {((0, -1), (0, 1))}
    # Initialise set of searched beam states (location, direction)
    searched = set()
    # While there are moving beams
    while beams:
        # Initialise new set of beams after one step of movement from current states
        new_beams = set()
        # For each current beam state
        for loc, direction in beams:
            # Find new location of beam
            new_loc = add_tuple(loc, direction)
            # If the new location is out of the grid, just add the beam state to searched and
            # do not consider it any further
            if any(p < 0 for p in new_loc) or new_loc[0] >= len(grid) or new_loc[1] >= len(grid[0]):
                searched.add((loc, direction))
                continue
            # For \ mirrors, reflection causes direction in each axis to swap around
            if grid[new_loc] == '\\':
                new_dir = (direction[1], direction[0])
                # If not searched this state before, add it to new_beams
                if (new_beam := (new_loc, new_dir)) not in searched:
                    new_beams.add(new_beam)
            # For \ mirrors, reflection causes direction in each axis to swap around and then
            # flip direction (multiply by -1)
            elif grid[new_loc] == '/':
                new_dir = (-direction[1], -direction[0])
                # If not searched this state before, add it to new_beams
                if (new_beam := (new_loc, new_dir)) not in searched:
                    new_beams.add(new_beam)
            # For | splitters, if the beam is travelling horizontally then add two new beams,
            # one moving down from here and one moving up
            elif grid[new_loc] == '|' and direction[1]:
                # If not searched this state before, add it to new_beams
                if (new_beam1 := (new_loc, (-1, 0))) not in searched:
                    new_beams.add(new_beam1)
                # If not searched this state before, add it to new_beams
                if (new_beam2 := (new_loc, (1, 0))) not in searched:
                    new_beams.add(new_beam2)
            # For - splitters, if the beam is travelling vertically then add two new beams,
            # one moving left from here and one moving right
            elif grid[new_loc] == '-' and direction[0]:
                # If not searched this state before, add it to new_beams
                if (new_beam1 := (new_loc, (0, -1))) not in searched:
                    new_beams.add(new_beam1)
                # If not searched this state before, add it to new_beams
                if (new_beam2 := (new_loc, (0, 1))) not in searched:
                    new_beams.add(new_beam2)
            # If beam was moving in the wrong direction for a splitter, or is on an empty tile,
            # just move to the next position and add to new beams if not searched before
            elif (new_beam := (new_loc, direction)) not in searched:
                new_beams.add(new_beam)
            # Add this beam state to searched
            searched.add((loc, direction))
        # Set beams to the new set of beams and continue the loop
        beams = new_beams.copy()

    # Find set of every unique tile visited by the beam in any direction
    energised = {b[0] for b in searched}

    # Find length of energised tiles set (-1 to remove start position outside grid)
    num_energised = len(energised) - 1
    
    return num_energised

from tqdm import tqdm

def Day16_Part2(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Determines the maximum possible number of tiles in a 2D grid containing a series of mirrors
    and beam splitters, the layout of which is given in an input file, which can be energised by
    a beam of light entering from any point on the outside of the grid, travelling inwards and
    bouncing around the grid.

    - If the beam encounters empty space (.), it continues in the same direction.
    - If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the
    angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would
    continue upward in the mirror's column, while a rightward-moving beam that encounters a \
    mirror would continue downward from the mirror's column.
    - If the beam encounters the pointy end of a splitter (| or -), the beam passes through the
    splitter as if the splitter were empty space. For instance, a rightward-moving beam that
    encounters a - splitter would continue in the same direction.
    - If the beam encounters the flat side of a splitter (| or -), the beam is split into two
    beams going in each of the two directions the splitter's pointy ends are pointing. For
    instance, a rightward-moving beam that encounters a | splitter would split into two beams:
    one that continues upward from the splitter's column and one that continues downward from
    the splitter's column.

    Beams do not interact with other beams; a tile can have many beams passing through it at the
    same time. A tile is energized if that tile has at least one beam pass through it, reflect in
    it, or split in it. Beams that reach the edges of the grid travelling outwards do not travel
    any further.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid layout.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    max_energised : int
        The maximum possible number of energised tiles which can be achieved after the beam has
        bounced around every part of its path, having entered from any point on the outside of the
        grid travelling inwards.

    """
    # Parse input file and extract grid layout
    grid = get_input(input_file)

    # Create list of possible starting states, outisde the grid and travelling in:
    # From the top
    possible_starts = [((-1, col), (1, 0)) for col in range(len(grid[0]))]
    # From the bottom
    possible_starts += [((len(grid), col), (-1, 0)) for col in range(len(grid[0]))]
    # From the left
    possible_starts += [((row, -1), (0, 1)) for row in range(len(grid))]
    # From the right
    possible_starts += [((row, len(grid[0])), (0, -1)) for row in range(len(grid))]

    # Initialise list of the number of energised tile for each starting position
    num_energised = []

    # For each starting position
    for start in tqdm(possible_starts):
        # Start at the current starting position
        beams = {start}
        # Initialise set of searched beam states (location, direction)
        searched = set()
        # While there are moving beams
        while beams:
            # Initialise new set of beams after one step of movement from current states
            new_beams = set()
            # For each current beam state
            for loc, direction in beams:
                # Find new location of beam
                new_loc = add_tuple(loc, direction)
                # If the new location is out of the grid, just add the beam state to searched and
                # do not consider it any further
                if any(p < 0 for p in new_loc) or new_loc[0] >= len(grid) or new_loc[1] >= len(grid[0]):
                    searched.add((loc, direction))
                    continue
                # For \ mirrors, reflection causes direction in each axis to swap around
                if grid[new_loc] == '\\':
                    new_dir = (direction[1], direction[0])
                    # If not searched this state before, add it to new_beams
                    if (new_beam := (new_loc, new_dir)) not in searched:
                        new_beams.add(new_beam)
                # For \ mirrors, reflection causes direction in each axis to swap around and then
                # flip direction (multiply by -1)
                elif grid[new_loc] == '/':
                    new_dir = (-direction[1], -direction[0])
                    # If not searched this state before, add it to new_beams
                    if (new_beam := (new_loc, new_dir)) not in searched:
                        new_beams.add(new_beam)
                # For | splitters, if the beam is travelling horizontally then add two new beams,
                # one moving down from here and one moving up
                elif grid[new_loc] == '|' and direction[1]:
                    # If not searched this state before, add it to new_beams
                    if (new_beam1 := (new_loc, (-1, 0))) not in searched:
                        new_beams.add(new_beam1)
                    # If not searched this state before, add it to new_beams
                    if (new_beam2 := (new_loc, (1, 0))) not in searched:
                        new_beams.add(new_beam2)
                # For - splitters, if the beam is travelling vertically then add two new beams,
                # one moving left from here and one moving right
                elif grid[new_loc] == '-' and direction[0]:
                    # If not searched this state before, add it to new_beams
                    if (new_beam1 := (new_loc, (0, -1))) not in searched:
                        new_beams.add(new_beam1)
                    # If not searched this state before, add it to new_beams
                    if (new_beam2 := (new_loc, (0, 1))) not in searched:
                        new_beams.add(new_beam2)
                # If beam was moving in the wrong direction for a splitter, or is on an empty tile,
                # just move to the next position and add to new beams if not searched before
                elif (new_beam := (new_loc, direction)) not in searched:
                    new_beams.add(new_beam)
                # Add this beam state to searched
                searched.add((loc, direction))
            # Set beams to the new set of beams and continue the loop
            beams = new_beams.copy()

        # Find set of every unique tile visited by the beam in any direction
        energised = {b[0] for b in searched}
        
        # Find length of energised tiles set (-1 to remove start position outside grid) and add
        # to list
        num_energised.append(len(energised) - 1)

    # Extract maximum number of energised tiles
    max_energised = max(num_energised)
    
    return max_energised
