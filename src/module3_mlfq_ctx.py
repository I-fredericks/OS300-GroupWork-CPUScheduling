# Module 3: MLFQ and context-switch cost
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Module 3: multi-level feedback queue and context-switch overhead.

mlfq returns (segments, per_process) like modules 1 and 2.
with_context_switch_cost returns (segments, per_process, total_overhead).
"""

from collections import deque

from .compare import metrics_from_segments


def mlfq(processes, levels=3, quanta=(2, 4, 8)):
    """Multi-level feedback queue.

    New arrivals enter the top queue. A process that uses its whole quantum is
    demoted one level; lower levels get bigger quanta. The bottom level uses
    the last quantum and never demotes further. Arrivals during a slice join
    their queue before the preempted process re-enters its (next) queue.
    """
    if levels <= 0:
        raise ValueError("levels must be > 0")
    if len(quanta) < levels:
        raise ValueError("need one quantum per level")
    if any(q <= 0 for q in quanta[:levels]):
        raise ValueError("quanta must be > 0")

    procs = sorted(processes, key=lambda p: p.arrival)  # stable on ties
    if not procs:
        return [], {}
    queues = [deque() for _ in range(levels)]
    rem = {p.pid: p.burst for p in procs}
    pending = procs[:]
    segments = []
    done = set()
    t = procs[0].arrival

    def drain_arrivals():
        while pending and pending[0].arrival <= t:
            queues[0].append(pending.pop(0))

    drain_arrivals()
    while len(done) < len(procs):
        level = next((i for i, q in enumerate(queues) if q), None)
        if level is None:
            t = pending[0].arrival  # idle gap: nothing ready yet
            drain_arrivals()
            continue
        p = queues[level].popleft()
        run = min(quanta[level], rem[p.pid])
        segments.append((p.pid, t, t + run))
        rem[p.pid] -= run
        t += run
        drain_arrivals()
        if rem[p.pid] > 0:
            queues[min(level + 1, levels - 1)].append(p)  # demote (bottom stays)
        else:
            done.add(p.pid)
    per, _ = metrics_from_segments(processes, segments)
    return segments, per


def with_context_switch_cost(processes, segments, cost):
    """Rebuild a timeline so every dispatch of a different process costs
    `cost` extra time units, then recompute metrics.

    Returns (segments, per_process, total_overhead): the new timeline (idle
    switch gaps show up as jumps between a segment's end and the next start),
    the recomputed per-process metrics, and the total overhead added.
    """
    if cost < 0:
        raise ValueError("cost must be >= 0")
    new_segments = []
    overhead = 0
    t = None
    prev_pid = None
    for pid, start, end in segments:
        if prev_pid is None:
            t = start
        elif pid != prev_pid:
            t += cost
            overhead += cost
        new_segments.append((pid, t, t + (end - start)))
        t += end - start
        prev_pid = pid
    per, _ = metrics_from_segments(processes, new_segments)
    return new_segments, per, overhead
