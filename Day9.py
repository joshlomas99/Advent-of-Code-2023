def get_input(input_file: str='Inputs/Day9_Inputs.txt') -> list:
    """
    Extracts a list of integer sequences from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the sequences.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    sequences : list(list(int))
        List of extracted integer sequences.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract sequences and convert numbers to integers
        sequences = [[int(i) for i in l.strip().split()] for l in f.readlines()]
    return sequences

def next_in_sequence(sequence):
    """
    Finds the next number in a sequence. If the sequence is not linear (the difference between
    every number is the same) then it recursively finds the next number in the sequence formed
    by the differences, and so on until a linear sequence is found.

    Parameters
    ----------
    sequence : list(int)
        List of integers forming the sequence.

    Returns
    -------
    next : int
        The next term in the sequence.

    """

    diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]
    if len(set(diffs)) == 1:
        return sequence[-1] + diffs[0]
    else:
        return sequence[-1] + next_in_sequence(diffs)

def Day9_Part1(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    """
    Find the sum of the next terms of a series of sequences given in an input file. If a given
    sequence is not linear (i.e. the difference between every number is not the same) then the next
    number in the sequence formed by the differences should be found, and so on until a linear
    sequence is found which can be used to work back up the chain and find the next term in the
    overall sequence.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the sequences.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    next_sum : int
        The sum of the next terms in all of the sequences.

    """
    # Extract sequences from input file
    sequences = get_input(input_file)
    # Find the next terms of each and sum
    next_sum = sum(next_in_sequence(sequence) for sequence in sequences)
    
    return next_sum

def Day9_Part2(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    """
    Find the sum of the first previous term before the start of a series of sequences given in an
    input file. If a given sequence is not linear (i.e. the difference between every number is not
    the same) then the next number in the sequence formed by the differences should be found, and
    so on until a linear sequence is found which can be used to work back up the chain and find the
    previous term in the overall sequence.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the sequences.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    next_sum : int
        The sum of the previous terms in all of the sequences.

    """
    # Extract sequences from input file
    sequences = get_input(input_file)
    # Flip each sequence's order, find the next terms of each and sum (equivalent to finding
    # the first previous term in the original sequences)
    next_sum = sum(next_in_sequence(sequence[::-1]) for sequence in sequences)
    
    return next_sum
