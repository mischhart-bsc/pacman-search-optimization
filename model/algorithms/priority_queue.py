r"""
Priority Queue Implementation using Binary Min-Heap (MC1).

Example heap structure:
         1
       /   \
      3     2
     / \   / \
    7   5 4   6

Students will implement this data structure from scratch.
*** If 'heapq' is used, points will be deducted from the grade.

Used for efficient pathfinding in the PacMan game (ghost AI) - in MC2.
"""


class PriorityQueue:
    """
    Min-heap based priority queue where lower priority value = higher priority.

    The heap is a binary tree where the root always has the minimum priority value,
        so you always get the "most urgent" item first.

    HEAP PROPERTY EXAMPLE:
    [('A', 1), ('B', 3), ('C', 2), ('D', 7), ('E', 5)]
    Priority 1 (root) < Priority 3 and 2 (children) ✓
    Priority 3 < Priority 7 and 5 (its children) ✓

    Example usage:
        pq = PriorityQueue()
        pq.insert((5, 10), priority=15)  # coordinate with priority
        item, priority = pq.extract_min()  # returns ((5, 10), 15)
    """

    def __init__(self):
        """
        Initialize the priority queue with an empty heap.

        TODO: Student implementation
        Hint: self.heap = []  # Store (item, priority) tuples

        The heap list represents a complete binary tree.
        Example after insertions:
        self.heap = [('low', 1), ('med', 3), ('high', 5)]
        """
        self.heap = []

    def insert(self, item, priority):
        """
        Enqueue: Insert item with given priority into the queue using heap insertion.

        Args:
            item: The item to insert (e.g., coordinate tuple)
            priority: Priority value (lower number = higher priority)

        TODO: Student implementation
        ALGORITHM:
        1. Append (item, priority) tuple to end of heap array
        2. Call _bubble_up() on the last index to restore heap property

        EXAMPLE: Insert (X, priority=2) into heap [(1, A), (5, B), (3, C)]
        Step 1: heap = [(1, A), (5, B), (3, C), (2, X)]  # append
        Step 2: bubble_up from index 3 to restore min-heap property
        Result: [(1, A), (2, X), (3, C), (5, B)]  # 2 bubbled up
        """
        assert isinstance(priority, (int, float)), "Priority must be a number"
        assert priority >= 0, "Priority must be non-negative"
        assert item is not None, "Item cannot be None"

        self.heap.append((item, priority))
        # Get the index of last element
        index = len(self.heap) - 1
        # Call Function for asserting heap structure
        self._bubble_up(index)

    def extract_min(self):
        """
        Dequeue: Remove and return item with minimum priority (root of min-heap).

        Returns:
            tuple: (item, priority)

        Raises:
            IndexError: If queue is empty

        TODO: Student implementation
        ALGORITHM:
        1. Save the root element (index 0) - this has minimum priority
        2. Move the last element to the root position
        3. Remove the last element from heap
        4. Call _bubble_down() from index 0 to restore heap property
        5. Return (item, priority) from saved root

        EXAMPLE: Extract from heap [(1, A), (2, B), (3, C), (5, D)]
        Step 1: Save (1, A)
        Step 2-3: heap = [(5, D), (2, B), (3, C)]  # last moved to root
        Step 4: bubble_down from index 0
        Result: heap = [(2, B), (5, D), (3, C)]  # 5 bubbled down
        Return: (A, 1)
        """
        if self.is_empty():
            raise "Error"
        else:
            root = self.heap[0]
            index = len(self.heap) - 1
            self.heap[0] = self.heap[index]
            self.heap.pop()
            self._bubble_down(0)
            return root

    def is_empty(self):
        """Check if queue is empty."""
        if not self.heap :
            return True
        else:
            return False

    def size(self):
        """Return number of items in queue."""
        return len(self.heap)

    def plot_performance(self, max_n=5000):
        """
        Plot empirical runtime of insert and extract_min as a function
        of heap size n.

        For each heap size n:
        - build a heap of size n
        - measure one insert operation
        - build a heap of size n
        - measure one extract_min operation
        - repeat several trials and average

        This gives a cleaner comparison with the theoretical O(log n) trend.
        """
        import time
        import random
        import math
        import matplotlib.pyplot as plt

        sizes = []
        insert_times = []
        extract_times = []

        trials = 10

        for n in range(100, max_n + 1):

            trial_insert_times = []
            trial_extract_times = []
            
            for _ in range(trials):
                # ---------- Measure insert on heap of size n ----------
                pq_insert = PriorityQueue()

                data_insert = [
                    ((random.randint(0, 100), random.randint(0, 100)),
                    random.randint(0, 1000))
                    for _ in range(n)
                ]
                for item, priority in data_insert:
                    pq_insert.insert(item, priority)

                new_item = (random.randint(0, 100), random.randint(0, 100))
                new_priority = random.randint(0, 1000)

                start = time.perf_counter_ns()
                pq_insert.insert(new_item, new_priority)
                end = time.perf_counter_ns()

                trial_insert_times.append(end - start)

                # ---------- Measure extract_min on heap of size n ----------
                data_extract = [
                    ((random.randint(0, 100), random.randint(0, 100)),
                    random.randint(0, 1000))
                    for _ in range(n)
                ]

                pq_extract = PriorityQueue()
                for item, priority in data_extract:
                    pq_extract.insert(item, priority)

                start = time.perf_counter_ns()
                pq_extract.extract_min()
                end = time.perf_counter_ns()

                trial_extract_times.append(end - start)

            avg_insert = sum(trial_insert_times) / trials
            avg_extract = sum(trial_extract_times) / trials

            sizes.append(n)
            insert_times.append(avg_insert)
            extract_times.append(avg_extract)

        # Theoretical log curves, scaled separately for visual comparison
        log_curve = [math.log(n) for n in sizes]

        scale_insert = insert_times[-1] / log_curve[-1]
        scale_extract = extract_times[-1] / log_curve[-1]

        scaled_log_insert = [scale_insert * x for x in log_curve]
        scaled_log_extract = [scale_extract * x for x in log_curve]

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, insert_times, label="Insert (measured)")
        plt.plot(sizes, extract_times, label="Extract min (measured)")
        plt.plot(sizes, scaled_log_insert, label="Scaled log(n) for insert")
        plt.plot(sizes, scaled_log_extract, label="Scaled log(n) for extract")

        plt.xlabel("Heap size before operation (n)")
        plt.ylabel("Average time per operation (ns)")
        plt.title("Priority Queue Heap Performance")
        plt.legend()
        plt.grid(True)
        plt.show()
        

    # ========== Helper Methods for Heap Operations ==========
    # These methods navigate the binary tree structure

    def _parent_index(self, index):
        """
        Return parent index in the binary heap.

        Example: child at index 4 → parent at 1
        """
        return (index - 1) // 2

    def _left_child_index(self, index):
    
        # Return left child index in the binary heap.
        return 2 * index + 1

    def _right_child_index(self, index):
        
        # Return right child index in the binary heap.
        return 2 * index + 2

    def _swap(self, i, j):
        """
        Swap elements at indices i and j in the heap.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _bubble_up(self, index):
        """
        Move element up the heap to restore min-heap property after insertion.

        EXAMPLE: After inserting priority=1 at end of [(3, A), (5, B), (4, C)]
        Start: [(3, A), (5, B), (4, C), (1, D)]  # index=3
        Result:  [(1, D), (3, A), (4, C), (5, B)]  # heap property restored
        """
        # the parent is at (index - 1) // 2
        # value is extracted by self.heap[index][1]
        while index > 0 and self.heap[index][1] < self.heap[(index - 1) // 2][1]:
            self.heap[index], self.heap[(index - 1) //2] = self.heap[(index - 1) // 2], self.heap[index]
            # moving up to the parent
            index = (index - 1) // 2

    def _bubble_down(self, index):
        """
        Move element down the heap to restore min-heap property after extraction.

        EXAMPLE: After moving last element to root in [(5, D), (2, B), (3, C)]
        Start: index=0, element=5
        Result: [(2, B), (5, D), (3, C)]  # heap property restored
        """
        size = len(self.heap)

        while True:
            left = self._left_child_index(index)
            right = self._right_child_index(index)
            smallest = index

            # compare left child
            if left < size and self.heap[left][1] < self.heap[smallest][1]:
                smallest = left
            
            # compare right child
            if right < size and self.heap[right][1] < self.heap[smallest][1]:
                smallest = right
            
            # if parent is already the smallest, stop
            if smallest == index:
                break

            # swap and continue
            self._swap(index, smallest)
            index = smallest

    # ========== Additional Utility Methods ==========
    
    def peek_min(self):
        """Return item with minimum priority without removing it"""
        if self.is_empty():
            raise IndexError("Priority queue ist empty")
        else:
            return self.heap[0][0]
        
    def decrease_priority(self, item, new_priority):
        """Decrease priority of a given item (if it exists) and restore heap property."""
        # find the item in the heap
        index = -1
        for i, (stored_item, priority) in enumerate(self.heap):
            if stored_item == item:
                index = i
                break

        if index == -1:
            raise ValueError(f"Item {item} not found in queue")
        
        # Update old priority
        old_priority = self.heap[index][1]
        if new_priority >= old_priority:
            raise ValueError("New priority must be lower than current")
        
        self.heap[index] = (item, new_priority)

        # Bubble Up because lower priority
        self._bubble_up(index)


    def plot_performance_batches(self, max_n=5000, step=100, trials=25, batch_size=300):
        """
        Empirical benchmark for insert and extract_min.

        Method:
        - For each heap size n:
            1. Build a random heap of size n
            2. Copy that heap for each trial
            3. Measure a batch of insert operations
            4. Measure a batch of extract_min operations
            5. Repeat for several trials
        - Report median time per operation
        - Also plot time / log2(n) to assess O(log n) behaviour

        Notes:
        - Batch timing reduces measurement noise from Python overhead
        - Median is more robust than mean for noisy timing data
        - Percentile bands show variability across trials
        """
        import time
        import random
        import math
        import statistics
        import matplotlib.pyplot as plt

        sizes = []

        insert_median = []
        extract_median = []

        insert_p25 = []
        insert_p75 = []

        extract_p25 = []
        extract_p75 = []

        insert_norm = []
        extract_norm = []

        insert_norm_p25 = []
        insert_norm_p75 = []

        extract_norm_p25 = []
        extract_norm_p75 = []

        def percentile(sorted_data, p):
            """
            Simple percentile function.
            p should be between 0 and 1.
            """
            if not sorted_data:
                return None
            k = (len(sorted_data) - 1) * p
            f = int(math.floor(k))
            c = int(math.ceil(k))
            if f == c:
                return sorted_data[f]
            return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)

        for n in range(100, max_n + 1, step):
            insert_trial_times = []
            extract_trial_times = []

            # Build one base heap of size n
            base_data = [
                ((random.randint(0, 100), random.randint(0, 100)),
                random.randint(0, 100000))
                for _ in range(n)
            ]

            base_pq = PriorityQueue()
            for item, priority in base_data:
                base_pq.insert(item, priority)

            for _ in range(trials):
                # -------------------------
                # Measure insert batch
                # -------------------------
                pq_insert = PriorityQueue()
                pq_insert.heap = base_pq.heap.copy()

                insert_batch = [
                    ((random.randint(0, 100), random.randint(0, 100)),
                    random.randint(0, 100000))
                    for _ in range(batch_size)
                ]

                start = time.perf_counter_ns()
                for item, priority in insert_batch:
                    pq_insert.insert(item, priority)
                end = time.perf_counter_ns()

                avg_insert_time = (end - start) / batch_size
                insert_trial_times.append(avg_insert_time)

                # -------------------------
                # Measure extract batch
                # -------------------------
                pq_extract = PriorityQueue()
                pq_extract.heap = base_pq.heap.copy()

                # Do not extract more than available
                extract_ops = min(batch_size, len(pq_extract.heap))

                start = time.perf_counter_ns()
                for _ in range(extract_ops):
                    pq_extract.extract_min()
                end = time.perf_counter_ns()

                avg_extract_time = (end - start) / extract_ops
                extract_trial_times.append(avg_extract_time)

            # Sort trial data for percentile calculation
            insert_trial_times.sort()
            extract_trial_times.sort()

            ins_med = statistics.median(insert_trial_times)
            ext_med = statistics.median(extract_trial_times)

            ins_p25 = percentile(insert_trial_times, 0.25)
            ins_p75 = percentile(insert_trial_times, 0.75)

            ext_p25 = percentile(extract_trial_times, 0.25)
            ext_p75 = percentile(extract_trial_times, 0.75)

            logn = math.log2(n)

            sizes.append(n)

            insert_median.append(ins_med)
            extract_median.append(ext_med)

            insert_p25.append(ins_p25)
            insert_p75.append(ins_p75)

            extract_p25.append(ext_p25)
            extract_p75.append(ext_p75)

            insert_norm.append(ins_med / logn)
            extract_norm.append(ext_med / logn)

            insert_norm_p25.append(ins_p25 / logn)
            insert_norm_p75.append(ins_p75 / logn)

            extract_norm_p25.append(ext_p25 / logn)
            extract_norm_p75.append(ext_p75 / logn)

        # ==========================================
        # Plot 1: raw median runtime per operation
        # ==========================================
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, insert_median, label="Insert median time/op")
        plt.plot(sizes, extract_median, label="Extract_min median time/op")

        plt.fill_between(sizes, insert_p25, insert_p75, alpha=0.2)
        plt.fill_between(sizes, extract_p25, extract_p75, alpha=0.2)

        plt.xlabel("Heap size n")
        plt.ylabel("Time per operation (ns)")
        plt.title("Priority Queue Performance: Raw Runtime")
        plt.legend()
        plt.grid(True)
        plt.show()

        # ==========================================
        # Plot 2: runtime normalised by log2(n)
        # ==========================================
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, insert_norm, label="Insert / log2(n)")
        plt.plot(sizes, extract_norm, label="Extract_min / log2(n)")

        plt.fill_between(sizes, insert_norm_p25, insert_norm_p75, alpha=0.2)
        plt.fill_between(sizes, extract_norm_p25, extract_norm_p75, alpha=0.2)

        plt.xlabel("Heap size n")
        plt.ylabel("Time per operation divided by log2(n)")
        plt.title("Priority Queue Performance: Normalised by log2(n)")
        plt.legend()
        plt.grid(True)
        plt.show()