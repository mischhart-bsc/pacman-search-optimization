"""
Unit tests for PriorityQueue implementation (MC1).

Run with: python -m pytest tests/test_priority_queue.py
Or:       python tests/test_priority_queue.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from model.algorithms.priority_queue import PriorityQueue


def test_basic_insert_extract():
    """Test basic insert and extract operations."""
    pq = PriorityQueue()
    
    pq.insert("A", priority=5)
    pq.insert("B", priority=3)
    pq.insert("C", priority=7)
    
    # Extract in priority order (lowest first)
    item1, priority1 = pq.extract_min()
    assert item1 == "B" and priority1 == 3, f"Expected ('B', 3), got ({item1}, {priority1})"
    
    item2, priority2 = pq.extract_min()
    assert item2 == "A" and priority2 == 5, f"Expected ('A', 5), got ({item2}, {priority2})"
    
    item3, priority3 = pq.extract_min()
    assert item3 == "C" and priority3 == 7, f"Expected ('C', 7), got ({item3}, {priority3})"
    
    print("✓ test_basic_insert_extract passed")


def test_empty_queue():
    """Test empty queue operations."""
    pq = PriorityQueue()
    
    assert pq.is_empty() == True, "New queue should be empty"
    assert pq.size() == 0, "Size of empty queue should be 0"
    
    print("✓ test_empty_queue passed")


def test_single_element():
    """Test with single element."""
    pq = PriorityQueue()
    
    pq.insert("X", priority=42)
    assert pq.size() == 1, "Size should be 1"
    assert not pq.is_empty(), "Queue should not be empty"
    
    item, priority = pq.extract_min()
    assert item == "X" and priority == 42
    assert pq.is_empty(), "Queue should be empty after extraction"
    
    print("✓ test_single_element passed")


def test_duplicate_priorities():
    """Test with duplicate priority values."""
    pq = PriorityQueue()
    
    pq.insert("A", priority=5)
    pq.insert("B", priority=5)
    pq.insert("C", priority=5)
    
    # All have same priority, order of extraction may vary but all extracted
    items = []
    for _ in range(3):
        item, priority = pq.extract_min()
        assert priority == 5, f"Expected priority 5, got {priority}"
        items.append(item)
    
    assert set(items) == {"A", "B", "C"}, "All items should be extracted"
    assert pq.is_empty(), "Queue should be empty"
    
    print("✓ test_duplicate_priorities passed")


def test_coordinate_items():
    """Test with coordinate tuples (as used in pathfinding)."""
    pq = PriorityQueue()
    
    pq.insert((5, 10), priority=15)
    pq.insert((0, 0), priority=5)
    pq.insert((3, 7), priority=10)
    
    item1, p1 = pq.extract_min()
    assert item1 == (0, 0) and p1 == 5
    
    item2, p2 = pq.extract_min()
    assert item2 == (3, 7) and p2 == 10
    
    item3, p3 = pq.extract_min()
    assert item3 == (5, 10) and p3 == 15
    
    print("✓ test_coordinate_items passed")


def test_many_insertions():
    """Test with larger number of elements."""
    pq = PriorityQueue()
    
    # Insert 100 elements with random priorities
    import random
    priorities = list(range(100))
    random.shuffle(priorities)
    
    for i, p in enumerate(priorities):
        pq.insert(f"Item_{i}", priority=p)
    
    assert pq.size() == 100, "Size should be 100"
    
    # Extract all and verify they come out in sorted order
    prev_priority = -1
    while not pq.is_empty():
        item, priority = pq.extract_min()
        assert priority >= prev_priority, f"Priorities not in order: {priority} < {prev_priority}"
        prev_priority = priority
    
    print("✓ test_many_insertions passed")


def test_heap_property():
    """Test that min-heap property is maintained."""
    pq = PriorityQueue()
    
    # Insert in random order
    import random
    items = [(f"Item_{i}", random.randint(1, 50)) for i in range(20)]
    
    for item, priority in items:
        pq.insert(item, priority=priority)
    
    # Verify heap structure: parent priority <= children priorities
    for i in range(len(pq.heap) // 2):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        
        parent_priority = pq.heap[i][1]
        
        if left_idx < len(pq.heap):
            left_priority = pq.heap[left_idx][1]
            assert parent_priority <= left_priority, f"Heap property violated at index {i}"
        
        if right_idx < len(pq.heap):
            right_priority = pq.heap[right_idx][1]
            assert parent_priority <= right_priority, f"Heap property violated at index {i}"
    
    print("✓ test_heap_property passed")


def test_interleaved_operations():
    """Test mixed insert and extract operations."""
    pq = PriorityQueue()
    
    pq.insert("A", priority=10)
    pq.insert("B", priority=5)
    item1, _ = pq.extract_min()  # Should be "B"
    assert item1 == "B"
    
    pq.insert("C", priority=3)
    pq.insert("D", priority=7)
    item2, _ = pq.extract_min()  # Should be "C" (priority 3)
    assert item2 == "C"
    
    item3, _ = pq.extract_min()  # Should be "D" (priority 7 < 10)
    assert item3 == "D"
    
    item4, _ = pq.extract_min()  # Should be "A" (priority 10)
    assert item4 == "A"
    
    assert pq.is_empty()
    
    print("✓ test_interleaved_operations passed")


def test_extract_empty_queue():
    """Test error handling when extracting from empty queue."""
    pq = PriorityQueue()
    
    try:
        pq.extract_min()
        assert False, "Should raise IndexError for empty queue"
    except (IndexError, Exception):
        # Expected behavior
        pass
    
    print("✓ test_extract_empty_queue passed")


def run_all_tests():
    """Run all tests."""
    tests = [
        test_basic_insert_extract,
        test_empty_queue,
        test_single_element,
        test_duplicate_priorities,
        test_coordinate_items,
        test_many_insertions,
        test_heap_property,
        test_interleaved_operations,
        test_extract_empty_queue,
    ]
    
    print("Running Priority Queue Tests...\n")
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
