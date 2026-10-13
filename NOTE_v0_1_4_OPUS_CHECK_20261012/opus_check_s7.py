"""Independent exact check of NOTE v0.1.4 section 7 (drawing register), written from the note's
statements, not from check_v0_1_4_drawing.py.  Standard library only.

Two exact routes:
  Route 1: Q(zeta_m) via Phi_m built from the Moebius product formula
           Phi_m = prod_{d|m} (x^d - 1)^{mu(m/d)}, and remainder mod Phi_m (monic, integer).
  Route 2 (m = 6 only): Z[w], w^2 = -1 - w, zeta_6 = 1 + w (= -w^2), coordinates (a, b) = a + b w.
Floats appear only in the labelled numerical cross-check of the viewer modes (N1).
"""
from fractions import Fraction
from itertools import combinations
from math import cos, sin, pi
from collections import defaultdict

FAIL = []


def ok(c, msg):
    if not c:
        FAIL.append(msg)
    return c


# ---------- integer polynomials (lists, low degree first) ----------
def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def pmul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return trim(r)


def pdiv_exact(a, b):
    """exact division of integer polys, b monic; returns quotient, asserts zero remainder"""
    a = trim(a)
    b = trim(b)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1]
        s = len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] -= c * y
        a = trim(a)
    assert not a, "non-exact division"
    return trim(q)


def prem(a, b):
    """remainder of a mod monic b"""
    a = trim(a)
    b = trim(b)
    while len(a) >= len(b):
        c = a[-1]
        s = len(a) - len(b)
        for i, y in enumerate(b):
            a[s + i] -= c * y
        a = trim(a)
    return a


def mobius(n):
    r, k, p = 1, n, 2
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0:
                return 0
            r = -r
        p += 1
    if k > 1:
        r = -r
    return r


def totient(n):
    return sum(1 for k in range(1, n + 1) if gcd_(k, n) == 1)


