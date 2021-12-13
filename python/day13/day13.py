from pathlib import Path
import re
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()


class Paper:
    def __init__(self, data):
        self.map = self.get_map(data)
        self.instr = self.get_instructions(data)

    def get_map(self, data):
        return {(int(x), int(y)) for x, y in re.findall(r'(\d+),(\d+)', data)}

    def draw(self):
        min_x, min_y = self.get_min()
        max_x, max_y = self.get_max()
        out = []
        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                line.append('#' if (x, y) in self.map else ' ')
            out.append(''.join(line))
        out = '\n'.join(out)
        print(out)
        return out

    def get_max(self):
        return (max(x[0] for x in self.map), max(x[1] for x in self.map))

    def get_min(self):
        return (min(x[0] for x in self.map), min(x[1] for x in self.map))

    def fold_x(self, n: int):
        nmap = set()
        for x, y in self.map:
            if x > n:
                nx = 2*n - x
                nmap.add((nx, y))
            else:
                nmap.add((x, y))
        self.map = nmap

    def fold_y(self, n: int):
        nmap = set()
        for x, y in self.map:
            if y > n:
                ny = 2*n - y
                nmap.add((x, ny))
            else:
                nmap.add((x, y))
        self.map = nmap

    def do_instr(self, i: int):
        axis, n = self.instr[i]
        match axis:
            case 'x':
                self.fold_x(n)
            case 'y':
                self.fold_y(n)

    def do_all(self, start=0):
        for i in range(start, len(self.instr)):
            self.do_instr(i)

    def get_instructions(self, data):
        return [(x, int(n)) for x, n in re.findall(r'(\w)=(\d+)', data)]


paper = Paper(RAW)
paper.do_instr(0)
print(len(paper.map))
paper.do_all(1)
paper.draw()
