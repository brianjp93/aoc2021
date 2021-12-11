from pathlib import Path
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

class Ocean:
    def __init__(self, data):
        self.map: dict[complex, int] = self.get_map(data)
        self.flash_count = 0

        self.flashed = set()

    def get_map(self, data):
        _map = {}
        for y, row in enumerate(data.split('\n')):
            for x, n in enumerate(row):
                _map[complex(x, y)] = int(n)
        return _map

    def get_adj(self, coord: complex):
        for adj in [1, 1j, -1, -1j, 1+1j, 1-1j, -1+1j, -1-1j]:
            ncoord = coord + adj
            if ncoord in self.map:
                yield ncoord

    def step(self):
        self.flashed = set()
        for coord in self.map:
            self.map[coord] += 1

        for coord in self.map:
            if self.map[coord] > 9:
                if coord not in self.flashed:
                    self.flashed.add(coord)
                    self.handle_flash(coord)

    def handle_flash(self, coord: complex):
        self.flash_count += 1
        self.map[coord] = 0
        for ncoord in self.get_adj(coord):
            if ncoord not in self.flashed:
                self.map[ncoord] += 1
                if self.map[ncoord] > 9:
                    self.flashed.add(ncoord)
                    self.handle_flash(ncoord)

    def do_steps(self, steps):
        for _ in range(steps):
            self.step()

    def find_sync(self):
        i = 0
        while len(self.flashed) != len(self.map):
            self.step()
            i += 1
        return i


ocean = Ocean(RAW)
ocean.do_steps(100)
print(ocean.flash_count)

ocean = Ocean(RAW)
print(ocean.find_sync())
