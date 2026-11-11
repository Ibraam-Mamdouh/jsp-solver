import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from jsp.parser import load_instance
from jsp.validation import is_valid
from jsp.genetic_algorithm import (generate_random_chromosome, generate_spt_chromosome, create_initial_population)


class TestGACore(unittest.TestCase):
    FILE_PATH = str(Path(__file__).resolve().parent.parent / "Data" / "jobshop1.txt")
    def setUp(self):
        try:
            self.jsp = load_instance(self.FILE_PATH, "ft06")
        except FileNotFoundError:
            self.skipTest(f"Data file not found at {self.FILE_PATH}")

    def test_random_feasibility(self):
        chrom = generate_random_chromosome(self.jsp)
        self.assertEqual(len(chrom.genes), self.jsp.total_operations)
        self.assertTrue(is_valid(self.jsp, chrom.schedule))
        self.assertGreater(chrom.fitness, 0.0)

    def test_spt_feasibility(self):
        spt = generate_spt_chromosome(self.jsp)
        self.assertEqual(len(spt.genes), self.jsp.total_operations)
        self.assertTrue(is_valid(self.jsp, spt.schedule))

    def test_population(self):
        pop = create_initial_population(self.jsp, pop_size=20, include_spt=True)
        self.assertEqual(len(pop), 20)
        for ind in pop:
            self.assertTrue(is_valid(self.jsp, ind.schedule))

    def test_clone_independence(self):
        orig = generate_random_chromosome(self.jsp)
        copy = orig.clone()
        self.assertEqual(orig.genes, copy.genes)
        copy.genes[0] = 999
        self.assertNotEqual(orig.genes, copy.genes)
        self.assertNotEqual(orig.genes[0], 999)

if __name__ == "__main__":
    unittest.main()