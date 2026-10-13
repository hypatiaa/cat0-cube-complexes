"""Independent exact check (delta verifier) of NOTE v0.1.7 section 7.6 G-claims.
Standard library only; does not import or copy check_v0_1_7_o6.py.

Representation: an element of Q(zeta_L) scaled by a common integer D is an integer
polynomial reduced modulo Phi_L (monic, so integer remainder). Phi_L comes from the
Moebius product formula. Positions use the viewer formula in mode 'positive':
pos(d) = sum_j (1/n_j) zeta_m^j (zeta_{n_j}^{e_j} - 1), z = sum_j e_j, primes ascending.
"""
from fractions import Fraction
from itertools import product, combinations
from math import gcd
from collections import defaultdict
import sys

def lcm(a, b): return a // gcd(a, b) * b

def factorize(n):
    out = []; p = 2
    while p * p <= n:
        a = 0
        while n % p == 0: n //= p; a += 1
        if a: out.append((p, a))
        p += 1 if p == 2 else 2
    if n > 1: out.append((n, 1))
    return out

def mobius(n):
    f = factorize(n)
    if any(a > 1 for _, a in f): return 0
    return -1 if len(f) % 2 else 1

def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r

def pdiv_exact(a, b):  # b monic integer
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for s in range(len(a) - len(b), -1, -1):
        c = a[s + len(b) - 1]
        q[s] = c
        for i, y in enumerate(b): a[s + i] -= c * y
    assert not any(a)
    return q

