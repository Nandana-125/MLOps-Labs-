import json
from pathlib import Path


def load_request(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    req = load_request("lab2/data/sample_tasks.json")
    tasks = req.get("tasks", [])
    print(f"Loaded {len(tasks)} tasks. Planning start: {req.get('planning_start')}")


if __name__ == "__main__":
    main()
