from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Dict, List, Tuple, Optional, Set

from dateutil import parser as dtparser


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    duration_min: int
    deadline: datetime
    priority: int
    depends_on: Tuple[str, ...]


@dataclass
class ScheduledBlock:
    task_id: str
    title: str
    start: datetime
    end: datetime


class ValidationError(ValueError):
    pass


class CycleError(ValueError):
    def __init__(self, cycle_path: List[str]):
        super().__init__("Dependency cycle detected: " + " -> ".join(cycle_path))
        self.cycle_path = cycle_path


def _parse_dt(s: str) -> datetime:
    # dateutil will parse ISO strings; we keep naive datetimes here for simplicity
    return dtparser.isoparse(s)


def parse_request(req: dict) -> tuple[datetime, time, time, List[Tuple[datetime, datetime, str]], List[Task]]:
    planning_start = _parse_dt(req["planning_start"])

    ww = req.get("work_window", {})
    ww_start = datetime.strptime(ww.get("start", "18:00"), "%H:%M").time()
    ww_end = datetime.strptime(ww.get("end", "23:00"), "%H:%M").time()

    blocked: List[Tuple[datetime, datetime, str]] = []
    for b in req.get("blocked", []):
        bs = _parse_dt(b["start"])
        be = _parse_dt(b["end"])
        if be <= bs:
            raise ValidationError(f"Blocked interval ends before it starts: {b}")
        blocked.append((bs, be, b.get("label", "blocked")))

    tasks: List[Task] = []
    for t in req.get("tasks", []):
        tasks.append(
            Task(
                id=str(t["id"]).strip(),
                title=str(t.get("title", "")).strip(),
                duration_min=int(t["duration_min"]),
                deadline=_parse_dt(t["deadline"]),
                priority=int(t.get("priority", 3)),
                depends_on=tuple(t.get("depends_on", [])),
            )
        )

    return planning_start, ww_start, ww_end, blocked, tasks


def validate_tasks(tasks: List[Task]) -> Dict[str, Task]:
    if not tasks:
        raise ValidationError("No tasks provided.")

    by_id: Dict[str, Task] = {}
    for t in tasks:
        if not t.id:
            raise ValidationError("Task has empty id.")
        if t.id in by_id:
            raise ValidationError(f"Duplicate task id: {t.id}")
        if t.duration_min <= 0:
            raise ValidationError(f"Task {t.id} has non-positive duration_min.")
        if not t.title:
            raise ValidationError(f"Task {t.id} has empty title.")
        by_id[t.id] = t

    # dependency existence check
    for t in tasks:
        for dep in t.depends_on:
            if dep not in by_id:
                raise ValidationError(f"Task {t.id} depends on missing task id: {dep}")
            if dep == t.id:
                raise ValidationError(f"Task {t.id} depends on itself.")

    return by_id


def detect_cycle(by_id: Dict[str, Task]) -> None:
    # DFS with colors: 0 unvisited, 1 visiting, 2 done
    color: Dict[str, int] = {tid: 0 for tid in by_id}
    parent: Dict[str, Optional[str]] = {tid: None for tid in by_id}

    def dfs(u: str) -> None:
        color[u] = 1
        for v in by_id[u].depends_on:
            if color[v] == 0:
                parent[v] = u
                dfs(v)
            elif color[v] == 1:
                # found back-edge; reconstruct cycle
                cycle = [v]
                cur = u
                while cur is not None and cur != v:
                    cycle.append(cur)
                    cur = parent[cur]
                cycle.append(v)
                cycle.reverse()
                raise CycleError(cycle)
        color[u] = 2

    for tid in by_id:
        if color[tid] == 0:
            dfs(tid)


def topological_order(by_id: Dict[str, Task]) -> List[str]:
    # Kahn's algorithm
    indeg: Dict[str, int] = {tid: 0 for tid in by_id}
    children: Dict[str, List[str]] = {tid: [] for tid in by_id}
    for tid, t in by_id.items():
        for dep in t.depends_on:
            # edge dep -> tid (dep must come before tid)
            children[dep].append(tid)
            indeg[tid] += 1

    ready = [tid for tid, d in indeg.items() if d == 0]

    def sort_key(tid: str):
        t = by_id[tid]
        return (t.deadline, -t.priority, t.id)

    ready.sort(key=sort_key)

    out: List[str] = []
    while ready:
        u = ready.pop(0)
        out.append(u)
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
        ready.sort(key=sort_key)

    if len(out) != len(by_id):
        # should not happen if detect_cycle ran, but keep safe
        raise CycleError(["<cycle>"])
    return out


