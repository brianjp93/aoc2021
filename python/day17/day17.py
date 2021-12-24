from typing import TypeAlias
from dataclasses import dataclass, field


Coord: TypeAlias = complex

@dataclass
class Trench:
    x: tuple[int, int]
    y: tuple[int, int]
    init_vels: set[Coord] = field(default_factory=set)

    def scan_from(self, vel: Coord):
        while vel.real > 0:
            coord = 0
            start_vel = vel
            while coord.imag >= self.y[0]:
                if self.is_in(coord):
                    self.init_vels.add(vel)
                coord, start_vel = self.next_coord(coord, start_vel)
            vel -= 1

    def scan_all(self):
        vel = complex(self.x[1], abs(self.y[0] + 1))
        while vel.imag >= self.y[0]:
            self.scan_from(vel)
            vel -= 1j

    def next_coord(self, coord: Coord, vel: Coord):
        ncoord = coord + vel
        vel = vel - 1j if vel.real == 0 else vel - (1+1j)
        return ncoord, vel

    def is_in(self, coord: Coord):
        x, y = coord.real, coord.imag
        return self.x[0] <= x <= self.x[1] and self.y[0] <= y <= self.y[1]


trench = Trench((138, 184), (-125, -71))
trench.scan_all()
print(len(trench.init_vels))
