from pathlib import Path
from collections import defaultdict
import re
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

start = RAW.split('\n')[0]
rules = {a: b for a, b in re.findall(r'(\w+) -> (\w+)', RAW)}

def get_next_pairs(pairs: defaultdict[str, int]):
    new_pairs: defaultdict[str, int] = defaultdict(int)
    for key, count in pairs.items():
        if len(key) == 2:
            middle_letter = rules[key]
            new_pairs[key[0] + middle_letter] += count
            new_pairs[middle_letter + key[1]] += count
        else:
            new_pairs[key] = count
    return new_pairs

def get_counts(pairs):
    letters = defaultdict(int)
    for pair, count in pairs.items():
        letters[pair[0]] += count
    counts = letters.values()
    return max(counts) - min(counts)

pairs: defaultdict[str, int] = defaultdict(int)
for i in range(len(start)):
    try:
        pairs[start[i:i+2]] += 1
    except IndexError:
        pairs[start[i]] += 1

for i in range(10):
    pairs = get_next_pairs(pairs)

print(get_counts(pairs))

for i in range(30):
    pairs = get_next_pairs(pairs)

print(get_counts(pairs))
