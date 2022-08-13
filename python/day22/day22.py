from pathlib import Path
import re
from typing import Literal, Any, TypeAlias

with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


POINT: TypeAlias = tuple[int, int, int]
RANGE: TypeAlias = tuple[int, int]
POWER: TypeAlias = Literal['on'] | Literal['off']

class Cuboid:
    def __init__(self, power: POWER, x_range: RANGE, y_range: RANGE, z_range: RANGE) -> None:
        self.power: POWER = power
        self.on = power == 'on'
        self.x0, self.x1 = x_range
        self.y0, self.y1 = y_range
        self.z0, self.z1 = z_range

    def overlap(self, other: 'Cuboid'):
        if self.x0 >= other.x0 and self.x1 <= other.x1:
            x0 = max(self.x0, other.x0)
            x1 = min(self.x1, other.x1)
            if self.y0 >= other.y0 and self.y1 <= other.y1:
                y0 = max(self.y0, other.y0)
                y1 = min(self.y1, other.y1)
                if self.z0 >= other.z0 and self.z1 <= other.z1:
                    z0 = max(self.z0, other.z0)
                    z1 = min(self.z1, other.z1)
                    return Cuboid(other.power, (x0, x1), (y0, y1), (z0, z1))
        return False


class Ocean:
    pass

# RAW = '''on x=10..12,y=10..12,z=10..12
# on x=11..13,y=11..13,z=11..13
# off x=9..11,y=9..11,z=9..11
# on x=10..10,y=10..10,z=10..10'''


def clamp_range(a, b, low: int|None=-50, high: int|None=50):
    if low is not None and a < low:
        a = low
    if high is not None and b > high:
        b = high
    return a, b


PAT = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')
def read_input(data: str, clamp: Any=clamp_range):
    for power, x1, x2, y1, y2, z1, z2 in PAT.findall(data):
        x1, x2, y1, y2, z1, z2 = (int(a) for a in (x1, x2, y1, y2, z1, z2))
        x1, x2 = clamp(x1, x2)
        y1, y2 = clamp(y1, y2)
        z1, z2 = clamp(z1, z2)
        # yield power, (x1, x2+1), (y1, y2+1), (z1, z2+1)
        yield power, (x1, x2), (y1, y2), (z1, z2)


def flip_lights(power: POWER, ocean: set[POINT], x_range: RANGE, y_range: RANGE, z_range: RANGE):
    method = ocean.add if power == 'on' else ocean.remove
    for x in range(*x_range):
        for y in range(*y_range):
            for z in range(*z_range):
                try: method((x, y, z))
                except KeyError: pass


if __name__ == '__main__':
    ocean: set[tuple[int, int, int]] = set()
    for power, x_range, y_range, z_range in read_input(RAW):
        flip_lights(power, ocean, x_range, y_range, z_range)

    # ocean: set[POINT] = set()
    # def no_clamp(a, b):
    #     return a, b
    # for power, x_range, y_range, z_range in read_input(RAW, clamp=no_clamp):
    #     flip_lights(power, ocean, x_range, y_range, z_range)

    print(len(ocean))
