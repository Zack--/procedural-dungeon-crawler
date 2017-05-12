import numpy


def randint(start, end):
    """
    Returns a random integer between start and end inclusive
    Args:
        end (int): upper limit of the range (inclusive)
        start (int): lower limit of the range (exclusive)
    Returns:
        (int) random integer between start and end
    """
    return numpy.random.randint(start, end)


def random_choice(pool, exclude=None):
    """
    Randomly returns an element in a list
    Args:
        pool (list): pool to pick the element from
        exclude (): element that is in the pool and to be excluded
    Returns:
        random element from pool that is not exclude
    """

    idx = numpy.random.randint(0, len(pool) - 1)
    if exclude:
        while pool[idx] == exclude:
            idx = numpy.random.randint(0, len(pool) - 1)
    return pool[idx]


def chance(randomness):
    """
    Randomly generates a number between 0 and 100 and return
    True if it's below the randomness factor on a scale of a hundred
    Args:
        randomness (float): number between 0.0 and 1.0
    Returns:
        bool. True if it randomly got a num below randomness, False otherwise
    """

    return numpy.random.randint(1, 101) < randomness*100
