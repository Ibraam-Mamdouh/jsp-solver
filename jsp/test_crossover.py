import random
import unittest
from collections import Counter

from jsp.crossover import jox_crossover, _jox_child


class TestJoxCrossover(unittest.TestCase):

    def test_known_example(self):
        p1 = [0, 1, 0, 2, 1, 2]
        p2 = [2, 0, 1, 1, 2, 0]
        self.assertEqual(_jox_child(p1, p2, {0}), [0, 2, 0, 1, 1, 2])

    def test_children_keep_gene_counts(self):
        p1 = [0, 1, 0, 2, 1, 2]
        p2 = [2, 0, 1, 1, 2, 0]
        rng = random.Random(42)
        for _ in range(100):
            c1, c2 = jox_crossover(p1, p2, rng)
            self.assertEqual(Counter(c1), Counter(p1))
            self.assertEqual(Counter(c2), Counter(p1))

    def test_parents_not_modified(self):
        p1 = [0, 1, 0, 2, 1, 2]
        p2 = [2, 0, 1, 1, 2, 0]
        jox_crossover(p1, p2, random.Random(1))
        self.assertEqual(p1, [0, 1, 0, 2, 1, 2])
        self.assertEqual(p2, [2, 0, 1, 1, 2, 0])

    def test_different_lengths_raise(self):
        with self.assertRaises(ValueError):
            jox_crossover([0, 1], [0, 1, 1])


if __name__ == "__main__":
    unittest.main()