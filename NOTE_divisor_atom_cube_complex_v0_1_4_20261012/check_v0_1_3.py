"""Exact checks for NOTE.md v0.1.3 (v0.1.1 checks unchanged, plus A1-A3 for Astra #255).

Original header (v0.1.1):
Exact checks for NOTE.md v0.1.1 (divisor atom as a CAT(0) cube complex).

Check script for the note only; not an instrument core. Python standard library;
exact arithmetic with int/Fraction throughout. v0.1.1 additions follow the
independent check of v0.1 (REPORT.md d1ce9054...): C4b (bijection), C7b
(convex-set classification), C9 against the cube list plus inversion, C12 made
exact (reduction modulo the cyclotomic polynomial), R3 divisible pairs, R2/R3
gate lifted, R5 against enumerated cubes. The v0.1 floating-point C12 is kept
as C12n, labelled NUMERICAL.
"""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, prod, isqrt, cos, sin, pi
from collections import deque

CASES = [1, 12, 30, 36, 60, 360, 900, 6300, 30030]
PAIRS = [(12, 18), (30, 42), (8, 12), (360, 30030), (6, 12), (30, 30030), (4, 36)]

failures = []


def check(cond, label):
    if not cond:
        failures.append(label)
    return cond


def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def lcm(a, b):
    return a // gcd(a, b) * b


def divisors(n):
    f = factor(n)
    ds = [1]
    for p, a in f.items():
        ds = [d * p ** k for d in ds for k in range(a + 1)]
    return sorted(ds)


def v(p, n):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def mobius(n):
    f = factor(n)
    return 0 if any(a > 1 for a in f.values()) else (-1) ** len(f)


def phi(n):
    return prod(p ** (a - 1) * (p - 1) for p, a in factor(n).items())


def omega(n):
    return len(factor(n))


def Omega(n):
    return sum(factor(n).values())


def cubes(N):
    """All cubes of X(N): (base d, frozenset S of primes) with d*prod(S) | N."""
    P = sorted(factor(N))
    out = []
    for d in divisors(N):
        for k in range(len(P) + 1):
            for S in combinations(P, k):
                if N % (d * prod(S)) == 0:
                    out.append((d, frozenset(S)))
    return out


def f_vector_formula(N):
    f = factor(N)
    P = sorted(f)
    return [sum(prod(f[p] for p in S) * prod(f[p] + 1 for p in P if p not in S)
                for S in combinations(P, k)) for k in range(len(P) + 1)]


def edges(N):
    return [(d, d * p) for d in divisors(N) for p in factor(N) if N % (d * p) == 0]


def bfs_dist(N, s):
    adj = {d: [] for d in divisors(N)}
    for a, b in edges(N):
        adj[a].append(b)
        adj[b].append(a)
    dist = {s: 0}
    q = deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def median(a, b, c):
    return gcd(gcd(lcm(a, b), lcm(b, c)), lcm(c, a))


def interval(a, b, N):
    g, l = gcd(a, b), lcm(a, b)
    return {d for d in divisors(N) if d % g == 0 and l % d == 0}


def geodesic_interval(a, b, N):
    da, db = bfs_dist(N, a), bfs_dist(N, b)
    return {d for d in divisors(N) if da[d] + db[d] == da[b]}


