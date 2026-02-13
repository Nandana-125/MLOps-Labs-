import pytest
from datetime import datetime

from src.planner import (
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
    # helper for readable tests
    return datetime.fromisoformat(s)


def test_validate_rejects_missing_dependency():
    tasks = [
        Task(
            id="a",
            title="A",
            duration_min=30,
            deadline=dt("2026-02-14T21:00:00"),
            priority=3,
            depends_on=("missing",),
        )
    ]
    with pytest.raises(ValidationError) as e:
        validate_tasks(tasks)
    assert "missing task id" in str(e.value)


def test_cycle_detection_reports_path():
    tasks = [
        Task("a", "A", 10, dt("2026-02-14T21:00:00"), 3, ("b",)),
        Task("b", "B", 10, dt("2026-02-14T21:00:00"), 3, ("c",)),
        Task("c", "C", 10, dt("2026-02-14T21:00:00"), 3, ("a",)),
    ]
    by_id = validate_tasks(tasks)
    with pytest.raises(CycleError) as e:
        detect_cycle(by_id)
    # path looks like a -> b -> c -> a (order can vary slightly but should include all)
    msg = str(e.value)
    assert "Dependency cycle detected" in msg
    for node in ["a", "b", "c"]:
        assert node in msg


def test_topological_order_respects_dependencies():
    tasks = [
        Task("t1", "First", 10, dt("2026-02-15T20:00:00"), 3, ()),
        Task("t2", "Second", 10, dt("2026-02-14T20:00:00"), 5, ("t1",)),
        Task("t3", "Third", 10, dt("2026-02-14T19:00:00"), 1, ()),
    ]
    by_id = validate_tasks(tasks)
    detect_cycle(by_id)
    order = topological_order(by_id)
    assert order.index("t1") < order.index("t2")  # dep honored
    assert set(order) == {"t1", "t2", "t3"}


def test_schedule_avoids_blocked_overlap_and_can_split_tasks():
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
    assert len(blocks) == 2, "Should split around blocked time"

    b1, b2 = blocks[0], blocks[1]
    assert b1["start"] == "2026-02-13T18:00:00"
    assert b1["end"] == "2026-02-13T18:30:00"
    assert b2["start"] == "2026-02-13T19:30:00"
    assert b2["end"] == "2026-02-13T19:50:00"

    # Ensure no overlap with blocked interval
    block_s = dt("2026-02-13T18:30:00")
    block_e = dt("2026-02-13T19:30:00")
    for b in blocks:
        s = dt(b["start"])
        e = dt(b["end"])
        assert not (s < block_e and block_s < e), "Scheduled block overlaps a blocked interval"
