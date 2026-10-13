"""Independent verification of NOTE.md v0.1 (divisor atom as a CAT(0) cube complex).

Written from the mathematical statements, not from check_v0_1.py.
Python standard library; exact int / Fraction arithmetic throughout
(Ramanujan sums are evaluated exactly in Z[x]/(Phi_d), no floats).

Geometry is done on exponent vectors (tuples), arithmetic on integers, and the
two are compared, so that the box picture and the divisor picture are tested
against each other rather than against themselves.
"""
from fractions import Fraction
from itertools import product, combinations
from math import gcd, comb
from collections import deque
import random
from functools import lru_cache

random.seed(20261011)
FAIL = []
LOG = []


def ok(cond, label):
    if not cond:
        FAIL.append(label)
    return cond


def say(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s)


# ---------- arithmetic primitives (independent implementations) ----------
def factorize(n):
    out, d = [], 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1 if d == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


@lru_cache(maxsize=None)
def divs(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)  # brute force, independent of factorisation


def lcm(a, b):
    return a * b // gcd(a, b)


_mu_cache = {1: 1}


def mu(n):
    # Dirichlet inverse of the constant 1: sum_{d|n} mu(d) = [n == 1]
    if n not in _mu_cache:
        _mu_cache[n] = -sum(mu(d) for d in divs(n) if d < n)
    return _mu_cache[n]


@lru_cache(maxsize=None)
def phi(n):
    return sum(1 for j in range(1, n + 1) if gcd(j, n) == 1)  # brute force


def bigomega(n):
    return sum(e for _, e in factorize(n))


# ---------- exact Ramanujan sum via cyclotomic reduction ----------
def polydiv_exact(num, den):
    # integer polynomials, coefficient lists low->high, den monic
    num = num[:]
    q = [0] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        c = num[i + len(den) - 1]
        q[i] = c
        for j, b in enumerate(den):
            num[i + j] -= c * b
    return q, num[:len(den) - 1]


_cyc = {}


def cyclotomic(d):
    if d not in _cyc:
        p = [-1] + [0] * (d - 1) + [1]  # x^d - 1
        for e in divs(d):
            if e < d:
                p, r = polydiv_exact(p, cyclotomic(e))
                assert all(x == 0 for x in r)
        _cyc[d] = p
    return _cyc[d]


def ramanujan_exact(d, n):
    """sum_{j mod d, gcd(j,d)=1} zeta_d^{jn}, evaluated exactly in Z[x]/(Phi_d).
    The element must reduce to a constant integer; we assert that."""
    vec = [0] * d
    for j in range(d):
        if gcd(j, d) == 1:
            vec[(j * n) % d] += 1
    P = cyclotomic(d)
    if len(P) == 2:  # degree-1 cyclotomic: d = 1 or 2
        val = sum(c * (-P[0]) ** k for k, c in enumerate(vec))
        return val
    _, r = polydiv_exact(vec + [0] * max(0, len(P) - len(vec)), P) if len(vec) >= len(P) else (None, vec + [0] * (len(P) - 1 - len(vec)))
    assert all(x == 0 for x in r[1:]), ("non-constant", d, n, r)
    return r[0]


