"""Follow-up probes: m = 2 (a,a) atoms and the 900900 third-type coincidences. Imports verify_o6 helpers."""
import sys, io, contextlib
from itertools import combinations
sys.argv = [sys.argv[0], "NUL_unused.txt"]
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    import verify_o6 as V   # re-runs the main script silently (its output file is written to NUL_unused.txt)

def show(fac, maxcls=12):
    r = V.analyse(fac, mech=True)
    A = r['A']
    print(V.fac_str(fac), "lost", r['lost'], "R-path", r['explained_R'], "span-classes", r['classes_in_span'])
    for c in r['classes'][:maxcls]:
        vals = [A.value(e) for e in c]
        H = [A.hcoord(e) for e in c]
        diffs = []
        for a, b in combinations(range(len(c)), 2):
            d = {A.lab[i]: H[a][i] - H[b][i] for i in range(len(H[a])) if H[a][i] - H[b][i]}
            diffs.append((vals[a], vals[b], d))
        print("  class", vals, diffs)
    return r

print("--- 2^3*3^3 (216) ---"); show([(2, 3), (3, 3)])
print("--- 2^5*3^5 ---"); show([(2, 5), (3, 5)])

print("--- 900900: decomposition of 55 vs 14 ---")
A = V.Atom(V.factor(900900))
idx = {lab: i for i, lab in enumerate(A.lab)}
d = A.D
print("D =", d, "L =", A.L)
for lab in [(2, 1), (5, 1), (7, 1), (11, 1)]:
    print(lab, "D*w =", A.w[idx[lab]])
lhs = V.vadd(A.w[idx[(5, 1)]], A.w[idx[(2, 1)]], -1)
rhs = V.vadd(A.w[idx[(7, 1)]], A.w[idx[(11, 1)]], -1)
print("w(5,1)-w(2,1) == w(7,1)-w(11,1):", lhs == rhs, lhs)
# pos(55) and pos(14) equal?
e55 = tuple(1 if p in (5, 11) else 0 for p, a in A.fac)
e14 = tuple(1 if p in (2, 7) else 0 for p, a in A.fac)
print("pos(55) == pos(14):", A.pos(e55) == A.pos(e14), A.pos(e55))
# integrality: D*(w(5,1)-w(2,1)) should equal D * (-zeta_3), i.e. -D*zeta_6^2 reduced
v = [0] * A.L; v[(A.L // 3) % A.L] = -A.D
print("w(5,1)-w(2,1) == -zeta_3:", lhs == V.reduce_mod(v, A.L))

print("--- 900900 class-size histogram and per-class R-components ---")
r = V.analyse(V.factor(900900), mech=True)
from collections import Counter
print(Counter(len(c) for c in r['classes']))
