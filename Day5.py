def get_input(input_file: str='Inputs/Day5_Inputs.txt') -> list:
    """
    Extracts a set of seed numbers and a series of maps from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the seeds and maps.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    seeds : list(int)
        List of extracted seed numbers.

    maps : list(list(list(int)))
        A list of maps, where each map is a split into a list of different ranges, with each range
        given in the form [destination range start, source range start, range length].

    """
    # Parse input file
    with open(input_file) as f:
        # Extract lines
        lines = [l.strip() for l in f.readlines()]
        # Extract seed numbers and convert to int
        seeds = [int(s) for s in lines[0].split(': ')[-1].split()]
        maps = []
        # For each line after the seeds, if it has content
        for line in [l for l in lines[1:] if len(l) > 0]:
            # If it starts with a letter, start a new map
            if line[0].isalpha():
                maps.append([])
            # Else append this line to the latest map
            else:
                maps[-1].append([int(i) for i in line.split()])

    return seeds, maps

def Day5_Part1(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    """
    Finds the lowest location number that corresponds to any of the initial seed numbers given in
    an input file. The location corresponding to a given seed can be found by running the seed
    number through a series of maps, given in the same input file. Each map describes how to
    convert numbers from a source category into numbers in a destination category, by describing
    entire ranges of numbers that can be converted. Each line within a map contains three numbers:
    the destination range start, the source range start, and the range length. If a number does not
    fall into any of the ranges covered by the next map, it is unaffected.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the seeds and maps.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    min_loc : int
        The lowest location number corresponding to any of the given seed numbers.

    """
    # Parse input file
    seeds, maps = get_input(input_file)
    
    locations = []
    # For each seed
    for seed in seeds:
        # Loop through every map
        for curr_map in maps:
            # If the seed if covered by any of the ranges in the current map, convert it
            if any(pos := [seed >= m[1] and seed - m[1] < m[2] for m in curr_map]):
                # Find which range applies
                ind = pos.index(True)
                # Perform conversion
                seed = curr_map[ind][0] + (seed - curr_map[ind][1])
        # After every map is applied we have the location, append to list
        locations.append(seed)

    # Find the minimum location
    min_loc = min(locations)

    return min_loc

def Day5_Part2(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    """
    Finds the lowest location number that corresponds to any of the initial seed numbers given in
    an input file. The location corresponding to a given seed can be found by running the seed
    number through a series of maps, given in the same input file. Each map describes how to
    convert numbers from a source category into numbers in a destination category, by describing
    entire ranges of numbers that can be converted. Each line within a map contains three numbers:
    the destination range start, the source range start, and the range length. If a number does not
    fall into any of the ranges covered by the next map, it is unaffected.

    However, instead of just giving the seed numbers directly, the seeds line in the input file
    actually describes ranges of seed numbers, in pairs of values. Within each pair, the first
    value is the start of the range and the second value is the length of the range.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the seeds and maps.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    min_loc : int
        The lowest location number corresponding to any of the given seed numbers.

    """
    # Parse input file
    seeds, maps = get_input(input_file)

    # Loop through every map
    for curr_map in maps:
        # Create new list of seed number ranges
        new_seeds = []
        # For each pair of numbers in the seeds line
        for n in range(len(seeds)//2):
            # Extract the correpsonding seed number range
            seed_start, seed_range = seeds[2*n], seeds[2*n + 1]
            seed_end = seed_start + seed_range
            # Move through the seed number range
            while seed_start < seed_end:
                # If the current start number intersects with a map range, do the conversion
                if any(pos := [seed_start >= m[1] and seed_start - m[1] < m[2] for m in curr_map]):
                    # Find which range applies
                    ind = pos.index(True)
                    # If this map range covers the remainder of the seed range, convert the full
                    # range and move on to the next seed range
                    if curr_map[ind][1] + curr_map[ind][2] >= seed_end:
                        new_seeds += [curr_map[ind][0] + (seed_start - curr_map[ind][1]), seed_end - seed_start]
                        break
                    # Else convert the seed range which is covered and add it to the new seed range
                    # list, and then move to the start of the next seed range
                    else:
                        new_seeds += [curr_map[ind][0] + (seed_start - curr_map[ind][1]), curr_map[ind][1] + curr_map[ind][2] - seed_start]
                        seed_start = curr_map[ind][1] + curr_map[ind][2]
                # If the current start number doesn't intersect with any map range
                else:
                    # Check if there are any map ranges which start above the current seed value
                    if (next_maps := [m[1] for m in curr_map if m[1] > seed_start]):
                        # If there are, find the nearest one
                        next_map = min(next_maps)
                        # If this nearest map starts after the end of the current seed range, add
                        # the seed range as is it to the new seed range list and move on to the
                        # next seed range
                        if next_map >= seed_end:
                            new_seeds += [seed_start, seed_end - seed_start]
                            break
                        # Else add the seed range before the next map as it is to the new seed
                        # range list, and move to the start of the next map
                        else:
                            new_seeds += [seed_start, next_map - seed_start]
                            seed_start = next_map
                    # If there are no remaining map ranges above the current seed value
                    else:
                        # Add the remainder of the current seed range as it is to the new seed
                        # range list, and move on to the next seed range
                        new_seeds += [seed_start, seed_end - seed_start]
                        break
    
        # Set seeds to a copy of new seeds and repeat for every map
        seeds = new_seeds.copy()

    # The minimum corresponding location is the lowest start point of any of the location ranges
    min_loc = min(seeds[::2])

    return min_loc
    