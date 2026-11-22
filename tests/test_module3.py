# Module 3 tests
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Unit tests checking hand-worked answers (worked by hand, not by the program).

MLFQ levels=3, quanta=(2,4,8), procs P1(0,5) P2(2,3):
  P1 Q0 0-2 (full quantum -> demoted), P2 arrives -> Q0: P2 2-4 (demoted),
  Q0 empty -> Q1: P1 4-7 (rem 3 < quantum 4, stays), P2 7-8
  waiting 2,3 -> avg 2.5; turnaround 7,6 -> avg 6.5

FCFS on inputs/test1_basic.csv with context-switch cost 1:
  base: P1 0-7, P2 7-11, P3 11-12, P4 12-16
  with cost: P1 0-7, P2 8-12, P3 13-14, P4 15-19; overhead 3
  avg turnaround (7+10+10+14)/4 = 10.25; avg waiting (0+6+9+10)/4 = 6.25
"""

import pytest

from src.loader import load_processes, Process
from src.module1_fcfs_sjf_srtf import fcfs
from src.module3_mlfq_ctx import mlfq, with_context_switch_cost

TEST1 = "inputs/test1_basic.csv"


def test_mlfq_hand_worked_example():
    procs = [Process("P1", 0, 5, 1), Process("P2", 2, 3, 1)]
    segments, per = mlfq(procs, levels=3, quanta=(2, 4, 8))
    assert segments == [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 7), ("P2", 7, 8)]
    assert per["P1"]["waiting"] == 2
    assert per["P2"]["waiting"] == 3
    assert per["P2"]["completion"] == 8


def test_mlfq_demotes_full_quantum_jobs():
    # P1 (burst 4) uses its whole top quantum 2 and is demoted, so the fresh
    # arrival P2 runs before P1 gets the CPU again.
    procs = [Process("P1", 0, 4, 1), Process("P2", 2, 1, 1)]
    segments, _ = mlfq(procs, levels=3, quanta=(2, 4, 8))
    assert segments == [("P1", 0, 2), ("P2", 2, 3), ("P1", 3, 5)]


def test_context_switch_cost_hand_worked():
    procs = load_processes(TEST1)
    base_segments, _ = fcfs(procs)
    new_segments, per, overhead = with_context_switch_cost(
        procs, base_segments, cost=1
    )
    assert new_segments == [
        ("P1", 0, 7), ("P2", 8, 12), ("P3", 13, 14), ("P4", 15, 19)
    ]
    assert overhead == 3
    assert per["P4"]["turnaround"] == 14
    avg_turnaround = sum(m["turnaround"] for m in per.values()) / 4
    assert avg_turnaround == pytest.approx(10.25)


def test_context_switch_cost_zero_is_identity():
    procs = load_processes(TEST1)
    base_segments, base_per = fcfs(procs)
    new_segments, per, overhead = with_context_switch_cost(
        procs, base_segments, cost=0
    )
    assert new_segments == base_segments
    assert per == base_per
    assert overhead == 0


def test_context_switch_cost_increases_every_completion():
    procs = load_processes(TEST1)
    base_segments, base_per = fcfs(procs)
    _, per, _ = with_context_switch_cost(procs, base_segments, cost=2)
    for pid in per:
        assert per[pid]["turnaround"] > base_per[pid]["turnaround"]
