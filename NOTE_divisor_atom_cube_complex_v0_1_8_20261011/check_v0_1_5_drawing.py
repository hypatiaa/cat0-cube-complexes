"""Exact checks for NOTE.md v0.1.4, section 7 (drawing register: the 30030 known-answer test).

Separate from check_v0_1_3.py, which is unchanged. Python standard library only.
Exact arithmetic: elements of Z[zeta_m] are integer coefficient vectors reduced modulo the
cyclotomic polynomial Phi_m (so equality is exact). One NUMERICAL cross-check (V0) compares
the exact drawing map with a float transcription of the viewer's shift-and-rotate formula
(helix_atlas_doily_witness_v27_patched_3_wl2.html, sha256 3d65e14a..., lines 1412-1423,
'positive' reversal mode), tolerance 1e-12, labelled numerical.
"""
import re
from itertools import combinations
from math import gcd, cos, sin, pi
from collections import defaultdict

failures = []


passes = {}


def check(cond, label):
    key = re.split(r"[ (]", label, maxsplit=1)[0]          # check ID, e.g. "C4b", "A2", "S6"
    passes.setdefault(key, [0, 0])
    passes[key][1] += 1
    if not cond:
        failures.append(label)
    else:
        passes[key][0] += 1
    return cond


def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def pdivmod(a, b):
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and any(a):
        c = a[-1] // b[-1]
        assert c * b[-1] == a[-1]
        s = len(a) - len(b)
        q[s] = c
        for i, x in enumerate(b):
            a[s + i] -= c * x
        while a and a[-1] == 0:
            a.pop()
    return q, a


_cyc = {}


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def cyclotomic(d):
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                num, r = pdivmod(num, cyclotomic(e))
                assert not any(r)
        _cyc[d] = num
    return _cyc[d]


def reduce_m(vec, m):
    """canonical exact form of sum vec[i] zeta_m^i in Z[zeta_m]"""
    a = list(vec)
    while a and a[-1] == 0:          # strip trailing zeros first, so zero vectors reduce too
        a.pop()
    _, r = pdivmod(a, cyclotomic(m)) if a else (None, [])
    deg = len(cyclotomic(m)) - 1      # = phi(m)
    assert len(r) <= deg
    return tuple(r + [0] * (deg - len(r)))


def drawing_exact(S, m):
    """(xy, z) for the squarefree divisor with seat set S: xy = -sum_{i in S} zeta_m^i, z = |S|"""
    v = [0] * m
    for i in S:
        v[i] -= 1
    return reduce_m(v, m), len(S)


def drawing_float_viewer(S, m):
    """float transcription of the viewer formula for squarefree N (a_i = 1, n_i = 2, r_i = 1/2)"""
    x = y = 0.0
    for i in range(m):
        e = 1 if i in S else 0
        phi = 2 * pi * i / m if m > 1 else 0.0
        x += 0.5 * (cos(2 * pi * e / 2 + phi) - cos(phi))
        y += 0.5 * (sin(2 * pi * e / 2 + phi) - sin(phi))
    return x, y, len(S)


def is_prime(n):
    return n >= 2 and all(n % q for q in range(2, int(n ** 0.5) + 1))


P = primes_upto(60)
report = []
num_max = 0.0

