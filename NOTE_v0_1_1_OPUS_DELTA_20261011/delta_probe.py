"""Delta verifier probe for NOTE v0.1.1. Reads check_v0_1_1.py as text, never modifies it.
(1) instrumented run: counts how many times each check label prefix executes;
(2) negative controls: in-memory mutations that must make specific new checks fail;
(3) independent checks of new note text (X(6) caveat, 3.3 hyperplane map, F9, cyclotomic, C12 values)."""
import sys, re, io, contextlib
from math import gcd, prod
from fractions import Fraction
from itertools import combinations, product
import cmath

SRC_PATH = r"C:\Users\robin\s6_atom\cat0_cube_complexes\NOTE_divisor_atom_cube_complex_v0_1_1_20261011\check_v0_1_1.py"
SRC = open(SRC_PATH, encoding="utf-8").read()

COUNT_PATCH_OLD = "def check(cond, label):\n    if not cond:"
COUNT_PATCH_NEW = ("def check(cond, label):\n    _k = label.split()[0] + ' ' + label.split()[1]\n"
                   "    COUNTS[_k] = COUNTS.get(_k, 0) + 1\n    if not cond:")
assert SRC.count(COUNT_PATCH_OLD) == 1


def run(src, light=False):
    if light:
        # restrict heavy loops to keep mutation runs short: drop 6300, 30030 from CASES
        src = src.replace("CASES = [1, 12, 30, 36, 60, 360, 900, 6300, 30030]", "CASES = [1, 12, 30, 36, 60]")
        src = src.replace("for N in [12, 30, 360, 900]:", "for N in [12, 30, 36]:")
        src = src.replace("for N in [12, 30, 360]:", "for N in [12]:")
    print("run start light=%s" % light, file=sys.stderr, flush=True)
    g = {"__name__": "__probe__", "COUNTS": {}}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, "check_v0_1_1_probe", "exec"), g)
    return g, buf.getvalue()


out = []
P = out.append

# ---------- (1) instrumented full run ----------
g, txt = run(SRC.replace(COUNT_PATCH_OLD, COUNT_PATCH_NEW))
P("== instrumented full run ==")
P("failures: %d" % len(g["failures"]))
for k in sorted(g["COUNTS"]):
    P("  %-28s %d" % (k, g["COUNTS"][k]))
# which pairs reach R2/R3
for M, N in g["PAIRS"]:
    l = M // gcd(M, N) * N
    P("  pair (%d,%d) tau(lcm)=%d divisible=%s" % (M, N, len(g["divisors"](l)), M % N == 0 or N % M == 0))
P("  C7b cases (tau<=12): %s" % [N for N in g["CASES"] if len(g["divisors"](N)) <= 12])

# ---------- (2) negative controls ----------
def mutate(name, old, new, expect_prefixes, light=True):
    assert SRC.count(old) >= 1, name
    s = SRC.replace(old, new)
    try:
        gg, _ = run(s, light=light)
        fails = sorted(set(gg["failures"]))
        err = None
    except AssertionError as e:
        fails, err = [], "AssertionError raised (%s)" % e
    except Exception as e:
        fails, err = [], "%s: %s" % (type(e).__name__, e)
    hit = sorted({f.split()[0] for f in fails})
    caught = err is not None or any(h in expect_prefixes for h in hit)
    others = [h for h in hit if h not in expect_prefixes]
    P("  %-34s caught=%s fail-prefixes=%s %s" % (name, caught, hit, err or ""))
    return caught

P("== negative controls (light run: CASES without 6300, 30030) ==")
mutate("M1 cyclotomic = x^d-1 (no division)",
       "        _cyc[d] = num\n", "        _cyc[d] = [-1] + [0] * (d - 1) + [1]\n", {"C12"})
mutate("M2 C12 poly exponent j+n",
       "poly[(j * n) % d] += 1", "poly[(j + n) % d] += 1", {"C12"})
