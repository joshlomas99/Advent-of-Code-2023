def get_input(input_file: str='Inputs/Day12_Inputs.txt', unfold=False) -> list:
    """
    Extracts a list of spring conditions and corresponding sizes of each contiguous group of
    damaged springs on that row. For each row, the spring condition records whether each spring is
    operational (.) or damaged (#). However, some of the data is damaged and so for some springs,
    it is simply unknown (?) whether the spring is operational or damaged.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the spring conditions and group sizes.
        The default is 'Inputs/Day12_Inputs.txt'.

    unfold : bool, optional
        Whether or not to unfold each row, copying the spring conditions and damaged group sizes 5
        times, with the repeated spring conditions separated by additional '?'s.
        The default is False.

    Returns
    -------
    springs : list(tuple(str, tuple(int)))
        List of tuples, which each tuple described a single row in the form (springs, nums) where
        the springs are given as a string and the nums are the sizes of each contiguous group of
        damaged springs on that row as a tuple of integers.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines and split into springs and group sizes
        lines = [l.strip().split() for l in f.readlines()]
        # If unfolding
        if unfold:
            # Multiply springs by 5 and join with '?', and multiply group sizes by 5
            springs = [('?'.join([arr]*5), tuple(int(n) for n in nums.split(','))*5)\
                       for arr, nums in lines]
        # Else just format group sizes as they are
        else:
            springs = [(arr, tuple(int(n) for n in nums.split(',')))\
                       for arr, nums in lines]

    return springs

import functools

# Use a cache wrapper to massively speed up runtime
@functools.lru_cache(maxsize=None)
def valid_arrs(arr, nums):
    """
    Recursively finds the number of unique valid arrangements which can correspond to a given
    spring record, where '.' indicates an operational spring, '#' indicates a damaged spring and
    '?' could be either type of spring. The sizes of each contiguous group of damaged springs in
    the row of springs is also given, thus constraining the possible states.

    Parameters
    ----------
    arr : str
        String of the spring conditions in the current row.
    nums : tuple(int)
        The sizes of each contiguous group of damaged springs in the row of springs.

    Returns
    -------
    arrs : int
        The number of unique and valid arrangements of the springs.

    """
    # Start with count of zero
    arrs = 0
    # Find position of first '?'
    i = arr.index('?')
    # Test each possible spring type
    for rep in ['#', '.']:
        # Create a copy of the array as a list to allow for item assignment
        arr_copy = [c for c in arr]
        # Perform substitution for current test
        arr_copy[i] = rep
        # Format back to string
        arr_copy = ''.join(arr_copy)
        # If there are still further unknowns to test
        if '?' in arr_copy:
            # Find the sizes of each group of '#' up to the index just replaced
            test = tuple(len(s) for s in arr_copy[:i+1].split('.') if s)
            # If there are no '#'s yet, just recursively continue testing the row at the next '?'
            if len(test) == 0:
                arrs += valid_arrs(arr_copy, nums)
            # Else if the test is valid so far, i.e. doesn't give more groups than are possible,
            # matches the given groups up to the latest complete one and hasn't exceeded the
            # maximum possible size of the latest damaged group, then we continue recursively,
            # otherwise abondon this branch
            elif len(test) <= len(nums) and test[:-1] == nums[:len(test)-1] and test[-1] <= nums[len(test)-1]:
                # Now we will continue recursively finding the valid arrangements of the remaining
                # string, but we can cut the part of the string which is now set in stone, which
                # increases the effectiveness of the cache by generalising the strings more:

                # If we replaced with '.' then find the end of the last complete group of '#' and
                # cut the string at the beginning of that group, and cut the group size tuple
                # accordingly
                if rep == '.':
                    arrs += valid_arrs(arr_copy[arr_copy.rindex('#', 0, i) - test[-1] + 1:],
                                       nums[len(test)-1:])
                # Else if we replaced with '#' then move to the beginning of the current group of
                # '#' and cut there, and cut the group size tuple accordingly
                else:
                    arrs += valid_arrs(arr_copy[i - test[-1] + 1:], nums[len(test)-1:])
        # Else if there are no more '?' just test if this is a valid arrangement and count it if so
        else:
            if tuple(len(s) for s in arr_copy.split('.') if s) == nums:
                arrs += 1

    return arrs

def Day12_Part1(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Finds the sum of the number of possible valid arrangements of a series of spring condition
    records given in an input file. Each character in a given record represents a single spring,
    where '.' indicates an operational spring, '#' indicates a damaged spring and '?' could be
    either type of spring. The sizes of each contiguous group of damaged springs in the row of
    springs is also given, thus constraining the possible states for each row.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the spring conditions and group sizes.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of the total numbers of arrangements for each row of springs.

    """
    # Extract spring condition records and group sizes from input file and format
    springs = get_input(input_file)
    
    # Count total states
    total = 0
    # For each spring record
    for arr, nums in springs:
        # Recursively find the number of possible valid arrangements
        total += valid_arrs(arr, nums)
    
    return total
    
from tqdm import tqdm

def Day12_Part2(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Finds the sum of the number of possible valid arrangements of a series of spring condition
    records given in an input file. Each character in a given record represents a single spring,
    where '.' indicates an operational spring, '#' indicates a damaged spring and '?' could be
    either type of spring. The sizes of each contiguous group of damaged springs in the row of
    springs is also given, thus constraining the possible states for each row.

    However, now the spring records need to be unfolded, by replacing the list of spring conditions
    on a given row with five copies of itself (separated by '?') and replace the list of contiguous
    groups of damaged springs with five copies of itself (separated by ,).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the spring conditions and group sizes.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of the total numbers of arrangements for each row of springs.

    """
    # Extract spring condition records and group sizes from input file, unfold and format
    springs = get_input(input_file, unfold=True)
    
    # Count total states
    total = 0
    # For each spring record
    for arr, nums in tqdm(springs):
        # Recursively find the number of possible valid arrangements
        total += valid_arrs(arr, nums)
    
    return total
