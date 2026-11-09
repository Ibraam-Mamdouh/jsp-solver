import unittest
from dataclasses import FrozenInstanceError
from schedule import ScheduledOperation, Schedule

class TestSchedule(unittest.TestCase):
    def test_scheduled_operation_creation_and_duration(self):
        """Test the creation of ScheduledOperation and its duration property."""
        op1 = ScheduledOperation(job_id=1, op_index=0, machine=0, start=0, end=2)
        op2 = ScheduledOperation(job_id=0, op_index=0, machine=0, start=2, end=5)

        self.assertEqual(op1.duration, 2)
        self.assertEqual(op2.duration, 3)

    def test_scheduled_operation_is_frozen(self):
        """Test that the ScheduledOperation instance is immutable (frozen)."""
        op1 = ScheduledOperation(job_id=1, op_index=0, machine=0, start=0, end=2)
        
        with self.assertRaises(FrozenInstanceError):
            op1.start = 5  # Modifying should raise FrozenInstanceError

    def test_schedule_features_with_mixed_order(self):
        """Test Schedule makespan, sorting in operations_on_machine, and get lookup using table data."""
        # Inserting operations in a shuffled/mixed order to test automatic sorting by start time
        ops = [
            # Machine 1 operations
            ScheduledOperation(job_id=0, op_index=1, machine=1, start=8, end=10),
            ScheduledOperation(job_id=2, op_index=0, machine=1, start=0, end=4),
            ScheduledOperation(job_id=1, op_index=2, machine=1, start=4, end=8),
            
            # Machine 0 operations
            ScheduledOperation(job_id=0, op_index=0, machine=0, start=2, end=5),
            ScheduledOperation(job_id=1, op_index=0, machine=0, start=0, end=2),
            
            # Machine 2 operations
            ScheduledOperation(job_id=0, op_index=2, machine=2, start=10, end=12),
            ScheduledOperation(job_id=1, op_index=1, machine=2, start=2, end=3),
            ScheduledOperation(job_id=2, op_index=1, machine=2, start=4, end=7),
        ]

        schedule = Schedule(operations=ops)

        # 1. Test makespan (should be 12)
        self.assertEqual(schedule.makespan, 12)

        # 2. Test operations_on_machine(1) returns sorted operations: job 2 -> job 1 -> job 0
        mach1_ops = schedule.operations_on_machine(1)
        self.assertEqual(len(mach1_ops), 3)
        self.assertEqual(mach1_ops[0].job_id, 2)
        self.assertEqual(mach1_ops[1].job_id, 1)
        self.assertEqual(mach1_ops[2].job_id, 0)

        # 3. Test get(0, 2) returns machine 2 operation from 10 to 12
        op_target = schedule.get(0, 2)
        self.assertEqual(op_target.machine, 2)
        self.assertEqual(op_target.start, 10)
        self.assertEqual(op_target.end, 12)

        # 4. Test get with non-existent job/op raises ValueError
        with self.assertRaises(ValueError):
            schedule.get(9, 0)

        # 5. Test empty schedule makespan returns 0
        empty_schedule = Schedule([])
        self.assertEqual(empty_schedule.makespan, 0)

if __name__ == '__main__':
    unittest.main()