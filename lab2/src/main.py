import json
from pathlib import Path

from planner import parse_request, schedule


def load_request(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_output(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote schedule to: {path}")


def main():
    req = load_request("lab2/data/sample_tasks.json")
    planning_start, ww_start, ww_end, blocked, tasks = parse_request(req)
    report = schedule(planning_start, ww_start, ww_end, blocked, tasks)
    write_output("lab2/data/output_schedule.json", report)

    # tiny console summary
    print(f"Planned {len(report['schedule'])} blocks across {len(report['task_order'])} tasks.")
    if report["warnings"]:
        print("Warnings:")
        for w in report["warnings"]:
            print(" -", w)


if __name__ == "__main__":
    main()
