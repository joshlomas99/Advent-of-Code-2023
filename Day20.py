def get_input(input_file: str='Inputs/Day20_Inputs.txt', split_loops: bool=False) -> list:
    """
    Parse an input file to extract a module configuration. This lists the name of every module,
    preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a
    list of its destination modules.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the module configuration.
        The default is 'Inputs/Day20_Inputs.txt'.
    split_loops : bool, optional
        Whether to seperate the independent loops of the machine.
        The default is False.

    Returns
    -------
    config : list or list of lists
        If not split_loops, returns the parsed lines describing the module configuration. If
        split_loops is True then returns the parsed lines but seperated into several lists, one
        for each independent loop.

    """
    # Parse input file and split module names and connections
    with open(input_file) as f:
        config = [l.strip().split(' -> ') for l in f.readlines()]

    # If not splitting loops, we're done
    if not split_loops:
        return config

    # Find the broadcaster
    for i in range(len(config)):
        if config[i][0] == 'broadcaster':
            break

    # Extract it and use each of its connections to initiate a new loop
    loops = [[['broadcaster', name]] for name in config.pop(i)[1].split(', ')]
    # Find the names of all the conjunction modules
    conj = [l[0][1:] for l in config if l[0].startswith('&')]

    # For each loop
    for loop in loops:
        # Starting with the connection from the broadcaster
        next_mod = loop[-1][1]
        # While we haven't reached the conjunction module which closes the loop
        while not loop[-1][0].startswith('&'):
            # Find the next module definition in the list
            for i in range(len(config)):
                if config[i][0][1:] == next_mod:
                    break#
            # Extract and add to the loop
            loop.append(config.pop(i))
            # Find next connections
            next_mods = loop[-1][1].split(', ')
            # If there is only 1 continue
            if len(next_mods) == 1:
                next_mod = next_mods[0]
            # Else if there are multiple, continue with the first which isn't a conjunction module
            else:
                for next_mod in next_mods:
                    if next_mod not in conj:
                        break

    return loops

def extract_modules(config: list) -> tuple:
    """
    Extract the initial states and connections of a series of modules, with a given configuration.
    There are 4 types of module enumerated as follows:
        - 0 = flip-flop modules, which start as "off" or 0
        - 1 = conjunction modules, which start with every input at 0
        - 2 = broadcaster module
        - 3 = untyped module, which starts with no inputs

    Parameters
    ----------
    config : list
        List giving the module configuration.

    Returns
    -------
    modules : dict(str: int)
        Dict mapping each module name onto its enumerated type.
    states : dict(str: int or dict(str: int) or list(int))
        Dict mapping each module name into its state, which is an int for flip-flop modules, a dict
        mapping the name of every input module onto its remembered state for conjunction modules,
        and a list of each input for untyped modules.
    connected : dict(str: list(str))
        Dict mapping the name of every module onto the names of the modules it outputs to.

    """

    # 0 - flip-flop
    # 1 - conjunction
    # 2 - broadcaster
    # 3 - untyped
    
    modules, states, connected = dict(), dict(), dict()
    # Loop through config
    for name, conn in config:
        # Identify module type and initialise accordingly
        if name.startswith('%'):
            modules[name[1:]] = 0
            states[name[1:]] = 0
            connected[name[1:]] = conn.split(', ')
        elif name.startswith('&'):
            modules[name[1:]] = 1
            states[name[1:]] = dict()
            connected[name[1:]] = conn.split(', ')
        elif name == 'broadcaster':
            modules[name] = 2
            connected[name] = conn.split(', ')

    # Loop back through all connections
    for name, conn in connected.items():
        for c in conn:
            # If there is a connection which wasn't defined in the config, this is an untyped
            # module
            if c not in modules:
                modules[c] = 3
                states[c] = []
            # Else if this module outputs to a conjunction module, add it to the state of that
            # module
            elif modules[c] == 1:
                states[c][name] = 0

    return modules, states, connected

