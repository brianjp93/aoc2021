from pathlib import Path
from collections import Counter
import re
with Path(Path(__file__).parent, 'data').open() as f:
    RAW = f.read().strip()
NUM = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
NUM_COUNT = Counter(''.join(NUM))
NUM_SUMS = {sum(NUM_COUNT[x] for x in chars): n for n, chars in enumerate(NUM)}

class Entry:
    def __init__(self, one: list[frozenset[str]], two: list[frozenset[str]]):
        self.one = one
        self.two = two
        self.map = self.get_mapping()

    def output(self):
        return int(''.join(str(self.map[x]) for x in self.two))

    def get_mapping(self):
        counts = Counter(''.join(''.join(chars) for chars in self.one))
        return {chars: NUM_SUMS[sum(counts[x] for x in chars)] for chars in self.one}

    def count(self):
        return sum(1 for x in self.two if self.map.get(x, None) in {1, 4, 7, 8})


count = total = 0
for one, two in re.findall(r'(.*) \| (.*)\n?', RAW):
    one = [frozenset(chars) for chars in one.strip().split()]
    two = [frozenset(chars) for chars in two.strip().split()]
    entry = Entry(one, two)
    count += entry.count()
    total += entry.output()

print(count)
print(total)
