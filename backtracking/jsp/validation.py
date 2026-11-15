from models import JSPInstance
from schedule import Schedule

def validate_instance(instance: JSPInstance) -> list[str]:
    """
    Validates a JSPInstance configuration against basic structural rules.
    Returns a list of error messages. An empty list means the instance is valid.
    """
    errors = []
    
    # 1. Check if n_jobs matches the actual number of jobs provided
    if instance.n_jobs != len(instance.jobs):
        errors.append(
            f"Instance Error: n_jobs mismatch. Declared {instance.n_jobs} jobs, "
            f"but found {len(instance.jobs)} jobs in the instance."
        )
        
    # 2. Check if any job has an empty operations list
    for job in instance.jobs:
        if not job.operations:
            errors.append(
                f"Instance Error: Job {job.job_id} has no operations (empty operations list)."
            )
    
    for job in instance.jobs:
        for op_idx, op in enumerate(job.operations):
            # 3. Check if machine ID is within valid range [0, n_machines - 1]
            if not (0 <= op.machine < instance.n_machines):
                errors.append(
                    f"Instance Error: Job {job.job_id}, Op {op_idx} specifies invalid machine {op.machine}. "
                    f"Must be between 0 and {instance.n_machines - 1}."
                )
            
            # 4. Check if duration is strictly greater than 0
            if op.duration <= 0:
                errors.append(
                    f"Instance Error: Job {job.job_id}, Op {op_idx} has invalid duration {op.duration}. "
                    f"Duration must be greater than 0."
                )
                
    return errors

def validate_schedule(instance: JSPInstance, schedule: Schedule) -> list[str]:
    """
    Validates a schedule against the job shop instance constraints.
    Returns a list of error messages. An empty list means the schedule is valid.
    """
    errors = []
    
    # Build a set of all expected operations from the instance
    expected_ops = set()
    for job in instance.jobs:
        for op_idx, _ in enumerate(job.operations):
            expected_ops.add((job.job_id, op_idx))
            
    # Map schedule operations and check for duplicates or extra operations
    schedule_ops_map = {}
    for op in schedule.operations:
        key = (op.job_id, op.op_index)
        if key in schedule_ops_map:
            errors.append(f"Completeness Error: Operation (Job {op.job_id}, Op {op.op_index}) is duplicated in the schedule.")
        else:
            schedule_ops_map[key] = op
            
    # Check for missing operations
    for key in expected_ops:
        if key not in schedule_ops_map:
            errors.append(f"Completeness Error: Operation (Job {key[0]}, Op {key[1]}) is missing from the schedule.")
            
    # Check for extra/invalid operations not in the instance
    for key in schedule_ops_map:
        if key not in expected_ops:
            errors.append(f"Completeness Error: Operation (Job {key[0]}, Op {key[1]}) does not exist in the instance.")

    # Time constraint: start >= 0 and Data Consistency
    for key, op in schedule_ops_map.items():
        if op.start < 0:
            errors.append(f"Time Error: Job {op.job_id}, Op {op.op_index} starts at negative time ({op.start}).")
            
        if key in expected_ops:
            instance_op = instance.get_operation(op.job_id, op.op_index)
            if op.machine != instance_op.machine:
                errors.append(f"Data Consistency Error: Job {op.job_id}, Op {op.op_index} is on machine {op.machine}, but instance specifies machine {instance_op.machine}.")
            if op.duration != instance_op.duration:
                errors.append(f"Duration Error: Job {op.job_id}, Op {op.op_index} has duration {op.duration}, but instance specifies duration {instance_op.duration}.")

    # Precedence: for each job, operation k+1 start >= operation k end
    for job in instance.jobs:
        for op_idx in range(job.n_operations - 1):
            curr_key = (job.job_id, op_idx)
            next_key = (job.job_id, op_idx + 1)
            if curr_key in schedule_ops_map and next_key in schedule_ops_map:
                curr_op = schedule_ops_map[curr_key]
                next_op = schedule_ops_map[next_key]
                if next_op.start < curr_op.end:
                    errors.append(f"Precedence Error: Job {job.job_id}: Op {op_idx + 1} starts at {next_op.start} before previous op {op_idx} ends at {curr_op.end}.")

    # Machine Capacity: for each machine, ordered by start time, each operation start >= previous end
    for m in range(instance.n_machines):
        mach_ops = schedule.operations_on_machine(m)
        for i in range(len(mach_ops) - 1):
            op_curr = mach_ops[i]
            op_next = mach_ops[i+1]
            if op_next.start < op_curr.end:
                errors.append(f"Machine Capacity Error: Machine {m} has overlapping operations: Job {op_curr.job_id} Op {op_curr.op_index} ends at {op_curr.end}, but Job {op_next.job_id} Op {op_next.op_index} starts at {op_next.start}.")

    return errors

def is_valid(instance: JSPInstance, schedule: Schedule) -> bool:
    """Returns True if the schedule is valid for the given instance, False otherwise."""
    return len(validate_schedule(instance, schedule)) == 0