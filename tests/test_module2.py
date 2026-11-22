# Module 2 tests
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Unit tests checking hand-worked answers (worked by hand, not by the program).

RR q=2 on inputs/test1_basic.csv, arrivals-first requeue convention:
  slices: P1 0-2, P2 2-4, P1 4-6, P3 6-7, P2 7-9, P4 9-11, P1 11-13, P4 13-15, P1 15-16
  waiting 9,3,2,6 -> avg 5.0; response 0,0,2,4 -> avg 1.5

RR q=4 on the same input:
  slices: P1 0-4, P2 4-8, P1 8-11, P3 11-12, P4 12-16
  waiting 4,2,7,7 -> avg 5.0 (same); response 0,2,7,7 -> avg 4.0 (worse)

Aging, interval=1, procs P1(0,3,p5) P2(0,4,p1) P3(4,3,p2):
  P2 0-4; at t=4: P1 effective 5-4=1 beats fresh P3 effective 2 -> P1 4-7, P3 7-10
  Without aging P3 (priority 2 < 5) would have run before P1.
"""

import pytest

from src.loader import load_processes, Process
from src.module2_rr_priority import round_robin, priority_aging

TEST1 = "inputs/test1_basic.csv"


def test_round_robin_hand_worked_q2():
    procs = load_processes(TEST1)
    segments, per = round_robin(procs, quantum=2)
    assert segments == [
        ("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 6), ("P3", 6, 7),
        ("P2", 7, 9), ("P4", 9, 11), ("P1", 11, 13), ("P4", 13, 15),
        ("P1", 15, 16),
    ]
    assert per["P1"]["waiting"] == 9
    assert per["P3"]["response"] == 2


def test_round_robin_q4_hand_worked_differs_from_q2():
    procs = load_processes(TEST1)
    segments_q4, per_q4 = round_robin(procs, quantum=4)
    segments_q2, per_q2 = round_robin(procs, quantum=2)
    assert segments_q4 == [
        ("P1", 0, 4), ("P2", 4, 8), ("P1", 8, 11), ("P3", 11, 12),
        ("P4", 12, 16),
    ]
    # same average waiting time (5.0), worse average response time
    assert per_q4["P2"]["response"] == 2
    assert per_q2["P3"]["response"] == 2 and per_q4["P3"]["response"] == 7


def test_priority_aging_beats_fresh_higher_priority():
    procs = [
        Process("P1", 0, 3, 5),
        Process("P2", 0, 4, 1),
        Process("P3", 4, 3, 2),
    ]
    segments, per = priority_aging(procs, aging_interval=1)
    assert segments == [("P2", 0, 4), ("P1", 4, 7), ("P3", 7, 10)]
    assert per["P1"]["waiting"] == 4
    assert per["P3"]["waiting"] == 3


def test_priority_aging_no_starvation():
    # P6 arrives last with the worst priority but must still complete
    procs = load_processes("inputs/test3_edge.csv")
    segments, per = priority_aging(procs, aging_interval=2)
    assert set(per) == {"P1", "P2", "P3", "P4", "P5", "P6"}
    assert per["P6"]["completion"] == 36


def test_round_robin_rejects_bad_quantum():
    procs = load_processes(TEST1)
    with pytest.raises(ValueError):
        round_robin(procs, quantum=0)
