from functools import reduce
import operator

def get_input(input_file: str='Inputs/Day6_Inputs.txt', combine=False) -> list:
    """
    Extracts the allowed times and record distances for a series of races from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the times and distances.
        The default is 'Inputs/Day6_Inputs.txt'.
    combine : bool, optional
        Whether to combine the times and distances into single time and distance values (True)
        or make a list of the different values (False).
        The default is False.

    Returns
    -------
    races : list(tuple(int, int))
        List of races, where each race is a tuple in the form (time, distance).

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines
        lines = [l.strip() for l in f.readlines()]
        # If combining the times/distances into single values
        if combine:
            # Add up all the strings first before converting to single integers for a single race
            races = tuple(int(reduce(operator.add, [line.split()[i+1]\
                                                    for i in range(len(line.split()) - 1)]))\
                          for line in lines)
        # Else just extract each value separately to give multiple races
        else:
            races = [(int(lines[0].split()[i+1]), int(lines[1].split()[i+1]))\
                     for i in range(len(lines[0].split()) - 1)]

    return races

def Day6_Part1(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Finds the product of the number of different ways it is possible to beat the record in a boat
    race, for a series of races given in an input file. For each race the time allowed and current
    distance record is given. In each race, the boat starts at 0 mm/ms, and once the time starts,
    a button can be held down which will increase the speed of the boat upon the button's release by
    1 mm/ms for every second it is held. The boat then has the remaining time after the button is
    released to travel some distance.

    Notes
    -----
    For any given race with time :math:`t`, the range of times :math:`t_b` which the button can be
    held down for which result in breaking the distance record can be determined analytically. The
    boat speed when the button is released will be equal to :math:`t_b` since the acceleration is
    1. Therefore the eventual distance travelled will be

    .. math:: d(t_b) = (t - t_b)t_b.

    So to determine what values of :math:`t_b` will break the record we need to solve the equation

    .. math:: (t - t_b)t_b > d,

    where :math:`d` is the current distance record. We can find the boundaries of the range of
    corresponding :math:`t_b` values by replacing :math:`>` with :math:`=` and rearranging to give
    a quadratic equation:

    .. math:: t_b^2 - tt_b + d = 0.

    Which has the solutions

    .. math:: t_b = \\frac{t\pm\sqrt{t^2 - 4d}}{2}.

    This gives two solutions, a lower bound :math:`t_b^+` and an upper bound :math:`t_b^-`. Since
    by symmetry :math:`t_b^+` = t - :math:`t_b^+` we only need the lower bound from this equation.
    Then since we the problem only considered integer solutions, we should take the ceiling of
    this lower bound

    .. math:: t_b = \\lceil{\\frac{t + \sqrt{t^2 - 4d}}{2}}\\rceil.

    Equivalently the floor of the upper bound is the highest solution for :math:`t_b`, which is
    also equal to :math:`t - t_b`. Then, the total number of integer solutions :math:`n` which
    result in breaking the record is given as

    .. math:: n = (t - t_b) - t_b + 1 = t - 2t_b + 1.


    Parameters
    ----------
    input_file : str, optional
        Input file giving the times and distances.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    product : int
        Product of the number of different ways you can beat the record in each race.

    """
    # Parse input file and extract race times and distance records
    races = get_input(input_file)

    product = 1
    # Loop over races
    for t, d in races:
        # Calculate analytical solution for lowest winning value of t_b
        t_b_min = int((t - (t**2 - 4*d)**0.5)/2) + 1
        # Multiply the current product by the number of possible winning values
        product *= t - (2*t_b_min) + 1
    
    return product

def Day6_Part2(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Finds the product of the number of different ways it is possible to beat the record in a boat
    race, for a race given in an input file. The time allowed and distance record is now found by
    ignoring the spaces between the numbers on the lines corresponding to each value. For each race
    the time allowed and current distance record is given. In each race, the boat starts at
    0 mm/ms, and once the time starts, a button can be held down which will increase the speed of
    the boat upon the button's release by 1 mm/ms for every second it is held. The boat then has
    the remaining time after the button is released to travel some distance.

    Notes
    -----
    For any given race with time :math:`t`, the range of times :math:`t_b` which the button can be
    held down for which result in breaking the distance record can be determined analytically. The
    boat speed when the button is released will be equal to :math:`t_b` since the acceleration is
    1. Therefore the eventual distance travelled will be

    .. math:: d(t_b) = (t - t_b)t_b.

    So to determine what values of :math:`t_b` will break the record we need to solve the equation

    .. math:: (t - t_b)t_b > d,

    where :math:`d` is the current distance record. We can find the boundaries of the range of
    corresponding :math:`t_b` values by replacing :math:`>` with :math:`=` and rearranging to give
    a quadratic equation:

    .. math:: t_b^2 - tt_b + d = 0.

    Which has the solutions

    .. math:: t_b = \\frac{t\pm\sqrt{t^2 - 4d}}{2}.

    This gives two solutions, a lower bound :math:`t_b^+` and an upper bound :math:`t_b^-`. Since
    by symmetry :math:`t_b^+` = t - :math:`t_b^+` we only need the lower bound from this equation.
    Then since we the problem only considered integer solutions, we should take the ceiling of
    this lower bound

    .. math:: t_b = \\lceil{\\frac{t + \sqrt{t^2 - 4d}}{2}}\\rceil.

    Equivalently the floor of the upper bound is the highest solution for :math:`t_b`, which is
    also equal to :math:`t - t_b`. Then, the total number of integer solutions :math:`n` which
    result in breaking the record is given as

    .. math:: n = (t - t_b) - t_b + 1 = t - 2t_b + 1.


    Parameters
    ----------
    input_file : str, optional
        Input file giving the times and distances.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    num_solutions : int
        The number of different ways you can beat the record in the race.

    """
    # Parse input file and extract race time and distance record by combining all values
    t, d = get_input(input_file, combine=True)

    # Calculate analytical solution for lowest winning value of t_b
    t_b_min = int((t - (t**2 - 4*d)**0.5)/2) + 1
    # Calculate the number of possible winning values
    num_solutions = t - (2*t_b_min) + 1
    
    return num_solutions
