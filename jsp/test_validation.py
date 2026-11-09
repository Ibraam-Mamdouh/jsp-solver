import unittest
from models import Operation, Job, JSPInstance
from schedule import ScheduledOperation, Schedule
from validation import validate_schedule, is_valid, validate_instance
from parser import load_instance
from pathlib import Path

class TestValidator(unittest.TestCase):
    
    FILE_PATH = str(Path(__file__).resolve().parent.parent / "Data" / "jobshop1.txt")

    def setUp(self):
        """Set up the sample plant instance (3 jobs, 3 machines) from image example."""
        self.instance = JSPInstance(
            name="image_example",
            n_jobs=3,
            n_machines=3,
            jobs=[
                Job(job_id=0, operations=[Operation(0, 3), Operation(1, 2), Operation(2, 2)]),
                Job(job_id=1, operations=[Operation(0, 2), Operation(2, 1), Operation(1, 4)]),
                Job(job_id=2, operations=[Operation(1, 4), Operation(2, 3)])
            ]
        )
        
        self.valid_ops = [
            ScheduledOperation(job_id=1, op_index=0, machine=0, start=0, end=2),
            ScheduledOperation(job_id=0, op_index=0, machine=0, start=2, end=5),
            ScheduledOperation(job_id=2, op_index=0, machine=1, start=0, end=4),
            ScheduledOperation(job_id=1, op_index=2, machine=1, start=4, end=8),
            ScheduledOperation(job_id=0, op_index=1, machine=1, start=8, end=10),
            ScheduledOperation(job_id=1, op_index=1, machine=2, start=2, end=3),
            ScheduledOperation(job_id=2, op_index=1, machine=2, start=4, end=7),
            ScheduledOperation(job_id=0, op_index=2, machine=2, start=10, end=12),
        ]
        self.valid_schedule = Schedule(self.valid_ops)

    def test_validate_instance_n_jobs_mismatch(self):
        """Test validate_instance when n_jobs does not match len(jobs)."""
        bad_instance = JSPInstance(
            name="n_jobs_mismatch",
            n_jobs=3,
            n_machines=3,
            jobs=[Job(job_id=0, operations=[Operation(0, 3)])]
        )
        errors = validate_instance(bad_instance)
        self.assertTrue(any("n_jobs mismatch" in err for err in errors))

    def test_validate_instance_empty_job_operations(self):
        """Test validate_instance when a job has an empty operations list."""
        bad_instance = JSPInstance(
            name="empty_ops",
            n_jobs=1,
            n_machines=3,
            jobs=[Job(job_id=0, operations=[])]
        )
        errors = validate_instance(bad_instance)
        self.assertTrue(any("has no operations" in err for err in errors))

    def test_validate_instance_invalid_machine(self):
        """Test validate_instance with an invalid machine ID."""
        bad_instance = JSPInstance(
            name="bad_machine",
            n_jobs=1,
            n_machines=3,
            jobs=[Job(job_id=0, operations=[Operation(machine=5, duration=3)])]
        )
        errors = validate_instance(bad_instance)
        self.assertTrue(any("machine" in err for err in errors))

    def test_validate_instance_invalid_duration(self):
        """Test validate_instance with zero duration."""
        bad_instance = JSPInstance(
            name="bad_duration",
            n_jobs=1,
            n_machines=3,
            jobs=[Job(job_id=0, operations=[Operation(machine=0, duration=0)])]
        )
        errors = validate_instance(bad_instance)
        self.assertTrue(any("duration" in err for err in errors))

    def test_validate_instance_valid_cases(self):
        """Verify that valid instances return an empty error list."""
        img_errors = validate_instance(self.instance)
        self.assertEqual(img_errors, [])

        try:
            jsp_ft06 = load_instance(self.FILE_PATH, "ft06")
            ft06_errors = validate_instance(jsp_ft06)
            self.assertEqual(ft06_errors, [])
        except FileNotFoundError:
            self.skipTest(f"Data file {self.FILE_PATH} not found.")

    def test_valid_image_schedule(self):
        errors = validate_schedule(self.instance, self.valid_schedule)
        self.assertEqual(errors, [])
        self.assertTrue(is_valid(self.instance, self.valid_schedule))

    def test_missing_operation(self):
        ops_missing = self.valid_ops[:-1]
        sched = Schedule(ops_missing)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Completeness Error" in err for err in errors))

    def test_duplicate_operation(self):
        ops_dup = self.valid_ops + [self.valid_ops[0]]
        sched = Schedule(ops_dup)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Completeness Error" in err for err in errors))

    def test_wrong_machine(self):
        ops_wrong_mach = [ScheduledOperation(1, 0, 2, 0, 2)] + self.valid_ops[1:]
        sched = Schedule(ops_wrong_mach)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Data Consistency Error" in err for err in errors))

    def test_wrong_duration(self):
        ops_wrong_dur = [ScheduledOperation(1, 0, 0, 0, 4)] + self.valid_ops[1:]
        sched = Schedule(ops_wrong_dur)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Duration Error" in err for err in errors))

    def test_precedence_violation(self):
        ops_mod = []
        for op in self.valid_ops:
            if op.job_id == 1 and op.op_index == 1:
                ops_mod.append(ScheduledOperation(1, 1, 2, 1, 2))
            else:
                ops_mod.append(op)
        sched = Schedule(ops_mod)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Precedence Error" in err for err in errors))

    def test_machine_capacity_violation(self):
        ops_mod = []
        for op in self.valid_ops:
            if op.job_id == 0 and op.op_index == 0:
                ops_mod.append(ScheduledOperation(0, 0, 0, 1, 4))
            else:
                ops_mod.append(op)
        sched = Schedule(ops_mod)
        errors = validate_schedule(self.instance, sched)
        self.assertTrue(any("Machine Capacity Error" in err for err in errors))

    def test_ft06_integration_sequential(self):
        try:
            jsp = load_instance(self.FILE_PATH, "ft06")
        except FileNotFoundError:
            self.skipTest(f"Data file {self.FILE_PATH} not found.")

        machine_available_time = {m: 0 for m in range(jsp.n_machines)}
        job_available_time = {j.job_id: 0 for j in jsp.jobs}
        ops = []
        
        for job in jsp.jobs:
            for op_idx, op in enumerate(job.operations):
                start = max(machine_available_time[op.machine], job_available_time[job.job_id])
                end = start + op.duration
                machine_available_time[op.machine] = end
                job_available_time[job.job_id] = end
                ops.append(ScheduledOperation(job_id=job.job_id, op_index=op_idx, machine=op.machine, start=start, end=end))
        
        sequential_schedule = Schedule(ops)
        self.assertTrue(is_valid(jsp, sequential_schedule))
        
        total_durations = sum(op.duration for job in jsp.jobs for op in job.operations)
        self.assertLessEqual(sequential_schedule.makespan, total_durations)

        max_job_duration = max(sum(op.duration for op in job.operations) for job in jsp.jobs)
        self.assertGreaterEqual(sequential_schedule.makespan, max_job_duration)

        machine_loads = {m: 0 for m in range(jsp.n_machines)}
        for job in jsp.jobs:
            for op in job.operations:
                machine_loads[op.machine] += op.duration
        max_machine_load = max(machine_loads.values())
        self.assertGreaterEqual(sequential_schedule.makespan, max_machine_load)

if __name__ == '__main__':
    unittest.main()