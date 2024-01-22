import heapq

class Node:
    def __init__(self, x, y, g=0, h=0):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star(start, end, maze):
    open_set = []
    closed_set = set()
    start_node = Node(start[0], start[1])
    goal_node = Node(end[0], end[1])
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)
        closed_set.add((current_node.x, current_node.y))

        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            return reconstruct_path(current_node)

        neighbors = get_neighbors(current_node, maze)
        for neighbor in neighbors:
            if (neighbor.x, neighbor.y) in closed_set:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor, goal_node)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current_node

            if not any(node.x == neighbor.x and node.y == neighbor.y for node in open_set):
                heapq.heappush(open_set, neighbor)

    return None

def get_neighbors(node, maze):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2, y2 = node.x + dx, node.y + dy
        if 0 <= x2 < len(maze) and 0 <= y2 < len(maze[0]) and maze[x2][y2] == 0:
            neighbors.append(Node(x2, y2))
    return neighbors

def reconstruct_path(node):
    path = []
    while node is not None:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]

# Przykład użycia
maze = [
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
end = (4, 4)

path = a_star(start, end, maze)
print("Ścieżka:", path)
