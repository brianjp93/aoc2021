from pathlib import Path
with Path(Path(__file__).parent, 'data').open() as f:
    data = f.readlines()

x = z = 0
for line in data:
    dir, n = line.split()
    n = int(n)
    match dir:
        case 'forward':
            x += n
        case 'up':
            z -= n
        case 'down':
            z += n
print(x * z)

x = z = aim = 0
for line in data:
    dir, n = line.split()
    n = int(n)
    match dir:
        case 'forward':
            x += n
            z += n * aim
        case 'up':
            aim -= n
        case 'down':
            aim += n
print(x * z)
