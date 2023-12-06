def get_input(input_file: str='Inputs/Day4_Inputs.txt') -> list:
    """
    Extracts the numbers from a series of scratchcards given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the scratchcards. Each one has two lists of numbers separated by a
        vertical bar (|): a list of winning numbers and then a list of numbers you have.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    cards : list(tuple(set(int), set(int)))
        List of extracted scratchcards, in the form of a tuple with two sets of integers, the
        winning numbers first and the numbers you have second.

    """
    # Parse input file
    with open(input_file) as f:
        cards = [l.strip().split(': ')[1] for l in f.readlines()]
        # Split lists of numbers and convert into sets, then make a tuple per card
        cards = [(set(c.split('|')[0].split()), set(c.split('|')[1].split())) for c in cards]
    return cards

def Day4_Part1(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    """
    Determines how many points in total a set of scratchcards given in an input file are. Each
    scratchcard has two lists of numbers separated by a vertical bar (|): a list of winning numbers
    and then a list of numbers you have. The points a card is worth is determined by the number of
    numbers you have which match the winning numbers, 1 point for the first match and doubling for
    each additional match.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the scratchcards.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    total : int
        Total points value of the given scratchcards.

    """
    # Parse input file to extract winning numbers and your numbers for each card
    cards = get_input(input_file)
    # Find number of matches as intersection between two sets of numbers on each card
    # Points are then equal to 2 to the power of (matches - 1)
    total = sum(2**(len(matches)-1) for c in cards if (matches := c[0].intersection(c[1])))

    return total

import numpy as np

def Day4_Part2(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    """
    Determines how many scratchcards are recieved in total after processing a set of scratchcards
    given in an input file are. Each scratchcard has two lists of numbers separated by a vertical
    bar (|): a list of winning numbers and then a list of numbers you have. For each match you win
    copies of the scratchcards below the current card equal to the number of matches, which are
    themselved processed.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the scratchcards.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    total_cards : int
        The total number of scratchcards recieved.

    """
    # Parse input file
    cards = get_input(input_file)
    # Start with one of each card
    card_nums = np.ones(len(cards), dtype=int)
    # For each card
    for n, card in enumerate(cards):
        # Calculate number of matches
        matches = len(card[0].intersection(card[1]))
        # Add number of these cards owned to the next 'matches' number of cards
        card_nums[n+1:n+matches+1] += card_nums[n]

    # Sum up numbers of every card
    total_cards = np.sum(card_nums)

    return total_cards
