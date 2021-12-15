from pathlib import Path
from queue import PriorityQueue
from dataclasses import dataclass, field
from itertools import product
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


@dataclass(order=True)
class Point:
    risk: int
    coord: complex = field(compare=False)


class Cave:
    def __init__(self, data):
        self.map, self.end = self.get_map(data)

    def get_map(self, data):
        _map: dict[complex, int] = {}
        x = y = None
        for y, row in enumerate(data.split('\n')):
            for x, n in enumerate(row):
                _map[complex(x, y)] = int(n)
        assert x and y
        return _map, complex(x, y)

    def get_adj(self, coord: complex):
        for adj in (1, -1, 1j, -1j):
            if adj + coord in self.map:
                yield adj + coord

    def find(self):
        cache = {}
        queue: PriorityQueue[Point] = PriorityQueue()
        queue.put(Point(0, 0))
        while not queue.empty():
            point = queue.get()
            for ncoord in self.get_adj(point.coord):
                new_risk = point.risk + self.map[ncoord]
                if new_risk < cache.get(ncoord, float('inf')):
                    cache[ncoord] = new_risk
                    queue.put(Point(new_risk, ncoord))
        return cache[self.end]


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

print(Cave(RAW).find())
print(BigCave(RAW).find())
