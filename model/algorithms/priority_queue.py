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
    [(1, 'A'), (3, 'B'), (2, 'C'), (7, 'D'), (5, 'E')]
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
        Hint: self.heap = []  # Store (priority, item) tuples

        The heap list represents a complete binary tree.
        Example after insertions:
        self.heap = [(1, 'low'), (5, 'med'), (3, 'high')]
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
        1. Append (priority, item) tuple to end of heap array
        2. Call _bubble_up() on the last index to restore heap property

        EXAMPLE: Insert (X, priority=2) into heap [(1, A), (5, B), (3, C)]
        Step 1: heap = [(1, A), (5, B), (3, C), (2, X)]  # append
        Step 2: bubble_up from index 3 to restore min-heap property
        Result: [(1, A), (2, X), (3, C), (5, B)]  # 2 bubbled up
        """
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

    def plot_performance(self, max_n=1000):
        """
        Plot the time complexity of insert and extract_min operations.

        Creates a graph showing time complexity behavior by:
        1. Testing with increasing input sizes
        2. Measuring time for insert and extract operations
        3. Plotting actual time vs theoretical

        Args:
            max_n: Maximum number of elements to test

        TODO: Student implementation
        Hint: Use time measurements
        Hint: Use matplotlib or a choice of yours for visualization
        Hint: Compare to verify complexity
        """
        import time
        import random
        import math
        import matplotlib.pyplot as plt

        # X-Axis = n Heap Size
        # Y-Axis = time per operation
        insert_times = []
        extract_times = []
        sizes = []

        for n in range(1, max_n):
            pq = PriorityQueue()

            # --- Measure Insert ---
            start = time.perf_counter()

            for _ in range(n):
                item = (random.randint(0,100), random.randint(0,100))
                priority = random.randint(0,1000)
                pq.insert(item,priority)
            
            end = time.perf_counter()
            insert_time = (end - start) / n

            # --- Measure Extract ---
            start = time.perf_counter()

            for _ in range(n):
                pq.extract_min()
            
            end = time.perf_counter()
            extract_time = (end - start) / n

            sizes.append(n)
            insert_times.append(insert_time)
            extract_times.append(extract_time)
        
        # --- Theoretical Curve O(log(n)) ---
        log_curve = [math.log(n) for n in sizes]


        # --- Plot ---
        plt.figure()
        plt.plot(sizes, insert_times, label = "Insert (measured)")
        plt.plot(sizes, extract_times, label = "Extract (measured)")
        plt.plot(sizes, log_curve, label = "O(log n)")

        plt.xlabel("Number of elements (n)")
        plt.ylabel("Time per operation (seconds)")
        plt.title("Heap Operation Time Complexity")

        plt.legend()
        plt.grid()
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

