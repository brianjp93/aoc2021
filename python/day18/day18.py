from pathlib import Path
from itertools import permutations
from math import ceil
from ast import literal_eval

with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


class Node:
    def __init__(
        self, raw: str | list | int, is_l: bool = False, parent: "Node" = None
    ):
        self.is_l = is_l
        self.parent = parent
        data = raw if isinstance(raw, (list, int)) else literal_eval(raw)
        self.left, self.right, self.val = self.parse(data)

    @property
    def magnitude(self):
        if self.val is not None:
            return self.val
        assert self.left and self.right
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def parse(self, data):
        if isinstance(data, int):
            return None, None, data
        return Node(data[0], True, self), Node(data[1], False, self), None

    def __repr__(self):
        if self.val is not None:
            return str(self.val)
        return f"[{self.left}, {self.right}]"

    def __add__(self, other):
        node = Node(f"[{self}, {other}]", is_l=False)
        node.reduce()
        return node

    def __radd__(self, other):
        return self if other == 0 else self.__add__(other)

    def is_nested(self, depth=4):
        node = self
        if node.val is not None:
            node = node.parent
        for _ in range(depth):
            node = node.parent if node else None
        return bool(node)

    def reduce(self):
        while True:
            found_explode = False
            found_split = False
            for node in self.visit:
                pair = node.pair
                if pair is not None and node.is_nested():
                    assert node.parent
                    found_explode = True
                    node.parent.explode()
                    break
            if found_explode:
                continue

            for node in self.visit:
                if node.val is not None and node.val >= 10:
                    node.split()
                    found_split = True
                    break
            if not found_split and not found_explode:
                break

    def split(self):
        assert self.val is not None and self.val >= 10
        self.left = Node(self.val // 2, is_l=True, parent=self)
        self.right = Node(ceil(self.val / 2), is_l=False, parent=self)
        self.val = None

    def explode(self):
        assert self.left and self.right
        assert self.left.val is not None and self.right.val is not None
        left, _ = self.left.sides
        _, right = self.right.sides
        if left:
            assert left.val is not None
            left.val += self.left.val
        if right:
            assert right.val is not None
            right.val += self.right.val
        assert self.parent
        if self.is_l:
            self.parent.left = Node(0, is_l=True, parent=self.parent)
        else:
            self.parent.right = Node(0, is_l=False, parent=self.parent)

    @property
    def root(self):
        node = self
        while node.parent:
            node = node.parent
        return node

    @property
    def sides(self):
        items = list(self.root.visit)
        idx = None
        left = right = None
        for i, node in enumerate(items):
            if id(node) == id(self):
                idx = i
                break
        if idx is not None:
            if idx - 1 >= 0:
                left = items[idx - 1]
            if idx + 1 < len(items):
                right = items[idx + 1]
        return left, right

    @property
    def pair(self):
        if not self.parent:
            return None
        assert self.parent.right and self.parent.left
        if self.is_l:
            return self.parent.right.val
        return self.parent.left.val

    @property
    def visit(self):
        if self.val is not None:
            yield self
        else:
            assert self.left and self.right
            yield from self.left.visit
            yield from self.right.visit


nodes = [Node(row) for row in RAW.split("\n")]
node_sum: Node = sum(nodes)
print(node_sum.magnitude)
print(max((n1 + n2).magnitude for n1, n2 in permutations(nodes, 2)))
