from pathlib import Path

with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

print(RAW)
