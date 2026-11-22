# Shared: CLI entry point
# Owner: split (whole group) — shown in commit history
"""Run every algorithm on one input file and show chart + comparison table.

Usage: python3 -m src.main inputs/test1_basic.csv [--quantum N] [--levels N] [--cs-cost N]
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="CPU scheduling simulator")
    parser.add_argument("input", help="CSV process list")
    parser.add_argument("--quantum", type=int, default=2, help="RR time quantum")
    parser.add_argument("--levels", type=int, default=3, help="MLFQ levels")
    parser.add_argument("--cs-cost", type=int, default=0, help="context-switch cost")
    args = parser.parse_args()
    # TODO: load input, run all algorithms, print step-by-step timeline,
    # print comparison table, and open the matplotlib charts.


if __name__ == "__main__":
    main()
