# Simple Grid Pathfinder with Uninformed Searches + Dynamic Obstacles
# Requirements: pygame, numpy
# pip install pygame numpy

import pygame
import sys
import random
import time
import collections
import copy
from collections import deque

# ================= CONFIG =================
GRID_SIZE = 15         # 20×20 grid
CELL_SIZE = 15
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

START = (2, 2)
GOAL = (GRID_SIZE-3, GRID_SIZE-3)

# Colors
BLACK   = (0, 0, 0)
WHITE   = (240, 240, 240)
GRAY    = (140, 140, 140)
BLUE    = (60, 120, 255)
GREEN   = (40, 200, 80)
RED     = (220, 60, 60)
YELLOW  = (255, 220, 60)
PURPLE  = (180, 80, 220)
ORANGE  = (255, 140, 40)

# Movement - 8 directions (clockwise starting from UP)
DIRECTIONS = [
    (-1, 0),   # Up
    (0, 1),    # Right
    (1, 0),    # Down
    (1, 1),    # Down-Right
    (0, -1),   # Left
    (-1, -1)   # Up-Left
]


DYNAMIC_OBSTACLE_PROB = 0.015   # ~1.5% chance per step
STEP_DELAY = 0.04               # seconds between visualization steps

# ==========================================

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 80))
pygame.display.set_caption("GOOD PERFORMANCE TIME APP")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

def draw_grid(grid, frontier_set, explored_set, path=None, message=""):
    screen.fill(BLACK)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if grid[r][c] == 1:
                color = GRAY
            elif (r,c) == START:
                color = GREEN
            elif (r,c) == GOAL:
                color = RED
            elif path and (r,c) in path:
                color = YELLOW
            elif (r,c) in frontier_set:
                color = BLUE
            elif (r,c) in explored_set:
                color = PURPLE
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50,50,50), rect, 1)

    # Status bar
    status = font.render(message, True, WHITE)
    screen.blit(status, (10, WINDOW_SIZE + 25))

    pygame.display.flip()


def get_neighbors(r, c, grid):
    nei = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] == 0:
            nei.append((nr, nc))
    return nei


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]


def spawn_dynamic_obstacle(grid):
    empty_cells = [(r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)
                   if grid[r][c] == 0 and (r,c) != START and (r,c) != GOAL]
    if empty_cells and random.random() < DYNAMIC_OBSTACLE_PROB:
        r, c = random.choice(empty_cells)
        grid[r][c] = 1
        return (r, c)
    return None


# ────────────────────────────────────────────────
#                   SEARCH ALGORITHMS
# ────────────────────────────────────────────────

def bfs(start, goal, grid):
    queue = deque([start])
    came_from = {start: None}
    explored = set()

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        explored.add(current)

        new_obs = spawn_dynamic_obstacle(grid)
        draw_grid(grid, set(queue), explored, message=f"BFS  |  Frontier: {len(queue)}  | Explored: {len(explored)}")

        if current == goal:
            return reconstruct_path(came_from, goal)

        for nei in get_neighbors(*current, grid):
            if nei not in came_from:
                queue.append(nei)
                came_from[nei] = current

        time.sleep(STEP_DELAY)

    return None  # no path


def dfs(start, goal, grid):
    stack = [start]
    came_from = {start: None}
    explored = set()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.pop()
        if current in explored:
            continue
        explored.add(current)

        new_obs = spawn_dynamic_obstacle(grid)
        draw_grid(grid, set(stack), explored, message=f"DFS  |  Frontier: {len(stack)}  | Explored: {len(explored)}")

        if current == goal:
            return reconstruct_path(came_from, goal)

        for nei in get_neighbors(*current, grid):
            if nei not in came_from and nei not in explored:
                stack.append(nei)
                came_from[nei] = current

        time.sleep(STEP_DELAY)

    return None


def ucs(start, goal, grid):
    # Since all costs = 1 → same as BFS (but we keep it separate for clarity)
    return bfs(start, goal, grid)


