"""Independent exact re-check of NOTE v0.1.6 section 7.6 (O6), mode 'positive'.

Written independently of check_v0_1_6_o6.py. Standard library only.
Arithmetic: positions are scaled by D = lcm(n_j) so they live in Z[zeta_L], L = lcm(m, n_j).
Elements are integer coefficient vectors mod Phi_L; Phi_L is built from the Moebius product
Phi_L = prod_{d|L} (x^d - 1)^{mu(L/d)} (a different construction from the note's script).
"""
import sys
from fractions import Fraction
from itertools import product, combinations
from math import gcd, cos, sin, pi
from collections import defaultdict

out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

FAIL = []
def expect(cond, msg):
    if not cond:
        FAIL.append(msg)
        say("  EXPECTATION FAILED:", msg)

def lcm(a, b):
    return a * b // gcd(a, b)

def factor(n):
    res = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            a = 0
            while n % p == 0:
                n //= p; a += 1
            res.append((p, a))
        p += 1 if p == 2 else 2
    if n > 1:
        res.append((n, 1))
    return res

def mobius(n):
    f = factor(n)
    if any(a > 1 for _, a in f):
        return 0
    return -1 if len(f) % 2 else 1

# integer polynomials, low degree first
def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r

def pdiv_exact(a, b):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    for s in range(len(a) - len(b), -1, -1):
        c = a[s + len(b) - 1]
        assert c % b[-1] == 0
        c //= b[-1]
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] -= c * y
    assert not any(a), "inexact division"
    return q

