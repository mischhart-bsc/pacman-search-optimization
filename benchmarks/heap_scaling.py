"""Measure how the time per heap operation grows with the heap size.

Run from the repository root:
    python benchmarks/heap_scaling.py

Writes docs/heap_performance.png. Each value is the fastest of several repeats
of a batch of operations, which filters out noise from other processes.
"""
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model.algorithms.priority_queue import PriorityQueue

random.seed(3)
SIZES = [2**k for k in range(8, 18)]
BATCH = 1500
REPEATS = 9


def random_entry():
    return (random.randint(0, 99), random.randint(0, 99)), random.randint(0, 10**6)


insert_us, extract_us = [], []
for n in SIZES:
    base = PriorityQueue()
    for _ in range(n):
        base.insert(*random_entry())
    entries = [random_entry() for _ in range(BATCH)]
    extract_batch = min(BATCH, n // 2)

    insert_times, extract_times = [], []
    for _ in range(REPEATS):
        pq = PriorityQueue()
        pq.heap = base.heap.copy()
        start = time.perf_counter_ns()
        for item, priority in entries:
            pq.insert(item, priority)
        insert_times.append((time.perf_counter_ns() - start) / BATCH)

        pq = PriorityQueue()
        pq.heap = base.heap.copy()
        start = time.perf_counter_ns()
        for _ in range(extract_batch):
            pq.extract_min()
        extract_times.append((time.perf_counter_ns() - start) / extract_batch)

    insert_us.append(min(insert_times) / 1000)
    extract_us.append(min(extract_times) / 1000)
    print(f"n={n:>7}  insert {insert_us[-1]:.2f} µs  extract_min {extract_us[-1]:.2f} µs")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(SIZES, extract_us, "o-", label="extract_min", color="#0072B2")
ax.plot(SIZES, insert_us, "s-", label="insert", color="#E69F00")
ax.set_xscale("log", base=2)
ax.set_xlabel("heap size n")
ax.set_ylabel("time per operation (µs)")
ax.set_title(f"Binary min-heap: time per operation (n grows {SIZES[-1] // SIZES[0]}×)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()

out = ROOT / "docs" / "heap_performance.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=130)
print("saved", out)
