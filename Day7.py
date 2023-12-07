def get_input(input_file: str='Inputs/Day7_Inputs.txt') -> list:
    """
    Extracts a series of hands of cards and the corresponding bids against them.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the hands and bids.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    hands : list(tuple(str, int))
        List of hands, where each hand is a tuple in the form (cards, bid).

    """
    # Parse input file
    with open(input_file) as f:
        # Extract hands, convert bids to integers
        hands = [(l.strip().split()[0], int(l.strip().split()[1])) for l in f.readlines()]
    return hands

def hand_strength(cards):
    """
    Calculates the strength of a hand of cards. A hand consists of five cards labeled one of A, K,
    Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order
    where A is the highest and 2 is the lowest. Hands are ranked first by what type they are, in
    descending order of strength the possible types are: 5 of a kind (e.g. AAAAA), 4 of a kind
    (e.g. AAAAK), full house (e.g. AAAKK), 3 of a kind (e.g. AAAKQ), 2 pairs (e.g. AAKQQ), 1 pair
    (e.g. AAKQJ) and high card (e.g. AKQJT). If two hands have the same type, their relative
    strengths are determined by comparing the first cards in both hands, then the second if they
    still match, etc.

    Parameters
    ----------
    cards : str
        The five card hand as a string of the card types in order.

    Returns
    -------
    strength : int
        An unique integer representing the strength of the hand, higher meaning stronger.

    """
    # Dict to score card types based on strength, using hexidecimal scores as there are >10 types
    card_scores = {'A': 'c', 'K': 'b', 'Q': 'a', 'J': '9', 'T': '8', '9': '7', '8': '6',
                   '7': '5', '6': '4', '5': '3', '4': '2', '3': '1', '2': '0'}

    # Determine each hand's strength uniquely by creating a bitwise score using hexadecimal bits,
    # since there are >10 card types. Order the bits by strength priority, so hand type first,
    # followed by strength of each card in order.
    strength = ''
    # Create a dict of every card in the set, and the count of each one, to determine hand type
    card_dict = {c: cards.count(c) for c in set(cards)}
    # 5 of a kind
    if len(card_dict) == 1:
        strength += '6'
    # 4 of a kind or full house
    elif len(card_dict) == 2:
        # 4 of a kind
        if 4 in card_dict.values():
            strength += '5'
        # Full house
        else:
            strength += '4'
    # 3 of a kind or 2 pairs
    elif len(card_dict) == 3:
        # 3 of a kind
        if 3 in card_dict.values():
            strength += '3'
        # 2 pairs
        else:
            strength += '2'
    # 1 pair
    elif len(card_dict) == 4:
        strength += '1'
    # High card
    else:
        strength += '0'

    # Add to the end of the hand type score, the score of each card in order
    strength += ''.join(card_scores[c] for c in cards)

    # Convert to an integer, which is higher for stronger hands
    strength = int(strength, base=16)

    return strength

