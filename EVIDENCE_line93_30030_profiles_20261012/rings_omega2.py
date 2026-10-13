"""Read-only evidence for the Idea Catalog line-93 question (saphir/Astra, 2026-10-12).
Omega = 2 slice of the frozen viewer drawing (mode 'positive', viewer sha256 3d65e14a...),
for N = 30030 and N = 30030^2. Positions exact in Q(zeta_L) using the cat0 note v0.1.8 map
(imported from ../NOTE_divisor_atom_cube_complex_v0_1_8_20261011/check_v0_1_7_o6.py, unchanged).
Radii and zeta_12 phases are then read off in floating point (NUMERICAL register) and checked
to be integral within 1e-9; the coincidence groups themselves are exact.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', 'NOTE_divisor_atom_cube_complex_v0_1_8_20261011', 'check_v0_1_7_o6.py'), encoding='utf-8').read()
ns = {}
exec(src[:src.index('CASES = [')], ns)
from itertools import product
from math import pi, atan2, sqrt, isclose
from collections import defaultdict
for label, N in [('squarefree 30030', 30030), ('exponent 2, 30030^2', 30030 ** 2)]:
    fac, m, F = ns['setup'](N)
    pts = defaultdict(list)
    for e in product(*[range(a + 1) for p, a in fac]):
        if sum(e) != 2:
            continue
        d = 1
        for (p, a), x in zip(fac, e):
            d *= p ** x
        pts[ns['pos_exact'](e, fac, m, F)[0]].append(d)
    print(f'== {label}: {sum(len(v) for v in pts.values())} divisors at Omega=2, {len(pts)} points')
    rings = defaultdict(list)
    for v, ds in pts.items():
        z = ns['to_complex'](v, F)
        if abs(z) < 1e-12:
            rings['origin'].append(sorted(ds))
            continue
        ph = atan2(z.imag, z.real) * 6 / pi % 12
        rings[round(abs(z) ** 2, 9)].append((ph, sorted(ds)))
    for k in sorted(rings, key=lambda x: (x != 'origin', x)):
        if k == 'origin':
            print('  origin:', rings[k])
            continue
        rows = sorted(rings[k])
        print(f'  radius^2={k} (radius {sqrt(k):.6f}): zeta12 powers {[int(round(p)) for p, _ in rows]}, integral={all(isclose(p, round(p), abs_tol=1e-9) for p, _ in rows)}')
        for p, ds in rows:
            print(f'     zeta12^{int(round(p))}: {ds}')