mutate("M3 pdivmod drops last coef update",
       "        for i, x in enumerate(b):\n            a[s + i] -= c * x",
       "        for i, x in enumerate(b[:-1]):\n            a[s + i] -= c * x\n        a[-1] = 0", {"C12"})
mutate("M4 C7b is_convex always True",
       "    return all(interval(a, b, N) <= S for a in S for b in S)", "    return True", {"C7b"})
mutate("M5 C7b sub_boxes only l=N",
       "for g in D for l in D if l % g == 0}", "for g in D for l in [N]}", {"C7b"})
mutate("M6 C4b principal orientation shifted",
       "ok = tuple(d % p ** k == 0 for p, k in H) == choice", "ok = tuple(d % p ** (k + 1) == 0 for p, k in H) == choice", {"C4b"})
mutate("M7 C9 cube dimension +1",
       "tops[(base, base * prod(S))] = len(S)", "tops[(base, base * prod(S))] = len(S) + 1", {"C9"})
mutate("M8 C9 cube list drops 2-cubes",
       "    for base, S in cs:\n        tops", "    for base, S in [c for c in cs if len(c[1]) != 2]:\n        tops", {"C9"})
mutate("M9 R3 old one-direction claim (never convex)",
       "check(convex == (M % N == 0 or N % M == 0)", "check(convex == False", {"R3"})
mutate("M10 R5 enumerated MN cubes perturbed",
       "a, b, c = enum_fv(M), enum_fv(N), enum_fv(M * N)", "a, b, c = enum_fv(M), enum_fv(N), enum_fv(M * N * 2)", {"R5"})
mutate("M11 R2 hull stops after one round",
       "            if not new:\n                break", "            break", {"R2"})
mutate("M12 C9 inversion uses mu(d) not mu(n/d)",
       "sum(mobius(n // d) * gN[d]", "sum(mobius(d) * gN[d]", {"C9"})

# ---------- (3) independent checks ----------
P("== independent checks ==")
divisors, cyclotomic, pdivmod, phi, mobius, factor = (g[k] for k in ("divisors", "cyclotomic", "pdivmod", "phi", "mobius", "factor"))
rer = g["ramanujan_exact_from_roots"]


def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

bad = 0
for d in range(1, 211):
    c = cyclotomic(d)
    if len(c) - 1 != phi(d) or c[-1] != 1:
        bad += 1
    pr = [1]
    for e in divisors(d):
        pr = pmul(pr, cyclotomic(e))
    if pr != [-1] + [0] * (d - 1) + [1]:
        bad += 1
    z = cmath.exp(2j * cmath.pi / d)
    if abs(sum(co * z ** i for i, co in enumerate(c))) > 1e-6:
        bad += 1
P("  cyclotomic d=1..210: deg=phi, monic, prod_{e|d} Phi_e = x^d-1, Phi_d(zeta_d)~0 : bad=%d" % bad)
P("  Phi_105 has coefficient -2: %s" % (-2 in cyclotomic(105)))

