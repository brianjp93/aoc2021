from pathlib import Path
from math import prod
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

data: dict[complex, int] = {}
for y, row in enumerate(RAW.split("\n")):
    for x, n in enumerate(row):
        data[complex(x, y)] = int(n)

def get_adj(coord: complex):
    for near in [1, -1, 1j, -1j]:
        if data.get(coord + near) is not None:
            yield coord + near

def get_basin(coord: complex, basin: set[complex]):
    basin.add(coord)
    check = [
        ncoord for ncoord in get_adj(coord)
        if all((ncoord not in basin, data[ncoord] > data[coord], data[ncoord] != 9))
    ]
    return basin.union(*(get_basin(x, basin) for x in check))

output = [
    (h+1, len(get_basin(coord, set())))
    for coord, h in data.items()
    if all(h < data[x] for x in get_adj(coord))
]
output.sort(key=lambda x: -x[1])

print(sum(x[0] for x in output))
print(prod(x[1] for x in output[:3]))
