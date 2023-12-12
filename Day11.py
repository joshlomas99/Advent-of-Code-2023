import numpy as np

def get_input(input_file: str='Inputs/Day11_Inputs.txt') -> list:
    """
    Extracts 2D grid of galaxies and empty space from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid.
        The default is 'Inputs/Day11_Inputs.txt'.
    Returns
    -------
    space : numpy.2darray(char)
        2D numpy array of characters representing the grid of space.

    """
    # Parse input file
    with open(input_file) as f:
        space = [[c for c in l.strip()] for l in f.readlines()]

    return np.array(space)

def Day11_Part1(input_file: str='Inputs/Day11_Inputs.txt') -> int:
    """
    Calculates the sum of the shortest distances between every pair of galaxies in a grid of
    galaxies separated by empty space, which is given in an input file. Distances are calculated
    only along orthogonal directions, and should account for the expansion of space by doubling
    the width of any rows or columns in the grid which contain no galaxies.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    total_distance : int
        The sum of the shortest distances between every pair of galaxies in the grid, accounting
        for the expansion of empty rows and columns.

    """
    # Parse input file to get the grid
    space = get_input(input_file)
    # Find all the galaxy coordinates
    galaxies = np.where(space == '#')
    # Convert to tuples
    galaxies = [(galaxies[0][j], galaxies[1][j]) for j in range(len(galaxies[0]))]
    # Find indices of empty rows and columns
    empty_rows = np.array([i for i in range(len(space)) if set(space[i, :]) == {'.'}])
    empty_cols = np.array([j for j in range(len(space[0])) if set(space[:, j]) == {'.'}])

    # Count the total distance
    total_distance = 0
    # For every galaxy
    for i in range(len(galaxies)):
        # For every other galaxy not counted yet
        for j in range(i+1, len(galaxies)):
            # Get galaxy coordinates
            galaxy1 = galaxies[i]
            galaxy2 = galaxies[j]
            # Find shortest distance between the galaxies (Manhattan distance)
            total_distance += sum(abs(galaxy1[i] - galaxy2[i]) for i in range(2))
            # Filter empty rows which have a higher index than the lower galaxy
            rows_more = empty_rows[min(galaxy1[0], galaxy2[0]) < empty_rows]
            # Count how many of the filtered rows have a lower index than the higher galaxy
            # These are all the empty rows between the two galaxies, so should be accounted for
            # again to include expansion
            total_distance += sum(rows_more < max(galaxy1[0], galaxy2[0]))
            # Filter empty columns which have a higher index than the lower galaxy
            cols_more = empty_cols[min(galaxy1[1], galaxy2[1]) < empty_cols]
            # Count how many of the filtered columns have a lower index than the higher galaxy
            # These are all the empty columns between the two galaxies, so should be accounted for
            # again to include expansion
            total_distance += sum(cols_more < max(galaxy1[1], galaxy2[1]))
    
    return total_distance

def Day11_Part2(input_file: str='Inputs/Day11_Inputs.txt', expansion = 1000000 - 1) -> int:
    """
    Calculates the sum of the shortest distances between every pair of galaxies in a grid of
    galaxies separated by empty space, which is given in an input file. Distances are calculated
    only along orthogonal directions, and should account for the expansion of space by adding a
    given amount to the width of any rows or columns in the grid which contain no galaxies.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid.
        The default is 'Inputs/Day11_Inputs.txt'.

    expansion : int, optional
        The number of extra rows/columns should be added to every empty row/column to account for
        the expansion of space.

    Returns
    -------
    total_distance : int
        The sum of the shortest distances between every pair of galaxies in the grid, accounting
        for the given expansion of empty rows and columns.

    """
    # Parse input file to get the grid
    space = get_input(input_file)
    # Find all the galaxy coordinates
    galaxies = np.where(space == '#')
    # Convert to tuples
    galaxies = [(galaxies[0][j], galaxies[1][j]) for j in range(len(galaxies[0]))]
    # Find indices of empty rows and columns
    empty_rows = np.array([i for i in range(len(space)) if set(space[i, :]) == {'.'}])
    empty_cols = np.array([j for j in range(len(space[0])) if set(space[:, j]) == {'.'}])

    # Count the total distance
    total_distance = 0
    # For every galaxy
    for i in range(len(galaxies)):
        # For every other galaxy not counted yet
        for j in range(i+1, len(galaxies)):
            # Get galaxy coordinates
            galaxy1 = galaxies[i]
            galaxy2 = galaxies[j]
            # Find shortest distance between the galaxies (Manhattan distance)
            total_distance += sum(abs(galaxy1[i] - galaxy2[i]) for i in range(2))
            # Filter empty rows which have a higher index than the lower galaxy
            rows_more = empty_rows[min(galaxy1[0], galaxy2[0]) < empty_rows]
            # Count how many of the filtered rows have a lower index than the higher galaxy
            # These are all the empty rows between the two galaxies, so should be added again
            # 'expansion' times to include expansion
            total_distance += expansion*sum(rows_more < max(galaxy1[0], galaxy2[0]))
            # Filter empty columns which have a higher index than the lower galaxy
            cols_more = empty_cols[min(galaxy1[1], galaxy2[1]) < empty_cols]
            # Count how many of the filtered columns have a lower index than the higher galaxy
            # These are all the empty columns between the two galaxies, so should be added again
            # 'expansion' times to include expansion
            total_distance += expansion*sum(cols_more < max(galaxy1[1], galaxy2[1]))
    
    return total_distance
