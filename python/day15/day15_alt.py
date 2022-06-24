from pathlib import Path
import networkx as nx
from itertools import product
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


class Cave:
    def __init__(self, data):
        self.map, self.end = self.get_map(data)

    def get_map(self, data):
        g = nx.Graph()
        x = y = None
        for y, row in enumerate(data.split('\n')):
            for x, n in enumerate(row):
                g.add_node(complex(x, y))
        for y, row in enumerate(data.split('\n')):
            for x, n in enumerate(row):
                node = complex(x, y)
                n = int(n)
                if x > 0:
                    left = complex(x - 1, y)
                    g.add_edge(node, left, weight=n)
                if y > 0:
                    up = complex(x, y - 1)
                    g.add_edge(node, up, weight=n)
        assert x and y
        g.add_node('start')
        g.add_edge('start', 0, weight=int(data[0]))
        return g, complex(x, y)


class BigCave(Cave):
    def get_map(self, data):
        _map: dict[complex, int] = {}
        real_x = real_y = None
        rows = data.split('\n')
        width, height = len(rows[0]), len(rows)
        for x_add, y_add in product(range(5), repeat=2):
            for y, row in enumerate(rows):
                for x, n in enumerate(row):
                    real_x = (x_add * width) + x
                    real_y = (y_add * height) + y
                    val = ((int(n) - 1 + x_add + y_add) % 9) + 1
                    _map[complex(real_x, real_y)] = val
        assert real_x and real_y
        return _map, complex(real_x, real_y)

cave = Cave(RAW)
x = nx.shortest_paths.bidirectional_dijkstra(cave.map, 0, cave.end)
print(x)
# print(Cave(RAW).find())
# print(BigCave(RAW).find())