def Day7_Part1(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    """
    Determines the total winnings from a series of hands of cards given in an input, which are put
    up against corresponding bids given in the same input file. The total winnings are found by
    ranking every given hand in order of strength, where the weakest hand is ranked 1, etc. Each
    hand then wins an amount equal to its bid multiplied by its rank.

    A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The
    relative strength of each card follows this order where A is the highest and 2 is the lowest.
    Hands are ranked first by what type they are, in descending order of strength the possible
    types are: 5 of a kind (e.g. AAAAA), 4 of a kind (e.g. AAAAK), full house (e.g. AAAKK), 3 of a
    kind (e.g. AAAKQ), 2 pairs (e.g. AAKQQ), 1 pair (e.g. AAKQJ) and high card (e.g. AKQJT). If two
    hands have the same type, their relative strengths are determined by comparing the first cards
    in both hands, then the second if they still match, etc.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the hands and bids.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    winnings : int
        Total winnings.

    """
    # Parse input file to extract hands and bids
    hands = get_input(input_file)
    # Sort the hands according to their strength score, calculated with the hand_strength function
    hands = sorted(hands, key=lambda hand: hand_strength(hand[0]))
    # Sum up the rank of each hand multiplied by its rank
    winnings = sum(hands[i][1]*(i+1) for i in range(len(hands)))
    
    return winnings

def hand_strength_with_joker(cards):
    """
    Calculates the strength of a hand of cards. A hand consists of five cards labeled one of A, K,
    Q, T, 9, 8, 7, 6, 5, 4, 3, 2 or J. The relative strength of each card follows this order
    where A is the highest and J is the lowest. Hands are ranked first by what type they are, in
    descending order of strength the possible types are: 5 of a kind (e.g. AAAAA), 4 of a kind
    (e.g. AAAAK), full house (e.g. AAAKK), 3 of a kind (e.g. AAAKQ), 2 pairs (e.g. AAKQQ), 1 pair
    (e.g. AAKQT) and high card (e.g. AKQT9). If two hands have the same type, their relative
    strengths are determined by comparing the first cards in both hands, then the second if they
    still match, etc.

    However, J cards are now jokers, which are wildcards which can act like whatever card would
    make the hand the strongest type possible. But when splitting ties between hands of the same
    type, J is now the weakest card, weaker than 2.

    Parameters
    ----------
    cards : str
        The five card hand as a string of the card types in order.

    Returns
    -------
    strength : int
        An unique integer representing the strength of the hand, higher meaning stronger.

    """
    # Dict to score card types based on strength, using hexidecimal scores as there are >10 types
    card_scores = {'A': 'c', 'K': 'b', 'Q': 'a', 'T': '9', '9': '8', '8': '7', '7': '6',
                   '6': '5', '5': '4', '4': '3', '3': '2', '2': '1', 'J': '0'}

    # Determine each hand's strength uniquely by creating a bitwise score using hexadecimal bits,
    # since there are >10 card types. Order the bits by strength priority, so hand type first,
    # followed by strength of each card in order.
    strength = ''
    # Create a dict of every card in the set, and the count of each one, to determine hand type
    card_dict = {c: cards.count(c) for c in set(cards)}
    # 5 of a kind
    if len(card_dict) == 1:
        strength += '6'
    # 4 of a kind or full house
    elif len(card_dict) == 2:
        # If either card type is J then it's 5 of a kind
        if 'J' in card_dict:
            strength += '6'
        else:
            # 4 of a kind
            if 4 in card_dict.values():
                strength += '5'
            # Full house
            else:
                strength += '4'
    # 3 of a kind or 2 pairs
    elif len(card_dict) == 3:
        # If 3 of a kind
        if 3 in card_dict.values():
            # If any card type is J then it's 4 of a kind
            if 'J' in card_dict:
                strength += '5'
            # Else 3 of a kind
            else:
                strength += '3'
        # Else 2 pairs
        else:
            # If any card type is J, could be 4 or 3 of a kind
            if 'J' in card_dict:
                # If one of the pairs is J then it's 4 of a kind
                if card_dict['J'] == 2:
                    strength += '5'
                # Else the single card is J so it's full house
                else:
                    strength += '4'
            # Else 2 pairs
            else:
                strength += '2'
    # 1 pair
    elif len(card_dict) == 4:
        # If any of the card types is J then it's 3 of a kind
        if 'J' in card_dict:
            strength += '3'
        # Else 1 pair
        else:
            strength += '1'
    # High card
    else:
        # If any of the card types is J then it's 1 pair
        if 'J' in card_dict:
            strength += '1'
        # Else high card
        else:
            strength += '0'

    # Add to the end of the hand type score, the score of each card in order
    strength += ''.join(card_scores[c] for c in cards)

    # Convert to an integer, which is higher for stronger hands
    strength = int(strength, base=16)

    return strength

def Day7_Part2(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    """
    Determines the total winnings from a series of hands of cards given in an input, which are put
    up against corresponding bids given in the same input file. The total winnings are found by
    ranking every given hand in order of strength, where the weakest hand is ranked 1, etc. Each
    hand then wins an amount equal to its bid multiplied by its rank.

    A hand consists of five cards labeled one of A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2 or J. The
    relative strength of each card follows this order where A is the highest and 2 is the lowest.
    Hands are ranked first by what type they are, in descending order of strength the possible
    types are: 5 of a kind (e.g. AAAAA), 4 of a kind (e.g. AAAAK), full house (e.g. AAAKK), 3 of a
    kind (e.g. AAAKQ), 2 pairs (e.g. AAKQQ), 1 pair (e.g. AAKQT) and high card (e.g. AKQT9). If two
    hands have the same type, their relative strengths are determined by comparing the first cards
    in both hands, then the second if they still match, etc.

    However, J cards are now jokers, which are wildcards which can act like whatever card would
    make the hand the strongest type possible. But when splitting ties between hands of the same
    type, J is now the weakest card, weaker than 2.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the hands and bids.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    winnings : int
        Total winnings.

    """
    # Parse input file to extract hands and bids
    hands = get_input(input_file)
    # Sort the hands according to their strength score, calculated with the
    # hand_strength_with_joker function
    hands = sorted(hands, key=lambda hand: hand_strength_with_joker(hand[0]))
    # Sum up the rank of each hand multiplied by its rank
    winnings = sum(hands[i][1]*(i+1) for i in range(len(hands)))
    
    return winnings
