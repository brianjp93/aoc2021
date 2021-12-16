from pathlib import Path
from math import prod
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip()

def window(data: str, n: int):
    for i in range(0, len(data), n):
        yield data[i: i + n], i + n

handlers = {
    0: lambda x: sum(x),
    1: lambda x: prod(x, start=1),
    2: lambda x: min(x),
    3: lambda x: max(x),
    5: lambda x: x[0] > x[1],
    6: lambda x: x[0] < x[1],
    7: lambda x: x[0] == x[1],
}

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
        if type_id == 4:
            num = []
            index = None
            for bits, index in window(data, 5):
                num.append(bits[1:])
                if bits[0] == '0':
                    break
            out.append(int(''.join(num), 2))
            assert index
            data = data[index:]
        else:
            if data[0] == '0':
                n = int(data[1:16], 2)
                data = data[16:]
                n_out, n_versions, _ = parse_data(data[:n])
                data = data[n:]
            else:
                sub_packets = int(data[1:12], 2)
                data = data[12:]
                n_out, n_versions, data = parse_data(data, packet_count=sub_packets)

            out.append(handlers[type_id](n_out))
            versions.extend(n_versions)

    return out, versions, data


bits = ''.join(bin(int(ch, 16))[2:].zfill(4) for ch in RAW)
out, versions, _ = parse_data(bits)
print(sum(versions))
print(out[0])
