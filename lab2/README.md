# Lab 2 — Constraint-Based Study Planner (MLOps)

This lab implements a constraint-based scheduling engine that generates a feasible study plan from structured task input.

Unlike a basic calculator-style lab, this project supports:

- Task dependencies (must complete A before B)
- Cycle detection in dependency graphs
- Scheduling within a daily work window
- Avoiding blocked time intervals (e.g., class, shift, gym)
- Automatic task splitting when blocked time interrupts availability
- Deadline warnings when tasks cannot be completed on time

---

## Project Structure

```
lab2/
│
├── src/
│   ├── planner.py              # Core scheduling engine
│   └── main.py                 # CLI entrypoint
│
├── test/
│   ├── test_pytest_planner.py   # Pytest test suite
│   └── test_unittest_planner.py # Unittest test suite
│
├── data/
│   ├── sample_tasks.json        # Example input
│   └── output_schedule.json     # Generated output (ignored by git)
│
└── requirements.txt
```

---

## Setup Instructions

From the repository root:

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r lab2/requirements.txt
```

---

## 3. Running the Scheduler

From the repository root:

```bash
python lab2/src/main.py
```

The program will:

1. Read input from:

```
lab2/data/sample_tasks.json
```

2. Generate a schedule and write it to:

```
lab2/data/output_schedule.json
```

The output file is automatically ignored in version control since it is generated.

---

## How the Scheduler Works

### 1. Validation

- Ensures task IDs are unique
- Ensures durations are positive
- Verifies dependencies exist
- Detects circular dependencies (cycles)

If a cycle is detected, an error is raised and scheduling stops.

---

### 2. Task Ordering

Tasks are ordered using:

1. Dependency constraints
2. Earliest deadline first
3. Higher priority first (tie-breaker)

This guarantees a valid execution order.

---

### 3. Time Allocation

Scheduling respects:

- `planning_start`
- Daily `work_window`
- `blocked` time intervals

Tasks are placed only in available time slots.

If a blocked interval interrupts a task, it is automatically split across available segments.

---

### 4. Deadline Warnings

If a task finishes after its deadline, the scheduler still completes it but adds a warning in the output report.

---

## Input Format (sample_tasks.json)

Key fields:

```json
{
  "planning_start": "2026-02-13T18:00:00",
  "work_window": { "start": "18:00", "end": "23:00" },
  "blocked": [{ "start": "...", "end": "...", "label": "Gym" }],
  "tasks": [
    {
      "id": "t1",
      "title": "Task name",
      "duration_min": 45,
      "deadline": "2026-02-14T21:00:00",
      "priority": 3,
      "depends_on": []
    }
  ]
}
```

---

## Running Tests

### Pytest

```bash
pytest -q
```

### Unittest

```bash
python -m unittest lab2.test.test_unittest_planner -v
```

Both frameworks test:

- Validation logic
- Cycle detection
- Topological ordering
- Blocked time handling
- Task splitting behavior

---

## Continuous Integration (GitHub Actions)

Two workflows are configured:

- **Lab2 - Pytest**
- **Lab2 - Unittest**

They automatically run on:

- Push to `main`
- Pull requests targeting `main`

The workflows:

- Install dependencies from `lab2/requirements.txt`
- Execute both test suites
- Fail if any test fails

---

## Summary

This lab demonstrates:

- Dependency graph validation
- Cycle detection using DFS
- Topological sorting
- Constraint-based scheduling
- Time window segmentation
- Automated test coverage
- CI integration with GitHub Actions

