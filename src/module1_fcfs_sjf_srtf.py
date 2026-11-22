# Module 1: FCFS, SJF (non-preemptive), SRTF
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Module 1 algorithms. Every function returns (segments, per_process):

segments:    list of (pid, start, end) timeline pieces
per_process: dict pid -> {"waiting", "turnaround", "response", "completion"}
"""

from .compare import metrics_from_segments


def fcfs(processes):
    """First-Come First-Served: run in arrival order, no preemption."""
    order = sorted(processes, key=lambda p: p.arrival)  # stable on ties
    t = order[0].arrival if order else 0
    segments = []
    for p in order:
        start = max(t, p.arrival)  # skips idle gaps with no ready process
        segments.append((p.pid, start, start + p.burst))
        t = start + p.burst
    per, _ = metrics_from_segments(processes, segments)
    return segments, per


def sjf(processes):
    """Shortest Job First, non-preemptive: at each dispatch pick the shortest
    burst among the processes that have arrived (ties: earlier arrival, then
    input order)."""
    remaining = sorted(processes, key=lambda p: p.arrival)
    order_index = {p.pid: i for i, p in enumerate(processes)}
    t = remaining[0].arrival if remaining else 0
    segments = []
    while remaining:
        ready = [p for p in remaining if p.arrival <= t]
        if not ready:
            t = min(p.arrival for p in remaining)
            continue
        p = min(ready, key=lambda q: (q.burst, q.arrival, order_index[q.pid]))
        segments.append((p.pid, t, t + p.burst))
        t += p.burst
        remaining.remove(p)
    per, _ = metrics_from_segments(processes, segments)
    return segments, per


def srtf(processes):
    """Shortest Remaining Time First (preemptive SJF): a newly arrived process
    with strictly less remaining time preempts the running one.

    The timeline advances event to event: each run piece ends at the next
    arrival or at the current process's completion, whichever comes first.
    """
    procs = sorted(processes, key=lambda p: p.arrival)
    if not procs:
        return [], {}
    order_index = {p.pid: i for i, p in enumerate(processes)}
    arr_time = {p.pid: p.arrival for p in procs}
    rem = {p.pid: p.burst for p in procs}
    pending = procs[:]  # sorted by arrival; not yet arrived
    arrived = set()
    done = set()
    segments = []
    t = procs[0].arrival

    def rank(pid):
        return (rem[pid], arr_time[pid], order_index[pid])

    cur = None
    while len(done) < len(procs):
        # move every process that has arrived by now into the ready set
        new_pids = []
        while pending and pending[0].arrival <= t:
            pid = pending.pop(0).pid
            arrived.add(pid)
            new_pids.append(pid)
        # a newcomer with strictly less remaining time preempts the running one
        if cur is not None and new_pids:
            best_new = min(new_pids, key=rank)
            if rank(best_new) < rank(cur):
                cur = None  # the running piece already ends exactly at t
        if cur is None:
            ready = [pid for pid in arrived if rem[pid] > 0]
            if not ready:
                t = pending[0].arrival  # idle until the next arrival
                continue
            cur = min(ready, key=rank)
            segments.append((cur, t, t))  # opened; extended below
        next_arrival = pending[0].arrival if pending else float("inf")
        run_end = min(next_arrival, t + rem[cur])
        segments[-1] = (cur, segments[-1][1], run_end)
        rem[cur] -= run_end - t
        t = run_end
        if rem[cur] == 0:
            done.add(cur)
            cur = None
    per, _ = metrics_from_segments(processes, segments)
    return segments, per
