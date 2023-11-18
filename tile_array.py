from collections import namedtuple
from tile import Tile

Point = namedtuple('Point', 'x, y')

class Node:
    def __init__(self, coords, data) -> None:
        self.left = None
        self.right = None
        self.coords = coords
        self.data = data


class KDTree:
    def __init__(self) -> None:
        self.root = None

    def get_root(self):
        return self.root

    def kd_tree(self, arr, deph):
        self.root = self._kd_tree(arr, deph)
    
    def _kd_tree(self, arr):
        deph = len(arr)
        if deph == 0:
            return None
        elif deph == 1:
            return Node(arr[0].coords, arr[0].data)
        k = len(arr[0].coords)
        axis = deph % k
        arr = sorted(arr, key = lambda i: i.coords[axis])
        median = arr[(len(arr) - 1) // 2]
        node = Node(arr[median].coords, arr[median].data)
        node.left = self._kd_tree(arr[:median])
        node.right = self._kd_tree(arr[median+1:])

        return node


