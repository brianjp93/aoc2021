from pathlib import Path

with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

IEA, IMAGE = RAW.split('\n\n')

class Image:
    def __init__(self, image):
        self.image, self.bounds = self.get_image(image)
        self.outer = '.'

    def enhance_many(self, count):
        for _ in range(count):
            self.enhance()

    def enhance(self):
        new_image: dict[tuple[int, int], str] = {}
        minx = miny = float('inf')
        maxx = maxy = -float('inf')
        x0, x1, y0, y1 = self.bounds
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                pixel = self.get_new_pixel((x, y))
                new_image[(x, y)] = pixel
                if pixel == '#':
                    miny = min(miny, y)
                    maxy = max(maxy, y)
                    minx = min(minx, x)
                    maxx = max(maxx, x)
        self.image = new_image
        if IEA[0] == '#':
            self.outer = '#' if self.outer == '.' else '.'
        self.bounds = int(minx-1), int(maxx+1), int(miny-1), int(maxy+1)

    @staticmethod
    def get_image(image):
        ret: dict[tuple[int, int], str] = {}
        minx = miny = float('inf')
        maxx = maxy = -float('inf')
        for y, row in enumerate(image.split('\n')):
            for x, char in enumerate(row):
                ret[(x, y)] = char
                if char == '#':
                    miny = min(miny, y)
                    maxy = max(maxy, y)
                    minx = min(minx, x)
                    maxx = max(maxx, x)
        return ret, (int(minx-1), int(maxx+1), int(miny-1), int(maxy+1))

    def get_pixels(self, pos: tuple[int, int]):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                npos = (pos[0] + dx, pos[1] + dy)
                yield self.image.get(npos, self.outer)

    def get_new_pixel(self, pos: tuple[int, int]):
        index = sum((2**i) * (x == '#') for i, x in enumerate(reversed(list(self.get_pixels(pos)))))
        return IEA[index]

image = Image(IMAGE)
image.enhance_many(2)
print(list(image.image.values()).count('#'))

image = Image(IMAGE)
image.enhance_many(50)
print(list(image.image.values()).count('#'))
