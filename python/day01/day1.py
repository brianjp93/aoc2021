from pathlib import Path

with Path(Path(__file__).parent, 'data').open() as f:
    raw_data = f.read()

data = [int(x) for x in raw_data.splitlines()]

increasing = [b > a for a, b in zip(data, data[1:])]
print(sum(increasing))
x = [b > a for a,b in zip(data, data[3:])]
print(sum(x))
