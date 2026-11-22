# Module 1 tests
# Module owner: Ako-Nnubeng Frederick (initial implementation; confirm/adjust in group README)
"""Unit tests checking hand-worked answers (worked by hand, not by the program).

Input inputs/test1_basic.csv: P1[0,7,p3] P2[2,4,p1] P3[4,1,p4] P4[5,4,p2]

FCFS  order P1,P2,P3,P4: runs 0-7, 7-11, 11-12, 12-16
      waiting 0,5,7,7 (avg 4.75); turnaround 7,9,8,11 (avg 8.75)
SJF   at t=7 pick shortest arrived: P3(1); then P2(4) ties P4(4) -> earlier arrival P2
      runs 0-7, 7-8, 8-12, 12-16; avg waiting (0+6+3+7)/4 = 4.0
SRTF  P1 0-2 (P2 arrives, 4<5 preempts), P2 2-4 (P3 arrives, 1<2 preempts),
      P3 4-5, P2 5-7, P4 7-11 (4<5 beats P1), P1 11-16
      avg waiting (9+1+0+2)/4 = 3.0; avg response (0+0+0+2)/4 = 0.5
"""

import pytest

from src.loader import load_processes, Process
from src.module1_fcfs_sjf_srtf import fcfs, sjf, srtf

TEST1 = "inputs/test1_basic.csv"


def test_fcfs_hand_worked_example():
    procs = load_processes(TEST1)
    segments, per = fcfs(procs)
    assert segments == [
        ("P1", 0, 7), ("P2", 7, 11), ("P3", 11, 12), ("P4", 12, 16)
    ]
    assert per["P2"]["waiting"] == 5
    assert per["P4"]["turnaround"] == 11
    assert per["P1"]["response"] == 0
    assert per["P3"]["completion"] == 12


def test_sjf_hand_worked_example():
    procs = load_processes(TEST1)
    segments, per = sjf(procs)
    assert segments == [
        ("P1", 0, 7), ("P3", 7, 8), ("P2", 8, 12), ("P4", 12, 16)
    ]
    assert per["P3"]["waiting"] == 3
    assert per["P2"]["waiting"] == 6


def test_srtf_hand_worked_example():
    procs = load_processes(TEST1)
    segments, per = srtf(procs)
    assert segments == [
        ("P1", 0, 2), ("P2", 2, 4), ("P3", 4, 5),
        ("P2", 5, 7), ("P4", 7, 11), ("P1", 11, 16),
    ]
    assert per["P3"]["waiting"] == 0
    assert per["P1"]["waiting"] == 9
    assert per["P4"]["response"] == 2


def test_fcfs_idle_gap_edge_case():
    # inputs/test3_edge.csv has empty gaps (nothing ready at t=10..12 and t=18..30)
    # P2 waits 0->11 (10), P3 waits 0->12 (11): queued behind P1's burst
    procs = load_processes("inputs/test3_edge.csv")
    segments, per = fcfs(procs)
    assert segments == [
        ("P1", 0, 10), ("P2", 10, 11), ("P3", 11, 12),
        ("P4", 12, 15), ("P5", 15, 18), ("P6", 30, 36),
    ]
    assert per["P6"]["waiting"] == 0
    assert per["P2"]["waiting"] == 10
    assert per["P3"]["waiting"] == 11


def test_srtf_simultaneous_arrivals_tie_break():
    # P1,P2,P3 all arrive at 0 with bursts 10,1,1 -> SJF/SRTF run P2,P3 then P1
    procs = [Process("P1", 0, 10, 5), Process("P2", 0, 1, 5), Process("P3", 0, 1, 5)]
    segments, per = srtf(procs)
    assert segments == [("P2", 0, 1), ("P3", 1, 2), ("P1", 2, 12)]
    assert per["P1"]["waiting"] == 2
