def get_input(input_file: str='Inputs/Day3_Inputs.txt') -> list:
    """
    Extracts an engine schematic from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the schematic.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    schematic : list(str)
        Extracted engine schematic as a list of strings.

    """
    # Parse input file
    with open(input_file) as f:
        schematic = [l.strip() for l in f.readlines()]
    return schematic

def Day3_Part1(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Find the sum of all of the part numbers in an engine schematic given in an input file. The
    engine schematic containes numbers and symbols, and any number adjacent to a symbol (except
    for '.'), even diagonally, is a "part number".

    Parameters
    ----------
    input_file : str, optional
        Input file giving the engine schematic.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    part_sum : int
        Sum of all the part numbers in the given engine schematic.

    """
    # Parse input file
    schematic = get_input(input_file)
    
    part_sum = 0
    # Move through engine schematic line by line
    for r, row in enumerate(schematic):
        n = 0
        # Move through each line
        while n < len(row):
            # If a number is found
            if row[n].isnumeric():
                num_start = 1*n
                # Keep moving along until the end of the number (a non-number) is found
                while n < len(row) and row[n].isnumeric():
                    n += 1
                # Extract the full number
                num = int(row[num_start:n])
                # Now search around the number for a symbol other than '.', if one is found then
                # add the number to the part_sum and continue
                # Search left
                if num_start > 0 and row[num_start-1] != '.':
                    part_sum += num
                    continue
                # Search right
                elif n < len(row) and row[n] != '.':
                    part_sum += num
                    continue
                # Search above
                elif r > 0 and any(v != '.' and not v.isnumeric()\
                                   for v in schematic[r-1][max(0, num_start-1):n+1]):
                    part_sum += num
                    continue
                # Search below
                elif r < len(schematic) - 1 and\
                    any(v != '.' and not v.isnumeric()\
                        for v in schematic[r+1][max(0, num_start-1):n+1]):
                    part_sum += num
                    continue
            n += 1
    
    return part_sum

def Day3_Part2(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Find the sum of all of the gear ratios in an engine schematic given in an input file. The
    engine schematic containes numbers and symbols, and a gear is any '*' symbol that is adjacent
    to exactly two part numbers, including diagonally. Its gear ratio is then the result of
    multiplying those two numbers together.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the engine schematic.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    ratio_sum : int
        Sum of all the part numbers in the given engine schematic.

    """
    # Parse input file
    schematic = get_input(input_file)
    
    ratios = []
    # Move through engine schematic line by line
    for r, row in enumerate(schematic):
        n = 0
        # Move through each line
        while n < len(row):
            # If a gear is found, search around it for numbers, and record each one
            if row[n] == '*':
                nums = []
                # Search left
                if n > 0 and row[n-1].isnumeric():
                    # If a number is found, keep moving left to find where it begins
                    num_start, num_end = 1*n, 1*n
                    while num_start > 0 and row[num_start-1].isnumeric():
                        num_start -= 1
                    # Extract the full number
                    nums.append(int(row[num_start:num_end]))
                # Search right
                if n < len(row) - 1 and row[n+1].isnumeric():
                    # If a number is found, keep moving right to find where it ends
                    num_start, num_end = n + 1, n + 1
                    while num_end < len(row) and row[num_end].isnumeric():
                        num_end += 1
                    # Extract the full number
                    nums.append(int(row[num_start:num_end]))
                # Other rows (above and/or below) to search for numbers
                other_rows = []
                # Can only search above if not one the first line
                if r > 0:
                    other_rows.append(r-1)
                # Can only search below if not one the last line
                if r < len(schematic) - 1:
                    other_rows.append(r+1)
                # For each row to be searched
                for other_row in other_rows:
                    # Check if there are any numbers adjacent to the gear, if not then continue
                    if not any(v.isnumeric() for v in schematic[other_row][n-1:n+2]):
                        continue
                    # If the middle of the row (directly above the gear) is numeric, there is
                    # exactly one number here
                    if schematic[other_row][n].isnumeric():
                        num_start, num_end = n, n + 1
                        # Keep moving left to find where the number starts
                        while num_start > 0 and schematic[other_row][num_start-1].isnumeric():
                            num_start -= 1
                        # Keep moving right to find where the number ends
                        while num_end < len(schematic[other_row]) and\
                            schematic[other_row][num_end].isnumeric():
                            num_end += 1
                        # Extract the full number
                        nums.append(int(schematic[other_row][num_start:num_end]))
                    # Else there could be up to 2 numbers here, need to check either side
                    else:
                        # Search left
                        if schematic[other_row][n-1].isnumeric():
                            # If a number is found, keep moving left to find where it begins
                            num_start, num_end = 1*n, 1*n
                            while num_start > 0 and schematic[other_row][num_start-1].isnumeric():
                                num_start -= 1
                            # Extract the full number
                            nums.append(int(schematic[other_row][num_start:num_end]))
                        # Search right
                        if schematic[other_row][n+1].isnumeric():
                            # If a number is found, keep moving right to find where it ends
                            num_start, num_end = n + 1, n + 1
                            while num_end < len(schematic[other_row]) - 1 and\
                                schematic[other_row][num_end + 1].isnumeric():
                                num_end += 1
                            # Extract the full number
                            nums.append(int(schematic[other_row][num_start:num_end + 1]))
                # If there are exactly two numbers, this is a gear: calculate the gear ratio and
                # add to list
                if len(nums) == 2:
                    ratios.append(nums[0]*nums[1])
            n += 1

    # Find sum of all ratios
    ratio_sum = sum(ratios)

    return ratio_sum
