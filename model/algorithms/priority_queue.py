r"""
Priority Queue Implementation using Binary Min-Heap (MC1).

Example heap structure:
         1
       /   \
      3     2
     / \   / \
    7   5 4   6

Students will implement this data structure from scratch by using only primitive data structures.
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
        pass

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
        pass

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
        pass

    def is_empty(self):
        """Check if queue is empty."""
        pass

    def size(self):
        """Return number of items in queue."""
        pass

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
        pass

    # ========== Helper Methods for Heap Operations ==========
    # These methods navigate the binary tree structure

    def _parent_index(self, index):
        """
        Return parent index in the binary heap.

        Example: child at index 4 → parent at 1
        """
        pass

    def _left_child_index(self, index):
        """
        Return left child index in the binary heap.

        Example: parent at index 1 → left child at 3
        """
        pass

    def _right_child_index(self, index):
        """
        Return right child index in the binary heap.

        Example: parent at index 1 → right child at 4
        """
        pass

    def _swap(self, i, j):
        """
        Swap elements at indices i and j in the heap.
        """
        pass

    def _bubble_up(self, index):
        """
        Move element up the heap to restore min-heap property after insertion.

        EXAMPLE: After inserting priority=1 at end of [(3, A), (5, B), (4, C)]
        Start: [(3, A), (5, B), (4, C), (1, D)]  # index=3
        Result:  [(1, D), (3, A), (4, C), (5, B)]  # heap property restored
        """
        pass

    def _bubble_down(self, index):
        """
        Move element down the heap to restore min-heap property after extraction.

        EXAMPLE: After moving last element to root in [(5, D), (2, B), (3, C)]
        Start: index=0, element=5
        Result: [(2, B), (5, D), (3, C)]  # heap property restored
        """
        pass
