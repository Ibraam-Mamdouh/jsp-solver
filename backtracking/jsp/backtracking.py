import time
from models import JSPInstance
from schedule import Schedule, ScheduledOperation
from validation import validate_schedule

def solve_backtracking(instance , time_limit=None):
    start_wall_time = time.time()
    
    best_makespan = float('inf')
    best_scheduled_ops = None

    job_next_op = {job.job_id: 0 for job in instance.jobs}
    machine_free_time = {m: 0 for m in range(instance.n_machines)}
    job_ready_time = {job.job_id: 0 for job in instance.jobs}
    current_ops_schedule = [] 

    def backtrack():
        nonlocal best_makespan, best_scheduled_ops

        if time_limit and (time.time() - start_wall_time) > time_limit:
            return

        if all(job_next_op[job.job_id] >= job.n_operations for job in instance.jobs):
            current_makespan = max(job_ready_time.values())
            if current_makespan < best_makespan:
                best_makespan = current_makespan
                best_scheduled_ops = list(current_ops_schedule)
            return

        for job in instance.jobs:
            op_idx = job_next_op[job.job_id]
            if op_idx < job.n_operations:
                op = job.operations[op_idx]
                machine = op.machine
                duration = op.duration

                start_time = max(job_ready_time[job.job_id], machine_free_time[machine])
                end_time = start_time + duration

                if start_time >= best_makespan:
                    continue

                old_machine_time = machine_free_time[machine]
                old_job_time = job_ready_time[job.job_id]

                job_next_op[job.job_id] += 1
                machine_free_time[machine] = end_time
                job_ready_time[job.job_id] = end_time
                
                sched_op = ScheduledOperation(
                    job_id=job.job_id,
                    op_index=op_idx,
                    machine=machine,
                    start=start_time,  
                    end=end_time       
                )
                current_ops_schedule.append(sched_op)

                backtrack()
                current_ops_schedule.pop()
                job_next_op[job.job_id] -= 1
                machine_free_time[machine] = old_machine_time
                job_ready_time[job.job_id] = old_job_time

    backtrack()
    if best_scheduled_ops is not None:
        final_schedule = Schedule(operations=best_scheduled_ops)
        errors = validate_schedule(instance, final_schedule)
        if errors:
            print("Validation Errors found in Backtracking schedule:", errors)
        return final_schedule

    return None