def _next_work_window_start(dt: datetime, ww_start: time) -> datetime:
    candidate = dt.replace(hour=ww_start.hour, minute=ww_start.minute, second=0, microsecond=0)
    if dt <= candidate:
        return candidate
    # go to next day
    nd = (dt + timedelta(days=1)).date()
    return datetime.combine(nd, ww_start)


def _work_window_end(dt: datetime, ww_end: time) -> datetime:
    return dt.replace(hour=ww_end.hour, minute=ww_end.minute, second=0, microsecond=0)


def _overlap(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return a_start < b_end and b_start < a_end


def _clip_available_segments(
    window_start: datetime,
    window_end: datetime,
    blocked: List[Tuple[datetime, datetime, str]],
) -> List[Tuple[datetime, datetime]]:
    segs = [(window_start, window_end)]
    for bs, be, _label in blocked:
        new_segs: List[Tuple[datetime, datetime]] = []
        for s, e in segs:
            if not _overlap(s, e, bs, be):
                new_segs.append((s, e))
            else:
                if s < bs:
                    new_segs.append((s, min(bs, e)))
                if be < e:
                    new_segs.append((max(be, s), e))
        segs = [(s, e) for s, e in new_segs if e > s]
    segs.sort(key=lambda x: x[0])
    return segs


def schedule(
    planning_start: datetime,
    ww_start: time,
    ww_end: time,
    blocked: List[Tuple[datetime, datetime, str]],
    tasks: List[Task],
) -> Dict[str, object]:
    by_id = validate_tasks(tasks)
    detect_cycle(by_id)
    order = topological_order(by_id)

    scheduled: List[ScheduledBlock] = []
    cursor = planning_start

    for tid in order:
        t = by_id[tid]
        remaining = t.duration_min

        while remaining > 0:
            # ensure we are in a valid work window
            ws = _next_work_window_start(cursor, ww_start)
            we = _work_window_end(ws, ww_end)

            # available segments inside today's window after subtracting blocked
            segments = _clip_available_segments(ws, we, blocked)

            # move cursor to the first segment that is after current cursor
            placed = False
            for seg_start, seg_end in segments:
                start = max(seg_start, cursor)
                if start >= seg_end:
                    continue

                minutes_here = int((seg_end - start).total_seconds() // 60)
                if minutes_here <= 0:
                    continue

                use = min(remaining, minutes_here)
                end = start + timedelta(minutes=use)

                scheduled.append(ScheduledBlock(task_id=t.id, title=t.title, start=start, end=end))
                remaining -= use
                cursor = end
                placed = True
                if remaining == 0:
                    break

            if not placed:
                # no room today; advance cursor to after today's window
                cursor = we + timedelta(minutes=1)

            # deadline check (soft warning; we still schedule but flag it)
            # We check after placement loop in report build.

    # Build report with warnings
    warnings: List[str] = []
    last_end_by_task: Dict[str, datetime] = {}
    for b in scheduled:
        last_end_by_task[b.task_id] = b.end

    for tid in order:
        t = by_id[tid]
        end_time = last_end_by_task.get(tid)
        if end_time and end_time > t.deadline:
            warnings.append(
                f"Task {tid} finishes at {end_time.isoformat()} after its deadline {t.deadline.isoformat()}."
            )

    return {
        "planning_start": planning_start.isoformat(),
        "work_window": {"start": ww_start.strftime("%H:%M"), "end": ww_end.strftime("%H:%M")},
        "task_order": order,
        "schedule": [
            {
                "task_id": b.task_id,
                "title": b.title,
                "start": b.start.isoformat(),
                "end": b.end.isoformat(),
                "minutes": int((b.end - b.start).total_seconds() // 60),
            }
            for b in scheduled
        ],
        "warnings": warnings,
    }
