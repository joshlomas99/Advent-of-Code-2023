def get_input(input_file: str='Inputs/Day8_Inputs.txt') -> list:
    """
    Extracts a list of links between different nodes in a network and a list of instructions for
    how to move through the network from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the network and instructions.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    instructions : list(char)
        List of instructions to follow, either L for left or R for right.

    network : dict(str: tuple(str, str))
        Dictionary giving the links between nodes in the network, each node has two connected
        nodes, one to the left and one to the right, given in the form (left, right).

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines
        lines = [line for l in f.readlines() if len(line := l.strip()) > 0]
        # Extract instructions from top line
        instructions = lines[0]
        # Extract network
        network = {l.split(' = ')[0]: l.strip().split(' = ')[1].strip('(').strip(')') for l in lines[1:]}
        # Format links in tuples
        network = {s: (e.split(', ')[0], e.split(', ')[1]) for s, e in network.items()}
    return instructions, network

def Day8_Part1(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Determines the number of steps required to move from node 'AAA' to node 'ZZZ' in a network
    of nodes, while following a list of instructions given in an input file. The connections
    between different nodes in the network is given in the same input file. Each node has two
    connected nodes, one to the left and one to the right, given in the form (left, right). Each
    instruction is either L for left or R for right. If the end of the instructions is reached
    before the 'ZZZ' node then it loops back round to the first instruction.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the network and instructions.
        The default is 'Inputs/Day8_Inputs.txt'.

    Raises
    ------
    Exception
        If an unknown instruction (not L or R) is reached.

    Returns
    -------
    steps : int
        Steps required to move from 'AAA' to 'ZZZ' in the network while following the instructions.

    """
     # Parse input file to extract network and instructions
    instructions, network = get_input(input_file)
    # Start at node 'AAA'
    node, steps = 'AAA', 0
    # Until node 'ZZZ' is reached
    while node != 'ZZZ':
        # Read next instruction, with looping past the end of the list
        next_instruction = instructions[steps%len(instructions)]
        # Execute instruction
        if next_instruction == 'L':
            node = network[node][0]
        elif next_instruction == 'R':
            node = network[node][1]
        else:
            raise Exception(f'Unknown instruction {next_instruction}!')
        # Count steps
        steps += 1
    
    return steps

### All this is just to find the lowest common multiple of several numbers ####
                                                                              #
def next_prime(n: int) -> int:                                                #
    """                                                                       #
    Finds the next highest prime number after a given integer.                #
                                                                              #
    Parameters                                                                #
    ----------                                                                #
    n : int                                                                   #                                                                      #                                                                         #
        The current number.                                                   #
                                                                              #                                                                     #                                                                         #
    Returns                                                                   #
    -------                                                                   #
    n : int                                                                   #
        The next highest prime number after the given integer.                #
                                                                              #
    """                                                                       #
    n += 1                                                                    #
    # While the number has any factors between 2 and sqrt(n), increment       #
    while not all(n%i for i in range(2, int(n**0.5))):                        #
        n += 1                                                                #
                                                                              #
    return n                                                                  #
                                                                              #
def prime_factors(n: int) -> set:                                             #
    """                                                                       #
    Finds the prime factors of a given integer.                               #
                                                                              #
    Parameters                                                                #
    ----------                                                                #
    n : int                                                                   #
        Number to find the prime factors for.                                 #
                                                                              #
    Returns                                                                   #
    -------                                                                   #
    factors : set(tuple(int))                                                 #
        Set of the prime factors of the given number, in the form             #
        (factor, occurance).                                                  #
                                                                              #
    """                                                                       #
                                                                              #
    factors = set()                                                           #
    # Start at 2                                                              #
    f = 2                                                                     #
    # While there are remaining factors                                       #
    while n > 1:                                                              #
        # Count occurances of current factor                                  #
        num = 1                                                               #
        while n%f == 0:                                                       #
            n /= f                                                            #
            # Add new factor with occurance count                             #
            factors.add((f, num))                                             #
            num += 1                                                          #
        # Check next highest prime number                                     #
        f = next_prime(f)                                                     #
                                                                              #
    return factors                                                            #
                                                                              #
import operator                                                               #
from functools import reduce                                                  #
                                                                              #
def lcm(nums: list) -> int:                                                   #
    """                                                                       #
    Find the lowest common multiple of a list of integers.                    #
                                                                              #
    Parameters                                                                #
    ----------                                                                #
    num : list(int)                                                           #
        List of integers.                                                     #
                                                                              #
    Returns                                                                   #
    -------                                                                   #
    lcm : int                                                                 #
        Lowest common multiple of the integers.                               #
                                                                              #
    """                                                                       #
    # Create list of the prime factors of each number                         #
    factors = [prime_factors(n) for n in nums]                                #
    # Create set of every unique factor found across every integer            #
    unique_factors = {f[0] for factor in factors for f in factor}             #
    # Find the highest power of each factor present between the integers      #
    max_unique_factors = {(unique_factor, max(f[1] for factor in factors\
                                              for f in factor if f[0] == unique_factor))\
                          for unique_factor in unique_factors}                #
    # Find the product of each unique prime factor to its highest power       #
    # across all the numbers                                                  #
    lcm = reduce(operator.mul, [f[0]**f[1] for f in max_unique_factors])      #
    return lcm                                                                #
                                                                              #
###############################################################################

def Day8_Part2(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Determines the number of steps required to move simultaneously from every node in a network
    ending in 'A', until every path reaches a node ending in 'Z', while following a list of
    instructions given in an input file. The connections between different nodes in the network is
    given in the same input file. Each node has two connected nodes, one to the left and one to the
    right, given in the form (left, right). Each instruction is either L for left or R for right.
    If the end of the instructions is reached before the 'ZZZ' node then it loops back round to the
    first instruction.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the network and instructions.
        The default is 'Inputs/Day8_Inputs.txt'.

    Raises
    ------
    Exception
        If an unknown instruction (not L or R) is reached.

    Returns
    -------
    steps : int
        Steps required to simultaneously reach nodes ending in 'Z' having started from every node
        ending in 'A'.

    """
     # Parse input file to extract network and instructions
    instructions, network = get_input(input_file)
    # Find all starting nodes ending in 'A'
    nodes = [n for n in network if n[-1] == 'A']
    steps_to_Z = []
    # For each starter node count how many steps are required to reach a node ending in 'Z'
    for node in nodes:
        steps = 0
        # Until a node ending in 'Z' is reached
        while node[-1] != 'Z':
            # Read next instruction, with looping past the end of the list
            next_instruction = instructions[steps%len(instructions)]
            # Execute instruction
            if next_instruction == 'L':
                node = network[node][0]
            elif next_instruction == 'R':
                node = network[node][1]
            else:
                raise Exception(f'Unknown instruction {next_instruction}!')
            # Count steps
            steps += 1
        # Add to list
        steps_to_Z.append(steps)

    # Find the lowest common multiple of all steps required, which is the soonest they will all
    # sync up and be reached simultaneously
    min_steps = lcm(steps_to_Z)

    return min_steps