def push_button(modules: dict, states: dict, connected: dict,
                n_low: int=0, n_high: int=0) -> tuple:
    """
    Determines the number of low and high pulses which are sent after a button which sends a single
    low pulse to the broadcaster module of a machine, whose configuration is given as input, is
    pushed. Modules communicate using pulses. Each pulse is either a high pulse or a low pulse.
    When a module sends a pulse, it sends that type of pulse to each module in its list of
    destination modules. There are several different types of modules:
        - Flip-flop modules (prefix %) are either on or off; they are initially off. If a
          flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a
          flip-flop module receives a low pulse, it flips between on and off. If it was off, it
          turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
        - Conjunction modules (prefix &) remember the type of the most recent pulse received from
          each of their connected input modules; they initially default to remembering a low pulse
          for each input. When a pulse is received, the conjunction module first updates its memory
          for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse;
          otherwise, it sends a high pulse.
        - There is a single broadcast module (named broadcaster). When it receives a pulse, it
          sends the same pulse to all of its destination modules.
    Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a,
    b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to
    modules b and c would have to be handled first.

    Parameters
    ----------
    modules : dict(str: int)
        Dict mapping each module name onto its enumerated type.
    states : dict(str: int or dict(str: int) or list(int))
        Dict mapping each module name into its state, which is an int for flip-flop modules, a dict
        mapping the name of every input module onto its remembered state for conjunction modules,
        and a list of each input for untyped modules.
    connected : dict(str: list(str))
        Dict mapping the name of every module onto the names of the modules it outputs to.
    n_low : int, optional
        The number of low pulses to start with.
        The default is 0.
    n_high : int, optional
        The number of high pulses to start with.
        The default is 0.

    Returns
    -------
    n_low : int
        The new number of low pulses sent.
    n_high : int
        The new number of high pulses sent.

    """
    # Reset inputs to untyped modules
    for name, m in modules.items():
        if m == 3:
            states[name] = []
    # Add one low pulse for the button press
    n_low += 1
    # Start a queue of pulses with each low pulse sent by the broadcaster
    queue = [(0, c, 'broadcaster') for c in connected['broadcaster']]
    # While there are pulses left to be processed
    while queue:
        # Extract the oldest one
        pulse, mod, source = queue.pop(0)
        # Increment corresponding counter
        if pulse == 0:
            n_low += 1
        else:
            n_high += 1
        # For flip-flop modules
        if modules[mod] == 0:
            # If the pulse is high do nothing
            if pulse > 0:
                continue
            # Else flip the state and output the new state
            else:
                states[mod] = (states[mod] + 1)%2
                for c in connected[mod]:
                    queue.append((states[mod], c, mod))
        # For conjunction modules
        elif modules[mod] == 1:
            # Update the source module in memory
            states[mod][source] = pulse
            # If all input states are high output low
            if all(states[mod].values()):
                for c in connected[mod]:
                   queue.append((0, c, mod))
            # Else output high
            else:
                for c in connected[mod]:
                   queue.append((1, c, mod))
        # For untyped modules, record the input
        elif modules[mod] == 3:
            states[mod].append(pulse)

    return n_low, n_high

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

