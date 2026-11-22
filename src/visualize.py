# Shared module: visual display
# Owner: split (whole group) — shown in commit history
"""Charts for the simulator (matplotlib).

- one figure with a Gantt subplot per algorithm
- bar chart comparing average metrics across algorithms
"""

import matplotlib.pyplot as plt


def plot_gantt(segments, title="Gantt chart"):
    """Draw a single Gantt chart from a list of (pid, start, end) segments."""
    fig, ax = plt.subplots(figsize=(10, 2.5))
    _draw_gantt(ax, segments, title)
    fig.tight_layout()
    plt.show()


def plot_all_gantts(results):
    """One figure, one Gantt subplot per result (from main.run_all)."""
    n = len(results)
    fig, axes = plt.subplots(n, 1, figsize=(11, 2.4 * n), squeeze=False)
    for ax, r in zip(axes[:, 0], results):
        _draw_gantt(ax, r["segments"], r["name"])
    fig.tight_layout()
    plt.show()


def plot_comparison(results):
    """Grouped bar chart: average waiting / turnaround / response per algorithm."""
    ordered = sorted(results, key=lambda r: r["avg"]["waiting"])
    names = [r["name"] for r in ordered]
    metrics = ("waiting", "turnaround", "response")
    width = 0.26
    positions = range(len(names))
    fig, ax = plt.subplots(figsize=(11, 5))
    for i, metric in enumerate(metrics):
        values = [r["avg"][metric] for r in ordered]
        ax.bar([p + i * width for p in positions], values, width, label=metric)
    ax.set_xticks([p + width for p in positions])
    ax.set_xticklabels(names, rotation=20, ha="right")
    ax.set_ylabel("time units")
    ax.set_title("Average metrics per algorithm (sorted by avg waiting)")
    ax.legend()
    fig.tight_layout()
    plt.show()


def _draw_gantt(ax, segments, title):
    colors = {}
    for pid, start, end in segments:
        if pid not in colors:
            colors[pid] = plt.cm.tab20(len(colors) % 20)
        ax.barh(0, end - start, left=start, height=0.6, color=colors[pid])
        ax.text(
            start + (end - start) / 2, 0, pid,
            ha="center", va="center", fontsize=8,
        )
    ax.set_xlabel("time")
    ax.set_yticks([])
    ax.set_ylim(-0.6, 0.6)
    ax.set_title(title)
