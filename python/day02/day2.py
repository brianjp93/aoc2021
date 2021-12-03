from pathlib import Path
import re

with Path(Path(__file__).parent, 'data').open() as f:
    data = [(a, int(b)) for a, b in re.findall(r'(\w+) (\d+)', f.read())]

x = z = 0
for dir, n in data:
    match dir:
        case 'forward':
            x += n
        case 'up':
            z -= n
        case 'down':
            z += n
print(x * z)

x = z = aim = 0
for dir, n in data:
    match dir:
        case 'forward':
            x += n
            z += n * aim
        case 'up':
            aim -= n
        case 'down':
            aim += n
print(x * z)
