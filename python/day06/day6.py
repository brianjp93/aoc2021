from pathlib import Path
from collections import defaultdict
with Path(Path(__file__).parent, 'data').open() as f:
    data = [int(x) for x in f.read().strip().split(',')]

class School:
    def __init__(self, data):
        self.fish = defaultdict(int)
        for x in data[:]:
            self.fish[x] += 1

    def next_day(self):
        new_fish = defaultdict(int)
        for timer, count in self.fish.items():
            new_fish[timer - 1] += count
        new_fish[8] = new_fish.pop(-1, 0)
        new_fish[6] += new_fish[8]
        self.fish = new_fish

    @property
    def total_fish(self):
        return sum(self.fish.values())

    def next(self, days):
        for _ in range(days):
            self.next_day()


x = School(data)
x.next(80)
print(x.total_fish)

x = School(data)
x.next(256)
print(x.total_fish)
