# Job Shop Scheduling (JSP) Solver

A Python framework for the **Job Shop Scheduling Problem**, built for the AI310 / CS361 group project (Project 17).
The goal is to solve JSP instances with three algorithms: **Backtracking Search**, a **Genetic Algorithm (GA)** and a **Memetic Algorithm (MA)**.

This README documents the shared foundation every module builds on: problem representation, constraints, input validation and the benchmark loader.

---

## 1. Problem Description

A set of **jobs** must be processed on a set of **machines**.

- Each job is a strict, ordered sequence of **operations**.
- Each operation runs on one specific machine for a fixed **duration**.
- A **schedule** assigns a start time to every operation.

**Objective:** minimise the **makespan**, i.e. the time at which the last operation finishes.

### Constraints

A schedule is valid only if all of the following hold:

1. **Precedence:** inside a job, operation `k+1` cannot start before operation `k` ends.
2. **Machine capacity:** a machine processes at most one operation at a time.
3. **No preemption:** an operation runs continuously from its start to its end (`end - start` equals its duration).
4. **Completeness:** every operation of the instance is scheduled exactly once (nothing missing, duplicated or extra).

Start times must also be non-negative. Back-to-back operations are allowed (`start == previous end`).

### Example

| Job | Operations as (machine, duration) |
|---|---|
| 0 | (0, 3), (1, 2), (2, 2) |
| 1 | (0, 2), (2, 1), (1, 4) |
| 2 | (1, 4), (2, 3) |

One valid schedule for this instance has a makespan of **12**:

| Machine | Operations as job(op) start-end |
|---|---|
| 0 | job1(0) 0-2, job0(0) 2-5 |
| 1 | job2(0) 0-4, job1(2) 4-8, job0(1) 8-10 |
| 2 | job1(1) 2-3, job2(1) 4-7, job0(2) 10-12 |

---

## 2. Project Structure

```
jsp-solver/
├── Data/
│   └── jobshop1.txt        # benchmark instances (OR-Library format)
├── jsp/
│   ├── __init__.py
│   ├── models.py           # Operation, Job, JSPInstance
│   ├── schedule.py         # ScheduledOperation, Schedule (+ makespan)
│   ├── parser.py           # load_instance(): read a benchmark by name
│   ├── validation.py       # validate_instance(), validate_schedule(), is_valid()
│   └── test_*.py           # unit tests
├── .gitignore
└── README.md
```

**Requirements:** Python 3.9 or newer. No external packages are needed.

---

## 3. Conventions (read this before writing code)

- **All indices start at 0:** `job_id`, machine ids and `op_index`.
- Machine ids are in the range `0 .. n_machines - 1`.
- Times and durations are **integers**.
- `op_index` is the position of the operation inside its job, so `(job_id, op_index)` identifies an operation uniquely.
- Import everything through the package: `from jsp.models import Operation`.

---

## 4. Core Classes

### Problem side (`jsp/models.py`)

| Class | Fields | Members |
|---|---|---|
| `Operation` (frozen) | `machine: int`, `duration: int` | |
| `Job` | `job_id: int`, `operations: list[Operation]` | `n_operations` (property) |
| `JSPInstance` | `name: str`, `n_jobs: int`, `n_machines: int`, `jobs: list[Job]` | `total_operations` (property), `get_operation(job_id, op_index)` |

### Solution side (`jsp/schedule.py`)

| Class | Fields | Members |
|---|---|---|
| `ScheduledOperation` (frozen) | `job_id`, `op_index`, `machine`, `start`, `end` (all `int`) | `duration` (property, `end - start`) |
| `Schedule` | `operations: list[ScheduledOperation]` | `makespan` (property, 0 if empty), `operations_on_machine(m)` (sorted by start), `get(job_id, op_index)` |

`Schedule.get` raises `ValueError` if the operation is not scheduled. `JSPInstance.get_operation` raises `ValueError` for an unknown job.

---

## 5. Functions

