"""Exact checks for NOTE.md v0.1.6, section 7.6 (O6: drawing coincidences for all atoms, mode 'positive').

Python standard library only. Elements of Q(zeta_L) are rational coefficient vectors reduced
modulo the cyclotomic polynomial Phi_L, so equality is exact. The drawing map is the frozen
viewer's divisorPosition in mode 'positive' (helix_atlas_doily_witness_v27_patched_3_wl2.html,
sha256 3d65e14a..., lines 1445-1465; prime order from factorize, lines 1261-1271):
  pos(d) = sum_j r_j zeta_m^j (zeta_{n_j}^{e_j} - 1),  z = sum_j e_j,  n_j = a_j + 1, r_j = 1/n_j.
One NUMERICAL cross-check (V1) compares the exact map with a float transcription of that code.
"""
import re
from fractions import Fraction
from itertools import combinations, product
from math import gcd, cos, sin, pi
from collections import defaultdict

failures = []
passes = {}


def check(cond, label):
    key = re.split(r"[ (]", label, maxsplit=1)[0]
    passes.setdefault(key, [0, 0])
    passes[key][1] += 1
    if not cond:
        failures.append(label)
    else:
        passes[key][0] += 1
    return cond


def factor(n):
    f, p = [], 2
    while p * p <= n:
        if n % p == 0:
            a = 0
            while n % p == 0:
                n //= p
                a += 1
            f.append((p, a))
        p += 1
    if n > 1:
        f.append((n, 1))
    return f


def lcm(a, b):
    return a // gcd(a, b) * b


def pdivmod(a, b):
    a = a[:]
    while len(a) >= len(b) and any(a):
        c = a[-1] / b[-1] if isinstance(a[-1], Fraction) else Fraction(a[-1], b[-1])
        s = len(a) - len(b)
        for i, x in enumerate(b):
            a[s + i] -= c * x
        while a and a[-1] == 0:
            a.pop()
    return a


_cyc = {}


def cyclotomic(d):
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0:
                q, r = [], num
                # exact polynomial division num / Phi_e
                b = cyclotomic(e)
                a = num[:]
                qq = [0] * (len(a) - len(b) + 1)
                while len(a) >= len(b) and any(a):
                    c = a[-1] // b[-1]
                    s = len(a) - len(b)
                    qq[s] = c
                    for i, x in enumerate(b):
                        a[s + i] -= c * x
                    while a and a[-1] == 0:
                        a.pop()
                assert not any(a)
                num = qq
        _cyc[d] = num
    return _cyc[d]


