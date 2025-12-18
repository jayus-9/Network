import math
from itertools import combinations


def hamming_encode(info):
    data = [int(b) for b in info]
    k = len(data)
    r = 0
    while 2 ** r < k + r + 1:
        r += 1
    n = k + r
    code = [0] * n
    j = 0
    for i in range(1, n + 1):
        if i & (i - 1) != 0:
            code[i - 1] = data[j]
            j += 1
    for p in range(r):
        pos = 2 ** p
        parity = 0
        for i in range(1, n + 1):
            if i & pos:
                parity ^= code[i - 1]
        code[pos - 1] = parity
    return ''.join(map(str, code))


def hamming_syndrome(received):
    received = [int(b) for b in received]
    n = len(received)
    r = 0
    while 2 ** r <= n:
        r += 1
    syndrome = 0
    for p in range(r):
        pos = 2 ** p
        parity = 0
        for i in range(1, n + 1):
            if i & pos:
                parity ^= received[i - 1]
        if parity:
            syndrome += pos
    return syndrome


info_vector = '1011'
v = hamming_encode(info_vector)
print("Кодовое слово:", v)

n = 7
print("i\tCin\tNo\tCo\tNk\tCk")
for i in range(1, n + 1):
    Cin = math.comb(n, i)
    Nk = 0
    No = 0
    for err_pos in combinations(range(n), i):
        r_list = list(v)
        for p in err_pos:
            r_list[p] = '1' if r_list[p] == '0' else '0'
        r = ''.join(r_list)
        synd = hamming_syndrome(r)

        if synd != 0:
            No += 1
            corrected = r
            if 1 <= synd <= n:
                corr_list = list(r)
                corr_list[synd - 1] = '1' if corr_list[synd - 1] == '0' else '0'
                corrected = ''.join(corr_list)
        else:
            corrected = r

        if corrected == v:
            Nk += 1

    Co = No / Cin if Cin > 0 else 0
    Ck = Nk / Cin if Cin > 0 else 0
    print(f"{i}\t{Cin}\t{No}\t{round(Co, 3)}\t{Nk}\t{round(Ck, 3)}")