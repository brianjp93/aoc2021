from typing import Tuple, Literal
from pathlib import Path
from dataclasses import dataclass
from uuid import uuid4
from collections import defaultdict
from itertools import combinations

with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f'{self.x, self.y, self.z}'

    def __add__(self, other: 'Point' | Tuple[int, int, int]):
        x, y, z = other if isinstance(other, tuple) else (other.x, other.y, other.z)
        return Point(self.x + x, self.y + y, self.z + z)

    def dist(self, other: 'Point'):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def copy(self):
        return Point(self.x, self.y, self.z)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def rotate_xy(self):
        x, y = self.y, -self.x
        return Point(x, y, self.z)

    def rotate_xz(self):
        x, z = self.z, -self.x
        return Point(x, self.y, z)

    def rotate_yz(self):
        y, z = self.z, -self.y
        return Point(self.x, y, z)


class Cube:
    def __init__(self, data):
        self.location = Point(0, 0, 0)
        self.points = self.get_points(data)
        self.id = uuid4()

    def __repr__(self):
        return f'{self.__class__.__name__}(points={self.points})'

    def get_points(self, data):
        return {Point(*[int(x) for x in row.split(',')]) for row in data}

    def rotate(self, axis: Literal['xy', 'xz', 'yz']):
        self.points = {getattr(point, f'rotate_{axis}')() for point in self.points}
        self.location = getattr(self.location, f'rotate_{axis}')()

    def offset(self, vec: Point):
        self.points = {p + vec for p in self.points}
        self.location = self.location + vec

    def copy(self):
        x = Cube([])
        x.points = {a.copy() for a in self.points}
        x.id = self.id
        x.location = self.location.copy()
        return x

    def find_overlap(self, other: 'Cube', count=12):
        for p1 in self.points:
            for _ in other.orientations:
                for p2 in other.points:
                    other_copy = other.copy()
                    other_copy.offset(p1 - p2)
                    overlap = self.points & other_copy.points
                    if len(overlap) >= count:
                        return other_copy
        return False

    @property
    def orientations(self):
        for _ in range(4):
            self.rotate('xy')
            yield self
        self.rotate('xz')
        for _ in range(4):
            self.rotate('xy')
            yield self
        self.rotate('xz')
        for _ in range(4):
            self.rotate('xy')
            yield self
        self.rotate('xz')
        for _ in range(4):
            self.rotate('xy')
            yield self
        self.rotate('xz')
        self.rotate('yz')
        for _ in range(4):
            self.rotate('xy')
            yield self
        self.rotate('yz')
        self.rotate('yz')
        for _ in range(4):
            self.rotate('xy')
            yield self


class System:
    def __init__(self, system: list[Cube]):
        self.system = system
        self.group = [self.system.pop(0)]
        self.no_overlap = defaultdict(list)

    def find_overlapping(self, count=12):
        while len(self.system):
            is_found = False
            for i in range(len(self.group)):
                s1 = self.group[i]
                for j in range(len(self.system)):
                    s2 = self.system[j]
                    if s2.id in self.no_overlap[s1.id]:
                        continue
                    if s2_overlap := s1.find_overlap(s2, count=count):
                        self.group.append(s2_overlap)
                        self.system.pop(j)
                        print('Found overlap')
                        print(f'Group Length: {len(self.group)}')
                        print(f'System Length: {len(self.system)}')
                        is_found = True
                        break
                    else:
                        self.no_overlap[s1.id].append(s2.id)
                        self.no_overlap[s2.id].append(s1.id)
                if is_found:
                    break

    def count_beacons(self):
        self.find_overlapping()
        beacons = set().union(*(x.points for x in self.group))
        return len(beacons)


scanners = [Cube(x.split('\n')[1:]) for x in RAW.strip().split('\n\n')]
system = System(scanners)
count = system.count_beacons()
dist = max(a.location.dist(b.location) for a, b in combinations(system.group, 2))
print(f'Beacons: {count}')
print(f'Max Dist: {dist}')
