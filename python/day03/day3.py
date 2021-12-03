from pathlib import Path
from collections import Counter
with Path(Path(__file__).parent, 'data').open() as f:
    data = [x.strip() for x in f.readlines()]

gamma = ['1' if bit.count('1') > bit.count('0') else '0' for bit in zip(*data)]
epsilon = ['1' if x == '0' else '0' for x in gamma]

x = int(''.join(gamma), 2)
y = int(''.join(epsilon), 2)
print(x * y)

def most_common(data: list[str], index: int):
    counts = Counter(x[index] for x in data)
    return '1' if counts['1'] >= counts['0'] else '0'

def least_common(data: list[str], index: int):
    counts = Counter(x[index] for x in data)
    return '0' if counts['0'] <= counts['1'] else '1'


def filter_by(data: list[str], filter_function):
    data = data[:]
    while len(data) > 1:
        for i in range(len(data[0])):
            value = filter_function(data, i)
            data = [x for x in data if x[i] == value]
            if len(data) == 1:
                break
    return int(''.join(data[0]), 2)

oxy = filter_by(data, most_common)
co2 = filter_by(data, least_common)
print(oxy * co2)
