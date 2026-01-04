import unittest

from utils import closest_factors


class TestClosestFactors(unittest.TestCase):
    """Test cases for the closest_factors function."""

    def test_perfect_square(self):
        """Test that perfect squares return (sqrt(n), sqrt(n))."""
        self.assertEqual(closest_factors(16), (4, 4))
        self.assertEqual(closest_factors(25), (5, 5))

    def test_prime_number(self):
        """Test that prime numbers return (1, n)."""
        self.assertEqual(closest_factors(2), (1, 2))
        self.assertEqual(closest_factors(7), (1, 7))

    def test_even_numbers(self):
        """Test even numbers that are not perfect squares."""
        self.assertEqual(closest_factors(12), (3, 4))
        self.assertEqual(closest_factors(20), (4, 5))

    def test_larger_numbers(self):
        """Test larger numbers."""
        self.assertEqual(closest_factors(72), (8, 9))
        self.assertEqual(closest_factors(100), (10, 10))

    def test_edge_cases(self):
        """Test edge cases."""
        # n = 1
        self.assertEqual(closest_factors(1), (1, 1))

        # Small composite numbers
        self.assertEqual(closest_factors(6), (2, 3))
        self.assertEqual(closest_factors(15), (3, 5))

    def test_factor_product(self):
        """Test that the factors always multiply to the original number."""
        test_cases = [19, 30, 144]
        for n in test_cases:
            a, b = closest_factors(n)
            self.assertEqual(a * b, n, f"Factors {a} * {b} should equal {n}")

    def test_factor_order(self):
        """Test that the smaller factor is first."""
        test_cases = [31, 60, 400]
        for n in test_cases:
            a, b = closest_factors(n)
            self.assertLessEqual(
                a, b, f"First factor {a} should be <= second factor {b}"
            )