def gcd_(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(n):
    return n >= 2 and all(n % q for q in range(2, int(n ** 0.5) + 1))


PHI = {}


def Phi(m):
    if m not in PHI:
        num, den = [1], [1]
        for d in range(1, m + 1):
            if m % d == 0:
                f = [-1] + [0] * (d - 1) + [1]
                mu = mobius(m // d)
                if mu == 1:
                    num = pmul(num, f)
                elif mu == -1:
                    den = pmul(den, f)
        # den is monic up to sign; make monic
        if den[-1] == -1:
            den = [-x for x in den]
            num = [-x for x in num]
        PHI[m] = pdiv_exact(num, den)
    return PHI[m]


def red(vec, m):
    """canonical form of sum vec[i] zeta_m^i: remainder mod Phi_m, padded to phi(m)"""
    r = prem(vec, Phi(m))
    deg = len(Phi(m)) - 1
    return tuple(r + [0] * (deg - len(r)))


def draw(S, m):
    v = [0] * m
    for i in S:
        v[i] -= 1
    return red(v, m), len(S)


def qrank(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    rank, col = 0, 0
    ncols = len(M[0]) if M else 0
    while rank < len(M) and col < ncols:
        piv = next((r for r in range(rank, len(M)) if M[r][col] != 0), None)
        if piv is None:
            col += 1
            continue
        M[rank], M[piv] = M[piv], M[rank]
        for r in range(len(M)):
            if r != rank and M[r][col] != 0:
                f = M[r][col] / M[rank][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[rank])]
        rank += 1
        col += 1
    return rank


out = []
P = lambda *a: out.append(" ".join(str(x) for x in a))

# ---------- E0: Phi_m degree = phi(m) ----------
for m in range(1, 13):
    ok(len(Phi(m)) - 1 == totient(m), f"E0 deg Phi_{m}")

# ---------- E1: rank K_m = m - phi(m); prime/1 kernel ----------
P("E1 m | phi(m) | rank image | rank K_m")
for m in range(1, 13):
    rows = [list(red([0] * i + [1], m)) for i in range(m)]
    rimg = qrank(rows) if rows[0] else 0
    rk = m - rimg
    ok(rk == m - totient(m), f"E1 rank K_{m}")
    P(" ", m, totient(m), rimg, rk)
# K_1: (1) maps to zeta_1^0 = 1, not 0
ok(red([1], 1) != red([0], 1), "E1b K_1 should be 0")
P("E1b m=1: image of (1) is", red([1], 1), "(nonzero) => K_1 = 0, NOT Z(1)")
for m in [2, 3, 5, 7, 11]:
    ok(red([1] * m, m) == red([0], m), f"E1c (1..1) in K_{m}")

# ---------- E2: counts, coincidence criterion, composite iff ----------
P("E2 m | 2^m | points | lost")
counts = {}
for m in range(1, 13):
    pts = defaultdict(list)
    subs = [frozenset(c) for k in range(m + 1) for c in combinations(range(m), k)]
    for S in subs:
        pts[draw(S, m)].append(S)
    lost = len(subs) - len(pts)
    counts[m] = (len(subs), len(pts), lost)
    P(" ", m, len(subs), len(pts), lost)
    ok((lost > 0) == (m > 1 and not is_prime(m)), f"E2 composite iff m={m}")
    # composite witness: two cosets of a proper nontrivial subgroup of order t
    if m > 1 and not is_prime(m):
        t = next(t for t in range(2, m) if m % t == 0)
        H = frozenset(range(0, m, m // t))
        H2 = frozenset((h + 1) % m for h in H)
        ok(H != H2 and draw(H, m) == draw(H2, m) and draw(H, m)[0] == red([0], m),
           f"E2 coset witness m={m}")
claimed = {4: (16, 15), 6: (64, 53), 8: (256, 189), 9: (512, 490), 10: (1024, 647)}
for m, (a, b) in claimed.items():
    ok(counts[m][:2] == (a, b), f"E2 claimed count m={m}")

# ---------- E3: antipode and Walsh, including m = 1 ----------
for m in range(1, 11):
    full = frozenset(range(m))
    anti = all(tuple(-x for x in draw(S, m)[0]) == draw(full - S, m)[0]
               and draw(full - S, m)[1] == m - len(S)
               for k in range(m + 1) for S in map(frozenset, combinations(range(m), k)))
    walsh = all(tuple(2 * x for x in draw(S, m)[0]) ==
                red([(-1 if i in S else 1) for i in range(m)], m)
                for k in range(m + 1) for S in map(frozenset, combinations(range(m), k)))
    P(f"E3 m={m}: antipode reflection holds: {anti}; 2*xy = sum zeta^i W_i holds: {walsh}")
    ok(anti == (m >= 2), f"E3 antipode m={m}")
    ok(walsh == (m >= 2), f"E3 walsh m={m}")

# ---------- E4: 30030 via route 2, Z[w] ----------
def wmul(x, y):
    a, b = x
    c, d = y
    # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2, w^2 = -1 - w
    return (a * c - b * d, a * d + b * c - b * d)


Z6 = [(1, 0)]
for _ in range(5):
    Z6.append(wmul(Z6[-1], (1, 1)))          # zeta_6 = 1 + w
ok(wmul(Z6[-1], (1, 1)) == (1, 0), "E4 zeta_6^6 = 1 in Z[w]")
ok(Z6[3] == (-1, 0), "E4 zeta_6^3 = -1")
PR = [2, 3, 5, 7, 11, 13]
pt = defaultdict(list)
for k in range(7):
    for c in combinations(range(6), k):
        d = 1
        xa = xb = 0
        for i in c:
            d *= PR[i]
            xa -= Z6[i][0]
            xb -= Z6[i][1]
        pt[((xa, xb), k)].append((d, frozenset(c)))
P("E4 30030 distinct points:", len(pt))
ok(len(pt) == 53, "E4 53 points")
lvl = {k: (sum(len(v) for (p, z), v in pt.items() if z == k), sum(1 for (p, z) in pt if z == k))
       for k in range(7)}
P("E4 per level:", lvl)
ok(lvl == {0: (1, 1), 1: (6, 6), 2: (15, 13), 3: (20, 13), 4: (15, 13), 5: (6, 6), 6: (1, 1)},
   "E4 per level")
spine = sorted(d for (p, z), v in pt.items() if p == (0, 0) for d, _ in v)
P("E4 spine divisors:", spine, "heights:", sorted(z for (p, z) in pt if p == (0, 0)))
ok(spine == [1, 14, 33, 65, 110, 273, 462, 910, 2145, 30030], "E4 spine")
lost_spine = sum(len(v) - 1 for (p, z), v in pt.items() if p == (0, 0))
lost_off = sum(len(v) - 1 for (p, z), v in pt.items() if p != (0, 0))
lost_l3 = sum(len(v) - 1 for (p, z), v in pt.items() if z == 3)
P("E4 points lost on spine:", lost_spine, " off spine:", lost_off, " at Omega=3:", lost_l3)
ok(lost_spine + lost_off == 11, "E4 total lost")
off_pairs = sorted(tuple(sorted(d for d, _ in v)) for (p, z), v in pt.items() if p != (0, 0) and len(v) > 1)
off_levels = sorted({z for (p, z), v in pt.items() if p != (0, 0) and len(v) > 1})
P("E4 off-spine groups:", off_pairs, "levels", off_levels)
ok(off_pairs == [(42, 195), (66, 130), (70, 165), (154, 715), (182, 429), (231, 455)], "E4 six off pairs")
ok(max(len(v) for v in pt.values()) == 3, "E4 multiplicity max 3")
# zero-sum subsets: disjoint unions of cosets of {0,3} and {0,2,4}
duads = [frozenset({i, i + 3}) for i in range(3)]
tris = [frozenset({0, 2, 4}), frozenset({1, 3, 5})]
cosets = duads + tris
disj_unions = set()
for k in range(len(cosets) + 1):
    for c in combinations(cosets, k):
        if all(a.isdisjoint(b) for a, b in combinations(c, 2)):
            disj_unions.add(frozenset().union(*c))
zero_sets = {S for (p, z), v in pt.items() if p == (0, 0) for _, S in v}
ok(zero_sets == disj_unions, "E4 zero-sum = disjoint unions of cosets")
nd = frozenset({0, 3}) | frozenset({0, 2, 4})
P("E4 non-disjoint union {0,3}u{0,2,4} =", sorted(nd), "is zero-sum:", nd in zero_sets)
ok(nd not in zero_sets, "E4 non-disjoint union not zero-sum")
# block swap via symmetric difference: A\B and B\A are distinct blocks of the same kind
for (p, z), v in pt.items():
    for (d, A), (e, B) in combinations(v, 2):
        a, b = A - B, B - A
        ok(a in cosets and b in cosets and len(a) == len(b) and a != b, f"E4 block swap {d},{e}")
# antipode in Z[w]
for (p, z), v in pt.items():
    for d, S in v:
        q = (-p[0], -p[1])
        ok(any(30030 // d == e for e, _ in pt[(q, 6 - z)]), f"E4 antipode {d}")
# saphir's k=2 reading: sum_{i in S} zeta^{2i} for the three duads
k2 = []
for D in duads:
    xa = xb = 0
    for i in D:
        xa += Z6[(2 * i) % 6][0]
        xb += Z6[(2 * i) % 6][1]
    k2.append((xa, xb))
P("E4 k=2 seat sums of duads {0,3},{1,4},{2,5}:", k2)
ok(len(set(k2)) == 3, "E4 k=2 separates duads")

# ---------- E5: height is frequency-0 Walsh data; xy alone does not separate spine ----------
# z = (m - sum_i W_i)/2 ; pairs equal in xy but different in z exist (spine)
ok(any(len({z for (p, z) in pt if p == (0, 0)}) > 1 for _ in [0]), "E5 spine has several heights")

# ---------- N1 (numerical, labelled): viewer reversal modes for squarefree ----------
def viewer(S, m, mode):
    x = y = 0.0
    for i in range(m):
        n, r, e = 2, 0.5, (1 if i in S else 0)
        phi = 2 * pi * i / m if m > 1 else 0.0
        w = 1 if mode == 'positive' else -1
        a = -1 if mode == 'global' else 1
        pu = a * phi
        ang = w * 2 * pi * e / n + pu
        x += r * (cos(ang) - cos(pu))
        y += r * (sin(ang) - sin(pu))
    return x, y


err_w = err_g = 0.0
for m in range(1, 11):
    for k in range(m + 1):
        for S in combinations(range(m), k):
            px, py = viewer(S, m, 'positive')
            wx, wy = viewer(S, m, 'winding')
            gx, gy = viewer(S, m, 'global')
            err_w = max(err_w, abs(px - wx), abs(py - wy))
            err_g = max(err_g, abs(px - gx), abs(py + gy))
P(f"N1 numerical: max|winding - positive| = {err_w:.2e}; max|global - conj(positive)| = {err_g:.2e}")
ok(err_w < 1e-12 and err_g < 1e-12, "N1 modes")

P("FAILURES:", len(FAIL), sorted(set(FAIL)))
print("\n".join(out))