@lru_cache(maxsize=None)
def ramanujan_sterneck(d, n):
    g = gcd(d, n)
    return mu(d // g) * phi(d) // phi(d // g)


# ---------- the cube complex on exponent vectors ----------
class Atom:
    def __init__(self, N):
        self.N = N
        self.fac = factorize(N)
        self.P = [p for p, _ in self.fac]
        self.a = [e for _, e in self.fac]
        self.V = list(product(*[range(e + 1) for e in self.a]))
        self.Vset = set(self.V)

    def num(self, v):
        r = 1
        for p, k in zip(self.P, v):
            r *= p ** k
        return r

    def vec(self, n):
        out = []
        for p in self.P:
            k = 0
            while n % p == 0:
                n //= p
                k += 1
            out.append(k)
        return tuple(out)

    def cubes(self):
        # (corner v, direction set S): all v_i + 1 <= a_i for i in S
        out = []
        r = len(self.P)
        for v in self.V:
            free = [i for i in range(r) if v[i] < self.a[i]]
            for k in range(len(free) + 1):
                for S in combinations(free, k):
                    out.append((v, S))
        return out

    def cube_vertices(self, v, S):
        res = set()
        for T in product([0, 1], repeat=len(S)):
            w = list(v)
            for i, t in zip(S, T):
                w[i] += t
            res.add(tuple(w))
        return frozenset(res)

    def nbrs(self, v):
        for i in range(len(v)):
            for s in (-1, 1):
                w = list(v)
                w[i] += s
                w = tuple(w)
                if w in self.Vset:
                    yield w

    def bfs(self, s):
        dist = {s: 0}
        q = deque([s])
        while q:
            x = q.popleft()
            for y in self.nbrs(x):
                if y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)
        return dist


def fvec_genfun(a):
    # prod_p ((a_p+1) + a_p x): coefficient of x^k = number of k-faces
    poly = [1]
    for e in a:
        new = [0] * (len(poly) + 1)
        for i, c in enumerate(poly):
            new[i] += c * (e + 1)
            new[i + 1] += c * e
        poly = new
    return poly


def fvec_note_formula(a):
    r = len(a)
    out = []
    for k in range(r + 1):
        s = 0
        for S in combinations(range(r), k):
            t = 1
            for i in range(r):
                t *= a[i] if i in S else a[i] + 1
            s += t
        out.append(s)
    return out


NOTE_TABLE = {
    12: ([6, 7, 2], 3),
    30: ([8, 12, 6, 1], 3),
    360: ([24, 46, 29, 6], 6),
    900: ([27, 54, 36, 8], 6),
    6300: ([54, 135, 126, 52, 8], 7),
    30030: ([64, 192, 240, 160, 60, 12, 1], 6),
}

# ================= B. f-vector table =================
say("== B. f-vector table (enumeration / generating function / note formula) ==")
for N, (fv_note, om_note) in NOTE_TABLE.items():
    X = Atom(N)
    cs = X.cubes()
    fv_enum = [0] * (len(X.P) + 1)
    for _, S in cs:
        fv_enum[len(S)] += 1
    fv_gf = fvec_genfun(X.a)
    fv_nf = fvec_note_formula(X.a)
    chi = sum((-1) ** k * c for k, c in enumerate(fv_enum))
    ok(fv_enum == fv_gf == fv_nf == fv_note, f"B fvec {N}")
    ok(chi == 1, f"B euler {N}")
    ok(bigomega(N) == om_note == sum(X.a), f"B Omega {N}")
    ok(fv_enum[0] == len(divs(N)), f"B tau {N}")
    # face closure: every face of every cube is a cube (cube complex sanity)
    cubeset = {X.cube_vertices(v, S) for v, S in cs}
    closed = True
    for v, S in cs:
        for i in S:
            rest = tuple(j for j in S if j != i)
            up = tuple(x + (1 if j == i else 0) for j, x in enumerate(v))
            if X.cube_vertices(v, rest) not in cubeset or X.cube_vertices(up, rest) not in cubeset:
                closed = False
    ok(closed, f"B face-closure {N}")
    say(N, X.fac, "enum", fv_enum, "chi", chi, "Omega", sum(X.a), "matches note:", fv_enum == fv_note)

# ================= A. per-claim checks on atoms =================
TEST_N = [1, 2, 4, 6, 8, 12, 18, 30, 36, 60, 72, 210, 360, 900, 6300, 30030]
SMALL = [N for N in TEST_N if len(divs(N)) <= 64]