| Function | Module | Returns | Description |
|---|---|---|---|
| `load_instance(path, name)` | `jsp.parser` | `JSPInstance` | Loads one benchmark by name (e.g. `"ft06"`). Raises `FileNotFoundError` or `ValueError` (unknown name, malformed data). |
| `validate_instance(instance)` | `jsp.validation` | `list[str]` | Checks the problem itself: machine ids in range, durations > 0. Empty list = valid. |
| `validate_schedule(instance, schedule)` | `jsp.validation` | `list[str]` | Checks a solution against the four constraints. Returns **all** violations, each with a readable message. Empty list = valid. |
| `is_valid(instance, schedule)` | `jsp.validation` | `bool` | Shortcut for `validate_schedule(...) == []`. |

Error messages start with a category: `Instance Error`, `Completeness Error`, `Time Error`, `Data Consistency Error`, `Duration Error`, `Precedence Error`, `Machine Capacity Error`.

---

## 6. Usage

### Load a benchmark and validate it

```python
from pathlib import Path
from jsp.parser import load_instance
from jsp.validation import validate_instance

data_file = Path("Data") / "jobshop1.txt"
instance = load_instance(str(data_file), "ft06")

print(instance.n_jobs, instance.n_machines, instance.total_operations)  # 6 6 36
print(instance.jobs[0].operations[0])  # Operation(machine=2, duration=1)

errors = validate_instance(instance)
print("Instance is valid" if not errors else errors)
```

### Build and validate a schedule

```python
from jsp.models import Operation, Job, JSPInstance
from jsp.schedule import Schedule, ScheduledOperation
from jsp.validation import validate_schedule, is_valid

instance = JSPInstance(
    name="example", n_jobs=3, n_machines=3,
    jobs=[
        Job(0, [Operation(0, 3), Operation(1, 2), Operation(2, 2)]),
        Job(1, [Operation(0, 2), Operation(2, 1), Operation(1, 4)]),
        Job(2, [Operation(1, 4), Operation(2, 3)]),
    ],
)

S = ScheduledOperation  # (job_id, op_index, machine, start, end)
schedule = Schedule([
    S(1, 0, 0, 0, 2), S(0, 0, 0, 2, 5),
    S(2, 0, 1, 0, 4), S(1, 2, 1, 4, 8), S(0, 1, 1, 8, 10),
    S(1, 1, 2, 2, 3), S(2, 1, 2, 4, 7), S(0, 2, 2, 10, 12),
])

print(is_valid(instance, schedule))   # True
print(schedule.makespan)              # 12
print(validate_schedule(instance, schedule))  # []
```

Run these snippets from the repository root.

---

## 7. Benchmark Data

`Data/jobshop1.txt` holds 82 instances. Each one looks like this:

```
 instance ft06
 +++++++++++++++++++++++++++++
 Fisher and Thompson 6x6 instance, alternate name (mt06)
 6 6                      <- number of jobs, number of machines
 2  1  0  3  1  6 ...     <- one line per job: machine duration machine duration ...
```

Instances used in this project (jobs x machines):

| Family | Instances | Size |
|---|---|---|
| `ft` (Fisher & Thompson) | `ft06`, `ft10`, `ft20` | 6x6, 10x10, 20x5 |
| `la` (Lawrence) | `la01`-`la05` / `la06`-`la10` / `la11`-`la15` | 10x5 / 15x5 / 20x5 |
| | `la16`-`la20` / `la21`-`la25` / `la26`-`la30` | 10x10 / 15x10 / 20x10 |
| | `la31`-`la35` / `la36`-`la40` | 30x10 / 15x15 |
| `abz` (Adams, Balas, Zawack) | `abz5`-`abz6` / `abz7`-`abz9` | 10x10 / 20x15 |
| `orb` (Applegate & Cook) | `orb01`-`orb10` | 10x10 |

Instance names are case sensitive and match exactly (`abz5`, not `abz05`; `la01`, not `la1`).

---

## 8. Running the Tests

From the **repository root**:

```bash
python -m unittest discover
```

For verbose output add `-v`. All tests should pass with no `skipped` entries; a skip means the data file was not found.

---

## 9. Project Modules

| Module | Responsibility |
|---|---|
| Problem representation, constraints, input validation, documentation | this foundation (`models`, `schedule`, `parser`, `validation`) |
| Backtracking search + tests | planned |
| GA: chromosomes, initial population, fitness function | planned |
| GA: selection, crossover, mutation, generations | planned |
| Memetic algorithm: local search + tests | planned |
| User interface, visualisation, performance comparison | planned |
