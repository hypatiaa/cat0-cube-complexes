"""F2/F3 probes. Own float transcription of divisorPosition (file 5, lines 1445-1465), all chiralities.
F2: squarefree, mode 'global' -> (-sum_{i in S} zeta_m^{-i}, |S|); 'positive' -> (-sum zeta_m^{i}, |S|).
F3: empty factorisation -> (0,0,0)."""
from math import cos, sin, pi
from itertools import product

def divisorPosition(exps, fac, chir='positive'):
    m = len(fac); x = y = z = 0.0
    wS = 1 if chir == 'positive' else -1
    aS = -1 if chir == 'global' else 1
    for i, a in enumerate(fac):
        n = a + 1; r = 1 / n; e = exps[i]
        phi = (2 * pi * i) / m if m > 1 else 0
        pu = aS * phi
        ang = wS * (2 * pi * e) / n + pu
        x += r * (cos(ang) - cos(pu)); y += r * (sin(ang) - sin(pu)); z += e
    return x, y, z

err_g = err_p = 0.0
for m in range(1, 11):
    fac = [1] * m
    for S in product([0, 1], repeat=m):
        z = [complex(cos(2 * pi * i / m), sin(2 * pi * i / m)) for i in range(m)]
        pg = -sum(z[i].conjugate() for i in range(m) if S[i])
        pp = -sum(z[i] for i in range(m) if S[i])
        X, Y, Z = divisorPosition(S, fac, 'global')
        err_g = max(err_g, abs(X - pg.real), abs(Y - pg.imag), abs(Z - sum(S)))
        X, Y, Z = divisorPosition(S, fac, 'positive')
        err_p = max(err_p, abs(X - pp.real), abs(Y - pp.imag), abs(Z - sum(S)))
print("F2 global formula max err m=1..10:", err_g)
print("positive formula max err m=1..10:", err_p)
print("F3 empty factorisation:", divisorPosition((), [], 'positive'), divisorPosition((), [], 'global'))
