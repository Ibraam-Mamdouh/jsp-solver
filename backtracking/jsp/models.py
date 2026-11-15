from dataclasses import dataclass, field

@dataclass(frozen=True)
class Operation:
    machine: int
    duration: int

@dataclass
class Job:
    job_id: int
    operations: list[Operation] = field(default_factory=list)

    @property
    def n_operations(self) -> int:
        return len(self.operations)

@dataclass
class JSPInstance:
    name : str
    n_jobs: int
    n_machines: int
    jobs: list[Job] = field(default_factory=list)

    @property
    def total_operations(self) -> int:
        return sum(job.n_operations for job in self.jobs)
    
    def get_operation(self, job_id: int, op_index: int) -> Operation:
        job = next((j for j in self.jobs if j.job_id == job_id), None)
        if job is None:
            raise ValueError(f"Job with id {job_id} not found.")
        return job.operations[op_index]