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

def get_input(input_file: str='Inputs/Day14_Inputs.txt') -> list:
    """
    Extracts the layout of different types of rocks on the surface of a satellite dish. There are
    either rounded rocks (O), cube-shaped rocks (#) and empty spaces (.). By default the direction
    of the top row is the North direction.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the rock layout.
        The default is 'Inputs/Day14_Inputs.txt'.


    Returns
    -------
    rocks : tuple(str)
        Tuple of strings, with each string giving the layout of a different row of the dish.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines and format in tuple
        rocks = tuple(l.strip() for l in f.readlines())

    return rocks

import functools

# Use cache to decrease runtime
@functools.lru_cache(maxsize=None)
def roll_rocks(rocks, direction):
    """
    Tilts a dish with a given layout of rocks on its surface in a given direction, causing all
    round rocks ('O') to roll until they hit another rock in the other direction. Cubic rocks ('#')
    do not roll and rocks cannot roll past the boundaries of the dish. By default the direction
    of the top row of the rock layout is the North direction.

    Parameters
    ----------
    rocks : tuple(str)
        Tuple of strings, with each string giving the rock layout of a different row of the dish.
    direction : str
        The direction of the tilt; N for North, E for East, etc.

    Returns
    -------
    rocks : tuple(str)
        The rock layout after the rocks have settled following the tilt of the dish.

    """
    # Format the rock layout into a 2D list of characters, with the direction of the rolling set
    # to the end of the rows
    if direction == 'N':
        rocks = [[row[col] for row in rocks[::-1]] for col in range(len(rocks[0]))]
    elif direction == 'S':
        rocks = [[row[col] for row in rocks] for col in range(len(rocks[0]))[::-1]]
    elif direction == 'W':
        rocks = [[col for col in l[::-1]] for l in rocks]
    elif direction == 'E':
        rocks = [[col for col in l] for l in rocks]

    # For each row in the layout
    for row in range(len(rocks)):
        # For each column in the row, starting from the right (not including rightmost row as any
        # rocks here cannot move)
        for col in range(len(rocks[row]) - 1)[::-1]:
            # If a round rock is found
            if rocks[row][col] == 'O':
                # Try and find the first cubic rock to the right of this one
                try:
                    next_cube = rocks[row].index('#', col)
                # If none exist then set to the rightmost end of the row
                except ValueError:
                    next_cube = len(rocks[row])
                # Try and find the first round rock to the right of this one
                try:
                    next_round = rocks[row].index('O', col+1)
                # If none exist then set to the rightmost end of the row
                except ValueError:
                    next_round = len(rocks[row])
                # Change the current position to empty space
                rocks[row][col] = '.'
                # Set the position one to the left of the nearest rock on the right of this one, to
                # be a round rock
                rocks[row][min(next_cube, next_round) - 1] = 'O'

    # Depending on how the rock layout was formatted before, convert it back into the general form
    if direction == 'N':
        rocks = tuple(''.join(row[col] for row in rocks) for col in range(len(rocks[0]))[::-1])
    elif direction == 'S':
        rocks = tuple(''.join(row[col] for row in rocks[::-1]) for col in range(len(rocks[0])))
    elif direction == 'W':
        rocks = tuple(''.join(row[::-1]) for row in rocks)
    elif direction == 'E':
        rocks = tuple(''.join(row) for row in rocks)

    return rocks

def rock_load(rocks):
    """
    Calculates the total load of the given rock layout on a satellite dish. The amount of load
    caused by a single rounded rock ('O') is equal to the number of rows from the rock to the south
    edge of the platform, including the row the rock is on. Cube-shaped rocks (#) don't contribute
    to load. By default the direction of the top row of the rock layout is the North direction.

    Parameters
    ----------
    rocks : tuple(str)
        Tuple of strings, with each string giving the rock layout of a different row of the dish.

    Returns
    -------
    load : int
        The total load on the dish.

    """
    # Calculate the product of each round rock with its row number + 1 and sum
    load = sum((n+1)*row.count('O') for n, row in enumerate(rocks[::-1]))

    return load

@time_function
def Day14_Part1(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Calculate the total load of a layout of rocks on a satellite dish with a starting layout given
    in an input file, after the dish is tilted North causing all round rocks to roll until they hit
    another rock. The rock layout contains rounded rocks (O), cube-shaped rocks (#) and empty
    spaces (.). By default the direction of the top row is the North direction. Cubic rocks ('#')
    do not roll and rocks cannot roll past the boundaries of the dish. The amount of load caused by
    a single rounded rock ('O') is equal to the number of rows from the rock to the south edge of
    the platform, including the row the rock is on. Cube-shaped rocks (#) don't contribute to load.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the rock layout.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    load : int
        The load on the dish after a tilt in the North direction.

    """
    # Parse input file to extract rock layout
    rocks = get_input(input_file)
    # Roll rocks in North direction
    rocks = roll_rocks(rocks, 'N')
    # Calculate load
    load = rock_load(rocks)
    
    return load

@functools.lru_cache(maxsize=None)
def cycle_rocks(rocks):
    """
    Performs a single cycle of tilts of a satellite with a given layout of rocks on its surface in
    the order North, West, South, East. Each tilt causes all round rocks ('O') to roll until they
    hit another rock in the other direction. Cubic rocks ('#') do not roll and rocks cannot roll
    past the boundaries of the dish. By default the direction of the top row of the rock layout is
    the North direction.

    Parameters
    ----------
    rocks : tuple(str)
        Tuple of strings, with each string giving the rock layout of a different row of the dish.

    Returns
    -------
    rocks : tuple(str)
        The rock layout after the rocks have settled following the cycle of tilts of the dish.

    """
    # For each direction in order
    for direction in ['N', 'W', 'S', 'E']:
        # Tilt the dish and find the new rock layout
        rocks = roll_rocks(rocks, direction)

    return rocks

@time_function
def Day14_Part2(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Calculate the total load of a layout of rocks on a satellite dish with a starting layout given
    in an input file, after the dish is cycled through a series of tilts 1 billion times. The rock
    layout contains rounded rocks (O), cube-shaped rocks (#) and empty spaces (.). By default the
    direction of the top row is the North direction. Each tilt causes all round rocks to roll until
    they hit another rock. Cubic rocks ('#') do not roll and rocks cannot roll past the boundaries
    of the dish. In each cycle the dish is tilted in every direction once in the order North, West,
    South, East. The amount of load caused by a single rounded rock ('O') is equal to the number of
    rows from the rock to the south edge of the platform, including the row the rock is on.
    Cube-shaped rocks (#) don't contribute to load.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the rock layout.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    load : int
        The load on the dish after 1 billion tilt cycles are performed on the dish.

    """
    # Parse input file to extract rock layout
    rocks = get_input(input_file)
    # Start at zero cycles
    cycles = 0
    # Create a dictionary of the rock layout obtained after each number of cycles
    rock_dict = {}
    # While we have not seen the current layout before, i.e. no loop has been found yet
    while rocks not in rock_dict.values():
        # Add the current layout to the rock_dict
        rock_dict[cycles] = rocks
        # Perform a single cycle on the rocks
        rocks = cycle_rocks(rocks)
        # Increment cycle counter
        cycles += 1

    # Once we find a match in rock_dict with the current rock layout, we have found a loop which
    # will repeat forever:
    # Find the index of the matched rock layout in rock_dict
    repeat = (list(rock_dict.keys())[list(rock_dict.values()).index(rocks)])
    print(f'Found Match: Cycle {cycles} matches Cycle {repeat}')

    # Find the length of the loop
    loop_length = cycles - repeat
    # Find the number of cycles left after an integer number of these loops from this point
    remainder = (1000000000 - repeat)%loop_length
    # Extract the layout correposnding to that many cycles into the loop
    final_layout = rock_dict[remainder+repeat]
    # Calculate the corresponding load
    load = rock_load(final_layout)

    return load
