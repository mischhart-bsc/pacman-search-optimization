"""
Unit tests for pathfinding algorithms (MC2).

Run with: python -m pytest tests/test_pathfinding.py
Or:       python tests/test_pathfinding.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from model.algorithms.pathfinding import (
    is_wall,
    get_valid_neighbors,
    manhattan_distance,
    reconstruct_path,
    dijkstra_pathfinding,
    a_star_pathfinding,
)

# find_shortest_path depends on settings.py (pygame), import separately
try:
    from model.algorithms.pathfinding import find_shortest_path
    DISPATCHER_AVAILABLE = True
except ImportError:
    DISPATCHER_AVAILABLE = False


# ==================== Mock Board ====================

class MockBoardDefinition:
    """
    Simple 7x7 test maze:

    W W W W W W W
    W . . . W . W
    W . W . . . W
    W . W W W . W
    W . . . . . W
    W W . W . . W
    W W W W W W W

    W = wall (value 3), . = walkable (value 0)

    Coordinates: board[row][col], i.e. board[y][x]
    """
    def __init__(self):
        W = 3
        _ = 0
        self.board = np.array([
            [W, W, W, W, W, W, W],
            [W, _, _, _, W, _, W],
            [W, _, W, _, _, _, W],
            [W, _, W, W, W, _, W],
            [W, _, _, _, _, _, W],
            [W, W, _, W, _, _, W],
            [W, W, W, W, W, W, W],
        ])


BOARD = MockBoardDefinition()


# ==================== is_wall ====================

def test_is_wall_wall_tile():
    assert is_wall(0, 0, BOARD) == True
    assert is_wall(3, 0, BOARD) == True
    print("✓ test_is_wall_wall_tile passed")


def test_is_wall_walkable_tile():
    assert is_wall(1, 1, BOARD) == False
    assert is_wall(1, 4, BOARD) == False
    print("✓ test_is_wall_walkable_tile passed")


def test_is_wall_out_of_bounds():
    assert is_wall(-1, 0, BOARD) == True
    assert is_wall(0, -1, BOARD) == True
    assert is_wall(100, 0, BOARD) == True
    assert is_wall(0, 100, BOARD) == True
    print("✓ test_is_wall_out_of_bounds passed")


# ==================== get_valid_neighbors ====================

def test_get_valid_neighbors_open_tile():
    # (1,4) is walkable, neighbors: up=(1,3) wall, down=(1,5) wall, left=(0,4) wall, right=(2,4) walkable
    neighbors = get_valid_neighbors((1, 4), BOARD)
    assert (2, 4) in neighbors
    assert (0, 4) not in neighbors  # wall
    print("✓ test_get_valid_neighbors_open_tile passed")


def test_get_valid_neighbors_corner():
    # (1,1): right=(2,1) walkable, down=(1,2) walkable, left=(0,1) wall, up=(1,0) wall
    neighbors = get_valid_neighbors((1, 1), BOARD)
    assert (2, 1) in neighbors
    assert (1, 2) in neighbors
    assert (0, 1) not in neighbors
    assert (1, 0) not in neighbors
    print("✓ test_get_valid_neighbors_corner passed")


def test_get_valid_neighbors_no_out_of_bounds():
    # No neighbor should be outside the board
    for x in range(7):
        for y in range(7):
            for nx, ny in get_valid_neighbors((x, y), BOARD):
                assert 0 <= nx < 7 and 0 <= ny < 7, f"Out of bounds neighbor ({nx},{ny})"
    print("✓ test_get_valid_neighbors_no_out_of_bounds passed")


# ==================== manhattan_distance ====================

def test_manhattan_distance_zero():
    assert manhattan_distance((3, 3), (3, 3)) == 0
    print("✓ test_manhattan_distance_zero passed")


def test_manhattan_distance_basic():
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((1, 1), (4, 5)) == 7
    print("✓ test_manhattan_distance_basic passed")


def test_manhattan_distance_symmetric():
    assert manhattan_distance((2, 5), (7, 1)) == manhattan_distance((7, 1), (2, 5))
    print("✓ test_manhattan_distance_symmetric passed")


# ==================== reconstruct_path ====================

def test_reconstruct_path_direct():
    came_from = {(2, 1): (1, 1), (3, 1): (2, 1)}
    path = reconstruct_path(came_from, (1, 1), (3, 1))
    assert path == [(1, 1), (2, 1), (3, 1)]
    print("✓ test_reconstruct_path_direct passed")


def test_reconstruct_path_single_step():
    came_from = {(2, 1): (1, 1)}
    path = reconstruct_path(came_from, (1, 1), (2, 1))
    assert path[0] == (1, 1)
    assert path[-1] == (2, 1)
    assert len(path) == 2
    print("✓ test_reconstruct_path_single_step passed")


# ==================== dijkstra_pathfinding ====================

def test_dijkstra_simple_path():
    # (1,1) to (1,4): straight down the left corridor
    result = dijkstra_pathfinding((1, 1), (1, 4), BOARD)
    assert result is not None
    distance, path = result
    assert distance == 3
    assert path[0] == (1, 1)
    assert path[-1] == (1, 4)
    print("✓ test_dijkstra_simple_path passed")


def test_dijkstra_path_around_wall():
    # (1,1) to (5,1): must go around the wall at (2,1) col area
    result = dijkstra_pathfinding((1, 1), (5, 1), BOARD)
    assert result is not None
    distance, path = result
    assert path[0] == (1, 1)
    assert path[-1] == (5, 1)
    # Verify path only steps through walkable tiles
    for tile in path:
        assert not is_wall(tile[0], tile[1], BOARD), f"Path goes through wall at {tile}"
    print("✓ test_dijkstra_path_around_wall passed")


def test_dijkstra_start_equals_goal():
    # find_shortest_path catches this, but test the guard
    result = find_shortest_path((1, 1), (1, 1), BOARD)
    assert result is None
    print("✓ test_dijkstra_start_equals_goal passed")


def test_dijkstra_unreachable_goal():
    # Goal is a wall tile – should return None
    result = dijkstra_pathfinding((1, 1), (0, 0), BOARD)
    assert result is None
    print("✓ test_dijkstra_unreachable_goal passed")


def test_dijkstra_path_is_shortest():
    # Verify distance matches actual path length
    result = dijkstra_pathfinding((1, 1), (5, 4), BOARD)
    assert result is not None
    distance, path = result
    assert distance == len(path) - 1, "Distance must equal number of steps in path"
    print("✓ test_dijkstra_path_is_shortest passed")


def test_dijkstra_consecutive_tiles():
    # Each step in path must be exactly 1 tile apart (no jumps)
    result = dijkstra_pathfinding((1, 1), (5, 4), BOARD)
    assert result is not None
    _, path = result
    for i in range(len(path) - 1):
        dx = abs(path[i+1][0] - path[i][0])
        dy = abs(path[i+1][1] - path[i][1])
        assert dx + dy == 1, f"Non-adjacent tiles in path: {path[i]} -> {path[i+1]}"
    print("✓ test_dijkstra_consecutive_tiles passed")


# ==================== a_star_pathfinding ====================

def test_astar_same_distance_as_dijkstra():
    # A* and Dijkstra must find the same shortest distance
    start, goal = (1, 1), (5, 4)
    d_result = dijkstra_pathfinding(start, goal, BOARD)
    a_result = a_star_pathfinding(start, goal, BOARD)
    assert d_result is not None and a_result is not None
    d_dist, _ = d_result
    a_dist, _ = a_result
    assert d_dist == a_dist, f"Dijkstra: {d_dist}, A*: {a_dist}"
    print("✓ test_astar_same_distance_as_dijkstra passed")


def test_astar_path_is_valid():
    result = a_star_pathfinding((1, 1), (5, 4), BOARD)
    assert result is not None
    distance, path = result
    assert path[0] == (1, 1)
    assert path[-1] == (5, 4)
    for tile in path:
        assert not is_wall(tile[0], tile[1], BOARD), f"A* path goes through wall at {tile}"
    print("✓ test_astar_path_is_valid passed")


def test_astar_unreachable_goal():
    result = a_star_pathfinding((1, 1), (0, 0), BOARD)
    assert result is None
    print("✓ test_astar_unreachable_goal passed")


# ==================== find_shortest_path (dispatcher) ====================

def test_dispatcher_returns_result():
    if not DISPATCHER_AVAILABLE:
        print("~ test_dispatcher_returns_result SKIPPED (settings/pygame not available)")
        return
    result = find_shortest_path((1, 1), (5, 4), BOARD)
    assert result is not None
    distance, path = result
    assert distance > 0
    assert len(path) >= 2
    print("✓ test_dispatcher_returns_result passed")


def test_dispatcher_start_equals_goal():
    if not DISPATCHER_AVAILABLE:
        print("~ test_dispatcher_start_equals_goal SKIPPED (settings/pygame not available)")
        return
    result = find_shortest_path((2, 2), (2, 2), BOARD)
    assert result is None
    print("✓ test_dispatcher_start_equals_goal passed")


# ==================== Runner ====================

def run_all_tests():
    tests = [
        test_is_wall_wall_tile,
        test_is_wall_walkable_tile,
        test_is_wall_out_of_bounds,
        test_get_valid_neighbors_open_tile,
        test_get_valid_neighbors_corner,
        test_get_valid_neighbors_no_out_of_bounds,
        test_manhattan_distance_zero,
        test_manhattan_distance_basic,
        test_manhattan_distance_symmetric,
        test_reconstruct_path_direct,
        test_reconstruct_path_single_step,
        test_dijkstra_simple_path,
        test_dijkstra_path_around_wall,
        test_dijkstra_start_equals_goal,
        test_dijkstra_unreachable_goal,
        test_dijkstra_path_is_shortest,
        test_dijkstra_consecutive_tiles,
        test_astar_same_distance_as_dijkstra,
        test_astar_path_is_valid,
        test_astar_unreachable_goal,
        test_dispatcher_returns_result,
        test_dispatcher_start_equals_goal,
    ]

    print("Running Pathfinding Tests...\n")
    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\u2717 {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\u2717 {test.__name__} ERROR: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    import sys
    sys.exit(0 if success else 1)
