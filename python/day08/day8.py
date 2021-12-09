from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
import re
with Path(Path(__file__).parent, 'data').open() as f:
    RAW = f.read().strip()


@dataclass
class Entry:
    one: list[frozenset[str]]
    two: list[frozenset[str]]

    def output(self):
        return int(''.join(str(self.map[x]) for x in self.two))

    @cached_property
    def map(self):
        my_map: dict[frozenset[str], int] = {}
        for chars in self.one:
            if chars not in my_map:
                match len(chars):
                    case 2: my_map[chars] = 1
                    case 3: my_map[chars] = 7
                    case 4: my_map[chars] = 4
                    case 7: my_map[chars] = 8
        revmap = {val: key for key, val in my_map.items()}
        for chars in self.one:
            if chars not in my_map:
                _7 = revmap[7]
                _4 = revmap[4]
                match [len(chars), len(chars - _7), len(chars ^ _4)]:
                    case [5, 3, 5]: my_map[chars] = 2
                    case [5, 2, 3]: my_map[chars] = 3
                    case [5, 3, 3]: my_map[chars] = 5
                    case [6, 3, 4]: my_map[chars] = 0
                    case [6, 4, 4]: my_map[chars] = 6
                    case [6, 3, 2]: my_map[chars] = 9
        return my_map

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
