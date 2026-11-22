# Module 1: FCFS, SJF (non-preemptive), SRTF
# Module owner: TODO — Member 1 (name + GitHub username)
"""Module 1 algorithms. Every function returns (segments, per_process):

segments:    list of (pid, start, end) timeline pieces
per_process: dict pid -> {"waiting", "turnaround", "response"}
"""


def fcfs(processes):
    """First-Come First-Served: run in arrival order, no preemption.

    TODO: implement.
    """
    raise NotImplementedError


def sjf(processes):
    """Shortest Job First, non-preemptive: at each dispatch pick the shortest
    burst among arrived processes.

    TODO: implement.
    """
    raise NotImplementedError


def srtf(processes):
    """Shortest Remaining Time First (preemptive SJF): a newly arrived process
    with less remaining time preempts the running one.

    TODO: implement.
    """
    raise NotImplementedError
