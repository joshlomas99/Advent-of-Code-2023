def get_input(input_file: str='Inputs/Day2_Inputs.txt') -> list:
    """
    Extracts the number of occurences of each colour of cube, for every set of cubes revealed from
    a bag in a game, for a series of different games, which are detailled in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file detailing the games. Each game is listed with its ID number (e.g. 11 for
        Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were
        revealed from the bag (like 3 red, 5 green, 4 blue).
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    all_games : dict(int: dict(str: list(int)))
        Extracted occurences of each colour of cube, in each set, in every game.

    """
    # Parse input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
        # Create empty games dict
        all_games = {}
        for line in lines:
            game_id, cube_sets = line.split(': ')
            # Extract game ID number
            game_id = int(game_id.split()[-1])
            # Split up cube_sets
            cube_sets = cube_sets.split('; ')
            # Create empty dict for each cube colour for the current game ID
            all_games[game_id] = {}
            for cube_set in cube_sets:
                # For each colour cube in each game
                for cube in cube_set.split(', '):
                    num, colour = cube.split()
                    # Fill dict with list of number of cubes of each colour in each set
                    if colour in all_games[game_id]:
                        all_games[game_id][colour].append(int(num))
                    else:
                        all_games[game_id][colour] = [int(num)]

    return all_games

def Day2_Part1(input_file: str='Inputs/Day2_Inputs.txt',
               max_cubes = {'red': 12, 'green': 13, 'blue': 14}) -> int:
    """
    Determines the sum of the IDs of games, out of a series given in an input file, which would be
    possible given a bag of cubes containing given amounts of each colour of cube. In each game, a
    series of sets of cubes are revealed from the bag, and the number of cubes of each colour is
    recorded for each set.

    Parameters
    ----------
    input_file : str, optional
        Input file detailing the games. Each game is listed with its ID number (e.g. 11 for
        Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were
        revealed from the bag (like 3 red, 5 green, 4 blue).
        The default is 'Inputs/Day1_Inputs.txt'.
    
    max_cubes : dict(str: int), optional
        The given number of cubes of each colour in the bag.
        The default is {'red': 12, 'green': 13, 'blue': 14}.

    Returns
    -------
    id_sum : int
        The sum of the IDs of games which are possible given the number of each coloured cubes in
        the bag.

    """
    # Parse input file to get the occurences of each colour across all sets in each game
    all_games = get_input(input_file)
    # For each game
    for game_id, game in all_games.items():
        # For each cube colour
        for colour, nums in game.items():
            # Find the max number of cubes of that colour were observed
            all_games[game_id][colour] = max(nums)

    # Find every game where the highest number of cubes of every colour observed in less than or
    # equal to the number given in the bag, sum the corresponding IDs
    id_sum = sum(game_id for game_id, game in all_games.items()\
                 if all(num <= max_cubes[colour] for colour, num in game.items()))

    return id_sum

import numpy as np

def Day2_Part2(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    """
    Determines the sum of the power of the minimum sets of cubes required to play a series of games
    given in an input file. In each game, a series of sets of cubes are revealed from the bag, and
    the number of cubes of each colour is recorded for each set. The power of a set of cubes is
    equal to the numbers of red, green, and blue cubes multiplied together.

    Parameters
    ----------
    input_file : str, optional
        Input file detailing the games. Each game is listed with its ID number (e.g. 11 for
        Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were
        revealed from the bag (like 3 red, 5 green, 4 blue).
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    power_sum : int
        The sum of the power of the minimum sets reqired to play each game.

    """
    # Parse input file to get the occurences of each colour across all sets in each game
    all_games = get_input(input_file)
    # For each game
    for game_id, game in all_games.items():
        # For each cube colour
        for colour, nums in game.items():
            # Find the max number of cubes of that colour were observed
            all_games[game_id][colour] = max(nums)

    # The minimum number of each coloured cube required is the maximum number observed, so find
    # the product of these values for each game, and then sum
    power_sum = sum(np.product([num for num in game.values()]) for game in all_games.values())

    return power_sum
