"""Exact checks for NOTE.md v0.1 (divisor atom as a CAT(0) cube complex).

Check script for the note only; not an instrument core. Python standard library;
exact arithmetic with int/Fraction. The one numerical check (C12) is labelled
NUMERICAL with its tolerance.
"""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, prod, isqrt, cos, sin, pi
from collections import deque

CASES = [1, 12, 30, 360, 900, 6300, 30030]
PAIRS = [(12, 18), (30, 42), (8, 12), (360, 30030)]

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
        count = 0
        for choice in product([True, False], repeat=len(H)):
            chosen = [halves[(h, c)] for h, c in zip(H, choice)]
            if all(x & y for x, y in combinations(chosen, 2)):
                count += 1
        check(count == len(D), f"C4 Sageev count N={N}")
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
    # C8 antipode d -> N/d is an automorphism (edges to edges); fixed vertex iff N is a square
    Es = {frozenset(e) for e in E}
    check({frozenset((N // a, N // b)) for a, b in E} == Es, f"C8 antipode N={N}")
    fixed = [d for d in D if d * d == N]
    check(bool(fixed) == (isqrt(N) ** 2 == N), f"C8 fixed N={N}")
    # C9 Moebius: mu(n/d) != 0 exactly on the unit cube below n spanned by primes of n, sign (-1)^dim
    for n in D:
        for d in divisors(n):
            q = n // d
            on_cube = all(a == 1 for a in factor(q).values())
            check((mobius(q) != 0) == on_cube, f"C9 support N={N}")
            if on_cube:
                check(mobius(q) == (-1) ** omega(q), f"C9 sign N={N}")
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

# C12 NUMERICAL register: c_d(n) equals the sum of the n-th powers of the primitive d-th roots
# of unity (floating point; tolerance 1e-9; labelled numerical, not exact)
num_max = 0.0
for N in [12, 30, 360]:
    for d in divisors(N):
        for n in range(N):
            z = sum(complex(cos(2 * pi * j * n / d), sin(2 * pi * j * n / d))
                    for j in range(1, d + 1) if gcd(j, d) == 1)
            err = abs(z - ramanujan(d, n))
            num_max = max(num_max, err)
check(num_max < 1e-9, "C12 numerical")

# Inter-atom relations
for M, N in PAIRS:
    g, l = gcd(M, N), lcm(M, N)
    DL = set(divisors(l))
    DM, DN = set(divisors(M)), set(divisors(N))
    # R1 intersection: Div(M) & Div(N) = Div(gcd)
    check(DM & DN == set(divisors(g)), f"R1 meet {M},{N}")
    # R2 convex hull (median/interval closure) of Div(M) | Div(N) inside X(l) is Div(l)
    if len(DL) <= 128:
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
    a, b, c = f_vector_formula(M), f_vector_formula(N), f_vector_formula(M * N)
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

print("N | factorisation | f-vector | Euler | hyperplanes")
for N, f, fv, chi, h in report:
    print(N, "|", f, "|", fv, "|", chi, "|", h)
print("C12 numerical max error:", f"{num_max:.3e}", "(tolerance 1e-9)")
print("FAILURES:", len(failures))
for x in sorted(set(failures)):
    print("  ", x)
print("RESULT:", "ALL CHECKS PASS" if not failures else "FAIL")
