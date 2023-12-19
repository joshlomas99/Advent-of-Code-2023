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

def get_input(input_file: str='Inputs/Day15_Inputs.txt') -> list:
    """
    Extracts a list of comma-separated instructions from an input file.
    
    Parameters
    ----------
    input_file : str, optional
        Input file giving the instructions.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    strings : list(str)
        List of instruction strings.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract line and split into list by commas
        strings = f.readlines()[0].strip().split(',')

    return strings

def HASH(string):
    """
    Calculates the hash of a given string according to the following algorithm:

    Current value starts at zero then loop through string:
        - Determine the ASCII code for the current character of the string.
        - Increase the current value by the ASCII code you just determined.
        - Set the current value to itself multiplied by 17.
        - Set the current value to the remainder of dividing itself by 256.

    Parameters
    ----------
    string : str
        The string to find the hash of.

    Returns
    -------
    current_value : int
        The final hash value of the given string.

    """
    # Start current_value at zero
    current_value = 0
    # Loop through string
    for char in string:
        # Find ASCII code of current character
        current_value += ord(char)
        # Execute the rest of the algorithm
        current_value = (17*current_value)%256

    return current_value

@time_function
def Day15_Part1(input_file: str='Inputs/Day15_Inputs.txt') -> int:
    """
    Finds the sum of the hashes of a series of comma-separated instructions given in an input file.
    The hash of a given string is determined according to the following algorithm:

    Current value starts at zero then loop through string:
        - Determine the ASCII code for the current character of the string.
        - Increase the current value by the ASCII code you just determined.
        - Set the current value to itself multiplied by 17.
        - Set the current value to the remainder of dividing itself by 256.
    
    Parameters
    ----------
    input_file : str, optional
        Input file giving the instructions.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    hash_sum : int
        Sum of the hashes of every instruction.

    """
    # Parse input file and extract list of instructions
    strings = get_input(input_file)

    # Calculate hash of each string and sum
    hash_sum = sum(HASH(string) for string in strings)

    return hash_sum

@time_function
def Day15_Part2(input_file: str='Inputs/Day15_Inputs.txt') -> int:
    """
    Calculates the total focusing power of a set of lenses, which are placed in a series of 256
    boxes according to a series of instructions given in an input file. Each instruction begins
    with a sequence of letters that indicate the label of the lens on which the step operates.
    The result of running the HASH algorithm on the label indicates the correct box for that step.
    The label is followed by a character that indicates the operation to perform: either an equals
    sign (=) or a dash (-). If the operation character is a dash (-), go to the relevant box and
    remove the lens with the given label if it is present in the box. Then, move any remaining
    lenses as far forward in the box as they can go without changing their order, filling any space
    made by removing the indicated lens. (If no lens in that box has the given label, nothing
    happens.) If the operation character is an equals sign (=), it will be followed by a number
    indicating the focal length of the lens that needs to go into the relevant box. There are two
    then possible situations:

        - If there is already a lens in the box with the same label, replace the old lens with the
        new lens: remove the old lens and put the new lens in its place, not moving any other
        lenses in the box.
        - If there is not already a lens in the box with the same label, add the lens to the box
        immediately behind any lenses already in the box.

    The focusing power of a single lens is then found by multiplying together one plus the box
    number of the lens in question, the slot number of the lens within the box: 1 for the first
    lens, 2 for the second lens, and so on; and the focal length of the lens.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the instructions.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    total_focusing_power : int
        The total focusing power of all the lenses in the boxes after following every instruction.

    """
    # Parse input file and extract list of instructions
    strings = get_input(input_file)
    # Start with 256 empty boxes
    boxes = {n: [] for n in range(256)}
    # Loop through strings
    for string in strings:
        # For '-' instructions
        if '-' in string:
            # Extract the label
            label = string[:-1]
            # Find the HASH of the label
            box_num = HASH(label)
            # Find the index in that box of a matching label
            box_ind = [i for i in range(len(boxes[box_num])) if boxes[box_num][i][0] == label]
            # If a match exists, remove the corresponding lens, else do nothing
            if box_ind:
                boxes[box_num].pop(box_ind[0])
        # For '=' instructions
        elif '=' in string:
            # Extract label and focal length
            label, focal_len = string.split('=')
            # Find the HASH of the label
            box_num = HASH(label)
            # Find the index in that box of a matching label
            box_ind = [i for i in range(len(boxes[box_num])) if boxes[box_num][i][0] == label]
            # If a match exists, replace with the new focal length
            if box_ind:
                boxes[box_num][box_ind[0]] = (label, int(focal_len))
            # Else add this one to the back of the box
            else:
                boxes[box_num].append((label, int(focal_len)))

    # Sum up focusing power
    total_focusing_power = 0
    # For each box
    for n, box in boxes.items():
        # For each lens in that box
        for i, (label, focal_length) in enumerate(box):
            # Calculate focusing power and add to sum
            total_focusing_power += (n+1)*(i+1)*focal_length
    
    return total_focusing_power
