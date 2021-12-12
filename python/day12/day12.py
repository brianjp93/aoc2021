from pathlib import Path
import re
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

START = 'start'
END = 'end'

class Node:
    def __init__(self, label: str):
        self.label = label
        self.edges: set[Node] = set()

    def max_visits(self, already_visited_twice=False):
        if self.label.isupper():
            return float('inf')
        elif self.label in (START, END) or already_visited_twice:
            return 1
        return 2

    def add(self, node: 'Node'):
        self.edges.add(node)
        node.edges.add(self)

def get_nodes():
    nodes: dict[str, Node] = {}
    for a, b in re.findall(r'(\w+)-(\w+)', RAW):
        anode = nodes.get(a, Node(a))
        bnode = nodes.get(b, Node(b))
        nodes[anode.label] = anode
        nodes[bnode.label] = bnode
        anode.add(bnode)
    return nodes

def count_paths(part_one=False):
    nodes = get_nodes()
    counts = 0
    stack: list[tuple[Node, dict[str, int], bool]] = []
    stack.append((nodes[START], {key: 0 for key in nodes}, False))
    while stack:
        node, visits, already_visited_twice = stack.pop()
        already_visited_twice = already_visited_twice or part_one
        if node.label == END:
            counts += 1
            continue

        if visits[node.label] < node.max_visits(already_visited_twice):
            visits[node.label] += 1
            if not already_visited_twice and node.label.islower() and visits[node.label] > 1:
                already_visited_twice = True
            for new_node in node.edges:
                stack.append((new_node, dict(visits), already_visited_twice))
    return counts


print(count_paths(True))
print(count_paths())
