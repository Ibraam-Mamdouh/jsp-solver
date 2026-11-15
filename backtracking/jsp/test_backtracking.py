from parser import load_instance
from backtracking import solve_backtracking

def test_solve_backtracking():
    print("Testing Backtracking Algorithm ") 
    file_path = "Data/jobshop1.txt"
    instance_name = "abz5" 

    try:
        print(f"Loading instance '{instance_name}'...")
        instance = load_instance(file_path, instance_name)
        print(f"Instance loaded successfully! Jobs: {instance.n_jobs}, Machines: {instance.n_machines}")
        print("Running Backtracking solver (with 10 seconds time limit)...")
        schedule = solve_backtracking(instance, time_limit=10) 

        if schedule:
            print("\n[SUCCESS] Schedule found!")
            print(f"Best Makespan: {schedule.makespan}")
            print(f"Total Scheduled Operations: {len(schedule.operations)}")            
            print("\nSample of scheduled operations:")

            for op in schedule.operations[:5]:
               print(f"Job {op.job_id}, Op {op.op_index} -> Machine {op.machine}: Start={op.start}, End={op.end}")

        else:
            print("\n[TIMEOUT / NO SOLUTION] Backtracking could not find a solution within the time limit.")

    except Exception as e:
        print(f"\n[ERROR] An error occurred during testing: {e}")
if __name__ == "__main__":
    test_solve_backtracking()