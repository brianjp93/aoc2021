from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from abc import ABC, abstractmethod
with Path(Path(__file__).parent, 'data').open() as f:
    positions = Counter(int(x) for x in f.read().strip().split(','))

@dataclass
class Swarm(ABC):
    positions: dict[int, int]

    @abstractmethod
    def calculate_alignment_cost(self, pos: int) -> int: ...

    def get_min_fuel(self):
        return min(self.calculate_alignment_cost(pos) for pos in self.positions)

class ConstantSwarm(Swarm):
    def calculate_alignment_cost(self, pos: int):
        return sum(abs(pos - other_pos) * count for other_pos, count in self.positions.items())

class IncreasingFuelSwarm(Swarm):
    def calculate_alignment_cost(self, pos: int):
        total = 0
        for npos, count in self.positions.items():
            n = abs(pos - npos)
            total += int((n * (n + 2)) / 2 * count)
        return total

swarm = ConstantSwarm(positions)
print(swarm.get_min_fuel())

swarm = IncreasingFuelSwarm(positions)
print(swarm.get_min_fuel())
