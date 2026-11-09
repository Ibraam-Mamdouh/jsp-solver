import unittest
from parser import load_instance

class TestJSPParser(unittest.TestCase):
    
    # Path to the benchmarks file (make sure it matches your file location)
    FILE_PATH = "Data/jobshop1.txt"

    def test_ft06_specifics(self):
        """Detailed test for ft06 (dimensions, first and last operations)"""
        try:
            jsp = load_instance(self.FILE_PATH, "ft06")
        except FileNotFoundError:
            self.skipTest("Data file not found at the specified path.")

        # Verify basic dimensions
        self.assertEqual(jsp.n_jobs, 6)
        self.assertEqual(jsp.n_machines, 6)
        self.assertEqual(jsp.total_operations, 36)

        # Verify the first operation in the first job
        first_op = jsp.jobs[0].operations[0]
        # Based on the standard ft06 file structure
        self.assertIsNotNone(first_op)

        # Verify the last operation in the last job
        last_op = jsp.jobs[5].operations[5]
        self.assertEqual(last_op.machine, 2)
        self.assertEqual(last_op.duration, 1)

    def test_benchmarks_loop(self):
        """Iterate over a set of benchmarks and verify dimensions and Job Shop conditions"""
        benchmarks = [
            ("ft06", 6, 6),
            ("ft10", 10, 10),
            ("la01", 10, 5),
            ("abz5", 10, 10),
            ("orb01", 10, 10)
        ]

        for name, exp_jobs, exp_mach in benchmarks:
            with self.subTest(name=name):
                try:
                    jsp = load_instance(self.FILE_PATH, name)
                except FileNotFoundError:
                    self.skipTest("Data file not found at the specified path.")

                # 1. Verify dimensions and matching total_operations
                self.assertEqual(jsp.n_jobs, exp_jobs)
                self.assertEqual(jsp.n_machines, exp_mach)
                self.assertEqual(jsp.total_operations, exp_jobs * exp_mach)

                # 2. Verify that each job contains all machines from 0 to n_machines - 1 exactly once
                for job in jsp.jobs:
                    self.assertEqual(job.n_operations, exp_mach)
                    machines = [op.machine for op in job.operations]
                    self.assertEqual(sorted(machines), list(range(exp_mach)))

    def test_error_cases(self):
        """Test error cases and expected exceptions"""
        # 1. Completely non-existent instance name
        with self.assertRaises(ValueError):
            load_instance(self.FILE_PATH, "xyz")

        # 2. Ensure no confusion between ft1 and ft10 (ft1 does not exist as an independent name)
        with self.assertRaises(ValueError):
            load_instance(self.FILE_PATH, "ft1")

        # 3. Incorrect or non-existent file path
        with self.assertRaises(FileNotFoundError):
            load_instance("wrong_path_to_benchmarks.txt", "ft06")


if __name__ == "__main__":
    unittest.main()