def depth_limited_search(start, goal, grid, limit=30):
    stack = [(start, 0)]  # (pos, depth)
    came_from = {start: None}
    explored = set()

    while stack:
        current, depth = stack.pop()
        if current in explored:
            continue
        explored.add(current)

        draw_grid(grid, {(p,d) for p,d in stack}, explored,
                  message=f"DLS (limit={limit})  |  Frontier: {len(stack)}")

        if current == goal:
            return reconstruct_path(came_from, goal)

        if depth >= limit:
            continue

        for nei in get_neighbors(*current, grid):
            if nei not in came_from:
                stack.append((nei, depth+1))
                came_from[nei] = current

        spawn_dynamic_obstacle(grid)
        time.sleep(STEP_DELAY/1.5)

    return None


def iterative_deepening_dfs(start, goal, grid):
    for limit in range(1, GRID_SIZE*2):
        draw_grid(grid, set(), set(), message=f"IDDFS — depth limit = {limit}")
        time.sleep(0.4)

        path = depth_limited_search(start, goal, grid, limit)
        if path is not None:
            return path

    return None


def bidirectional_search(start, goal, grid):
    front_start = deque([start])
    front_goal  = deque([goal])

    came_from_start = {start: None}
    came_from_goal  = {goal: None}

    explored_s = set()
    explored_g = set()

    while front_start and front_goal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Expand from start
        cur_s = front_start.popleft()
        explored_s.add(cur_s)

        if cur_s in came_from_goal:
            # found connection!
            path_s = reconstruct_path(came_from_start, cur_s)
            path_g = reconstruct_path(came_from_goal, cur_s)
            return path_s[:-1] + path_g[::-1]

        for nei in get_neighbors(*cur_s, grid):
            if nei not in came_from_start:
                front_start.append(nei)
                came_from_start[nei] = cur_s

        # Expand from goal (one step)
        cur_g = front_goal.popleft()
        explored_g.add(cur_g)

        if cur_g in came_from_start:
            path_s = reconstruct_path(came_from_start, cur_g)
            path_g = reconstruct_path(came_from_goal, cur_g)
            return path_s[:-1] + path_g[::-1]

        for nei in get_neighbors(*cur_g, grid):
            if nei not in came_from_goal:
                front_goal.append(nei)
                came_from_goal[nei] = cur_g

        spawn_dynamic_obstacle(grid)
        draw_grid(grid,
                  set(front_start) | set(front_goal),
                  explored_s | explored_g,
                  message=f"Bidirectional  |  Start frontier: {len(front_start)}  Goal frontier: {len(front_goal)}")

        time.sleep(STEP_DELAY)

    return None


# ────────────────────────────────────────────────
#                      MAIN
# ────────────────────────────────────────────────

def main():
    global STEP_DELAY

    # Create grid: 0 = free, 1 = wall
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Some static walls
    for i in range(4, 12):
        grid[8][i] = 1
        grid[i][12] = 1
    for i in range(5, 15):
        grid[i][5] = 1

    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", ucs),
        ("DLS", lambda s,g,gr: depth_limited_search(s,g,gr,18)),
        ("IDDFS", iterative_deepening_dfs),
        ("Bidirectional", bidirectional_search),
    ]

    for name, algo_func in algorithms:
        print(f"\n→ Running {name} ...")
        grid_copy = copy.deepcopy(grid)  # reset dynamic obstacles each time

        path = algo_func(START, GOAL, grid_copy)

        # Show final path longer
        if path:
            for _ in range(5):
                draw_grid(grid_copy, set(), set(), path, f"{name} — FOUND PATH (length: {len(path)})")
                time.sleep(0.6)
        else:
            for _ in range(4):
                draw_grid(grid_copy, set(), set(), None, f"{name} — NO PATH FOUND")
                time.sleep(0.8)

        time.sleep(1.5)

    # Final message
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_grid(grid, set(), set(), None, "GOOD PERFORMANCE TIME APP — All algorithms finished.")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