# C12 exact vs von Sterneck (independent closed form), d | 900 and d | 360, all n mod d
bad = 0; cnt = 0
for N in (360, 900):
    for d in divisors(N):
        for n in range(d):
            gg_ = gcd(n, d)
            vs = Fraction(mobius(d // gg_) * phi(d), phi(d // gg_))
            if rer(d, n) != vs:
                bad += 1
            cnt += 1
P("  exact Z[x]/Phi_d reduction vs von Sterneck, d | 360,900, n mod d: %d cases, bad=%d" % (cnt, bad))
# reduction returns None on non-constant elements (so C12 cannot pass vacuously)
P("  non-constant element x mod Phi_3 -> %s ; x mod Phi_5 -> %s" % (
    (lambda r: r)(pdivmod([0, 1], cyclotomic(3))[1]), pdivmod([0, 1], cyclotomic(5))[1]))
P("  pdivmod(x^4, Phi_3) remainder = %s (expect x i.e. [0,1])" % (pdivmod([0, 0, 0, 0, 1], cyclotomic(3))[1],))

# X(6) caveat
D6 = [1, 2, 3, 6]
E6 = {frozenset(e) for e in [(1, 2), (1, 3), (2, 6), (3, 6)]}
# graph geodesic convexity of {1,2,3,6} in the 1-skeleton of X(6) (it is the whole 1-skeleton)
interval = g["interval"]
conv_vs = all(interval(a, b, 6) <= set(D6) for a in D6 for b in D6)
full_has_square = (1, frozenset({2, 3})) in g["cubes"](6)
P("  X(6) caveat: vertex set convex=%s, edges=%d, X(6) has the square=%s -> 4-cycle w/o square is not full: %s" % (
    conv_vs, len(E6), full_has_square, full_has_square))

# 3.3 hyperplane map: d -> N/d sends H+(p,k) onto H-(p, a_p-k+1)
bad = 0
for N in [12, 30, 36, 60, 360, 900, 6300, 30030]:
    f = factor(N); D = divisors(N)
    for p, a in f.items():
        for k in range(1, a + 1):
            img = {N // d for d in D if d % p ** k == 0}
            target = {d for d in D if d % p ** (a - k + 1) != 0}
            if img != target:
                bad += 1
            img_h = {frozenset((N // x, N // y)) for x in D for y in [x * p] if N % y == 0 and x % p ** (k - 1) == 0 and x % p ** k != 0}
            tgt_h = {frozenset((x, x * p)) for x in D if N % (x * p) == 0 and x % p ** (a - k) == 0 and x % p ** (a - k + 1) != 0}
            if img_h != tgt_h:
                bad += 1
P("  3.3 antipode H+(p,k) -> H-(p,a_p-k+1) and dual edges H(p,k)->H(p,a_p-k+1): bad=%d" % bad)

# F9 argument: principal orientations are consistent and injective (general proof step), test cases
bad = 0
for N in [12, 30, 36, 60, 360, 900, 6300, 30030]:
    f = factor(N); D = divisors(N)
    H = [(p, k) for p in sorted(f) for k in range(1, f[p] + 1)]
    seen = set()
    for d in D:
        o = tuple(d % p ** k == 0 for p, k in H)
        if o in seen:
            bad += 1
        seen.add(o)
        # consistency: d lies in every chosen half-space, so pairwise intersections are nonempty (contain d)
    # count of consistent orientations by the down-set rule equals tau
    if prod(a + 1 for a in f.values()) != len(D):
        bad += 1
P("  F9 principal orientations injective; down-set count = tau: bad=%d" % bad)

# 5.1 finite proxies: ray {2^k} and multiples of g convex inside X(n)
n = 2 ** 6 * 3 ** 3 * 5 ** 2 * 7
Dn = divisors(n)
ray = {2 ** k for k in range(7)}
mult = {d for d in Dn if d % 6 == 0}
P("  5.1 proxy in X(%d): ray {2^k} convex=%s ; multiples of 6 convex=%s" % (
    n, all(interval(a, b, n) <= ray for a in ray for b in ray), all(interval(a, b, n) <= mult for a in mult for b in mult)))

# F8 frequency map j -> jN/M
bad = 0
for M, N in [(4, 12), (6, 36), (12, 360), (30, 30030)]:
    imgs = set()
    for j in range(M):
        J = j * (N // M) % N
        if M // gcd(j, M) != N // gcd(J, N):
            bad += 1
        for x in range(N):
            if (j * (x % M) * N - J * x * M) % (M * N):
                bad += 1
        imgs.add(J)
    if imgs != {J for J in range(N) if M % (N // gcd(J, N)) == 0} or len(imgs) != M:
        bad += 1
P("  F8 j -> jN/M: injective, order kept, image = order | M, values kept: bad=%d" % bad)

print("\n".join(out))
