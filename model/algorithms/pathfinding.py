"""
Pathfinding algorithms for ghost AI navigation (MC2).

Students will implement shortest path algorithms using their PriorityQueue.
"""

from typing import Tuple, List, Optional
from model.algorithms.priority_queue import PriorityQueue
from model.board_structure import BoardStructure


def find_shortest_path(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    board_definition,
    max_search_distance: int = 100,
) -> Optional[int]:
    """
    Find the shortest path distance from start to goal using shortest path algorithm.

    This function is called by ghosts to determine which direction to move
    when chasing the player. It returns the actual path distance so the ghost
    can compare all 4 directions and choose the best one.

    Args:
        start: Current position (tile_x, tile_y) in tile coordinates
        goal: Target position (tile_x, tile_y) in tile coordinates
        board_definition: BoardDefinition object to check for walls
        max_search_distance: Maximum distance to search (prevents infinite loops)

    Returns:
        Path distance (number of steps) from start to goal, or None if no path found

    TODO: Student implementation

    Algorithm suggestion: A*, Dijkstra's algorithm, or Greedy Best-First Search

    Example implementation steps:
    1. Initialize PriorityQueue with start node (priority=0)
    2. Track visited nodes and distance from start
    3. While queue not empty:
       - Extract node with minimum priority
       - If goal reached, return the distance
       - For each valid neighbor:
         * If not visited, add to queue with priority=distance+1
         * Track the distance to reach this neighbor
    4. Return None if no path found

    Hint: Use get_valid_neighbors() to find walkable adjacent tiles
    """
    pass


def get_valid_neighbors(
    position: Tuple[int, int], board_definition
) -> List[Tuple[int, int]]:
    """
    Get all valid (non-wall) neighboring positions.

    Args:
        position: Current tile position (x, y)
        board_definition: BoardDefinition object with board layout

    Returns:
        List of valid neighbor positions [(x, y), ...]

    TODO: Student implementation

    Hint: Check 4 directions (up, down, left, right)
    Hint: Use is_wall() to check if position is walkable
    """
    pass


def is_wall(x: int, y: int, board_definition) -> bool:
    """
    Check if given tile coordinate is a wall.

    Args:
        x: Tile x coordinate
        y: Tile y coordinate
        board_definition: BoardDefinition object

    Returns:
        True if wall, False if walkable

    TODO: Student implementation

    Hint: Check board_definition.board[y][x] against BoardStructure enum values
    Hint: VERTICAL_WALL, HORIZONTAL_WALL, and corner types are walls
    """
    pass


def reconstruct_path(
    came_from: dict, start: Tuple[int, int], goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Reconstruct path from goal to start using parent dictionary.

    Args:
        came_from: Dictionary mapping each node to its parent {node: parent}
        start: Starting position
        goal: Goal position

    Returns:
        Path from start to goal [start, ..., goal]
    """
    pass


# ==================== OPTIONAL: A* Algorithm ====================


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two positions.

    Good heuristic for grid-based pathfinding.

    TODO: Optional to implement, to be used with A* algorithm.
    """
    pass


def a_star_pathfinding(
    start: Tuple[int, int], goal: Tuple[int, int], board_definition
) -> Optional[int]:
    """
    A* pathfinding algorithm:
        Hint: Dijkstra + heuristic for better performance.

    Returns the path distance from start to goal, or None if no path found.

    Priority = g(n) + h(n) where:
    - g(n) = actual cost from start to n
    - h(n) = estimated cost from n to goal (heuristic)

    TODO: Optional to implement, for better performance than Dijkstra's algorithm.

    Hint: Similar to find_shortest_path() but priority = g_score + heuristic
    Hint: Use manhattan_distance() as heuristic function
    Hint: Return g_score[goal] when goal is reached
    """
    pass


# ==================== Integration Helper ====================


def get_next_direction_towards_target(
    current_pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    board_definition,
    tile_width: int,
    tile_height: int,
):
    """
    Helper function to integrate pathfinding with Ghost.follow_target() method.

    Converts pixel coordinates to tile coordinates, finds path, converts back.

    Args:
        current_pos: Current position in pixels (x, y)
        target_pos: Target position in pixels (x, y)
        board_definition: BoardDefinition object
        tile_width: Width of one tile in pixels
        tile_height: Height of one tile in pixels

    Returns:
        Next position in pixels (x, y), or None

    This function bridges the pathfinding algorithm with the existing game code.
    """
    # Convert pixel coordinates to tile coordinates
    start_tile = (current_pos[0] // tile_width, current_pos[1] // tile_height)
    goal_tile = (target_pos[0] // tile_width, target_pos[1] // tile_height)

    # Find next tile using pathfinding
    next_tile = find_shortest_path(start_tile, goal_tile, board_definition)

    if next_tile is None:
        return None

    # Convert back to pixel coordinates
    next_pixel = (next_tile[0] * tile_width, next_tile[1] * tile_height)
    return next_pixel