def ramanujan(q, n):
    return sum(mobius(q // k) * k for k in divisors(gcd(q, n)))


# exact integer polynomials, coefficient lists, lowest degree first
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


def cyclotomic(d):
    """Phi_d by exact division of x^d - 1 by Phi_e for e | d, e < d."""
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                num, r = pdivmod(num, cyclotomic(e))
                assert not any(r)
        _cyc[d] = num
    return _cyc[d]


def ramanujan_exact_from_roots(d, n):
    """Sum over primitive d-th roots zeta of zeta^n, computed in Z[x]/(Phi_d): returns
    the constant if the reduction is a constant, else None."""
    poly = [0] * d
    for j in range(1, d + 1):
        if gcd(j, d) == 1:
            poly[(j * n) % d] += 1
    _, r = pdivmod(poly, cyclotomic(d))
    r = r + [0] * (1 - len(r)) if not r else r
    return r[0] if all(x == 0 for x in r[1:]) else None


def is_convex(S, N):
    return all(interval(a, b, N) <= S for a in S for b in S)


def sub_boxes(N):
    D = divisors(N)
    return {frozenset(d for d in D if d % g == 0 and l % d == 0) for g in D for l in D if l % g == 0}


report = []

for N in CASES:
    D = divisors(N)
    f = factor(N)
    P = sorted(f)
    # C1 f-vector from the enumeration equals the closed formula; Euler characteristic 1
    cs = cubes(N)
    fv = [sum(1 for _, S in cs if len(S) == k) for k in range(len(P) + 1)]
    check(fv == f_vector_formula(N), f"C1 f-vector N={N}")
    chi = sum((-1) ** k * x for k, x in enumerate(fv))
    check(chi == 1, f"C1 Euler N={N}")
    check(len(D) == fv[0], f"C1 tau N={N}")
    check((len(fv) - 1) == omega(N), f"C1 dim N={N}")
    # C2 hyperplanes H(p,k), 1<=k<=a_p: count Omega(N); each is dual to exactly the edges d--dp with v_p(d)=k-1
    H = [(p, k) for p in P for k in range(1, f[p] + 1)]
    check(len(H) == Omega(N), f"C2 hyperplane count N={N}")
    E = edges(N)
    for a, b in E:
        p = next(q for q in P if b == a * q)
        dual = [(q, k) for (q, k) in H if (b % q ** k == 0) != (a % q ** k == 0)]
        check(dual == [(p, v(p, a) + 1)], f"C2 edge dual N={N} {a}-{b}")
    # C3 crossing: H(p,j), H(q,k) cross iff p != q (all four quadrants nonempty)
    for (p, j), (q, k) in combinations(H, 2):
        quads = {(d % p ** j == 0, d % q ** k == 0) for d in D}
        check((len(quads) == 4) == (p != q), f"C3 crossing N={N}")
    # C4 Sageev: consistent orientations of the pocset (choose a halfspace per hyperplane,
    # never two disjoint ones) number exactly tau(N), one per divisor
    if len(H) <= 14:
        halves = {}
        for h in H:
            p, k = h
            halves[(h, True)] = frozenset(d for d in D if d % p ** k == 0)
            halves[(h, False)] = frozenset(d for d in D if d % p ** k != 0)
        consistent = []
        for choice in product([True, False], repeat=len(H)):
            chosen = [halves[(h, c)] for h, c in zip(H, choice)]
            if all(x & y for x, y in combinations(chosen, 2)):
                consistent.append(choice)
        check(len(consistent) == len(D), f"C4 Sageev count N={N}")
        # C4b bijection: each consistent orientation's chosen half-spaces meet in exactly one
        # vertex d, and that d's principal orientation (H+ iff p^k | d) is the orientation itself
        seen = set()
        for choice in consistent:
            common = frozenset(D)
            for h, c in zip(H, choice):
                common &= halves[(h, c)]
            ok = len(common) == 1
            if ok:
                (d,) = common
                ok = tuple(d % p ** k == 0 for p, k in H) == choice and d not in seen
                seen.add(d)
            check(ok, f"C4b Sageev bijection N={N}")
        check(seen == set(D), f"C4b Sageev onto N={N}")
    # C5 combinatorial distance = number of separating hyperplanes = Omega(lcm/gcd)
    if len(D) <= 400:
        for a in D:
            da = bfs_dist(N, a)
            for b in D:
                check(da[b] == Omega(lcm(a, b) // gcd(a, b)), f"C5 distance N={N}")
    # C6 median: gcd-of-lcms equals lcm-of-gcds; lies in all three intervals; unique such vertex
    if len(D) <= 64:
        for a, b, c in product(D, repeat=3):
            m = median(a, b, c)
            check(m == lcm(lcm(gcd(a, b), gcd(b, c)), gcd(c, a)), f"C6 median dual N={N}")
            common = interval(a, b, N) & interval(b, c, N) & interval(c, a, N)
            check(common == {m}, f"C6 median unique N={N}")
    # C7 geodesic interval equals the divisor interval {g | d | l}, isomorphic to X(l/g)
    if len(D) <= 64:
        for a, b in product(D, repeat=2):
            I = interval(a, b, N)
            check(geodesic_interval(a, b, N) == I, f"C7 interval N={N}")
            check(len(I) == len(divisors(lcm(a, b) // gcd(a, b))), f"C7 interval size N={N}")
    # C7b every nonempty geodesically convex vertex set is a sub-box {g | d | l}, and every
    # sub-box is convex; count = prod C(a_p+2, 2). Exhaustive over all subsets for tau(N) <= 12.
    if len(D) <= 12:
        boxes = sub_boxes(N)
        check(all(is_convex(set(B), N) for B in boxes), f"C7b boxes convex N={N}")
        check(len(boxes) == prod((a + 2) * (a + 1) // 2 for a in f.values()), f"C7b box count N={N}")
        found = set()
        for mask in range(1, 1 << len(D)):
            S = {D[i] for i in range(len(D)) if mask >> i & 1}
            if is_convex(S, N):
                found.add(frozenset(S))
        check(found == boxes, f"C7b convex = boxes N={N}")
    # C8 antipode d -> N/d is an automorphism (edges to edges); fixed vertex iff N is a square
    Es = {frozenset(e) for e in E}
    check({frozenset((N // a, N // b)) for a, b in E} == Es, f"C8 antipode N={N}")
    fixed = [d for d in D if d * d == N]
    check(bool(fixed) == (isqrt(N) ** 2 == N), f"C8 fixed N={N}")
    # C9 Moebius against the cube list: mu(n/d) != 0 iff some cube of X(N) has d as its bottom
    # and n as its top vertex; then mu(n/d) = (-1)^(dim of that cube). Also Moebius inversion.
    tops = {}
    for base, S in cs:
        tops[(base, base * prod(S))] = len(S)
    for n in D:
        for d in divisors(n):
            q = n // d
            check((mobius(q) != 0) == ((d, n) in tops), f"C9 support N={N}")
            if (d, n) in tops:
                check(mobius(q) == (-1) ** tops[(d, n)], f"C9 sign N={N}")
    fN = {d: Fraction(3 * d - 5, d + 2) for d in D}
    gN = {n: sum(fN[d] for d in divisors(n)) for n in D}
    check(all(sum(mobius(n // d) * gN[d] for d in divisors(n)) == fN[n] for n in D), f"C9 inversion N={N}")
    # C10 frequency classes: #{j mod N : order of j in Z/N equals d} = phi(d); sum = N
    if N <= 30030:
        counts = {}
        for j in range(N):
            o = N // gcd(j, N)
            counts[o] = counts.get(o, 0) + 1
        check(counts == {d: phi(d) for d in D}, f"C10 classes N={N}")
    # C11 Ramanujan basis for functions of gcd(n,N): orthogonality and exact expansion
    if N <= 360:
        for d, e in product(D, repeat=2):
            s = sum(ramanujan(d, n) * ramanujan(e, n) for n in range(N))
            check(s == (N * phi(d) if d == e else 0), f"C11 orthogonality N={N}")
        # an arbitrary exact test function of gcd(n,N)
        F = {e: Fraction(e * e + 3 * e - 7, e + 1) for e in D}
        alpha = {d: Fraction(sum(F[e] * phi(N // e) * ramanujan(d, e) for e in D), N * phi(d)) for d in D}
        for n in range(N):
            check(sum(alpha[d] * ramanujan(d, n) for d in D) == F[gcd(n, N)], f"C11 expansion N={N}")
    report.append((N, dict(f), fv, chi, len(H)))

# C12 EXACT: in Z[x]/(Phi_d), the sum of x^(jn) over j coprime to d reduces to the constant c_d(n)
for N in [12, 30, 360, 900]:
    for d in divisors(N):
        for n in range(N):
            check(ramanujan_exact_from_roots(d, n) == ramanujan(d, n), f"C12 exact N={N} d={d} n={n}")

# C12n NUMERICAL register (kept from v0.1): c_d(n) equals the sum of the n-th powers of the primitive d-th roots
# of unity (floating point; tolerance 1e-9; labelled numerical, not exact)
num_max = 0.0
for N in [12, 30, 360]:
    for d in divisors(N):
        for n in range(N):
            z = sum(complex(cos(2 * pi * j * n / d), sin(2 * pi * j * n / d))
                    for j in range(1, d + 1) if gcd(j, d) == 1)
            err = abs(z - ramanujan(d, n))
            num_max = max(num_max, err)
check(num_max < 1e-9, "C12n numerical")

# Inter-atom relations
for M, N in PAIRS:
    g, l = gcd(M, N), lcm(M, N)
    DL = set(divisors(l))
    DM, DN = set(divisors(M)), set(divisors(N))
    # R1 intersection: Div(M) & Div(N) = Div(gcd)
    check(DM & DN == set(divisors(g)), f"R1 meet {M},{N}")
    # R2 convex hull (median/interval closure) of Div(M) | Div(N) inside X(l) is Div(l)
    if len(DL) <= 256:
        hull = DM | DN
        while True:
            new = {d for a in hull for b in hull for d in interval(a, b, l)} - hull
            if not new:
                break
            hull |= new
        check(hull == DL, f"R2 hull {M},{N}")
        # R3 the union itself is convex iff M | N or N | M
        union = DM | DN
        convex = all(interval(a, b, l) <= union for a in union for b in union)
        check(convex == (M % N == 0 or N % M == 0), f"R3 union convex {M},{N}")
    # R4 Ramanujan basis compatibility: for d | g the function c_d is the same on Z/M and Z/N
    # (it depends on gcd(n,d) only), and a function of gcd(n,M) is a function of gcd(n,N) when M | l
    for d in divisors(g):
        check(all(ramanujan(d, n) == ramanujan(d, n % M) == ramanujan(d, n % N)
                  for n in range(min(l, 5000))), f"R4 compat {M},{N}")

# R5 coprime product: X(MN) = X(M) x X(N): f-vector is the convolution, hyperplanes disjoint union,
# every M-hyperplane crosses every N-hyperplane (covered by C3 since primes differ)
for M, N in [(4, 9), (12, 35), (8, 15)]:
    def enum_fv(X):
        cX = cubes(X)
        return [sum(1 for _, S in cX if len(S) == k) for k in range(omega(X) + 1)]
    a, b, c = enum_fv(M), enum_fv(N), enum_fv(M * N)
    conv = [sum(a[i] * b[k - i] for i in range(len(a)) if 0 <= k - i < len(b)) for k in range(len(a) + len(b) - 1)]
    check(conv == c, f"R5 product {M},{N}")
    check(Omega(M * N) == Omega(M) + Omega(N), f"R5 hyperplanes {M},{N}")

# R6 multiplication by e (eM | N) embeds X(M) onto the convex sub-box {d : e | d | eM}
for M, e, N in [(6, 2, 360), (12, 5, 360), (30, 7, 30030 * 2)]:
    img = {e * d for d in divisors(M)}
    check(img == interval(e, e * M, N), f"R6 translate {M},{e},{N}")
    imgE = {frozenset((e * x, e * y)) for x, y in edges(M)}
    subE = {frozenset((x, y)) for x, y in edges(N) if x in img and y in img}
    check(imgE == subE, f"R6 full subcomplex {M},{e},{N}")

# ---- v0.1.3 additions for Astra review #255 ----
def alpha_of(N, F):
    """Ramanujan coefficients of the function n -> F[gcd(n,N)] on Z/N (exact)."""
    D = divisors(N)
    return {d: Fraction(sum(F[e] * phi(N // e) * ramanujan(d, e) for e in D), N * phi(d)) for d in D}


# A1 (C1): alpha is Q-linear in the values f(e) with rational weights, so rational-valued f gives
# rational alpha; a constant function c gives alpha(1) = c, alpha(d) = 0 otherwise (so c = sqrt 2
# gives the irrational alpha(1) = sqrt 2 of Astra's example).
for N in [12, 30, 360]:
    D = divisors(N)
    a = alpha_of(N, {e: Fraction(1) for e in D})
    check(a == {d: Fraction(int(d == 1)) for d in D}, f"A1 constant N={N}")

# A2 (C2): pullback invariance. If M | N and f_N(n) = f_M(n mod M), the coefficients on d | M are
# unchanged and those on d not dividing M are zero.
for M, N in [(2, 4), (6, 12), (12, 360), (30, 30030 // 7), (4, 36)]:
    DM = divisors(M)
    FM = {e: Fraction(e * e - 2 * e + 5, e + 3) for e in DM}
    aM = alpha_of(M, FM)
    FN = {e: FM[gcd(e, M)] for e in divisors(N)}   # value at gcd(n,N)=e of f_M(n mod M) is FM[gcd(e,M)]
    aN = alpha_of(N, FN)
    check(all(aN[d] == (aM[d] if M % d == 0 else 0) for d in divisors(N)), f"A2 pullback {M},{N}")

# A2b: without the pullback hypothesis the coefficients differ (Astra's example f_M(n) = gcd(n,M))
a2 = alpha_of(2, {e: Fraction(e) for e in divisors(2)})
a4 = alpha_of(4, {e: Fraction(e) for e in divisors(4)})
check(a2 == {1: Fraction(3, 2), 2: Fraction(1, 2)}, "A2b M=2 coefficients")
check(a4 == {1: Fraction(2), 2: Fraction(1), 4: Fraction(1, 2)}, "A2b M=4 coefficients")

# A3 (precision, line 139): in X(6) with M=2, N=3 the smallest convex cubical subcomplex containing
# Div(2) u Div(3) = {1,2,3} is the full square Div(6)
hull = {1, 2, 3}
while True:
    new = {d for a in hull for b in hull for d in interval(a, b, 6)} - hull
    if not new:
        break
    hull |= new
check(hull == {1, 2, 3, 6}, "A3 cubical hull X(6)")

print("N | factorisation | f-vector | Euler | hyperplanes")
for N, f, fv, chi, h in report:
    print(N, "|", f, "|", fv, "|", chi, "|", h)
print("C12 numerical max error:", f"{num_max:.3e}", "(tolerance 1e-9)")
print("FAILURES:", len(failures))
for x in sorted(set(failures)):
    print("  ", x)
print("RESULT:", "ALL CHECKS PASS" if not failures else "FAIL")
