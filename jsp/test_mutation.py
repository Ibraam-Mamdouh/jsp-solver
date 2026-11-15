import random
import unittest
from collections import Counter

from jsp.mutation import swap_mutation


class TestSwapMutation(unittest.TestCase):

    def test_rate_one_swaps_exactly_two_positions(self):
        c = [0, 1, 0, 2, 1, 2]
        rng = random.Random(7)
        for _ in range(100):
            m = swap_mutation(c, 1.0, rng)
            diff = [i for i in range(len(c)) if c[i] != m[i]]
            self.assertEqual(len(diff), 2)
            self.assertEqual(Counter(m), Counter(c))

    def test_rate_zero_changes_nothing(self):
        c = [0, 1, 0, 2, 1, 2]
        self.assertEqual(swap_mutation(c, 0.0, random.Random(1)), c)

    def test_input_not_modified(self):
        c = [0, 1, 0, 2, 1, 2]
        swap_mutation(c, 1.0, random.Random(3))
        self.assertEqual(c, [0, 1, 0, 2, 1, 2])

    def test_edge_cases(self):
        self.assertEqual(swap_mutation([0], 1.0), [0])
        self.assertEqual(swap_mutation([0, 0, 0], 1.0), [0, 0, 0])
        with self.assertRaises(ValueError):
            swap_mutation([0, 1], 1.5)


if __name__ == "__main__":
    unittest.main()