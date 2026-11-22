# OS300 Group Project — CPU Scheduling Simulator (Option 1)

Simulator for the OS200 group semester project (Valley View University, Fall 2026).
It reads process lists from CSV files, runs every scheduling algorithm in our
modules on the same input, prints a step-by-step Gantt chart and a comparison
table of metrics, and shows results visually with matplotlib.

**Language:** Python 3.10+
**Option:** 1 — CPU scheduling simulator

## Modules and owners

| Module | Algorithms | Owner (name + GitHub username) |
|--------|------------|-------------------------------|
| Module 1 | FCFS, SJF (non-preemptive), SRTF | TODO: Member 1 |
| Module 2 | Round Robin (settable quantum), Priority with aging | TODO: Member 2 |
| Module 3 | MLFQ, context-switch cost | TODO: Member 3 |
| Shared | Input loading, comparison table, visual display, README | Split (visible in commit history) |

Every member owns one module end to end: its code, its tests, and its part of
the video. The module owner is named at the top of each source file.

## Install

```bash
cd OS300-GroupWork-CPUScheduling
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# Run all algorithms on one input file
python3 -m src.main inputs/test1_basic.csv

# Override parameters while running (quantum, MLFQ levels, context-switch cost)
python3 -m src.main inputs/test2_mixed.csv --quantum 3 --levels 3 --cs-cost 1
```

The interactive mode also lets you change the time quantum, number of frames
parameters, and context-switch cost while running, then rerun.

## Test

```bash
pytest
```

Each module has at least one unit test that checks a hand-worked answer
worked out by hand (not copied from the program).

## Test inputs

| File | Purpose |
|------|---------|
| `inputs/test1_basic.csv` | Normal workloads, staggered arrivals |
| `inputs/test2_mixed.csv` | Mixed burst sizes and priorities |
| `inputs/test3_edge.csv` | Tricky edge case: simultaneous arrivals, 1-unit jobs, idle gap, convoy-effect long burst |

CSV format: `pid,arrival,burst,priority`

## GitHub rules (marking — read this)

- One repository per group named **OS300-GroupWork-CPUScheduling**.
- Every member commits **from their own GitHub account**, with real name and
  student email in `git config`.
- Each member needs **10+ meaningful commits spread over 3+ different weeks**.
- Clear commit messages: `add LRU replacement`, not `update`.
- Use branches and pull requests per module; another member reviews and merges.
- Never `git push --force` on main after the group-list date.

Commit evidence to produce at the end:

```bash
git shortlog -sne                      # screenshot for GroupWork_shortlog.png
git log --all --pretty=format:"%h | %an | %ae | %ad | %s" --date=iso > GroupWork_gitlog.txt
# + screenshot of GitHub Insights -> Contributors (GroupWork_contributors.png)
```

## Deliverables (zip: OS300_GroupWork_CPUScheduling.zip)

- `GroupWork_members.txt` — full name, index number, GitHub username, module owned
- `GroupWork_repo.txt` — repository link + submitted commit hash
- `GroupWork_gitlog.txt` — full git log export
- `GroupWork_contributors.png`, `GroupWork_shortlog.png` — commit evidence
- `GroupWork_report.pdf` — 6–10 pages: design, results tables/charts, comparison, who did what
- `GroupWork_video.mp4` — one unedited 12–18 min recording, all members in frame
