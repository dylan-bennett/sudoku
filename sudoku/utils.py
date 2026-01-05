import math


def closest_factors(n):
    """
    Returns a tuple of two integers (a, b) such that a * b == n and the
    absolute difference |a - b| is as small as possible.

    The function finds factor pairs of n that are as close to each other as
    possible, starting from the square root of n and searching downwards.

    Args:
        n (int): The integer to find factors for.

    Returns:
        tuple[int, int]: A tuple (a, b) where a * b == n and |a - b| is
            minimized.
    """
    sqrt_n = int(math.sqrt(n))
    for i in range(sqrt_n, 0, -1):
        if n % i == 0:
            return (i, n // i)
    return (1, n)