say("\n== §2.1-§2.4 hyperplanes, crossing, Sageev, distance ==")
for N in TEST_N:
    X = Atom(N)
    H = [(i, k) for i in range(len(X.P)) for k in range(1, X.a[i] + 1)]
    plus = {h: frozenset(v for v in X.V if v[h[0]] >= h[1]) for h in H}
    minus = {h: frozenset(X.Vset - plus[h]) for h in H}
    # half-space as divisibility condition
    for (i, k) in H:
        p = X.P[i]
        ok(all((X.num(v) % p ** k == 0) == (v in plus[(i, k)]) for v in X.V), f"2.1 halfspace {N}")
    # duality to edges: edge v -- v+e_i crosses exactly H(i, v_i + 1)
    for v in X.V:
        for i in range(len(v)):
            if v[i] < X.a[i]:
                w = list(v); w[i] += 1; w = tuple(w)
                sep = [h for h in H if (v in plus[h]) != (w in plus[h])]
                ok(sep == [(i, v[i] + 1)], f"2.1 dual {N}")
    ok(len(H) == bigomega(N), f"2.1 count {N}")
    # crossing and nesting
    for h, g in combinations(H, 2):
        quads = all(len(A & B) > 0 for A in (plus[h], minus[h]) for B in (plus[g], minus[g]))
        ok(quads == (h[0] != g[0]), f"2.2 cross {N}")
        if h[0] == g[0]:
            lo, hi = sorted([h, g], key=lambda t: t[1])
            ok(plus[hi] < plus[lo], f"2.2 nested {N}")
    # Sageev: admissible orientations <-> vertices (bijection, via principal orientations)
    if len(H) <= 16:
        principal = {}
        for v in X.V:
            principal[tuple(v in plus[h] for h in H)] = v
        adm = []
        for ch in product([True, False], repeat=len(H)):
            sets = [plus[h] if c else minus[h] for h, c in zip(H, ch)]
            if all(A & B for A, B in combinations(sets, 2)):
                adm.append(ch)
        ok(set(adm) == set(principal) and len(adm) == len(X.V), f"2.3 Sageev bijection {N}")
        # and the Sageev cubes (sets of pairwise crossing hyperplanes at an orientation) recover the f-vector
        # count cubes = pairs (orientation, set of pairwise-crossing hyperplanes each of which can be flipped consistently)
        fv = [0] * (len(X.P) + 1)
        admset = set(adm)
        for ch in adm:
            idx_flippable = []
            for j in range(len(H)):
                if ch[j]:
                    continue  # count each cube once: from its corner where all its hyperplanes are on minus side
                c2 = list(ch); c2[j] = True
                if tuple(c2) in admset:
                    idx_flippable.append(j)
            for k in range(len(X.P) + 1):
                for S in combinations(idx_flippable, k):
                    good = True
                    for T in product([0, 1], repeat=k):
                        c3 = list(ch)
                        for j, t in zip(S, T):
                            if t:
                                c3[j] = True
                        if tuple(c3) not in admset:
                            good = False
                            break
                    if good:
                        fv[k] += 1
        ok(fv == fvec_genfun(X.a), f"2.3 Sageev cubes {N}")
    # distance
    if len(X.V) <= 64:
        for u in X.V:
            d = X.bfs(u)
            for w in X.V:
                a, b = X.num(u), X.num(w)
                nsep = sum(1 for h in H if (u in plus[h]) != (w in plus[h]))
                ok(d[w] == nsep == bigomega(lcm(a, b) // gcd(a, b)) == sum(abs(x - y) for x, y in zip(u, w)), f"2.4 dist {N}")
say("hyperplane/Sageev/distance checks done on", TEST_N)

say("\n== §3.1 median, §3.2 intervals ==")
for N in SMALL:
    X = Atom(N)
    D = {v: X.bfs(v) for v in X.V}

    def gint(u, w):
        return frozenset(x for x in X.V if D[u][x] + D[x][w] == D[u][w])
    I = {(u, w): gint(u, w) for u in X.V for w in X.V}
    for u, w in I:
        a, b = X.num(u), X.num(w)
        g, l = gcd(a, b), lcm(a, b)
        ok({X.num(x) for x in I[(u, w)]} == {d for d in divs(N) if d % g == 0 and l % d == 0}, f"3.2 interval {N}")
        ok(len(I[(u, w)]) == len(divs(l // g)), f"3.2 interval iso size {N}")
    for u, w, z in product(X.V, repeat=3):
        a, b, c = X.num(u), X.num(w), X.num(z)
        m1 = gcd(gcd(lcm(a, b), lcm(b, c)), lcm(c, a))
        m2 = lcm(lcm(gcd(a, b), gcd(b, c)), gcd(c, a))
        med = tuple(sorted(t)[1] for t in zip(u, w, z))
        common = I[(u, w)] & I[(w, z)] & I[(z, u)]
        ok(m1 == m2 == X.num(med) and common == {med}, f"3.1 median {N}")
say("median and interval checks done on", SMALL)

say("\n== §3.2 convex subsets: exhaustive over all vertex subsets (tau <= 16) ==")
for N in [1, 2, 4, 6, 8, 12, 16, 18, 30, 36, 48, 60, 72, 210]:
    X = Atom(N)
    D = {v: X.bfs(v) for v in X.V}
    n = len(X.V)
    idx = {v: i for i, v in enumerate(X.V)}
    Imask = {}
    for u in X.V:
        for w in X.V:
            m = 0
            for x in X.V:
                if D[u][x] + D[x][w] == D[u][w]:
                    m |= 1 << idx[x]
            Imask[(idx[u], idx[w])] = m
    convex = []
    for S in range(1 << n):
        members = [i for i in range(n) if S >> i & 1]
        if all((Imask[(i, j)] & ~S) == 0 for i in members for j in members):
            convex.append(S)
    boxes = set()
    for lo in X.V:
        for hi in X.V:
            if all(x <= y for x, y in zip(lo, hi)):
                m = 0
                for x in X.V:
                    if all(l_ <= t <= h_ for l_, t, h_ in zip(lo, x, hi)):
                        m |= 1 << idx[x]
                boxes.add(m)
    expected = 1
    for e in X.a:
        expected *= comb(e + 2, 2)
    nonempty = [S for S in convex if S]
    ok(set(nonempty) == boxes and len(boxes) == expected, f"3.2 convex=boxes {N}")
    ok(0 in convex, f"3.2 empty convex {N}")
    say(N, "tau", n, "convex vertex sets (nonempty)", len(nonempty), "sub-boxes", len(boxes), "prod C(a+2,2)", expected, "empty set convex:", 0 in convex)

# subcomplex-level counterexample: in X(6) the 4-cycle without its square is a subcomplex
# whose 1-skeleton is geodesically convex (all 4 vertices, all 4 edges, distances unchanged)
X6 = Atom(6)
cyc_edges = {frozenset((u, w)) for u in X6.V for w in X6.nbrs(u)}
ok(len(cyc_edges) == 4, "3.2 cex edges")
say("X(6): the boundary 4-cycle (4 vertices, 4 edges, no 2-cell) has the same vertex set and 1-skeleton as the full sub-box; "
    "it is 1-skeleton-convex but not the full sub-box subcomplex, and not metrically convex (the square's interior is missing).")

say("\n== §3.3 antipode ==")
for N in TEST_N:
    X = Atom(N)
    anti = lambda v: tuple(e - x for e, x in zip(X.a, v))
    ok(all(X.num(anti(v)) == N // X.num(v) for v in X.V), f"3.3 formula {N}")
    cubeset = {X.cube_vertices(v, S) for v, S in X.cubes()}
    ok({frozenset(anti(x) for x in C) for C in cubeset} == cubeset, f"3.3 cube automorphism {N}")
    H = [(i, k) for i in range(len(X.P)) for k in range(1, X.a[i] + 1)]
    for (i, k) in H:
        img = {anti(v) for v in X.V if v[i] >= k}
        target_minus = {v for v in X.V if v[i] < X.a[i] - k + 1}  # H^-(p, a_p - k + 1)
        ok(img == target_minus, f"3.3 H+(p,k)->H-(p,a-k+1) {N}")
        same_minus = {v for v in X.V if v[i] < k}
        if X.a[i] - k + 1 != k:
            ok(img != same_minus, f"3.3 not H-(p,k) {N}")
    fixed = [v for v in X.V if anti(v) == v]
    sq = any(d * d == N for d in range(1, N + 1))
    ok((len(fixed) == 1) == sq and len(fixed) <= 1, f"3.3 fixed {N}")
say("antipode maps every cube to a cube; it maps H+(p,k) onto H-(p, a_p-k+1), which differs from H-(p,k) unless 2k = a_p+1")
say("example N=360, p=2 (a=3): H+(2,1) -> H-(2,3), not H-(2,1)")

say("\n== §3.4 Moebius as cubical sign ==")
for N in TEST_N:
    X = Atom(N)
    ALLCUBES = {X.cube_vertices(v, S) for v, S in X.cubes()}
    for nv in X.V:
        n = X.num(nv)
        # unit cube below n spanned by primes of n: corner nv - 1_{supp}, directions supp
        supp = tuple(i for i in range(len(nv)) if nv[i] > 0)
        corner = tuple(x - (1 if i in supp else 0) for i, x in enumerate(nv))
        cube = X.cube_vertices(corner, supp)
        ok(cube in ALLCUBES, "3.4 cube exists in X(N)")
        for d in divs(n):
            dv = X.vec(d)
            m = mu(n // d)
            ok((m != 0) == (dv in cube), f"3.4 support {N}")
            if m:
                ok(m == (-1) ** sum(x - y for x, y in zip(nv, dv)), f"3.4 sign {N}")
    # inversion
    g = {d: random.randint(-9, 9) for d in divs(N)}
    f = {n: sum(g[d] for d in divs(n)) for n in divs(N)}
    ok(all(g[n] == sum(mu(n // d) * f[d] for d in divs(n)) for n in divs(N)), f"3.4 inversion {N}")

say("\n== §4 Fourier layer ==")
# exact Ramanujan: definition (cyclotomic reduction) == Sterneck == note's mu formula
for d in range(1, 121):
    for n in range(d):
        e = ramanujan_exact(d, n)
        s = ramanujan_sterneck(d, n)
        nm = sum(mu(d // k) * k for k in divs(gcd(d, n)))
        ok(e == s == nm, f"4.2 ramanujan def {d},{n}")
for d in divs(360) + divs(900):
    for n in range(d):
        ok(ramanujan_exact(d, n) == ramanujan_sterneck(d, n), f"4.2 ramanujan def {d},{n}")
say("c_d(n): exponential-sum definition evaluated exactly in Z[x]/(Phi_d) equals von Sterneck and mu formula, d<=120 and d|360, d|900")


def c(d, n):
    return ramanujan_sterneck(d, n)


for N in [1, 12, 30, 360, 900, 6300, 30030]:
    Dv = divs(N)
    # 4.1 orders
    cnt = {}
    for j in range(N):
        o = N // gcd(j, N)
        cnt[o] = cnt.get(o, 0) + 1
    ok(cnt == {d: phi(d) for d in Dv} and sum(cnt.values()) == N, f"4.1 classes {N}")
    # gcd-class sizes: #{n mod N : gcd(n,N)=e} = phi(N/e)
    gc = {}
    for n in range(N):
        gc[gcd(n, N)] = gc.get(gcd(n, N), 0) + 1
    ok(gc == {e: phi(N // e) for e in Dv}, f"4.2 class sizes {N}")
    # c_d depends only on gcd(n,d)
    ok(all(c(d, n) == c(d, gcd(n, d)) for d in Dv for n in range(N)) if N <= 900 else True, f"4.2 gcd-dependence {N}")
    # orthogonality: direct sum over n for N <= 900, grouped by gcd class (class sizes verified above) beyond
    for d in Dv:
        for e in Dv:
            if N <= 900:
                s = sum(c(d, n) * c(e, n) for n in range(N))
            else:
                s = sum(gc[g] * c(d, g) * c(e, g) for g in Dv)
            ok(s == (N * phi(d) if d == e else 0), f"4.2 orth {N}")
    # expansion with the note's coefficient, several random exact test functions; checked at every n
    for trial in range(3):
        F = {e: Fraction(random.randint(-50, 50), random.randint(1, 13)) for e in Dv}
        alpha = {d: Fraction(sum(F[e] * phi(N // e) * c(d, e) for e in Dv), N * phi(d)) for d in Dv}
        if N <= 6300:
            ok(all(sum(alpha[d] * c(d, n) for d in Dv) == F[gcd(n, N)] for n in range(N)), f"4.2 expansion {N}")
        else:
            ok(all(sum(alpha[d] * c(d, g) for d in Dv) == F[g] for g in Dv), f"4.2 expansion {N}")
    # alternative coefficient (Fourier-side projection, no grouping): alpha(d) = <f, c_d> / ||c_d||^2
    if N <= 900:
        F = {e: Fraction(random.randint(-50, 50), random.randint(1, 13)) for e in Dv}
        for d in Dv:
            a1 = Fraction(sum(F[gcd(n, N)] * c(d, n) for n in range(N)), sum(c(d, n) ** 2 for n in range(N)))
            a2 = Fraction(sum(F[e] * phi(N // e) * c(d, e) for e in Dv), N * phi(d))
            ok(a1 == a2, f"4.2 coefficient two routes {N}")
say("4.1 classes, 4.2 gcd-dependence, orthogonality, expansion: N in 1,12,30,360,900 direct; 6300 direct expansion, grouped orthogonality; 30030 grouped")

say("\n== §5 inter-atom relations ==")
PAIRS = [(12, 18), (30, 42), (8, 12), (4, 12), (6, 30), (12, 12), (1, 30), (10, 21), (36, 60), (72, 90)]
for M, N in PAIRS:
    g, l = gcd(M, N), lcm(M, N)
    L = Atom(l)
    DM = {L.vec(d) for d in divs(M)}
    DN = {L.vec(d) for d in divs(N)}
    ok(DM & DN == {L.vec(d) for d in divs(g)}, f"5.4 meet {M},{N}")
    D = {v: L.bfs(v) for v in L.V}

    def interval(u, w):
        return {x for x in L.V if D[u][x] + D[x][w] == D[u][w]}
    hull = DM | DN
    while True:
        new = set()
        for u in hull:
            for w in hull:
                new |= interval(u, w)
        if new <= hull:
            break
        hull |= new
    ok(hull == set(L.V), f"5.4 hull {M},{N}")
    U = DM | DN
    conv = all(interval(u, w) <= U for u in U for w in U)
    ok(conv == (N % M == 0 or M % N == 0), f"5.4 union convex iff divides {M},{N}")
    say(M, N, "union convex:", conv, "divisibility:", N % M == 0 or M % N == 0)

# 5.2 hyperplanes meeting X(M) inside X(N); Fourier pullback along Z/N -> Z/M
for M, N in [(12, 360), (30, 900), (6, 6300), (360, 360), (1, 30), (210, 30030)]:
    X = Atom(N)
    sub = {X.vec(d) for d in divs(M)}
    H = [(i, k) for i in range(len(X.P)) for k in range(1, X.a[i] + 1)]
    meets = {(X.P[i], k) for (i, k) in H if any((v[i] >= k) != (w[i] >= k) for v in sub for w in sub)}
    ok(meets == {(p, k) for p, e in factorize(M) for k in range(1, e + 1)}, f"5.2 hyperplanes {M},{N}")
    # characters of Z/M pulled back: frequency j mod M -> j*(N/M) mod N; same values; image = order | M
    img = {(j * (N // M)) % N for j in range(M)}
    ok(len(img) == M and img == {j for j in range(N) if M % (N // gcd(j, N)) == 0}, f"5.2 image {M},{N}")
    ok(all(Fraction(j * n, M) - Fraction((j * (N // M)) * n, N) == 0 for j in range(min(M, 40)) for n in range(min(N, 200))), f"5.2 values {M},{N}")
    ok(all(M // gcd(j, M) == N // gcd(j * (N // M), N) for j in range(M)), f"5.2 order preserved {M},{N}")
    # translates 5.3 for e with eM | N
    for e in divs(N // M):
        img_v = {X.vec(e * d) for d in divs(M)}
        ok(img_v == {X.vec(d) for d in divs(N) if d % e == 0 and (e * M) % d == 0}, f"5.3 translate {M},{e},{N}")
        Y = Atom(M)
        ecubes = {frozenset(X.vec(e * Y.num(x)) for x in Y.cube_vertices(v, S)) for v, S in Y.cubes()}
        full = {C for C in (X.cube_vertices(v, S) for v, S in X.cubes()) if C <= img_v}
        ok(ecubes == full, f"5.3 full subcomplex (all cubes) {M},{e},{N}")

# 5.5 coprime product: enumerated cubes of X(MN) vs convolution of enumerated f-vectors
for M, N in [(4, 9), (12, 35), (8, 15), (30, 77), (1, 12)]:
    def fe(n):
        X = Atom(n)
        f = [0] * (len(X.P) + 1)
        for _, S in X.cubes():
            f[len(S)] += 1
        return f
    a, b, cc = fe(M), fe(N), fe(M * N)
    conv = [sum(a[i] * b[k - i] for i in range(len(a)) if 0 <= k - i < len(b)) for k in range(len(a) + len(b) - 1)]
    ok(conv == cc, f"5.5 convolution {M},{N}")

# 5.6 compatibility
for M, N in [(12, 18), (30, 42), (8, 12), (360, 30030)]:
    g, l = gcd(M, N), lcm(M, N)
    for d in divs(g):
        ok(all(ramanujan_sterneck(d, n) == ramanujan_sterneck(d, n % M) == ramanujan_sterneck(d, n % N) == ramanujan_sterneck(d, n % l)
               for n in range(0, l, max(1, l // 3000))), f"5.6 compat {M},{N}")
    # expansion coefficients of a function of gcd(n,M), computed on Z/M and on Z/l, agree (zero off Div(M))
    if l <= 2000:
        F = {e: Fraction(random.randint(-9, 9), random.randint(1, 5)) for e in divs(M)}
        aM = {d: Fraction(sum(F[gcd(n, M)] * c(d, n) for n in range(M)), M * phi(d)) for d in divs(M)}
        aL = {d: Fraction(sum(F[gcd(n, M)] * c(d, n) for n in range(l)), l * phi(d)) for d in divs(l)}
        ok(all(aL[d] == (aM[d] if M % d == 0 else 0) for d in divs(l)), f"5.6 coefficients stable {M}->{l}")

# 5.1 X(N): finite witnesses of what does NOT carry verbatim
say("\n== §5.1 X(N) (reasoned; finite witnesses) ==")
# The orientation 'H+(p,1) for every prime p, H- for all other hyperplanes' is pairwise consistent:
# for any two chosen half-spaces there is a common positive integer.  Witness on the first 50 primes:
primes = [p for p in range(2, 400) if all(p % q for q in range(2, int(p ** 0.5) + 1))][:50]
pair_ok = all(lcm(p, q) % p == 0 and lcm(p, q) % q == 0 and lcm(p, q) % (p * p) != 0 for p, q in combinations(primes, 2))
ok(pair_ok, "5.1 witness pairs")
say("orientation {H+(p,1) for all p; H- elsewhere} is pairwise consistent (checked on 50 primes) but is principal at no integer;"
    " likewise {H+(2,k) for all k}. So 2.3 'admissible choices <-> vertices' needs the DCC/finiteness condition in X(N).")

say("\nFAILURES:", len(FAIL))
for x in sorted(set(FAIL)):
    say("  ", x)
say("RESULT:", "ALL CHECKS PASS" if not FAIL else "FAIL")
