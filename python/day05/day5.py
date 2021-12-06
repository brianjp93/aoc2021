from pathlib import Path
from collections import defaultdict
import re
with Path(Path(__file__).parent, 'data').open() as f:
    data = [
        ((int(x), int(y)), (int(nx), int(ny)))
        for  x, y, nx, ny
        in re.findall(r'(\d+),(\d+) -> (\d+),(\d+)', f.read())
    ]

class System:
    def __init__(self, dia=False):
        self.map = defaultdict(int)
        self.dia = dia

    def add_vent(self, start: tuple[int, int], end: tuple[int, int]):
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            small = min(y1, y2)
            big = max(y1, y2) + 1
            for y in range(small, big):
                self.map[(x1, y)] += 1
        elif y1 == y2:
            small = min(x1, x2)
            big = max(x1, x2) + 1
            for x in range(small, big):
                self.map[(x, y1)] += 1
        elif self.dia:
            if x1 < x2:
                x_range = range(x1, x2 + 1)
            else:
                x_range = range(x1, x2 - 1, -1)
            if y1 < y2:
                y_range = range(y1, y2 + 1)
            else:
                y_range = range(y1, y2 - 1, -1)
            for x, y in zip(x_range, y_range):
                self.map[(x, y)] += 1

    def count_dangerous(self):
        return sum(count > 1 for count in self.map.values())



system = System()
for start, end in data:
    system.add_vent(start, end)
print(system.count_dangerous())

system = System(dia=True)
for start, end in data:
    system.add_vent(start, end)
print(system.count_dangerous())
