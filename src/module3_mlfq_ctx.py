# Module 3: MLFQ and context-switch cost
# Module owner: TODO — Member 3 (name + GitHub username)
"""Module 3 algorithms. Same return shape as modules 1 and 2, plus:

Multi-level feedback queue with per-level quanta; measure how adding a
context-switch cost changes the metrics.
"""


def mlfq(processes, levels=3, quanta=(2, 4, 8)):
    """Multi-level feedback queue: new jobs enter the highest level; a job that
    uses its whole quantum is demoted; lower levels get bigger quanta.

    TODO: implement.
    """
    raise NotImplementedError


def with_context_switch_cost(result_segments, cost):
    """Recompute metrics when every dispatch costs `cost` time units
    (adds idle switch gaps to the timeline and to turnaround/waiting).

    TODO: implement — also show the extra overhead in the comparison table.
    """
    raise NotImplementedError
