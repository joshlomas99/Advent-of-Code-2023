import numpy as np

def get_input(input_file: str='Inputs/Day13_Inputs.txt') -> list:
    """
    Extracts a series of patterns of ash (.) and rock (#) from an input file, each new pattern is
    separated with a newline.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the patterns.
        The default is 'Inputs/Day13_Inputs.txt'.


    Returns
    -------
    patterns : list(numpy.2darray(char))
        List of patterns, where each pattern is formatted as a 2D numpy array of characters,
        either '.' or '#', for easier indexing.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines
        lines = [l.strip() for l in f.readlines()]
        # Start list of patterns
        patterns = [[]]
        for l in lines:
            # If newline, convert latest pattern to numpy array and add new empty list
            if len(l) == 0:
                patterns[-1] = np.array(patterns[-1])
                patterns.append([])
            # Else add row to current pattern and split into individual characters
            else:
                patterns[-1].append([c for c in l])
        # Convert the final pattern to a numpy array
        patterns[-1] = np.array(patterns[-1])

    return patterns

def Day13_Part1(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Finds the summary of a series of patterns of rock and ash given in an input file. Each pattern
    is a 2D grid with '.' representing ash and '#' representing rock. Each pattern has a single
    line of reflection, either vertical or horizontal, where the patterns either side are mirrored,
    up to the end of the smaller side. The summary of all the patterns is found by adding up the
    number of columns to the left of each vertical line of reflection, to 100 multiplied by the
    number of rows above each horizontal line of reflection.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the patterns.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    summary : int
        Summary of all the given patterns.

    """
    # Parse input file and extract patterns
    patterns = get_input(input_file)

    # Sum up all summaries
    summary = 0
    # For each pattern
    for pattern in patterns:
        # Boolean check for if a vertical reflection is found
        col_ref = False
        # For each column, starting at the second column, which will be tested as the far left
        # column of the mirrored section on the right of the line of reflection
        for col in range(1, len(pattern[0])):
            # Extract the section of the pattern to the left of the current tested line of ref.
            left_section = pattern[:, max(0, 2*col - len(pattern[0])):col]
            # Extract the section of the pattern to the right of the current tested line of ref.
            right_section = pattern[:, col:2*col]
            # If the left side equals the right side flipped vertically in every place, this is a
            # valid line of reflection
            if (left_section == np.flip(right_section, axis=1)).all():
                # Add the column number to the left of the line of reflection
                summary += col
                # Set boolean check that a vertical line of reflection was found
                col_ref = True
                # No need to check for any further vertical lines of reflection
                break
        # If vertical reflection was found, no need to check for any horizontal lines of reflection
        if col_ref:
            continue
        # Else for each row, starting at the second row, which will be tested as the top row of the
        # mirrored section below the line of reflection
        for row in range(1, len(pattern)):
            # Extract the section of the pattern above the current tested line of reflection
            top_section = pattern[max(0, 2*row - len(pattern)):row, :]
            # Extract the section of the pattern below the current tested line of reflection
            bottom_section = pattern[row:2*row, :]
            # If the top section equals the bottom section flipped horizontally in every place,
            # this is a valid line of reflection
            if (top_section == np.flip(bottom_section, axis=0)).all():
                # Add 100 times the row number above the line of reflection
                summary += 100*row
                # No need to check for any further horizontal lines of reflection
                break
    
    return summary

def Day13_Part2(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Finds the summary of a series of patterns of rock and ash given in an input file. Each pattern
    is a 2D grid with '.' representing ash and '#' representing rock. Each pattern has a single
    line of reflection, either vertical or horizontal, where the patterns either side are mirrored,
    up to the end of the smaller side. The summary of all the patterns is found by adding up the
    number of columns to the left of each vertical line of reflection, to 100 multiplied by the
    number of rows above each horizontal line of reflection. However, every mirror has exactly one
    smudge: exactly one '.' or '#' should be the opposite type, so the line of reflection which can
    be found by flipping a single point should instead be found for each pattern.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the patterns.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    summary : int
        Summary of all the given patterns, accounting for the single smudge on each one.

    """
    # Parse input file and extract patterns
    patterns = get_input(input_file)

    # Sum up all summaries
    summary = 0
    # For each pattern
    for pattern in patterns:
        # Boolean check for if a vertical reflection is found
        col_ref = False
        # For each column, starting at the second column, which will be tested as the far left
        # column of the mirrored section on the right of the line of reflection
        for col in range(1, len(pattern[0])):
            # Extract the section of the pattern to the left of the current tested line of ref.
            left_section = pattern[:, max(0, 2*col - len(pattern[0])):col]
            # Extract the section of the pattern to the right of the current tested line of ref.
            right_section = pattern[:, col:2*col]
            # For a valid line of relfection with a single smudge, there should be exactly one
            # point which does not match between the two sides, so find the number of mismatched
            # points, and find where it is exactly 1
            if (left_section != np.flip(right_section, axis=1)).sum() == 1:
                # Add the column number to the left of the line of reflection
                summary += col
                # Set boolean check that a vertical line of reflection was found
                col_ref = True
                # No need to check for any further vertical lines of reflection
                break
        # If vertical reflection was found, no need to check for any horizontal lines of reflection
        if col_ref:
            continue
        # Else for each row, starting at the second row, which will be tested as the top row of the
        # mirrored section below the line of reflection
        for row in range(1, len(pattern)):
            # Extract the section of the pattern above the current tested line of reflection
            top_section = pattern[max(0, 2*row - len(pattern)):row, :]
            # Extract the section of the pattern below the current tested line of reflection
            bottom_section = pattern[row:2*row, :]
            # For a valid line of relfection with a single smudge, there should be exactly one
            # point which does not match between the two sides, so find the number of mismatched
            # points, and find where it is exactly 1
            if (top_section != np.flip(bottom_section, axis=0)).sum() == 1:
                # Add 100 times the row number above the line of reflection
                summary += 100*row
                # No need to check for any further horizontal lines of reflection
                break
    
    return summary
