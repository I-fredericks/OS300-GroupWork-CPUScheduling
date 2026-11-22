# Shared: CLI entry point
# Owner: split (whole group) — shown in commit history
"""Run every algorithm on one input file, print step-by-step timelines and the
comparison table, and show the charts. Parameters can be changed while running.

Usage: python3 -m src.main inputs/test1_basic.csv [--quantum N] [--levels N]
                  [--quanta Q1,Q2,...] [--cs-cost N] [--no-charts] [--batch]
"""

import argparse
import copy
import sys

from .compare import metrics_from_segments, print_timeline, print_comparison_table
from .loader import load_processes
from .module1_fcfs_sjf_srtf import fcfs, sjf, srtf
from .module2_rr_priority import round_robin, priority_aging
from .module3_mlfq_ctx import mlfq, with_context_switch_cost


def run_all(processes, quantum, levels, quanta, cs_cost):
    """Run every algorithm on the same input and collect results."""
    results = []

    def add(name, segments):
        per, avg = metrics_from_segments(processes, segments)
        results.append({"name": name, "segments": segments, "per": per, "avg": avg})

    segments, _ = fcfs(processes)
    add("FCFS", segments)
    segments, _ = sjf(processes)
    add("SJF (non-preemptive)", segments)
    segments, _ = srtf(processes)
    add("SRTF", segments)
    segments, _ = round_robin(processes, quantum)
    add(f"RR (q={quantum})", segments)
    segments, _ = priority_aging(processes)
    add("Priority + aging", segments)
    segments, _ = mlfq(processes, levels=levels, quanta=quanta)
    add(f"MLFQ ({levels} levels, q={list(quanta[:levels])})", segments)

    if cs_cost > 0:
        costed = []
        for r in list(results):
            cs_segments, per, overhead = with_context_switch_cost(
                processes, r["segments"], cs_cost
            )
            costed.append(
                {
                    "name": f"{r['name']} +CS({cs_cost})",
                    "segments": cs_segments,
                    "per": per,
                    "avg": metrics_from_segments(processes, cs_segments)[1],
                }
            )
            print(f"[{r['name']}] context-switch overhead added: {overhead}")
        results.extend(costed)
    return results


def parse_quanta(text, levels):
    quanta = tuple(int(x) for x in text.split(","))
    if any(q <= 0 for q in quanta) or len(quanta) < levels:
        raise ValueError("need positive quanta, one per level")
    return quanta


def main():
    parser = argparse.ArgumentParser(description="CPU scheduling simulator")
    parser.add_argument("input", help="CSV process list")
    parser.add_argument("--quantum", type=int, default=2, help="RR time quantum")
    parser.add_argument("--levels", type=int, default=3, help="MLFQ levels")
    parser.add_argument(
        "--quanta", default="2,4,8", help="MLFQ quanta per level, comma separated"
    )
    parser.add_argument("--cs-cost", type=int, default=0, help="context-switch cost")
    parser.add_argument("--no-charts", action="store_true", help="skip matplotlib")
    parser.add_argument(
        "--batch", action="store_true", help="no interactive parameter changes"
    )
    args = parser.parse_args()

    quanta = parse_quanta(args.quanta, args.levels)
    processes = load_processes(args.input)
    interactive = not args.batch and sys.stdin.isatty()

    while True:
        results = run_all(processes, args.quantum, args.levels, quanta, args.cs_cost)
        for r in results:
            print_timeline(r["name"], r["segments"])
        print_comparison_table(results)

        if not interactive:
            break
        answer = input(
            "\nChange parameters while running: 'q<N>' quantum, 'c<N>' CS cost, "
            "'m<q1,q2,...>' MLFQ quanta, Enter to show charts and exit: "
        ).strip()
        if not answer:
            break
        try:
            if answer.startswith("q") and answer[1:].isdigit():
                args.quantum = int(answer[1:])
            elif answer.startswith("c") and answer[1:].isdigit():
                args.cs_cost = int(answer[1:])
            elif answer.startswith("m"):
                quanta = parse_quanta(answer[1:], args.levels)
            else:
                print(f"ignored: {answer}")
        except ValueError as exc:
            print(f"bad input: {exc}")

    if not args.no_charts:
        try:
            from .visualize import plot_all_gantts, plot_comparison
        except ImportError:
            print("matplotlib not installed: run pip install -r requirements.txt")
            return
        plot_all_gantts(results)
        plot_comparison(results)


if __name__ == "__main__":
    main()
