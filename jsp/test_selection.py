import unittest

from jsp.selection import tournament_selection


class TestTournamentSelection(unittest.TestCase):

    def test_returns_best_when_k_equals_population(self):
        pop = [[0, 1], [1, 0], [0, 1]]
        self.assertEqual(tournament_selection(pop, [30, 10, 20], k=3), [1, 0])

    def test_returns_a_copy(self):
        pop = [[0, 1], [1, 0]]
        winner = tournament_selection(pop, [5, 1], k=2)
        winner.append(99)
        self.assertEqual(pop[1], [1, 0])

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            tournament_selection([[0]], [1, 2])
        with self.assertRaises(ValueError):
            tournament_selection([[0]], [1], k=2)


if __name__ == "__main__":
    unittest.main()