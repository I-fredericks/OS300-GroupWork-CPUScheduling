# Module 2: Round Robin, Priority with aging
# Module owner: TODO — Member 2 (name + GitHub username)
"""Module 2 algorithms. Same return shape as module 1:

segments:    list of (pid, start, end) timeline pieces
per_process: dict pid -> {"waiting", "turnaround", "response"}
"""


def round_robin(processes, quantum):
    """Round Robin with a settable time quantum (ready queue, quantum slices).

    TODO: implement. The quantum must be changeable at runtime for the live demo.
    """
    raise NotImplementedError


def priority_aging(processes, aging_interval=1):
    """Priority scheduling with aging: waiting processes gain priority every
    aging_interval so no process starves.

    TODO: implement.
    """
    raise NotImplementedError