for m in range(1, 11):
    seats = list(range(m))
    subsets = [frozenset(c) for k in range(m + 1) for c in combinations(seats, k)]
    pts = defaultdict(list)
    for S in subsets:
        pts[drawing_exact(S, m)].append(S)
        # V0 NUMERICAL: exact map agrees with the viewer's float formula
        X, Y, Z = drawing_float_viewer(S, m)
        z = complex(0, 0)
        for i in S:
            z -= complex(cos(2 * pi * i / m), sin(2 * pi * i / m))
        num_max = max(num_max, abs(X - z.real), abs(Y - z.imag))
    distinct = len(pts)
    lost = len(subsets) - distinct
    # D1: collisions occur iff m is composite (m >= 4); m = 1 and m prime: injective in 3D
    check((lost > 0) == (m >= 4 and not is_prime(m)), f"D1 collisions iff composite m={m}")
    # D2: two seat sets collide iff their difference lies in K_m = ker(Z^m -> Z[zeta_m]) and sizes agree
    zero = tuple([0] * (len(cyclotomic(m)) - 1))
    for S, T in combinations(subsets, 2):
        diff = [(1 if i in S else 0) - (1 if i in T else 0) for i in seats]
        same = drawing_exact(S, m) == drawing_exact(T, m)
        check(same == (reduce_m(diff, m) == zero and len(S) == len(T)), f"D2 kernel criterion m={m}")
    # D3: antipode S -> complement maps xy -> -xy (m >= 2) and z -> m - z
    if m >= 2:
        for S in subsets:
            (a, za), (b, zb) = drawing_exact(S, m), drawing_exact(frozenset(seats) - S, m)
            check(tuple(-x for x in a) == b and zb == m - za, f"D3 antipode m={m}")
    # D4: drawing map = sum_i (zeta^i / 2) * W_{i}(S), W_{i}(S) = (-1)^{[i in S]}, the degree-1 Walsh
    #     characters (m >= 2, using sum_i zeta^i = 0); checked as 2*xy = sum_i zeta^i W_i
    if m >= 2:
        for S in subsets:
            v = [(-1 if i in S else 1) for i in seats]
            xy2 = tuple(2 * x for x in drawing_exact(S, m)[0])
            check(xy2 == reduce_m(v, m), f"D4 Walsh degree-1 m={m}")
    report.append((m, len(subsets), distinct, lost))

# 30030 specifically: m = 6, seats ordered by ascending prime 2,3,5,7,11,13
PR = [2, 3, 5, 7, 11, 13]
m = 6
by_point = defaultdict(list)
for k in range(7):
    for c in combinations(range(6), k):
        d = 1
        for i in c:
            d *= PR[i]
        by_point[drawing_exact(c, m)].append(d)
zero = tuple([0] * (len(cyclotomic(6)) - 1))
spine = sorted(d for (xy, z), ds in by_point.items() if xy == zero for d in ds)
spine_points = sorted(z for (xy, z) in by_point if xy == zero)
per_level = {z: (sum(len(ds) for (xy, zz), ds in by_point.items() if zz == z),
                 sum(1 for (xy, zz) in by_point if zz == z)) for z in range(7)}
check(len(by_point) == 53, "S1 30030 distinct points = 53")
check(spine == sorted([1, 14, 33, 65, 110, 273, 462, 910, 2145, 30030]), "S2 30030 spine divisors")
check(spine_points == [0, 2, 3, 4, 6], "S3 30030 spine heights")
check(per_level == {0: (1, 1), 1: (6, 6), 2: (15, 13), 3: (20, 13), 4: (15, 13), 5: (6, 6), 6: (1, 1)},
      "S4 30030 per-level counts")
doubles = sorted(tuple(sorted(ds)) for ds in by_point.values() if len(ds) > 1)
check(all(len(ds) <= 3 for ds in by_point.values()), "S5 multiplicity <= 3")
# S6: every coincidence is a swap of one zero-sum block for another of the same size
# (antipodal duad <-> duad, or triangle <-> triangle), keeping the rest
duads = [frozenset({i, i + 3}) for i in range(3)]
tris = [frozenset({0, 2, 4}), frozenset({1, 3, 5})]
blocks = duads + tris


def seats_of(d):
    return frozenset(i for i, p in enumerate(PR) if d % p == 0)


for ds in by_point.values():
    for d, e in combinations(ds, 2):
        A, B = seats_of(d), seats_of(e)
        ok = any(a <= A and b <= B and a.isdisjoint(B - b) and len(a) == len(b) and (A - a) == (B - b)
                 for a in blocks for b in blocks if a != b)
        check(ok, f"S6 block swap {d},{e}")

# ---- v0.1.5 additions (independent check of v0.1.4: E1, E2, E4, E12) ----
from math import gcd as _g


def phi_(n):
    return sum(1 for k in range(1, n + 1) if _g(k, n) == 1)


