from pathlib import Path
with Path(Path(__file__).parent, 'data').open() as f:
    data = f.readlines()

x = z = 0
for line in data:
    dir, n = line.split()
    n = int(n)
    match [dir, n]:
        case ['forward', n]:
            x += n
        case ['up', n]:
            z -= n
        case ['down', n]:
            z += n
print(x * z)

x = z = aim = 0
for line in data:
    dir, n = line.split()
    n = int(n)
    match [dir, n]:
        case ['forward', n]:
            x += n
            z += n * aim
        case ['up', n]:
            aim -= n
        case ['down', n]:
            aim += n
print(x * z)
