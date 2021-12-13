from pathlib import Path
import re
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

class Paper:
    def __init__(self, data):
        self.map = self.get_map(data)

    def get_map(self, data):
        return {(int(x), int(y)) for x, y in re.findall(r'(\d+),(\d+)', data)}

    def get_instructions(self, data):
        pass


paper = Paper(RAW)
print(paper.map)
