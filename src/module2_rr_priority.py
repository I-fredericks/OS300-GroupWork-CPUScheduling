# Module 2: Round Robin, Priority with aging
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Module 2 algorithms. Same return shape as module 1:

segments:    list of (pid, start, end) timeline pieces
per_process: dict pid -> {"waiting", "turnaround", "response", "completion"}
"""

from collections import deque

from .compare import metrics_from_segments


def round_robin(processes, quantum):
    """Round Robin with a settable time quantum.

    Convention: processes that arrive during a slice enter the ready queue
    before the process whose quantum just expired re-enters it.
    """
    if quantum <= 0:
        raise ValueError("quantum must be > 0")
    procs = sorted(processes, key=lambda p: p.arrival)  # stable on ties
    if not procs:
        return [], {}
    rem = {p.pid: p.burst for p in procs}
    queue = deque()
    pending = procs[:]
    segments = []
    done = set()
    t = procs[0].arrival

    def drain_arrivals():
        # arrivals up to time t join the queue first
        while pending and pending[0].arrival <= t:
            queue.append(pending.pop(0))

    drain_arrivals()
    while len(done) < len(procs):
        if not queue:
            t = pending[0].arrival  # idle gap: nothing ready yet
            drain_arrivals()
            continue
        p = queue.popleft()
        run = min(quantum, rem[p.pid])
        segments.append((p.pid, t, t + run))
        rem[p.pid] -= run
        t += run
        drain_arrivals()  # newcomers first, then the preempted process
        if rem[p.pid] > 0:
            queue.append(p)
        else:
            done.add(p.pid)
    per, _ = metrics_from_segments(processes, segments)
    return segments, per


def priority_aging(processes, aging_interval=1):
    """Non-preemptive priority scheduling with aging.

    A process that has waited w time units gets its priority reduced by
    w // aging_interval (lower value = more urgent), so no process starves:
    old low-priority jobs eventually beat fresh high-priority ones.
    """
    if aging_interval <= 0:
        raise ValueError("aging_interval must be > 0")
    procs = sorted(processes, key=lambda p: p.arrival)  # stable on ties
    if not procs:
        return [], {}
    order_index = {p.pid: i for i, p in enumerate(processes)}
    remaining = procs[:]
    t = procs[0].arrival
    segments = []

    def effective_priority(p):
        waited = max(0, t - p.arrival)
        return p.priority - waited // aging_interval

    while remaining:
        ready = [p for p in remaining if p.arrival <= t]
        if not ready:
            t = min(p.arrival for p in remaining)
            continue
        p = min(
            ready,
            key=lambda q: (effective_priority(q), q.arrival, order_index[q.pid]),
        )
        segments.append((p.pid, t, t + p.burst))
        t += p.burst
        remaining.remove(p)
    per, _ = metrics_from_segments(processes, segments)
    return segments, per
