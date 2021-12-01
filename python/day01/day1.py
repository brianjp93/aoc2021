from pathlib import Path

with Path(Path(__file__).parent, 'data').open() as f:
    raw_data = f.read()