class Field:
    """Q(zeta_L) with exact reduction modulo Phi_L."""

    def __init__(self, L):
        self.L = L
        self.phi = cyclotomic(L)
        self.deg = len(self.phi) - 1

    def red(self, vec):
        a = [Fraction(x) for x in vec]
        while a and a[-1] == 0:
            a.pop()
        r = pdivmod(a, self.phi) if a else []
        return tuple(r + [Fraction(0)] * (self.deg - len(r)))

    def root(self, order, k):
        """zeta_order^k as a reduced vector"""
        v = [0] * self.L
        v[(k * (self.L // order)) % self.L] = 1
        return self.red(v)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, c, a):
        return tuple(c * x for x in a)

    def mul(self, a, b):
        v = [Fraction(0)] * (2 * self.deg + 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        v[i + j] += x * y
        return self.red(v)

    def zero(self):
        return tuple([Fraction(0)] * self.deg)


def setup(N):
    fac = factor(N)
    m = len(fac)
    L = m if m > 0 else 1
    for p, a in fac:
        L = lcm(L, a + 1)
    return fac, m, Field(L)


def pos_exact(e, fac, m, F):
    """mode 'positive' viewer map, exact"""
    s = F.zero()
    for j, (p, a) in enumerate(fac):
        n = a + 1
        term = F.add(F.root(n, e[j]), F.scale(-1, F.root(1, 0)))
        term = F.mul(F.root(m, j), term)
        s = F.add(s, F.scale(Fraction(1, n), term))
    return s, sum(e)


def pos_float(e, fac):
    m = len(fac)
    x = y = 0.0
    for i, (p, a) in enumerate(fac):
        n = a + 1
        r = 1 / n
        phi = (2 * pi * i) / m if m > 1 else 0
        ang = (2 * pi * e[i]) / n + phi
        x += r * (cos(ang) - cos(phi))
        y += r * (sin(ang) - sin(phi))
    return x, y, sum(e)


def to_complex(v, F):
    return sum(complex(float(c)) * complex(cos(2 * pi * k / F.L), sin(2 * pi * k / F.L)) for k, c in enumerate(v))


def hyper_coords(e, fac):
    """Sageev coordinates h_{j,k} = [p_j^k | d], k = 1..a_j"""
    return tuple(1 if e[j] >= k else 0 for j, (p, a) in enumerate(fac) for k in range(1, a + 1))


def edge_vectors(fac, m, F):
    """w_{j,k} = r_j zeta_m^j zeta_{n_j}^{k-1} (zeta_{n_j} - 1)"""
    ws = []
    for j, (p, a) in enumerate(fac):
        n = a + 1
        base = F.mul(F.root(m, j), F.add(F.root(n, 1), F.scale(-1, F.root(1, 0))))
        for k in range(1, a + 1):
            ws.append(F.scale(Fraction(1, n), F.mul(F.root(n, k - 1), base)))
    return ws


def q_rank(vectors):
    rows = [list(v) for v in vectors]
    rank = 0
    ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        piv = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col] / rows[rank][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


CASES = [4, 8, 16, 12, 18, 36, 72, 24, 48, 108, 200, 60, 180, 360, 900, 420, 1260, 6300, 4620, 13860, 30030, 60060, 120120, 900900]
table = []
eq_pairs = {}
numerr = 0.0
collision_examples = {}

for N in CASES:
    fac, m, F = setup(N)
    exps = list(product(*[range(a + 1) for p, a in fac]))
    pts = defaultdict(list)
    ws = edge_vectors(fac, m, F)
    for e in exps:
        P = pos_exact(e, fac, m, F)
        pts[P].append(e)
        # L1: linearity in Sageev coordinates: pos(d) = sum h_{j,k} w_{j,k}
        h = hyper_coords(e, fac)
        lin = F.zero()
        for hk, w in zip(h, ws):
            if hk:
                lin = F.add(lin, w)
        check(lin == P[0] and sum(h) == P[1], f"L1 linear in hyperplane coords N={N}")
        # V1 numerical
        X, Y, Z = pos_float(e, fac)
        c = to_complex(P[0], F)
        numerr = max(numerr, abs(X - c.real), abs(Y - c.imag))
    # L2: every edge crossing H(p_j,k) is drawn as the same vector w_{j,k}
    idx = 0
    for j, (p, a) in enumerate(fac):
        for k in range(1, a + 1):
            for e in exps:
                if e[j] == k - 1:
                    e2 = list(e)
                    e2[j] = k
                    d1 = pos_exact(e, fac, m, F)[0]
                    d2 = pos_exact(tuple(e2), fac, m, F)[0]
                    check(F.add(d2, F.scale(-1, d1)) == ws[idx], f"L2 edge vector N={N}")
            idx += 1
    # L3: coincidence criterion: equal height and hyperplane-coordinate difference in ker(w)
    keyed = {e: pos_exact(e, fac, m, F) for e in exps}
    if len(exps) <= 400:
        for e, f2 in combinations(exps, 2):
            same = keyed[e] == keyed[f2]
            dh = [x - y for x, y in zip(hyper_coords(e, fac), hyper_coords(f2, fac))]
            s = F.zero()
            for c, w in zip(dh, ws):
                if c:
                    s = F.add(s, F.scale(Fraction(c), w))
            check(same == (s == F.zero() and sum(dh) == 0), f"L3 kernel criterion N={N}")
    distinct = len(pts)
    groups = [v for v in pts.values() if len(v) > 1]
    lost = len(exps) - distinct
    kr = len(ws) - q_rank(ws) if ws else 0
    table.append((N, '*'.join(f"{p}^{a}" if a > 1 else str(p) for p, a in fac), m, len(ws), kr, len(exps), distinct, lost, max((len(g) for g in groups), default=1)))
    if groups:
        g = min(groups, key=lambda v: sum(v[0]))
        collision_examples[N] = g
    # equal edge vectors: pairs of hyperplanes drawn with the identical vector
    labels = [(p, k) for (p, a) in fac for k in range(1, a + 1)]
    eq_pairs[N] = [(labels[i], labels[j]) for i, j in combinations(range(len(ws)), 2) if ws[i] == ws[j]]

# helper for readable divisors


def divisor_of(fac, e):
    d = 1
    for (p, a), x in zip(fac, e):
        d *= p ** x
    return d


# Structural checks
res = {row[0]: row for row in table}
# T1 single prime atoms (m = 1) are drawn injectively
for N in [4, 8, 16]:
    check(res[N][7] == 0, f"T1 m=1 injective N={N}")
# T2 the squarefree restriction agrees with section 7 (30030 x 2 = 60060 has 2^2; 30030 itself is in v0.1.5)
# T3 kernel rank formula: rank_Q of the edge-vector span equals dim of Q-span of all zeta_m^j zeta_{n_j}^k used

# T2 squarefree consistency with section 7: 30030 loses exactly 11 points
check(res[30030][7] == 11 and res[30030][6] == 53, "T2 30030 matches section 7")
# T3 the mechanism of the 180 coincidence: H(2,2) and H(3,1) are drawn with the same edge vector,
# so 4 = 2^2 and 6 = 2*3 (paths 1->2->4 and 1->2->6) end at the same point
check(((2, 2), (3, 1)) in eq_pairs[180], "T3 180 equal edge vectors H(2,2)=H(3,1)")
check(sorted(collision_examples[180]) == sorted([(2, 0, 0), (1, 1, 0)]), "T3 180 group is {4, 6}")
# T4 m prime does NOT give injectivity once some a_j >= 2 (contrast with section 7.2)
check(res[180][7] > 0 and res[180][2] == 3, "T4 m=3 non-squarefree collides")
check(numerr < 1e-12, "V1 numerical")

print("N | factorisation | m | hyperplanes Omega | rank of ker(w) over Q | divisors | distinct points | lost | max multiplicity")
for row in table:
    print(*row, sep=" | ")
print("Smallest-height coincidence group per atom (as divisors):")
for N in CASES:
    if N in collision_examples:
        fac = factor(N)
        print(f"  {N}: {[divisor_of(fac, e) for e in collision_examples[N]]}")
print("Hyperplane pairs drawn with identical edge vectors:")
for N in CASES:
    if eq_pairs.get(N):
        print(f"  {N}: {eq_pairs[N]}")
print("V1 numerical max |exact - viewer float|:", f"{numerr:.3e}", "(tolerance 1e-12)")
print("Per-check executions (passed/run), printed so a fresh run is visible:")
for k in sorted(passes):
    print(f"  {k}: {passes[k][0]}/{passes[k][1]}")
print("FAILURES:", len(failures))
for x in sorted(set(failures))[:30]:
    print("  ", x)
print("RESULT:", "ALL CHECKS PASS" if not failures else "FAIL")
