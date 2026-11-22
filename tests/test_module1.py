# Module 1 tests
# Module owner: TODO — Member 1
"""Unit tests checking a hand-worked answer.

Hand-worked FCFS on inputs/test1_basic.csv (P1[0,7], P2[2,4], P3[4,1], P4[5,4]):
  order P1->P2->P3->P4; finishes 7, 11, 12, 16
  waiting   = 0, 5, 7, 7   -> avg 19/4 = 4.75
  turnaround= 7, 9, 8, 11  -> avg 35/4 = 8.75
"""

from src.loader import load_processes
from src.module1_fcfs_sjf_srtf import fcfs


def test_fcfs_hand_worked_example():
    procs = load_processes("inputs/test1_basic.csv")
    segments, per_process = fcfs(procs)
    assert segments == [
        ("P1", 0, 7), ("P2", 7, 11), ("P3", 11, 12), ("P4", 12, 16)
    ]
    assert per_process["P2"]["waiting"] == 5
    assert per_process["P4"]["turnaround"] == 11


def test_sjf_hand_worked_example():
    # TODO (Member 1): work SJF out by hand on test1 or another input and assert it
    raise NotImplementedError


def test_srtf_hand_worked_example():
    # TODO (Member 1): work SRTF out by hand (show a preemption!) and assert it
    raise NotImplementedError
