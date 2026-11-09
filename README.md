# Job Shop Scheduling (JSP) Framework

## 1. Problem Description
Job Shop Scheduling (JSP) is a classical optimization problem where a set of jobs must be processed on a given set of machines. Each job consists of a strict sequence of operations, and each operation requires a specific machine for a predetermined duration. The primary objective is to find a schedule that minimizes the **makespan** (the total completion time required to finish all jobs).

## 2. Constraints
The framework strictly enforces four core constraints:
1. **Precedence Constraint**: Operations belonging to the same job must be processed in their predefined sequential order (operation $k+1$ cannot start before operation $k$ finishes).
2. **Machine Capacity Constraint**: A machine can process at most one operation at a time (no overlapping operations on the same machine).
3. **No Preemption**: Once an operation starts, it runs continuously until completion.
4. **Completeness Constraint**: Every operation specified in the instance must be scheduled exactly once (no missing, extra, or duplicated operations).

## 3. Core Modules & Key Functions

| Class / Function | Type | Description |
| :--- | :--- | :--- |
| `load_instance` | Function | Loads and parses standard JSSP benchmark instances (e.g., `ft06`) from dataset files into a structured `JSPInstance`. |
| `validate_instance` | Function | Validates the structural integrity and bounds of the parsed `JSPInstance`. |
| `validate_schedule` | Function | Verifies that a given `Schedule` satisfies all precedence, machine capacity, non-preemption, and completeness constraints. |
| `is_valid` | Function | Returns a boolean (`True`/`False`) indicating whether a schedule is valid without throwing detailed validation errors. |
| `Operation` | Class | Represents a single operation of a job (`machine`, `duration`). |
| `Job` | Class | Represents a job composed of sequential operations (`job_id`, `operations`). |
| `JSPInstance` | Class | Represents the entire benchmark problem setup (`name`, `n_jobs`, `n_machines`, `jobs`). |
| `ScheduledOperation` | Class | Represents a scheduled operation timeline entry (`job_id`, `op_index`, `machine`, `start`, `end`). |
| `Schedule` | Class | Manages the collection of all scheduled operations, calculates total `makespan`, and indexes operations per machine. |

## 4. Benchmarks
The framework supports parsing and solving standard Job Shop Scheduling benchmark datasets, including:
* **Muth and Thompson**: `ft06` (6 jobs, 6 machines), `ft10`, `ft20`
* **Lawrence**: `la01`–`la40`
* **Adams, Balas, and Zawack**: `abz5`–`abz9`
* **Applegate and Cook**: `orb01`–`orb10`
* **Storer, Wu, and Vaccari**: `swv01`–`swv20`
* **Yamada and Nakano**: `yn1`–`yn4`

---

## 5. Usage Examples

### Loading an Instance and Validating Structure
```python
from pathlib import Path
from parser import load_instance
from validation import validate_instance

# Dynamic path resolution to handle execution from any directory
FILE_PATH = str(Path(__file__).resolve().parent / "Data" / "jobshop1.txt")

# Load benchmark instance 'ft06'
jsp = load_instance(FILE_PATH, "ft06")

# Validate structural integrity
errors = validate_instance(jsp)
if not errors:
    print("Instance is valid!")
```

### Validating a Schedule Timeline
```python
from schedule import Schedule, ScheduledOperation
from validation import validate_schedule, is_valid

# Example schedule construction
schedule = Schedule(operations=[
    ScheduledOperation(job_id=0, op_index=0, machine=2, start=0, end=3),
    ScheduledOperation(job_id=0, op_index=1, machine=0, start=3, end=9),
])

# Validate correctness and check makespan
errors = validate_schedule(jsp, schedule)
if is_valid(jsp, schedule):
    print(f"Schedule is valid! Total Makespan: {schedule.makespan}")
else:
    print(f"Validation failed with errors: {errors}")
```

---

## 6. Running Tests

To run the complete unit test suite cleanly without path execution issues, always execute `unittest` or `pytest` from the **root directory** of the repository:

```bash
python -m unittest discover
```
or:
```bash
pytest
```