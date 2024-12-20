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

def get_input(input_file: str='Inputs/Day19_Inputs.txt') -> tuple:
    """
    Extract a series of workflows followed by a list of parts from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the workflows and parts.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    workflows : dict(str: list(tuple(str) or str))
        Dict mapping the name of each workflow into a list of the rules it specifies.
    parts : list(dict(str: int))
        List of parts as dicts mapping each rating category to its value.

    """
    workflows, parts = {}, []
    # Parse input file and extract lines
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    i = 0
    # Until first newline, extract and format workflows
    while lines[i]:
        split = lines[i].index('{')
        workflows[lines[i][:split]] = [tuple(r.split(':')) if ':' in r else r \
                                       for r in lines[i][split:].strip('{}').split(',')]
        i += 1
    i += 1
    # Then extract and format parts
    while i < len(lines):
        parts.append({p.split('=')[0]: int(p.split('=')[1]) \
                      for p in lines[i].strip('{}').split(',')})
        i += 1

    return workflows, parts

def process_workflow(workflow: list, part: dict) -> str:
    """
    Determine the where a given part is sent after passing through a given workflow. Each part is
    rated in each of four categories: x, m, a and s. Each workflow will either accept or reject the
    part or send it to a different workflow. Each workflow has a name and contains a list of rules;
    each rule specifies a condition and where to send the part if the condition is true. The first
    rule that matches the part being considered is applied immediately, and the part moves on to
    the destination described by the rule. (The last rule in each workflow has no condition and
    always applies if reached.)

    Parameters
    ----------
    workflow : list(tuple(str) or str)
        List of the rules specified by the given workflow.
    part : dict(str: int)
        Parts as a dict mapping each rating category to its value.

    Raises
    ------
    Exception
        If an unknown condition is encountered in a rule.

    Returns
    -------
    dest : str
        Where the part is sent by this workflow.

    """
    # Loop through rules in order
    for rule in workflow:
        # If this rule has a condition
        if isinstance(rule, tuple):
            cond, dest = rule
            # Apply corresponding condition
            if '>' in cond:
                p, lim = cond.split('>')
                # If passed, send the part to the correpsonding destination
                if part[p] > int(lim):
                    return dest
            elif '<' in cond:
                p, lim = cond.split('<')
                # If passed, send the part to the correpsonding destination
                if part[p] < int(lim):
                    return dest
            else:
                raise Exception(f"Unknown condition {cond} in workflow {workflow} for part {part}!")
        else:
            # Else just send the part to this unconditional destination
            return rule

@time_function
def Day19_Part1(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Determines the sum of the rating numbers for all of the parts from a list given in an input
    file that ultimately get accepted after passing through a series of workflows given in the same
    input file. The rating of a part is the sum of its four values x, m, a and s.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the workflows and parts.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    ratings : int
        Sum of the ratings of all accepted parts.

    """
    # Parse input file tp extract workflows and parts
    workflows, parts = get_input(input_file)

    # Track accepted and rejected parts
    final_state = {'A': [], 'R': []}
    # Loop through parts
    for part in parts:
        # Always start by applying the 'in' workflow
        dest = process_workflow(workflows['in'], part)
        # Until the part is accepted or rejected
        while dest not in ['A', 'R']:
            # Keep passing the part through each workflow it is sent to
            dest = process_workflow(workflows[dest], part)

        # Track if the part was accepted or rejected
        final_state[dest].append(part)

    # Sum ratings for all accepted parts
    ratings = sum(sum(p.values()) for p in final_state['A'])

    return ratings

def split_dests(workflows, part_locs):
    """
    Find where a series of parts are sent after passing through given workflows, based on the range
    of values which the ratings of the parts can have.

    Parameters
    ----------
    workflows : dict(str: list(tuple(str) or str))
        Dict mapping the name of each workflow into a list of the rules it specifies.
    part_locs : list(tuple(str, dict(str: tuple(int, int))))
        List of part locations, where each location is a tuple with the workflow name the part is
        currently in and a dict mapping each rating onto a tuple giving the range of values which
        are currently at this workflow in the form (low, high).

    Raises
    ------
    Exception
        If an unknown condition is encountered in a rule.

    Returns
    -------
    parts_out : list(tuple(str, dict(str: tuple(int, int))))
        New list of part locations, where each location is a tuple with the workflow name the part
        is currently in and a dict mapping each rating onto a tuple giving the range of values
        which are currently at this workflow in the form (low, high).

    """
    # Start new list of part locations
    parts_out = []
    # Loop through workflows and part ranges in that workflow
    for wf, parts_in in part_locs:
        # Loop through rules of that workflow
        for rule in workflows[wf]:
            # If the rule is conditional
            if isinstance(rule, tuple):
                cond, dest = rule
                if '>' in cond:
                    p, lim = cond.split('>')
                    # Move the range of parts ratings which satisfy the condition to the
                    # corresponding workflow
                    parts_out.append((dest, {param:(int(lim), lims[1]) if param == p \
                                             else (lims[0], lims[1]) \
                                                 for param, lims in parts_in.items()}))
                    # Reduce the part range to the remaining values which didn't satsify this rule
                    parts_in = {param:(lims[0], int(lim)+1) if param == p else (lims[0], lims[1]) \
                                for param, lims in parts_in.items()}
                elif '<' in cond:
                    p, lim = cond.split('<')
                    # Move the range of parts ratings which satisfy the condition to the
                    # corresponding workflow
                    parts_out.append((dest, {param:(lims[0], int(lim)) if param == p \
                                             else (lims[0], lims[1]) \
                                                 for param, lims in parts_in.items()}))
                    # Reduce the part range to the remaining values which didn't satsify this rule
                    parts_in = {param:(int(lim)-1, lims[1]) if param == p else (lims[0], lims[1]) \
                                for param, lims in parts_in.items()}
                else:
                    raise Exception(f"Unknown condition {cond}")
            else:
                # Else move all remaining part ranges to this unconditional destination
                parts_out.append((rule, parts_in))
    
    return parts_out

from functools import reduce
import operator

@time_function
def Day19_Part2(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Determines how many distinct combinations of ratings will be accepted by a series of workflows
    given in an input file. Each rating can range from 1 to 4000

    Parameters
    ----------
    input_file : str, optional
        Input file giving the workflows. The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    num_comb : int
        The number of distinct combinations of ratings which will be accepted.

    """
    # Parse input file to extract workflows
    workflows, _ = get_input(input_file)

    # Start with every possible combination going into 'in'
    # Rpresent part ranges as ranges of values taken by each of the ratings, and track which
    # workflow each part range is currently at
    part_locs = [('in', {'x':(0, 4001), 'm':(0, 4001), 'a':(0, 4001), 's':(0, 4001)})]
    # Count states which are accepted or rejected
    final_state = {'A': 0, 'R': 0}

    # While there are states in workflows which aren't 'A' or 'R'
    while part_locs:
        # Split the part ranges based on which workflows they move to based on the rules of their
        # current workflow
        new_part_locs = split_dests(workflows, part_locs)
        part_locs = []
        # Loop through locations of part ranges
        for dest, parts in new_part_locs:
            # If they are accepted or rejected
            if dest in ['A', 'R']:
                # Add the number of combinations (product of the four rating ranges) to the total
                final_state[dest] += reduce(operator.mul, [lims[1] - lims[0] - 1 \
                                                           for lims in parts.values()])
            else:
                # Else add these parts ranges to the new list and continue processing
                part_locs.append((dest, parts))

    # Find the final number of accepted states
    num_comb = final_state['A']

    return num_comb
