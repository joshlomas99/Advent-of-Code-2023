import re

def get_input(input_file: str='Inputs/Day1_Inputs.txt') -> list:
    """
    Extracts the lines of a calibration document given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the calibration document.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    lines : list(str)
        Extracted lines of the document.

    """
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def Day1_Part1(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Computes the sum of all the calibration values in a document given in an input file.
    Calibration values are found by combining the first digit and the last digit (in that order)
    on each line to form a single two-digit number.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the calibration document.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of all calibration values.

    """
    # Parse input file
    lines = get_input(input_file)
    # Use regex to extract all digits on each line
    lines = [''.join(re.findall('\d+', l)) for l in lines]
    # Combine the first and last digits on each line, and sum the corresponding values
    total = sum(int(l[0] + l[-1]) for l in lines)

    return total

def Day1_Part2(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Computes the sum of all the calibration values in a document given in an input file.
    Calibration values are found by combining the first digit and the last digit (in that order)
    on each line to form a single two-digit number. However, some of the digits are actually
    spelled out with letters, i.e. one, two, three, four, five, six, seven, eight, and nine.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the calibration document.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of all calibration values.

    """
    # Parse input file
    lines = get_input(input_file)

    # Dict to convert spelled out numbers to values
    rep = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
           'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    # Dict to convert reversed spelled out numbers to values
    rev_rep = {s[::-1]: n for s, n in rep.items()}

    # Create regex patterns to sub in numbers for corresponding words in each dict
    pattern = re.compile("|".join(rep.keys()))
    rev_pattern = re.compile("|".join(rev_rep.keys()))

    # Sub in numbers for corresponding words in lines and reversed lines
    sub_lines = [pattern.sub(lambda m: rep[re.escape(m.group(0))], l)
             for l in lines]
    sub_rev_lines = [rev_pattern.sub(lambda m: rev_rep[re.escape(m.group(0))], l[::-1])
             for l in lines]

    # Extract all digits in both cases using regex
    lines = [''.join(re.findall('\d+', l)) for l in sub_lines]
    rev_lines = [''.join(re.findall('\d+', l)) for l in sub_rev_lines]

    # First digit is first in normal lines, last digit is first in reversed lines, then sum
    total = sum(int(lines[n][0] + rev_lines[n][0]) for n in range(len(lines)))

    return total
