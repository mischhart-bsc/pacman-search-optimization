"""Compare Dijkstra and A* on the real Pacman maze.

Run from the repository root:
    python benchmarks/search_comparison.py

Prints the average work over 300 random tile pairs and writes
docs/search_comparison.png (one example route, searched tiles highlighted).
"""
import os
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from model.algorithms import pathfinding as pf
from model.algorithms.priority_queue import PriorityQueue
from model.board_definition import BoardDefinition
from settings import BOARD

board = BoardDefinition(BOARD.copy())
rows, cols = board.board.shape
walkable = [(x, y) for y in range(rows) for x in range(cols) if not pf.is_wall(x, y, board)]

# Count how many tiles each search takes out of the priority queue.
popped = []
_original_extract_min = PriorityQueue.extract_min


def recording_extract_min(self):
    result = _original_extract_min(self)
    popped.append(result[0])
    return result


PriorityQueue.extract_min = recording_extract_min

ALGORITHMS = {"Dijkstra": pf.dijkstra_pathfinding, "A* (Manhattan heuristic)": pf.a_star_pathfinding}

# ---- average over random start/goal pairs ----
random.seed(7)
pairs = []
while len(pairs) < 300:
    a, b = random.sample(walkable, 2)
    if pf.dijkstra_pathfinding(a, b, board, 300):
        pairs.append((a, b))

lengths = {}
print(f"{len(walkable)} walkable tiles, {len(pairs)} random start/goal pairs")
for name, fn in ALGORITHMS.items():
    searched, micros, lengths[name] = [], [], []
    for a, b in pairs:
        popped.clear()
        start = time.perf_counter_ns()
        distance, _ = fn(a, b, board, 300)
        micros.append((time.perf_counter_ns() - start) / 1000)
        searched.append(len(popped))
        lengths[name].append(distance)
    print(f"{name:<26} tiles searched: {statistics.mean(searched):6.1f}   time: {statistics.mean(micros):7.1f} µs")
names = list(ALGORITHMS)
print("same path length on every pair:", lengths[names[0]] == lengths[names[1]])

# ---- one example route ----
START, GOAL = (14, 12), (26, 30)  # ghost house exit -> bottom right corner
wall = np.array([[pf.is_wall(x, y, board) for x in range(cols)] for y in range(rows)])
fig, axes = plt.subplots(1, 2, figsize=(11, 6.2))
for ax, (name, fn) in zip(axes, ALGORITHMS.items()):
    popped.clear()
    distance, path = fn(START, GOAL, board, 300)
    searched = set(popped)
    image = np.ones((rows, cols, 3)) * 0.98
    image[wall] = (0.17, 0.2, 0.45)
    for x, y in searched:
        image[y, x] = (0.99, 0.85, 0.55)
    ax.imshow(image, interpolation="nearest")
    ax.plot([p[0] for p in path], [p[1] for p in path], color="#D55E00", lw=2.5)
    ax.scatter(*START, s=90, color="#009E73", zorder=3, label="start (ghost house exit)")
    ax.scatter(*GOAL, s=90, color="#CC79A7", marker="X", zorder=3, label="goal")
    ax.set_title(f"{name}\n{len(searched)} tiles searched, path length {distance}", fontsize=11)
    ax.set_xticks([])
    ax.set_yticks([])
handles, labels = axes[0].get_legend_handles_labels()
handles += [Patch(color=(0.99, 0.85, 0.55)), Patch(color=(0.17, 0.2, 0.45))]
labels += ["searched", "wall"]
axes[0].legend(handles, labels, loc="lower left", fontsize=8, frameon=True)
fig.suptitle("Both algorithms find the same shortest path, A* searches far fewer tiles", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])

out = ROOT / "docs" / "search_comparison.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=130)
print("saved", out)
