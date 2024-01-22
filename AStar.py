import heapq
''''''
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Astar():
    """A class for A* Pathfinding algorithm"""

    def __init__(self, maze=None, start=None, end=None):
        self.maze = maze
        self.start = start
        self.end = end
    
    def set_endpoints(self, start, end):
        self.start = start
        self.end = end

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

                    if not any(
                            node.x == neighbor.x and node.y == neighbor.y for
                            node in open_set):
                        heapq.heappush(open_set, neighbor)

            return None

        def get_neighbors(node, maze):
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x2, y2 = node.x + dx, node.y + dy
                if 0 <= x2 < len(maze) and 0 <= y2 < len(maze[0]) and maze[x2][
                    y2] == 0:
                    neighbors.append(Node(x2, y2))
            return neighbors

        def reconstruct_path(node):
            path = []
            while node is not None:
                path.append((node.x, node.y))
                node = node.parent
            return path[::-1]

    def astar(self):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, self.start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.end)
        end_node.g = end_node.h = end_node.f = 0
        print("astar1")
        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:
            print("--------------------")
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            min_node = current_node
            min_index = current_index
            for index, item in enumerate(open_list):
                if item.f < min_node.f:
                    min_node = item
                    min_index = index
            current_node = min_node
            current_index = min_index

            # Pop current off open list, add to closed list
            print("poped:", open_list.pop(current_index).position)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                path = path[:-1] #we don't need the starting position
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.maze) - 1) or node_position[0] < 0 or node_position[1] > (len(self.maze[len(self.maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h


                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue
                open_list.append(child)
                print(child.position)

                # Add the child to the open list

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = Astar(maze, start, end).astar()
    print(path)


if __name__ == '__main__':
    main()