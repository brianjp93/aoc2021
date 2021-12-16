from pathlib import Path
from math import prod
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

convert = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

def window(data: str, n: int):
    for i in range(0, len(data), n):
        yield data[i: i + n], i + n

def parse_data(data, packet_count=float('inf')):
    out = []
    versions = []
    count = 0
    while data.strip('0') and count < packet_count:
        count += 1
        version = int(data[:3], 2)
        versions.append(version)
        type_id = int(data[3:6], 2)
        data = data[6:]
        match type_id:
            case 4:
                num = []
                index = None
                for bits, index in window(data, 5):
                    num.append(bits[1:])
                    if bits[0] == '0':
                        break
                out.append(int(''.join(num), 2))
                assert index
                data = data[index:]
            case _:
                if data[0] == '0':
                    n = int(data[1:16], 2)
                    data = data[16:]
                    n_out, n_versions, _ = parse_data(data[:n])
                    data = data[n:]
                else:
                    sub_packets = int(data[1:12], 2)
                    data = data[12:]
                    n_out, n_versions, data = parse_data(data, packet_count=sub_packets)

                match type_id:
                    case 0:
                        n_out = sum(n_out)
                    case 1:
                        n_out = prod(n_out, start=1)
                    case 2:
                        n_out = min(n_out)
                    case 3:
                        n_out = max(n_out)
                    case 5:
                        n_out = 1 if n_out[0] > n_out[1] else 0
                    case 6:
                        n_out = 1 if n_out[0] < n_out[1] else 0
                    case 7:
                        n_out = 1 if n_out[0] == n_out[1] else 0

                out.append(n_out)
                versions.extend(n_versions)

    return out, versions, data


bits = []
for ch in RAW:
    bits.append(convert[ch])
bits = ''.join(bits)

out, versions, _ = parse_data(bits)
print(sum(versions))
print(out[0])