_PHI = {}
def Phi(L):
    if L not in _PHI:
        num, den = [1], [1]
        for d in range(1, L + 1):
            if L % d == 0:
                mu = mobius(L // d)
                xd = [-1] + [0] * (d - 1) + [1]
                if mu == 1:
                    num = pmul(num, xd)
                elif mu == -1:
                    den = pmul(den, xd)
        _PHI[L] = pdiv_exact(num, den)
    return _PHI[L]

def reduce_mod(vec, L):
    """vec: length-L integer coefficients of sum c_k zeta_L^k. Return canonical tuple mod Phi_L."""
    ph = Phi(L)
    deg = len(ph) - 1
    a = list(vec)
    for s in range(len(a) - 1, deg - 1, -1):
        c = a[s]
        if c:
            for i, y in enumerate(ph):
                a[s - deg + i] -= c * y
    return tuple(a[:deg])

class Atom:
    def __init__(self, fac):
        self.fac = fac
        self.m = len(fac)
        self.ns = [a + 1 for _, a in fac]
        L = max(self.m, 1)
        D = 1
        for n in self.ns:
            L = lcm(L, n); D = lcm(D, n)
        self.L, self.D = L, D
        # hyperplanes: (j, k)
        self.hyp = [(j, k) for j, (p, a) in enumerate(fac) for k in range(1, a + 1)]
        self.lab = [(fac[j][0], k) for j, k in self.hyp]
        self.w = [self.edge(j, k) for j, k in self.hyp]

    def anchor(self, j):
        return (self.L // max(self.m, 1)) * j  # zeta_m^j = zeta_L^{(L/m) j}; m=1 -> 0

    def mono(self, e, coeff):
        v = [0] * self.L
        v[e % self.L] += coeff
        return v

    def pos(self, exps):
        v = [0] * self.L
        for j, e in enumerate(exps):
            n = self.ns[j]
            c = self.D // n
            v[(self.anchor(j) + (self.L // n) * e) % self.L] += c
            v[self.anchor(j) % self.L] -= c
        return reduce_mod(v, self.L), sum(exps)

    def edge(self, j, k):
        n = self.ns[j]
        c = self.D // n
        v = [0] * self.L
        v[(self.anchor(j) + (self.L // n) * k) % self.L] += c
        v[(self.anchor(j) + (self.L // n) * (k - 1)) % self.L] -= c
        return reduce_mod(v, self.L)

    def hcoord(self, exps):
        return tuple(1 if exps[j] >= k else 0 for j, k in self.hyp)

    def divisors(self):
        return list(product(*[range(a + 1) for _, a in self.fac]))

    def value(self, exps):
        d = 1
        for (p, _), e in zip(self.fac, exps):
            d *= p ** e
        return d

def vadd(a, b, c=1):
    return tuple(x + c * y for x, y in zip(a, b))

def comb(vecs, coeffs, dim):
    s = (0,) * dim
    for v, c in zip(vecs, coeffs):
        if c:
            s = vadd(s, v, c)
    return s

def rank(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    if not M:
        return 0
    rk, ncol = 0, len(M[0])
    for col in range(ncol):
        piv = None
        for r in range(rk, len(M)):
            if M[r][col] != 0:
                piv = r; break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][col] != 0:
                f = M[r][col] / M[rk][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[rk])]
        rk += 1
    return rk

def nullspace(cols_as_rows):
    """Given vectors v_1..v_r (each a tuple), return a basis of {c in Q^r : sum c_i v_i = 0}."""
    r = len(cols_as_rows)
    if r == 0:
        return []
    dim = len(cols_as_rows[0])
    # matrix A (dim x r), A[:, i] = v_i
    A = [[Fraction(cols_as_rows[i][t]) for i in range(r)] for t in range(dim)]
    pivcols, rk = [], 0
    for col in range(r):
        piv = None
        for row in range(rk, dim):
            if A[row][col] != 0:
                piv = row; break
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        pv = A[rk][col]
        A[rk] = [x / pv for x in A[rk]]
        for row in range(dim):
            if row != rk and A[row][col] != 0:
                f = A[row][col]
                A[row] = [x - f * y for x, y in zip(A[row], A[rk])]
        pivcols.append(col); rk += 1
    free = [c for c in range(r) if c not in pivcols]
    basis = []
    for fc in free:
        v = [Fraction(0)] * r
        v[fc] = Fraction(1)
        for i, pc in enumerate(pivcols):
            v[pc] = -A[i][fc]
        basis.append(v)
    return basis

def in_span(vec, basis):
    if not basis:
        return not any(vec)
    return rank(basis) == rank(basis + [list(vec)])

def float_viewer(atom, exps):
    # own transcription of divisorPosition, chirality 'positive' (file 5, lines 1445-1465)
    m = atom.m
    x = y = z = 0.0
    for i, (p, a) in enumerate(atom.fac):
        n = a + 1; r = 1 / n; e = exps[i]
        phi = (2 * pi * i) / m if m > 1 else 0
        ang = (2 * pi * e) / n + phi
        x += r * (cos(ang) - cos(phi)); y += r * (sin(ang) - sin(phi)); z += e
    return x, y, z

def to_c(atom, t):
    zL = complex(cos(2 * pi / atom.L), sin(2 * pi / atom.L))
    return sum(c * zL ** k for k, c in enumerate(t)) / atom.D

def resonance_formula(atom, a, b):
    (j, k), (j2, k2) = atom.hyp[a], atom.hyp[b]
    if j == j2:
        return False
    n, n2, m = atom.ns[j], atom.ns[j2], max(atom.m, 1)
    if n != n2:
        return False
    # j/m + (k-1)/n == j2/m + (k2-1)/n mod 1  <=>  j n + (k-1) m == j2 n + (k2-1) m mod m n
    return (j * n + (k - 1) * m - j2 * n - (k2 - 1) * m) % (m * n) == 0

def analyse(fac, verbose=True, mech=True):
    A = Atom(fac)
    divs = A.divisors()
    dim = len(A.w[0]) if A.w else 0
    pts = defaultdict(list)
    maxerr = 0.0
    lin_ok = True
    for e in divs:
        P = A.pos(e)
        pts[P].append(e)
        h = A.hcoord(e)
        if comb(A.w, h, dim) != P[0] or sum(h) != P[1]:
            lin_ok = False
        X, Y, Z = float_viewer(A, e)
        c = to_c(A, P[0])
        maxerr = max(maxerr, abs(X - c.real), abs(Y - c.imag), abs(Z - P[1]))
    # edge check: every edge dual to H(j,k) drawn as w_{j,k}
    edge_ok = True
    for idx, (j, k) in enumerate(A.hyp):
        for e in divs:
            if e[j] == k - 1:
                e2 = list(e); e2[j] = k
                if vadd(A.pos(tuple(e2))[0], A.pos(e)[0], -1) != A.w[idx]:
                    edge_ok = False
    rk_w = rank([list(v) for v in A.w]) if A.w else 0
    rk_wz = rank([list(v) + [1] for v in A.w]) if A.w else 0
    Om = len(A.hyp)
    classes = [v for v in pts.values() if len(v) > 1]
    lost = len(divs) - len(pts)
    maxmult = max((len(v) for v in pts.values()), default=1)
    # resonance pairs (direct equality) vs formula
    res_pairs = [(a, b) for a, b in combinations(range(Om), 2)
                 if A.hyp[a][0] != A.hyp[b][0] and A.w[a] == A.w[b]]
    form_pairs = [(a, b) for a, b in combinations(range(Om), 2) if resonance_formula(A, a, b)]
    same_prime_equal = [(a, b) for a, b in combinations(range(Om), 2)
                        if A.hyp[a][0] == A.hyp[b][0] and A.w[a] == A.w[b]]
    row = dict(N=None, fac=fac, m=A.m, Omega=Om, ker_w=Om - rk_w, ker_wz=Om - rk_wz,
               divisors=len(divs), points=len(pts), lost=lost, maxmult=maxmult,
               lin_ok=lin_ok, edge_ok=edge_ok, maxerr=maxerr,
               res=[(A.lab[a], A.lab[b]) for a, b in res_pairs],
               res_formula_agrees=(res_pairs == form_pairs), same_prime_equal=same_prime_equal,
               A=A, pts=pts, classes=classes)
    # kernel criterion over all pairs
    if len(divs) <= 600:
        crit_ok = True
        H = {e: A.hcoord(e) for e in divs}
        P = {e: A.pos(e) for e in divs}
        for e, f in combinations(divs, 2):
            dl = [x - y for x, y in zip(H[e], H[f])]
            ink = comb(A.w, dl, dim) == (0,) * dim and sum(dl) == 0
            if (P[e] == P[f]) != ink:
                crit_ok = False
        row['crit_ok'] = crit_ok
    if mech and classes:
        row.update(mechanisms(A, classes, res_pairs))
    return row

def mechanisms(A, classes, res_pairs):
    Om = len(A.hyp)
    dim = len(A.w[0])
    S = [i for i, (j, k) in enumerate(A.hyp) if A.ns[j] == 2]  # squarefree-seat hyperplanes
    # zero-sum blocks among S
    zblocks = []
    for r in range(1, len(S) + 1):
        for B in combinations(S, r):
            if comb([A.w[i] for i in B], [1] * r, dim) == (0,) * dim:
                zblocks.append(frozenset(B))
    strict_moves = set()
    for B, B2 in combinations(zblocks, 2):
        if len(B) == len(B2) and not (B & B2):
            v = [0] * Om
            for i in B: v[i] += 1
            for i in B2: v[i] -= 1
            strict_moves.add(tuple(v)); strict_moves.add(tuple(-x for x in v))
    res_moves = set()
    for a, b in res_pairs:
        v = [0] * Om; v[a] = 1; v[b] = -1
        res_moves.add(tuple(v)); res_moves.add(tuple(-x for x in v))
    # loose squarefree kernel subspace (in full coordinates)
    ns = nullspace([list(A.w[i]) + [1] for i in S]) if S else []
    Zloose = []
    for v in ns:
        full = [Fraction(0)] * Om
        for c, i in zip(v, S): full[i] = c
        Zloose.append(full)
    Rvecs = [[Fraction(x) for x in v] for v in res_moves]
    span_RZ = Rvecs + Zloose

    def is_loose_move(d):
        if any(d[i] for i in range(Om) if i not in S):
            return False
        return comb(A.w, d, dim) == (0,) * dim and sum(d) == 0

    def components(members, allow):
        parent = list(range(len(members)))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        H = [A.hcoord(e) for e in members]
        for a, b in combinations(range(len(members)), 2):
            d = tuple(x - y for x, y in zip(H[a], H[b]))
            if allow(d):
                parent[find(a)] = find(b)
        return len({find(x) for x in range(len(members))})

    lost_total = sum(len(c) - 1 for c in classes)
    exp_strict = exp_loose = exp_R = exp_Zstrict = exp_span = 0
    unexplained = []
    for c in classes:
        cs = components(c, lambda d: d in res_moves or d in strict_moves)
        cl = components(c, lambda d: d in res_moves or is_loose_move(d))
        cr = components(c, lambda d: d in res_moves)
        cz = components(c, lambda d: d in strict_moves)
        exp_strict += len(c) - cs
        exp_loose += len(c) - cl
        exp_R += len(c) - cr
        exp_Zstrict += len(c) - cz
        # span test: every pair difference in span(R + Zloose)?
        H = [A.hcoord(e) for e in c]
        all_span = True
        for a, b in combinations(range(len(c)), 2):
            d = [x - y for x, y in zip(H[a], H[b])]
            if not in_span(d, span_RZ):
                all_span = False
                unexplained.append(([A.value(c[a]), A.value(c[b])],
                                    {A.lab[i]: d[i] for i in range(Om) if d[i]}))
        if all_span:
            exp_span += len(c) - 1
    return dict(lost_total=lost_total, explained_R=exp_R, explained_Zstrict=exp_Zstrict,
                explained_R_Zstrict_path=exp_strict, explained_R_Zloose_path=exp_loose,
                classes_in_span=exp_span, unexplained_pairs=unexplained,
                zero_sum_blocks=[sorted(A.lab[i] for i in B) for B in zblocks])

def fac_str(fac):
    return "*".join(f"{p}^{a}" if a > 1 else str(p) for p, a in fac)

# ---------------- Section E: the test table ----------------
CASES = [4, 8, 16, 12, 18, 24, 36, 48, 72, 108, 200, 60, 180, 360, 900, 420, 1260, 6300,
         4620, 13860, 30030, 60060, 120120, 900900]
say("=== E. Test table (own exact computation) ===")
say("N | fac | m | Omega | rank ker w | rank ker (w,z) | divisors | points | lost | maxmult | L1 lin | L2 edge | L3 crit | float err")
rows = {}
for N in CASES:
    r = analyse(factor(N))
    r['N'] = N
    rows[N] = r
    say(N, "|", fac_str(r['fac']), "|", r['m'], "|", r['Omega'], "|", r['ker_w'], "|", r['ker_wz'], "|",
        r['divisors'], "|", r['points'], "|", r['lost'], "|", r['maxmult'], "|", r['lin_ok'], "|",
        r['edge_ok'], "|", r.get('crit_ok'), "|", f"{r['maxerr']:.2e}")
    expect(r['lin_ok'] and r['edge_ok'] and r.get('crit_ok', True), f"linearity/edge/criterion N={N}")

# expected values transcribed from NOTE.md section 7.6.6 table (the note, not file 2)
NOTE_TABLE = {
    4: (1, 2, 3, 3, 0, 1), 8: (1, 3, 4, 4, 0, 1), 16: (1, 4, 5, 5, 0, 1),
    60: (3, 4, 12, 12, 0, 1), 180: (3, 5, 18, 16, 2, 2), 360: (3, 6, 24, 24, 0, 1),
    900: (3, 6, 27, 18, 9, 4), 30030: (6, 6, 64, 53, 11, 3), 60060: (6, 7, 96, 90, 6, 2),
    120120: (6, 8, 128, 120, 8, 2), 900900: (6, 9, 216, 152, 64, 4),
}
NOTE_KER = {4: 0, 8: 1, 16: 0, 60: 2, 180: 3, 360: 3, 900: 4, 30030: 4, 60060: 5, 120120: 5, 900900: 7}
for N, t in NOTE_TABLE.items():
    r = rows[N]
    expect((r['m'], r['Omega'], r['divisors'], r['points'], r['lost'], r['maxmult']) == t, f"table row {N}")
    expect(r['ker_w'] == NOTE_KER[N], f"ker rank {N}")
# grouped rows
for N in [12, 18, 24, 36, 48, 72, 108, 200]:
    r = rows[N]
    expect(r['m'] == 2 and 3 <= r['Omega'] <= 5 and 1 <= r['ker_w'] <= 2 and 6 <= r['divisors'] <= 12 and r['lost'] == 0, f"m=2 group {N}")
for N in [420, 1260, 6300]:
    r = rows[N]
    expect(r['m'] == 4 and 5 <= r['Omega'] <= 7 and 2 <= r['ker_w'] <= 3 and r['lost'] == 0, f"m=4 group {N}")
expect([rows[N]['divisors'] for N in [420, 1260, 6300]] == [24, 36, 54], "m=4 divisors")
for N in [4620, 13860]:
    r = rows[N]
    expect(r['m'] == 5 and r['ker_w'] == 1 and r['lost'] == 0, f"m=5 group {N}")
expect([rows[N]['Omega'] for N in [4620, 13860]] == [6, 7] and [rows[N]['divisors'] for N in [4620, 13860]] == [48, 72], "m=5 omega/divisors")

say("")
say("=== D. Resonant pairs (direct equality of edge vectors, distinct primes) ===")
for N in CASES:
    r = rows[N]
    if r['res']:
        say(N, r['res'])
    expect(r['res_formula_agrees'], f"resonance formula agrees N={N}")
    expect(not r['same_prime_equal'], f"no equal edge vectors within one prime N={N}")
say("formula j/m+(k-1)/n == j'/m+(k'-1)/n (mod 1) with n_j=n_j' agrees with direct equality on all test atoms:",
    all(rows[N]['res_formula_agrees'] for N in CASES))

say("")
say("=== B. 8 = 2^3 ===")
A8 = rows[8]['A']
s = vadd(A8.w[0], A8.w[2])
say("w_1 + w_3 =", s, "(zero:", not any(s), ")", "; rank ker w =", rows[8]['ker_w'], "; rank ker (w,z) =", rows[8]['ker_wz'])
say("atoms with ker(w,z) != 0 and lost = 0 (true illustrations of the down-set constraint):",
    [N for N in CASES if rows[N]['ker_wz'] > 0 and rows[N]['lost'] == 0])

say("")
say("=== E. Mechanism analysis for atoms with coincidences ===")
for N in CASES:
    r = rows[N]
    if r['lost'] == 0:
        continue
    say(f"N={N} ({fac_str(r['fac'])}): lost={r['lost_total']}; explained by: R alone={r['explained_R']}, "
        f"strict zero-sum block swaps alone={r['explained_Zstrict']}, R+strict (path)={r['explained_R_Zstrict_path']}, "
        f"R+loose squarefree kernel (path)={r['explained_R_Zloose_path']}, classes whose pair differences lie in Q-span(R+Zloose): lost-count {r['classes_in_span']}")
    say("   squarefree zero-sum blocks:", r['zero_sum_blocks'])
    # list coincidence classes as divisors
    cls = sorted(sorted(r['A'].value(e) for e in c) for c in r['classes'])
    if len(cls) <= 16:
        say("   classes:", cls)
    else:
        say("   number of classes:", len(cls), "; sizes:", sorted((len(c) for c in cls), reverse=True)[:10], "...")
    if r['unexplained_pairs']:
        say("   pairs NOT in span(R + squarefree kernel):", len(r['unexplained_pairs']))
        for x in r['unexplained_pairs'][:8]:
            say("     ", x)

# 7.6.5 claims on 60060 and 120120 duads
for N in [60060, 120120]:
    A = rows[N]['A']
    cls = [sorted(A.value(e) for e in c) for c in rows[N]['classes']]
    say(N, "contains class [33, 65]:", [33, 65] in cls)

say("")
say("=== D. |w| = (2/n) sin(pi/n) strictly decreasing for n = 2..2000 (float) ===")
vals = [2 / n * sin(pi / n) for n in range(2, 2001)]
say(all(a > b for a, b in zip(vals, vals[1:])))

say("")
say("=== O7 probe: m = 2, N = p^a q^b, p<q<=13, 1<=a,b<=5 ===")
primes = [2, 3, 5, 7, 11, 13]
bad = []
total = 0
for p, q in combinations(primes, 2):
    for a in range(1, 6):
        for b in range(1, 6):
            r = analyse([(p, a), (q, b)], mech=False)
            total += 1
            if r['lost']:
                cls = sorted(sorted(r['A'].value(e) for e in c) for c in r['classes'])
                bad.append((p, a, q, b, r['lost'], cls[:3], r['res']))
say("atoms tested:", total, "; non-injective:", len(bad))
seen = set()
for x in bad:
    if (x[1], x[3]) not in seen:
        seen.add((x[1], x[3]))
        say(f"  exponents (a,b)=({x[1]},{x[3]}) e.g. {x[0]}^{x[1]}*{x[2]}^{x[3]}: lost {x[4]}, first classes {x[5]}, resonant pairs {x[6]}")
say("exponent patterns with coincidences:", sorted(seen))

say("")
say("=== O7 extended: m = 2, exponents 1<=a,b<=14 (positions depend only on (a,b)) ===")
pat = []
unexpl = []
for a in range(1, 15):
    for b in range(1, 15):
        r = analyse([(2, a), (3, b)], mech=True)
        if r['lost']:
            pat.append((a, b, r['lost']))
            if r.get('unexplained_pairs') or r['explained_R'] != r['lost']:
                unexpl.append((a, b, r['lost'], r['explained_R']))
say("non-injective (a,b,lost):", pat)
say("cases where resonance alone does not explain all losses:", unexpl)

say("")
say("=== C. m = 1 injective up to a = 30 ===")
say(all(analyse([(2, a)], mech=False)['lost'] == 0 for a in range(1, 31)))

say("")
say("=== Extra: resonance formula vs direct equality on more atoms ===")
extra_ok = True
cnt = 0
for fac in [[(2, a), (3, b), (5, c)] for a in range(1, 6) for b in range(1, 6) for c in range(1, 4)] + \
           [[(2, a), (3, b), (5, c), (7, d)] for a in range(1, 4) for b in range(1, 4) for c in range(1, 4) for d in range(1, 3)]:
    r = analyse(fac, mech=False) if len(Atom(fac).divisors()) <= 400 else None
    if r is None:
        A = Atom(fac)
        Om = len(A.hyp)
        rp = [(a, b) for a, b in combinations(range(Om), 2) if A.hyp[a][0] != A.hyp[b][0] and A.w[a] == A.w[b]]
        fp = [(a, b) for a, b in combinations(range(Om), 2) if resonance_formula(A, a, b)]
        ok = rp == fp
    else:
        ok = r['res_formula_agrees'] and not r['same_prime_equal']
    extra_ok &= ok
    cnt += 1
say("atoms:", cnt, "formula agrees:", extra_ok)

say("")
say("EXPECTATION FAILURES:", len(FAIL))
for f in FAIL:
    say("  ", f)
with open(sys.argv[1] if len(sys.argv) > 1 else "VERIFY_O6_OUTPUT.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
