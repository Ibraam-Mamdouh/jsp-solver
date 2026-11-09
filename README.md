# Job Shop Scheduling (JSP) Framework

## 1. Problem Description
Job Shop Scheduling (JSP) is a classical optimization problem where a set of jobs must be processed on a given set of machines. Each job consists of a strict sequence of operations, and each operation requires a specific machine for a predetermined duration. The primary objective is to find a schedule that minimizes the **makespan** (the total completion time required to finish all jobs).

## 2. Constraints
The framework strictly enforces four core constraints:
1. **Precedence Constraint**: Operations belonging to the same job must be processed in their predefined sequential order (operation $k+1$ cannot start before operation $k$ finishes).
2. **Machine Capacity Constraint**: A machine can process at most one operation at a time (no overlapping operations on the same machine).
3. **No Preemption**: Once an operation starts, it runs continuously until completion.
4. **Completeness Constraint**: Every operation specified in the instance must be scheduled exactly once (no missing, extra, or duplicated operations).

## 3. Core Classes

| Class Name | Description | Key Fields / Attributes |
| :--- | :--- | :--- |
| **Operation** | Represents a single step of a job | `machine` (int), `duration` (int) |
| **Job** | Represents a job composed of sequential operations | `job_id` (int), `operations` (list[Operation]) |
| **JSPInstance** | Represents the entire benchmark problem/factory setup | `name` (str), `n_jobs` (int), `n_machines` (int), `jobs` (list[Job]) |
| **ScheduledOperation** | Represents an operation placed on the timeline | `job_id` (int), `op_index` (int), `machine` (int), `start` (int), `end` (int) |
| **Schedule** | Represents a complete solution timeline for all jobs | `operations` (list[ScheduledOperation]) |

## 4. Usage Examples

### Loading an Instance and Validating It
```python
from parser import load_instance
from validation import validate_instance

# Load benchmark instance 'ft06' from the data file
jsp = load_instance("Data/jobshop1.txt", "ft06")

# Validate structural integrity
errors = validate_instance(jsp)
if not errors:
    print("Instance is valid!")