@time_function
def Day20_Part1(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Calculates the result from multiplying the total number of low pulses sent by a series of
    modules, whose configuration is given in an input file, by the total number of high pulses
    sent, after a button sending a low pulse to the broadcaster module is pressed 1000 times.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the module configuration.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    product : int
        The product of the numbers of low and high pulses after 1000 button presses.

    """
    # Parse input file to extract module configuration
    lines = get_input(input_file)
    # Initialise module types, states and connections
    modules, states, connected = extract_modules(lines)
    # Count pulses
    n_low, n_high = 0, 0
    # Push button 1000 times
    for i in range(1000):
        # Update number of pulses each push
        n_low, n_high = push_button(modules, states, connected, n_low, n_high)

    product = n_low*n_high

    return  product

def graphviz_input(modules, connected):
    """
    Prints the input to visualise a given series of modules using graphviz.

    Parameters
    ----------
    modules : dict(str: int)
        Dict mapping each module name onto its enumerated type.
    connected : dict(str: list(str))
        Dict mapping the name of every module onto the names of the modules it outputs to.

    Returns
    -------
    None.

    """
    # Loop over module types
    for name, m_type in modules.items():
        # Set shape based on module type
        if m_type == 0:
            shape = 'diamond'
        elif m_type == 1:
            shape = 'square'
        if m_type == 2:
            shape = 'doublecircle'
        if m_type == 3:
            shape = 'star'
        print(f'{name} [shape="{shape}"]')
        # Loop over connections
        if name in connected:
            for connection in connected[name]:
                print(f'{name} -> {connection}')

def pushes_to_low(modules: dict, states: dict, connected: dict) -> int:
    """
    Determines the number of times a button which sends a single low pulse to the broadcaster of a
    series of modules forming a loop, needs to be pushed for a single low pulse to be sent to the
    final untyped module at the output of the loop. The loop consists of a series of flip-flop
    modules, one of which is fed by the broadcaster module, and some of which feed into a single
    conjunction module, which outputs to the untyped module.

    Parameters
    ----------
    modules : dict(str: int)
        Dict mapping each module name onto its enumerated type.
    states : dict(str: int or dict(str: int) or list(int))
        Dict mapping each module name into its state, which is an int for flip-flop modules, a dict
        mapping the name of every input module onto its remembered state for conjunction modules,
        and a list of each input for untyped modules.
    connected : dict(str: list(str))
        Dict mapping the name of every module onto the names of the modules it outputs to.

    Returns
    -------
    n : int
        Number of button pushes before a single low pulse is sent to the untyped module.

    """
    # Find the name of the untyped module
    end = [k for k, v in modules.items() if v == 3][0]

    n = 0
    # Until there is a low pulse to the untyped module
    while 0 not in states[end]:
        # Keep pushing the button
        push_button(modules, states, connected)
        # Count pushes
        n += 1

    return n

### All this is just to find the lowest common multiple of two numbers ###
                                                                         #
def next_prime(n: int) -> int:                                           #
    """                                                                  #
    Finds the next highest prime number after a given integer.           #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    n : int                                                              #                                                                         #                                                                         #
        The current number.                                              #
                                                                         #                                                                         #                                                                         #
    Returns                                                              #
    -------                                                              #
    n : int                                                              #
        The next highest prime number after the given integer.           #
                                                                         #
    """                                                                  #
    n += 1                                                               #
    # While the number has any factors between 2 and sqrt(n), increment  #
    while not all(n%i for i in range(2, int(n**0.5))):                   #
        n += 1                                                           #
                                                                         #
    return n                                                             #
                                                                         #
def prime_factors(n: int) -> dict:                                       #
    """                                                                  #
    Finds the prime factors of a given integer.                          #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    n : int                                                              #
        Number to find the prime factors for.                            #
                                                                         #
    Returns                                                              #
    -------                                                              #
    factors : dict(int: int)                                             #
        Dict mapping each prime factors onto its occurence in the prime  #
        factors of n.                                                    #
                                                                         #
    """                                                                  #
    #
    factors = dict()                                                     #
    # Start at 2                                                         #
    f = 2                                                                #
    # While there are remaining factors                                  #
    while n > 1:                                                         #
        # Count occurances of current factor                             #
        num = 0                                                          #
        while n%f == 0:                                                  #
            n /= f                                                       #
            num += 1                                                     #
        # Add new factor with occurance count                            #
        if num > 0:                                                      #
            factors[f] = num                                             #
        # Check next highest prime number                                #
        f = next_prime(f)                                                #
                                                                         #
    return factors                                                       #
                                                                         #
import operator                                                          #
from functools import reduce                                             #
                                                                         #
def lcm(nums: list) -> int:                                              #
    """                                                                  #
    Find the lowest common multiple of a list of integers.               #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    nums : list(int)                                                     #
        List of integers.                                                #
                                                                         #
    Returns                                                              #
    -------                                                              #
    lcm : int                                                            #
        Lowest common multiple of the two integers.                      #
                                                                         #
    """                                                                  #
    # Find prime factors of each number                                  #
    p_f = [prime_factors(n) for n in nums]                               #
    all_f = set(f for d in p_f for f in d)                               #
    # Find maximum occurence of every prime factor occuring across all   #
    # the numbers                                                        #
    factors = [f**max(n[f] for n in p_f if f in n) for f in all_f]       #
    # Find total product                                                 #
    return reduce(operator.mul, factors, 1)                              #
                                                                         #
##########################################################################

@time_function
def Day20_Part2(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Determines the fewest number of button presses required to deliver a single low pulse to the
    module named rx, in a series of modules whose configuration is given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the module configuration.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    first_rx_low : int
        The fewest number of button pushes required to send a low pulse to rx.

    """
    # Parse input file to extract module configuration, and split into 4 loops which each feed
    # a single conjunction module. For a low pulse to be sent to rx, all 4 conjunction modules
    # have to send a low pulse at the same time, so we can test each one seperately, and then the
    # solution is the lowest common multiple of the required pushes for each loop
    loops = get_input(input_file, split_loops=True)

    # Track frequencies of low pulses from the loop
    loop_freqs = []
    # For each loop
    for loop in loops:
        # Initialise module types, states and connections for the current loop
        modules, states, connected = extract_modules(loop)
        # Find pushes required for a single low pulse to be sent by the conjunction module
        loop_freq = pushes_to_low(modules, states, connected)
        loop_freqs.append(loop_freq)

    # Find lowest common multiple to find overall solution
    first_rx_low = lcm(loop_freqs)

    return first_rx_low

@time_function
def Day20_Part2_Fast(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Determines the fewest number of button presses required to deliver a single low pulse to the
    module named rx, in a series of modules whose configuration is given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the module configuration.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    first_rx_low : int
        The fewest number of button pushes required to send a low pulse to rx.

    """
    # Parse input file to extract module configuration, and split into 4 loops which each feed
    # a single conjunction module. For a low pulse to be sent to rx, all 4 conjunction modules
    # have to send a low pulse at the same time, so we can test each one seperately, and then the
    # solution is the lowest common multiple of the required pushes for each loop
    loops = get_input(input_file, split_loops=True)

    # Track frequencies of low pulses from the loop
    loop_freqs = []
    # For each loop
    for loop in loops:
        # Find the name of the conjunction module at the end of the loop
        conj = loop[-1][0][1:]
        # Track frequency of this loop
        freq = 0
        # For each flip-flop module in the loop, each one will send a high pulse after the button
        # is pushed according to increasing powers of two
        for n, (name, conn) in enumerate(loop[1:-1]):
            # If the flip-flop is connected to the conjuction module, add the corresponding power
            # of two to the frequency
            if conj in conn:
                freq += (2**n)

        loop_freqs.append(freq)

    # Find lowest common multiple to find overall solution
    first_rx_low = lcm(loop_freqs)

    return first_rx_low