def kernel_rank(m):
    """rank of K_m = ker(Z^m -> Z[zeta_m]) computed from the exact images of the basis vectors"""
    rows = [list(reduce_m([1 if j == i else 0 for j in range(m)], m)) for i in range(m)]
    # rank of the image = rank of this integer matrix (fraction-free Gaussian elimination)
    from fractions import Fraction
    M = [[Fraction(x) for x in r] for r in rows]
    rank, col, ncol = 0, 0, len(M[0]) if M and M[0] else 0
    for col in range(ncol):
        piv = next((r for r in range(rank, len(M)) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        for r in range(len(M)):
            if r != rank and M[r][col] != 0:
                f = M[r][col] / M[rank][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[rank])]
        rank += 1
    return m - rank


for m in range(1, 13):
    check(kernel_rank(m) == m - phi_(m), f"E12 kernel rank m={m}")
check(reduce_m([1], 1) != tuple([0] * (len(cyclotomic(1)) - 1)) or len(cyclotomic(1)) - 1 == 0, "E2 setup")
# E2: K_1 = 0 (the image of (1) is zeta_1^0 = 1 != 0): Z[zeta_1] = Z, Phi_1 = x - 1, x = 1
check(len(cyclotomic(1)) == 2 and cyclotomic(1) == [-1, 1], "E2 Phi_1")
check(kernel_rank(1) == 0, "E2 K_1 = 0")

# E1: loss split for 30030: 5 on the spine, 6 off it, 7 at Omega = 3
lost_on = sum(len(ds) - 1 for (xy, z), ds in by_point.items() if xy == zero)
lost_off = sum(len(ds) - 1 for (xy, z), ds in by_point.items() if xy != zero)
lost_3 = sum(len(ds) - 1 for (xy, z), ds in by_point.items() if z == 3)
check((lost_on, lost_off, lost_3) == (5, 6, 7), "E1 loss split 30030")
# the six off-spine coincidences, asserted (were only printed in v0.1.4)
off = sorted(tuple(sorted(ds)) for (xy, z), ds in by_point.items() if xy != zero and len(ds) > 1)
check(off == [(42, 195), (66, 130), (70, 165), (154, 715), (182, 429), (231, 455)], "E1 six off-spine pairs")
check(all(z == 3 for (xy, z), ds in by_point.items() if xy != zero and len(ds) > 1), "E1 off-spine at Omega 3")

# E4: zero-sum seat sets of mu_6 are exactly the DISJOINT unions of cosets of {0,3} and {0,2,4};
# a non-disjoint union such as {0,3} | {0,2,4} is not zero-sum
cosets = [frozenset({0, 3}), frozenset({1, 4}), frozenset({2, 5}), frozenset({0, 2, 4}), frozenset({1, 3, 5})]
disjoint_unions = {frozenset()}
changed = True
while changed:
    changed = False
    for U in list(disjoint_unions):
        for c in cosets:
            if U.isdisjoint(c) and (U | c) not in disjoint_unions:
                disjoint_unions.add(U | c)
                changed = True
zero_sum = {frozenset(c) for k in range(7) for c in combinations(range(6), k) if drawing_exact(c, 6)[0] == zero}
check(zero_sum == disjoint_unions, "E4 zero-sum = disjoint coset unions")
check(drawing_exact(frozenset({0, 3}) | frozenset({0, 2, 4}), 6)[0] != zero, "E4 non-disjoint counterexample")

# E3: the antipode and Walsh identities fail at m = 1 (so the note states m >= 2)
(a1, z1), (b1, w1) = drawing_exact(frozenset(), 1), drawing_exact(frozenset({0}), 1)
check(not (tuple(-x for x in a1) == b1 and w1 == 1 - z1), "E3 antipode fails at m=1")

print("m | divisors 2^m | distinct 3D points | lost to coincidence")
for r in report:
    print(*r, sep=" | ")
print("30030 per level (Omega: divisors, points):", per_level)
print("30030 spine divisors:", spine, "at heights", spine_points)
print("30030 coincident groups:", doubles)
print("V0 numerical max |exact - viewer float|:", f"{num_max:.3e}", "(tolerance 1e-12)")
check(num_max < 1e-12, "V0 numerical")
print("Per-check executions (passed/run), printed so a fresh run is visible:")
for k in sorted(passes):
    print(f"  {k}: {passes[k][0]}/{passes[k][1]}")
print("FAILURES:", len(failures))
for x in sorted(set(failures)):
    print("  ", x)
print("RESULT:", "ALL CHECKS PASS" if not failures else "FAIL")
