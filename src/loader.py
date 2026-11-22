# Shared module: input loading
# Owner: split (whole group) — shown in commit history
"""Load process lists from CSV into Process objects.

CSV format: pid,arrival,burst,priority
"""

import csv
from dataclasses import dataclass


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def load_processes(path):
    """Read a CSV file and return a list of Process, sorted by arrival time.

    The sort is stable, so processes that arrive at the same time keep their
    file order (used as a tie-break by every algorithm). Raises ValueError
    with a clear message on malformed input.
    """
    procs = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        required = {"pid", "arrival", "burst", "priority"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
        for line_no, row in enumerate(reader, start=2):
            pid = (row.get("pid") or "").strip()
            if not pid:
                raise ValueError(f"{path}: line {line_no}: pid must be non-empty")
            try:
                arrival = int(row["arrival"])
                burst = int(row["burst"])
                priority = int(row["priority"])
            except (TypeError, ValueError):
                raise ValueError(
                    f"{path}: line {line_no}: arrival, burst, priority must be integers"
                )
            if arrival < 0:
                raise ValueError(f"{path}: line {line_no}: arrival must be >= 0")
            if burst <= 0:
                raise ValueError(f"{path}: line {line_no}: burst must be > 0")
            procs.append(Process(pid, arrival, burst, priority))
    if not procs:
        raise ValueError(f"{path}: no processes found")
    procs.sort(key=lambda p: p.arrival)
    return procs
