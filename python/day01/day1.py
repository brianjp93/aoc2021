from pathlib import Path

with Path(Path(__file__).parent, 'data').open() as f:
    data = [int(x) for x in f.readlines()]

print(sum(b > a for a, b in zip(data, data[1:])))
print(sum(b > a for a, b in zip(data, data[3:])))
