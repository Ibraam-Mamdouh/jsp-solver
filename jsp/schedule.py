from dataclasses import dataclass, field

@dataclass(frozen=True)
class ScheduledOperation:
    job_id: int
    op_index: int
    machine: int
    start: int
    end: int

    @property
    def duration(self) -> int:
        return self.end - self.start
    
@dataclass
class Schedule:
    operations: list[ScheduledOperation] = field(default_factory=list)

    @property
    def makespan(self) -> int:
        """Returns the maximum end time across all operations, or 0 if the schedule is empty."""
        if not self.operations:
            return 0
        return max(op.end for op in self.operations)
    
    def operations_on_machine(self, m: int) -> list[ScheduledOperation]:
        """Returns all operations assigned to machine m, sorted by start time."""
        machine_ops = [op for op in self.operations if op.machine == m]
        return sorted(machine_ops, key=lambda x: x.start)

    def get(self, job_id: int, op_index: int) -> ScheduledOperation:
        """Returns the ScheduledOperation matching the given job_id and op_index, or raises ValueError if not found."""
        for op in self.operations:
            if op.job_id == job_id and op.op_index == op_index:
                return op
        raise ValueError(f"Scheduled operation for job {job_id}, operation index {op_index} not found.")