_phi = {}
def Phi(L):
    if L in _phi: return _phi[L]
    num, den = [1], [1]
    for d in range(1, L + 1):
        if L % d == 0:
            mu = mobius(L // d)
            f = [-1] + [0] * (d - 1) + [1]
            if mu == 1: num = pmul(num, f)
            elif mu == -1: den = pmul(den, f)
    r = pdiv_exact(num, den)
    _phi[L] = r
    return r

def reduce(poly, L):
    """poly: dict exponent->int (mod x^L - 1 folded); reduce mod Phi_L, integer remainder."""
    a = [0] * L
    for k, c in poly.items(): a[k % L] += c
    P = Phi(L); deg = len(P) - 1
    for s in range(L - 1, deg - 1, -1):
        c = a[s]
        if c:
            for i, y in enumerate(P): a[s - deg + i] -= c * y
    return tuple(a[:deg])

class Atom:
    def __init__(self, fac):
        self.fac = fac; self.m = len(fac)
        self.ns = [a + 1 for _, a in fac]
        L = self.m
        for n in self.ns: L = lcm(L, n)
        self.L = L
        D = 1
        for n in self.ns: D = lcm(D, n)
        self.D = D
    def pos(self, e):
        L, m, D = self.L, self.m, self.D
        poly = defaultdict(int)
        for j, n in enumerate(self.ns):
            c = D // n; base = (L // m) * j
            poly[base + (L // n) * e[j]] += c
            poly[base] -= c
        return reduce(poly, L), sum(e)
    def edges(self):
        """edge vector of H(p_j,k) as a reduced integer tuple (scaled by D), with labels"""
        out = []
        L, m, D = self.L, self.m, self.D
        for j, (p, a) in enumerate(self.fac):
            n = a + 1; c = D // n; base = (L // m) * j
            for k in range(1, a + 1):
                poly = defaultdict(int)
                poly[base + (L // n) * k] += c
                poly[base + (L // n) * (k - 1)] -= c
                out.append(((p, k), j, n, reduce(poly, L)))
        return out
    def exps(self):
        return list(product(*[range(a + 1) for _, a in self.fac]))
    def hyp(self, e):
        return tuple(1 if e[j] >= k else 0 for j, (p, a) in enumerate(self.fac) for k in range(1, a + 1))
    def div(self, e):
        d = 1
        for (p, a), x in zip(self.fac, e): d *= p ** x
        return d

def qrank(rows):
    rows = [[Fraction(x) for x in r] for r in rows]
    rk = 0; nc = len(rows[0]) if rows else 0
    for c in range(nc):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c] / rows[rk][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk

def classes(A):
    pts = defaultdict(list)
    for e in A.exps(): pts[A.pos(e)].append(e)
    return pts

fails = []
def ok(c, msg):
    print(("PASS " if c else "FAIL ") + msg)
    if not c: fails.append(msg)

# ---------- table (all 26 atoms) ----------
CASES = [4, 8, 16, 12, 18, 36, 72, 24, 48, 108, 200, 60, 180, 360, 900, 420, 1260, 6300,
         4620, 13860, 30030, 60060, 120120, 900900, 216, 7776]
print("N | m | Omega | rk ker w | rk ker(w,z) | divisors | points | lost | maxmult | resonant pairs")
T = {}
for N in CASES:
    A = Atom(factorize(N)); E = A.edges()
    pts = classes(A)
    W = [w for _, _, _, w in E]
    rk = len(W) - qrank(W)
    rkz = len(W) - qrank([list(w) + [A.D] for w in W])  # height step scaled by D too
    ndiv = len(A.exps()); npts = len(pts)
    mm = max(len(v) for v in pts.values())
    res = [(E[i][0], E[k][0]) for i, k in combinations(range(len(E)), 2) if E[i][3] == E[k][3]]
    T[N] = (A.m, len(W), rk, rkz, ndiv, npts, ndiv - npts, mm, res)
    print(N, *T[N], sep=" | ")

# ---------- G1 family proof instance + sweep ----------
for n in (4, 6, 8, 10, 12, 14):
    a = n - 1
    A = Atom([(2, a), (3, a)]); E = {lab: w for lab, _, _, w in A.edges()}
    ok(E[(2, 1 + n // 2)] == E[(3, 1)] and E[(2, 1)] == E[(3, 1 + n // 2)],
       f"G1 family n={n}: w(H(p,1+n/2)) = w(H(q,1)) and w(H(p,1)) = w(H(q,1+n/2))")
    P = A.pos
    e1 = (1 + n // 2, 0); e2 = (n // 2, 1)
    ok(P(e1) == P(e2), f"G1 family n={n}: p^(1+n/2) ~ p^(n/2) q")
sweep = {}
for a in range(1, 15):
    for b in range(1, 15):
        A = Atom([(2, a), (3, b)])
        pts = classes(A)
        sweep[(a, b)] = (a + 1) * (b + 1) - len(pts)
bad = [(a, b) for (a, b), l in sweep.items() if (l > 0) != (a == b and a % 2 == 1 and a >= 3)]
ok(not bad, f"G1 sweep a,b<=14: non-injective iff a=b odd>=3 (exceptions: {bad})")
print("  losses at (a,a), a=1..14:", [sweep[(a, a)] for a in range(1, 15)])
ok([sweep[(a, a)] for a in (3, 5, 7, 9)] == [2, 6, 12, 20], "G1 losses 2,6,12,20 at a=3,5,7,9")
# prime-independence of POSITIONS (not only loss counts), several prime pairs, all a,b<=6
pi_ok = True
for a in range(1, 7):
    for b in range(1, 7):
        base = Atom([(2, a), (3, b)])
        for (p, q) in ((5, 7), (11, 13), (3, 101)):
            other = Atom([(p, a), (q, b)])
            for e in base.exps():
                if base.pos(e) != other.pos(e): pi_ok = False
ok(pi_ok, "G1 m=2 positions identical for prime pairs (2,3),(5,7),(11,13),(3,101), a,b<=6")
# 216 classes
A216 = Atom(factorize(216)); c216 = sorted(sorted(A216.div(e) for e in v) for v in classes(A216).values() if len(v) > 1)
ok(c216 == [[8, 12], [18, 27]], f"G1 216 classes {c216}")

# ---------- G2: 900900 ----------
A9 = Atom(factorize(900900)); E9 = A9.edges(); W9 = {lab: w for lab, _, _, w in E9}
dif = lambda u, v: tuple(x - y for x, y in zip(u, v))
# -zeta_3 scaled by D: zeta_3 = x^(L/3)
mz3 = reduce({A9.L // 3: -A9.D}, A9.L)
ok(dif(W9[(5, 1)], W9[(2, 1)]) == mz3 == dif(W9[(7, 1)], W9[(11, 1)]), "G2 w51-w21 = -zeta3 = w71-w111")
pts9 = classes(A9)
cls9 = [v for v in pts9.values() if len(v) > 1]
ok(any(sorted(A9.div(e) for e in v) == [14, 55] for v in cls9), "G2 {14,55} is a class")
lost9 = 216 - len(pts9)
print("  900900 lost:", lost9, " class sizes:", sorted(len(v) for v in cls9))

def merges(A, cls, moves):
    """moves: list of integer hyperplane-coordinate vectors delta. Build graph on all divisors:
    h -> h + delta when the result is a valid divisor (down-sets). Count merges inside classes."""
    ex = A.exps(); H = {A.hyp(e): e for e in ex}
    parent = {e: e for e in ex}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for h, e in H.items():
        for d in moves:
            h2 = tuple(x + y for x, y in zip(h, d))
            if h2 in H:
                a, b = find(e), find(H[h2])
                if a != b: parent[a] = b
    tot = 0
    for v in cls:
        tot += len(v) - len({find(e) for e in v})
    return tot

def resonance_moves(A):
    E = A.edges(); n = len(E); mv = []
    for i, k in combinations(range(n), 2):
        if E[i][3] == E[k][3]:
            d = [0] * n; d[i] = 1; d[k] = -1; mv.append(tuple(d)); mv.append(tuple(-x for x in d))
    return mv

def squarefree_block_moves(A):
    """all height-zero {-1,0,1} moves supported on squarefree seats with w.delta = 0 (superset of block swaps)"""
    E = A.edges(); n = len(E)
    sf = [i for i, (lab, j, nn, w) in enumerate(E) if nn == 2]
    mv = []
    for vals in product((-1, 0, 1), repeat=len(sf)):
        if not any(vals) or sum(vals) != 0: continue
        s = [0] * len(E[0][3])
        for i, c in zip(sf, vals):
            s = [x + c * y for x, y in zip(s, E[i][3])]
        if not any(s):
            d = [0] * n
            for i, c in zip(sf, vals): d[i] = c
            mv.append(tuple(d))
    return mv

rm9 = resonance_moves(A9); bm9 = squarefree_block_moves(A9)
r_res = merges(A9, cls9, rm9); r_blk = merges(A9, cls9, bm9); r_both = merges(A9, cls9, rm9 + bm9)
print(f"  900900: resonance moves {len(rm9)//2}, squarefree block moves {len(bm9)}")
ok(lost9 == 64 and r_res == 24, f"G2 900900: 64 lost, chains of single resonance swaps reach {r_res}")
ok(r_blk == 0, f"G2 900900: squarefree blocks reach {r_blk}")
ok(r_both == 24 and lost9 - r_both == 40, f"G2 900900: resonance+block chains combined reach {r_both}; not reached {lost9 - r_both}")

# Q-span test (checker's 60 pairs)
nH = len(E9)
span_rows = [list(d) for d in rm9[::2]] + [list(d) for d in bm9]
base_rk = qrank(span_rows) if span_rows else 0
outside = 0; npairs = 0
for v in cls9:
    for e, f in combinations(v, 2):
        npairs += 1
        d = [x - y for x, y in zip(A9.hyp(e), A9.hyp(f))]
        if qrank(span_rows + [d]) > base_rk: outside += 1
print(f"  900900: coincident pairs {npairs}, outside Q-span(resonance + squarefree height-0 kernel moves): {outside}")

# ---------- G3: 7776 ----------
A7 = Atom(factorize(7776)); pts7 = classes(A7); cls7 = [v for v in pts7.values() if len(v) > 1]
c7 = sorted(sorted(A7.div(e) for e in v) for v in cls7)
print("  7776 classes:", c7)
r7 = merges(A7, cls7, resonance_moves(A7))
ok(36 - len(pts7) == 6 and [108, 243] in c7 and [32, 72] in c7 and r7 == 4, f"G3 7776: 6 lost, single swaps reach {r7}")
# delta 243 - 108
e108 = (2, 3); e243 = (0, 5)
lab7 = [lab for lab, _, _, _ in A7.edges()]
d = {lab7[i]: x - y for i, (x, y) in enumerate(zip(A7.hyp(e243), A7.hyp(e108))) if x != y}
ok(d == {(3, 4): 1, (3, 5): 1, (2, 1): -1, (2, 2): -1}, f"G3 delta(243-108) = {d}")
# 900: all 9 losses by resonance swaps
A900 = Atom(factorize(900)); p900 = classes(A900); cl900 = [v for v in p900.values() if len(v) > 1]
ok(merges(A900, cl900, resonance_moves(A900)) == 9, "G2 900: 9 by resonance")

# ---------- G4: one non-squarefree seat fixed (60060, 120120, plus extra atoms) ----------
for N in (60060, 120120, 4620, 13860 // 3 * 1, 2 ** 4 * 3 * 5 * 7 * 11 * 13, 3 ** 2 * 2 * 5 * 7 * 11 * 13):
    A = Atom(factorize(N)); ns = [j for j, n in enumerate(A.ns) if n >= 3]
    if len(ns) != 1: continue
    cl = [v for v in classes(A).values() if len(v) > 1]
    ok(all(len({e[ns[0]] for e in v}) == 1 for v in cl), f"G4 N={N}: single non-squarefree seat fixed in all {len(cl)} classes")
# G4 algebraic-integer lemma: (zeta_n^t - 1)/n is not integral for n>=3, t != 0 mod n:
# norm test N((zeta_d-1)/n) = N(zeta_d - 1)/n^phi(d) must be a non-integer
def euler_phi(n): return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
lemma = True
for n in range(3, 60):
    for t in range(1, n):
        dd = n // gcd(n, t)
        f = factorize(dd)
        Nz = f[0][0] if len(f) == 1 else 1     # |Phi_d(1)|
        if dd == 2: Nz = 2
        val = Fraction(Nz, n ** euler_phi(dd))
        if val.denominator == 1: lemma = False
ok(lemma, "G4 lemma: |N((zeta_d - 1)/n)| is non-integral for all 3<=n<60, d|n, d>1")
# cross-check |Phi_d(1)| from the actual polynomial
ok(all(abs(sum(Phi(dd))) == (factorize(dd)[0][0] if len(factorize(dd)) == 1 else 1) for dd in range(2, 60)), "Phi_d(1) = p or 1")

# ---------- G5 ----------
A36 = Atom(factorize(36)); E36 = [w for _, _, _, w in A36.edges()]
v = [a - b + c - dd for a, b, c, dd in zip(*E36)]
ok(not any(v) and T[36][6] == 0 and T[36][3] == 1, "G5 36: (1,-1,1,-1) in ker, injective, rk ker(w,z)=1")

# ---------- G7/G8 counts ----------
g7 = sum(len(Atom(factorize(N)).edges()) * (len(Atom(factorize(N)).edges()) - 1) // 2 for N in CASES)
print("  hyperplane pairs over all 26 atoms (G7 executions):", g7)
# G8 sufficiency for n >= 3 (existence of k,k' given anchor gap multiple of 1/n), exhaustive small
suff = True
for n in range(2, 30):
    for c in range(1, n):  # gap*n mod n, nonzero for distinct seats
        exists = any((k - kp - c) % n == 0 for k in range(1, n) for kp in range(1, n))
        if exists != (n >= 3): suff = False
ok(suff, "G8: for gap c != 0 mod n, some k,k' in 1..n-1 resonate iff n >= 3 (n<30)")

print("FAILURES:", len(fails))
for f in fails: print("  ", f)
