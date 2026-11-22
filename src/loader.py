# Shared module: input loading
# Owner: split (whole group) — shown in commit history
"""Load process lists from CSV into Process objects.

CSV format: pid,arrival,burst,priority
"""

from dataclasses import dataclass


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def load_processes(path):
    """Read a CSV file and return a list of Process, sorted by arrival time.

    TODO: implement. Validate rows (non-negative arrival, burst > 0) and
    raise a clear error message on bad input.
    """
    raise NotImplementedError
