# Shared module: visual display
# Owner: split (whole group) — shown in commit history
"""Charts for the simulator (matplotlib).

- Gantt chart per algorithm (one bar per (pid, start, end) segment)
- Bar chart comparing metrics across algorithms
- Step-by-step animated mode for the live demo (parameter change on camera)
"""

import matplotlib.pyplot as plt


def plot_gantt(segments, title="Gantt chart"):
    """Draw a Gantt chart from a list of (pid, start, end) segments."""
    fig, ax = plt.subplots()
    for pid, start, end in segments:
        ax.barh(pid, end - start, left=start)
    ax.set_xlabel("time")
    ax.set_title(title)
    plt.show()
