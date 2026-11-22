# Shared module: comparison table and metrics
# Owner: split (whole group) — shown in commit history
"""Compute standard metrics from a timeline and print one comparison table.

Metrics for CPU scheduling: average waiting time, average turnaround time,
average response time, and makespan (total completion time).
"""


def merge_segments(segments):
    """Merge adjacent timeline pieces of the same process, e.g. RR slices that
    follow each other directly. Returns a new list of (pid, start, end)."""
    merged = []
    for pid, start, end in segments:
        if merged and merged[-1][0] == pid and merged[-1][2] == start:
            merged[-1] = (pid, merged[-1][1], end)
        else:
            merged.append((pid, start, end))
    return merged


def metrics_from_segments(processes, segments):
    """Derive per-process and average metrics from a timeline.

    processes: list of loader.Process (the input definition)
    segments:  list of (pid, start, end)

    waiting    = turnaround - burst
    turnaround = completion - arrival
    response   = first dispatch - arrival

    Returns (per_process, averages) where per_process maps pid -> dict of the
    metrics above plus "completion", and averages has "waiting", "turnaround",
    "response" and "makespan". Raises ValueError if the timeline does not run
    every process for exactly its burst time.
    """
    pmap = {p.pid: p for p in processes}
    merged = merge_segments(segments)
    per = {}
    for pid, p in pmap.items():
        runs = [(s, e) for spid, s, e in merged if spid == pid]
        if not runs:
            raise ValueError(f"{pid}: never scheduled")
        ran = sum(e - s for s, e in runs)
        if ran != p.burst:
            raise ValueError(f"{pid}: timeline covers {ran} of burst {p.burst}")
        completion = max(e for _, e in runs)
        turnaround = completion - p.arrival
        per[pid] = {
            "completion": completion,
            "turnaround": turnaround,
            "waiting": turnaround - p.burst,
            "response": min(s for s, _ in runs) - p.arrival,
        }
    n = len(per)
    averages = {
        "waiting": sum(m["waiting"] for m in per.values()) / n,
        "turnaround": sum(m["turnaround"] for m in per.values()) / n,
        "response": sum(m["response"] for m in per.values()) / n,
        "makespan": max(m["completion"] for m in per.values()) - min(
            p.arrival for p in processes
        ),
    }
    return per, averages


def print_timeline(name, segments):
    """Print the step-by-step timeline of one algorithm."""
    print(f"\n{name} Gantt timeline:")
    for pid, start, end in merge_segments(segments):
        print(f"  {start:>4} -> {end:<4} {pid}")


def print_comparison_table(results):
    """Print all results in one table, sorted by average waiting time.

    results: list of dicts with keys "name", "per", "avg" (from metrics_from_segments).
    """
    ordered = sorted(results, key=lambda r: r["avg"]["waiting"])
    header = f"{'Algorithm':<38}{'Avg wait':>10}{'Avg turnaround':>16}{'Avg response':>14}{'Makespan':>10}"
    print("\n" + "=" * len(header))
    print("COMPARISON TABLE (sorted by average waiting time)")
    print(header)
    print("-" * len(header))
    for r in ordered:
        a = r["avg"]
        print(
            f"{r['name']:<38}{a['waiting']:>10.2f}{a['turnaround']:>16.2f}"
            f"{a['response']:>14.2f}{a['makespan']:>10.0f}"
        )
    print("=" * len(header))
