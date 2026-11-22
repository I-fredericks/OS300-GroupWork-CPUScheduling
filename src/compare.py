# Shared module: comparison table
# Owner: split (whole group) — shown in commit history
"""Collect metrics from every algorithm and print one comparison table.

Standard metrics for this topic:
  average waiting time, average turnaround time, average response time,
  total completion time, (for module 3: context-switch overhead).
"""


def collect_result(algo_name, segments, per_process):
    """Store one algorithm's result.

    segments: list of (pid, start, end) timeline pieces for the Gantt chart.
    per_process: dict pid -> {"waiting": w, "turnaround": t, "response": r}
    """
    raise NotImplementedError


def print_comparison_table(results):
    """Print all collected results in one table sorted by average waiting time."""
    raise NotImplementedError
