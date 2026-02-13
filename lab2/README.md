# Lab 2 — Constraint-Based Study Planner (MLOps Lab)

This lab implements a mini scheduling engine that takes a list of study/tasks, validates constraints (IDs, durations, dependencies), detects dependency cycles, and produces a feasible time-block schedule.

- Supports **task dependencies** (must do A before B)
- Detects **cycles** and reports them as an error
- Schedules only inside a **daily work window** (example: 18:00–23:00)
- Skips **blocked time** (example: class, shift, gym)
- Can **split a task** into multiple blocks when a blocked interval interrupts the available time

## Project Structure

lab2/
src/
planner.py # scheduling engine + validation + cycle detection
main.py # CLI entrypoint that loads JSON and writes output JSON
test/
test_pytest_planner.py
test_unittest_planner.py
data/
sample_tasks.json # sample input request
requirements.txt

## Setup (from repo root)

### 1 Create + activate virtual environment

python3 -m venv .venv
source .venv/bin/activate

### 2 Install Dependencies

pip install -r lab2/requirements.txt

### Run the Scheduler

From repo root :

python lab2/src/main.py

This reads:

lab2/data/sample_tasks.json

and writes:

lab2/data/output_schedule.json

### Input Format (JSON)

Key fields:

planning_start: ISO datetime when scheduling begins

work_window: daily time window during which work can be scheduled

blocked: list of time intervals to avoid

tasks: each task has id, title, duration_min, deadline, priority, depends_on

See lab2/data/sample_tasks.json for a complete example.

### RUN TESTS

pytest -q

python -m unittest lab2.test.test_unittest_planner -v

### GITHUB Actions (CI)

This repo includes two workflows that run automatically on push / pull request to main:

Lab2 - Pytest

Lab2 - Unittest
They install lab2/requirements.txt and run both test suites in CI.
