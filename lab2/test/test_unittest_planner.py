import os
import sys
import unittest
from datetime import datetime

# --- Make lab2 importable when running unittest from repo root ---
THIS_DIR = os.path.dirname(__file__)
LAB2_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))          # .../lab2
if LAB2_ROOT not in sys.path:
    sys.path.insert(0, LAB2_ROOT)

from src.planner import (  # noqa: E402
    parse_request,
    schedule,
    validate_tasks,
    detect_cycle,
    topological_order,
    Task,
    ValidationError,
    CycleError,
)

def dt(s: str) -> datetime:
    return datetime.fromisoformat(s)


class TestPlanner(unittest.TestCase):

    def test_validate_rejects_duplicate_ids(self):
        tasks = [
            Task("a", "A", 10, dt("2026-02-14T21:00:00"), 3, ()),
            Task("a", "A2", 15, dt("2026-02-14T22:00:00"), 3, ()),
        ]
        with self.assertRaises(ValidationError) as ctx:
            validate_tasks(tasks)
        self.assertIn("Duplicate task id", str(ctx.exception))

    def test_cycle_detection_raises(self):
        tasks = [
            Task("a", "A", 10, dt("2026-02-14T21:00:00"), 3, ("b",)),
            Task("b", "B", 10, dt("2026-02-14T21:00:00"), 3, ("a",)),
        ]
        by_id = validate_tasks(tasks)
        with self.assertRaises(CycleError):
            detect_cycle(by_id)

    def test_topological_order_dependency(self):
        tasks = [
            Task("root", "Root", 10, dt("2026-02-14T21:00:00"), 3, ()),
            Task("child", "Child", 10, dt("2026-02-14T22:00:00"), 3, ("root",)),
        ]
        by_id = validate_tasks(tasks)
        detect_cycle(by_id)
        order = topological_order(by_id)
        self.assertLess(order.index("root"), order.index("child"))

    def test_schedule_splits_around_blocked(self):
        req = {
            "planning_start": "2026-02-13T18:00:00",
            "work_window": {"start": "18:00", "end": "20:00"},
            "blocked": [
                {"start": "2026-02-13T18:30:00", "end": "2026-02-13T19:30:00", "label": "block"}
            ],
            "tasks": [
                {"id": "x", "title": "Big task", "duration_min": 50, "deadline": "2026-02-13T23:00:00", "priority": 3, "depends_on": []}
            ]
        }
        planning_start, ww_start, ww_end, blocked, tasks = parse_request(req)
        report = schedule(planning_start, ww_start, ww_end, blocked, tasks)

        blocks = report["schedule"]
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]["start"], "2026-02-13T18:00:00")
        self.assertEqual(blocks[0]["end"], "2026-02-13T18:30:00")
        self.assertEqual(blocks[1]["start"], "2026-02-13T19:30:00")
        self.assertEqual(blocks[1]["end"], "2026-02-13T19:50:00")


if __name__ == "__main__":
    unittest.main()
