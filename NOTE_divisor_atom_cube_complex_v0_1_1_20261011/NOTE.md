# The divisor atom as a CAT(0) cube complex: note v0.1.1

Track `cat0-cube-complexes`, 2026-10-11. Owner: Opus [model: Claude Opus 5.5] (Skeleton), session `local_2851ecd3…`.
Status: **draft, spec scope.** Nothing is built. This is a note, not an instrument core.

**v0.1.1 supersedes v0.1** (folder `../NOTE_divisor_atom_cube_complex_v0_1_20261011/`, MANIFEST 3fb52de4…, which is kept unchanged).
- An independent Opus check of v0.1 returned PASS_WITH_FLAGS, with findings F1–F11 (`../NOTE_v0_1_OPUS_VERIFY_20261011/REPORT.md`, d1ce9054…).
- Every change below is marked **[v0.1.1, Fn]**, and the reviewer's suggested wording is adopted verbatim where it was given. The corrigendum table at the end lists each finding and its disposition.
- v0.1.1 has not itself been re-checked by an independent reviewer.

**Scope (saphir, verbatim).** "a general cubical/Fourier description of the whole divisor-atom family, plus its exact inter-atom relations. The small examples test that general construction; they don't define its limits."

**Registers.**
- **Exact:** every statement in §1–§5. `check_v0_1_1.py` checks them with integer or `Fraction` arithmetic, and the check IDs are given in brackets. Output is in `CHECK_OUTPUT.txt`. **[v0.1.1, F3]** Script checks cover the stated test cases where cited; §5.1, §5.2 and the §3.2 convexity classification rest on proof only. (Since v0.1.1, the §3.2 classification is also checked exhaustively for τ(N) ≤ 12 [C7b].)
- **Numerical:** only C12n, with floating point and tolerance 10⁻⁹; the maximum observed error was 2.1·10⁻¹². **[v0.1.1, F11]** The same statement is now also checked exactly [C12], so it no longer depends on the numerical register.
- **Drawing:** nothing yet.

A script check covers only the stated test cases. The general statements carry the short proofs given here, and those proofs are what a review should judge.

## 0. Notation

- N = ∏ p^{a_p} is the atom, with a_p ≥ 1 for each prime p dividing N.
- ω(N) is the number of distinct primes and Ω(N) = Σ a_p.
- τ, φ, μ are the divisor count, Euler's function and Möbius.
- v_p is the p-adic valuation.
- c_q(n) = Σ_{k | gcd(q,n)} μ(q/k)·k is the Ramanujan sum.

## 1. One atom: the cube complex X(N)

**Definition.**
- **Vertices:** Div(N).
- **Cubes:** for a vertex d and a set S of distinct primes with d·∏S | N, the cube spanned by S at d has the vertex set {d·∏T : T ⊆ S}.

**1.1 Product of paths.** d ↦ (v_p(d))_p identifies X(N) with the product of the paths [0, a_p], each subdivided into unit edges. Geometrically, X(N) is the Euclidean box ∏[0,a_p] ⊂ ℝ^{ω(N)}.
- It is a finite CAT(0) cube complex, being a product of trees.
- Its dimension is ω(N), and it has τ(N) vertices. [C1]

*Honest remark.* As a metric space, the CAT(0) property is trivial here, because a box is convex in Euclidean space. The content is combinatorial: the hyperplanes, the median and the convex subcomplexes. Those carry over to the whole family (§4), and they are what an instrument can read out exactly.

**1.2 Counts.** The number of k-cubes is
f_k(N) = Σ_{|S|=k} ∏_{p∈S} a_p · ∏_{p∉S} (a_p + 1),
and the Euler characteristic is 1 (the box is contractible). [C1]

| N | a_p | f-vector (f₀, f₁, …) | hyperplanes Ω |
|---|---|---|---|
| 12 | 2²·3 | 6, 7, 2 | 3 |
| 30 | 2·3·5 | 8, 12, 6, 1 | 3 |
| 360 | 2³·3²·5 | 24, 46, 29, 6 | 6 |
| 900 | 2²·3²·5² (a square) | 27, 54, 36, 8 | 6 |
| 6300 | 2²·3²·5²·7 | 54, 135, 126, 52, 8 | 7 |
| 30030 | 2·3·5·7·11·13 | 64, 192, 240, 160, 60, 12, 1 | 6 |

## 2. Hyperplanes, the Sageev picture, distance

**2.1 Hyperplanes.** There is one hyperplane H(p,k) for each prime power p^k dividing N, that is, 1 ≤ k ≤ a_p.
- Its half-spaces are H⁺(p,k) = {d : p^k | d} and H⁻(p,k) = {d : p^k ∤ d}.
- It is dual to exactly the edges d — dp with v_p(d) = k − 1.
- There are Ω(N) hyperplanes. [C2]

**2.2 Crossing.** H(p,j) and H(q,k) cross (all four quadrants are non-empty) if and only if p ≠ q. [C3]
- Hyperplanes of the same prime are nested: H⁺(p,k) ⊂ H⁺(p,j) for k > j.
- So the crossing graph is the complete multipartite graph with one part of size a_p per prime.

**2.3 Sageev reconstruction.** Choose one half-space per hyperplane such that no two chosen half-spaces are disjoint. The admissible choices correspond one-to-one with the vertices.
- For each p, the choice is a down-set of the chain H⁺(p,1) ⊃ … ⊃ H⁺(p,a_p), that is, a number v_p ∈ {0,…,a_p}.
- So the atom is recovered from its pocset of prime-power divisibility conditions alone. [C4: enumerated for every test case with Ω ≤ 14]
- **[v0.1.1, F9]** Why a count suffices: each vertex d gives a consistent orientation, namely H⁺(p,k) if and only if p^k | d. Distinct vertices give distinct orientations, so the map from vertices to orientations is injective, and equal finite counts make it a bijection. Since v0.1.1 the bijection is also checked directly: every consistent orientation meets in exactly one vertex, whose own orientation is that orientation. [C4b]

**2.4 Distance.** The combinatorial (ℓ¹) distance is the number of separating hyperplanes:
d(a,b) = Σ_p |v_p(a) − v_p(b)| = Ω(lcm(a,b)/gcd(a,b)). [C5, checked against breadth-first search on the 1-skeleton]

## 3. Median, intervals, symmetry, Möbius

**3.1 Median.** m(a,b,c) = gcd(lcm(a,b), lcm(b,c), lcm(c,a)) = lcm(gcd(a,b), gcd(b,c), gcd(c,a)).
- Coordinatewise, it is the median of three integers.
- It is the unique vertex lying in all three intervals I(a,b), I(b,c), I(c,a). Intervals are defined in §3.2. **[v0.1.1, F10]**
- So (Div(N), m) is the median algebra of the CAT(0) cube complex X(N). [C6: all triples for τ(N) ≤ 64]

**3.2 Intervals.** The geodesic interval between a and b, meaning the vertices on some shortest edge path, is
I(a,b) = {d : gcd(a,b) | d | lcm(a,b)}.
- This sub-box is isomorphic to X(lcm(a,b)/gcd(a,b)).
- The interval identity is checked for all pairs with τ(N) ≤ 64. [C7]
- ~~The convex subcomplexes of X(N) are exactly the sub-boxes {d : g | d | l} with g | l | N.~~ **[v0.1.1, F2]** The nonempty convex subcomplexes, in the CAT(0) metric sense or equivalently the full subcomplexes on geodesically convex vertex sets, are exactly the sub-boxes {d : g | d | l} with g | l | N, ∏C(a_p+2, 2) of them. [C7b: every vertex subset, τ(N) ≤ 12]
  - *Caveat:* convexity judged on the 1-skeleton alone is weaker. In X(6), the 4-cycle 1–2–6–3 without its square has a convex 1-skeleton but is not a full subcomplex, and so is not a sub-box.

**3.3 Antipode.** d ↦ N/d is an automorphism of X(N): it reverses every coordinate. ~~and swaps H⁺ with H⁻~~ **[v0.1.1, F4]** It maps H(p,k) to H(p, a_p−k+1), sending H⁺(p,k) onto H⁻(p, a_p−k+1).
- It fixes a vertex if and only if N is a square. [C8, with the square case 900 included]
- For squarefree N, it is the central symmetry of the Boolean cube and fixes only the centre point.

**3.4 Möbius as a cubical sign.** μ(n/d) ≠ 0 if and only if d is a vertex of the unit cube below n, spanned by the primes of n. On that cube, μ(n/d) = (−1)^{dim of the cube spanned from d to n}. [C9: since v0.1.1 tested against the enumerated cube list, not against μ's own definition]
- So Möbius inversion is the alternating sum over that one cube. **[v0.1.1, F7]** If g(n) = Σ_{d|n} f(d) for all n | N, then f(n) = Σ_{d|n} μ(n/d) g(d). [C9 inversion]

## 4. The Fourier layer: vertices are frequency classes

This is the bridge to the Fourier instrument.

**4.1 Frequency classes.** In the DFT of ℤ/N, the frequency j has additive order d = N/gcd(j,N), which is a divisor of N.
- The frequencies of order exactly d number φ(d), and Σ_{d|N} φ(d) = N. [C10]
- **Reading:** vertex d of X(N) is the Galois orbit of the primitive d-th roots of unity among the DFT characters of ℤ/N.
- **Reading:** H⁺(p,k) is the set of frequencies whose order is divisible by p^k.

**4.2 Ramanujan sums are the vertex characters.**
- c_d(n) = Σ_{j mod d, gcd(j,d)=1} e^{2πi jn/d}: the sum, over the vertex's orbit, of the selected DFT characters. **[v0.1.1, F11]** This is checked exactly in ℤ[x]/(Φ_d) for N ∈ {12, 30, 360, 900} [C12]. The v0.1 floating-point check is kept as C12n.
- Exactly, c_d(n) depends only on gcd(n,d).
- [C11, exact for N ≤ 360] The functions on ℤ/N that depend only on gcd(n,N) form a space of dimension τ(N), one coordinate per vertex.
- [C11] {c_d : d | N} is an orthogonal basis of that space, with Σ_{n mod N} c_d(n) c_e(n) = N φ(d) δ_{de}.
- [C11] The expansion coefficients are exact rationals:
  f(n) = Σ_{d|N} α(d) c_d(n), with α(d) = (1/(N φ(d))) Σ_{e|N} f(e) φ(N/e) c_d(e), writing f(e) for the value at gcd = e.

## 5. Inter-atom relations: the whole family

**5.1 The family is one complex.** X(N) is the convex sub-box I(1,N) of a single infinite cube complex X(ℕ).
- **Vertices:** all positive integers.
- **Edges:** n — np for every prime p.
- **Hyperplanes:** H(p,k) for all primes p and all k ≥ 1.

X(ℕ) is the restricted product of one ray per prime. It is locally infinite, with cubes of every finite dimension but no infinite cube.

~~It is an infinite-dimensional, locally infinite CAT(0) cube complex in the combinatorial sense: median, hyperplanes and Sageev duality, with the formulas of §2–§3 holding verbatim. The finite atoms are its finite convex sub-boxes.~~

**[v0.1.1, F1]** Distance (§2.4), median (§3.1) and intervals (§3.2) hold verbatim. Sageev duality holds for orientations that choose only finitely many H⁺. The finite convex subcomplexes are exactly the I(g,l), each isomorphic to X(l/g). Infinite convex subcomplexes also exist. §3.3 has no global analogue. Metric CAT(0) follows from the link condition in arbitrary dimension [Leary 2013, to pin].
- *Why the old wording failed.* The choice {H⁺(2,k) for all k} is consistent but corresponds to no integer. The multiples of g, and the ray {2^k}, are infinite convex subcomplexes. There is no global antipode, and the §1.2 counts are infinite.
- *What does hold.* The 1-skeleton is a median graph, and every finite configuration lies inside some convex X(n). The complex is simply connected with flag links. This combinatorial structure is all the construction uses; the metric CAT(0) statement waits on pinning Leary 2013.

**[v0.1.1, F5]** The atoms are the boxes I(1,N); each finite convex sub-box I(g,l) is a translate of X(l/g). This is the general construction asked for in the scope. Every relation below is a statement about convex subcomplexes of X(ℕ), and the test cases only sample it.

**5.2 Divisibility = convex inclusion.** If M | N, then X(M) = I(1,M) ⊂ X(N) is a convex subcomplex.
- The hyperplanes of X(N) meeting it are the H(p,k) with k ≤ v_p(M).
- On the Fourier side, the characters of ℤ/N whose order divides M are exactly the characters of the quotient ℤ/M. So the inclusion of complexes is dual to the quotient map ℤ/N → ℤ/M. **[v0.1.1, F8]** Explicitly, a frequency j mod M corresponds to the frequency j·N/M mod N. This map is injective, keeps the order and the character values, and its image is the set of frequencies of order dividing M.
- Neither statement in §5.2 has its own script check; both rest on the proofs here. Convexity is §3.2 with g = 1 and l = M, and the duality is standard character theory of ℤ/N.

**5.3 Translates.** If eM | N, then d ↦ ed maps X(M) isomorphically onto the convex sub-box I(e, eM), as a full subcomplex. [R6]

**5.4 Meet and hull.** Inside X(lcm(M,N)):
- Div(M) ∩ Div(N) = Div(gcd(M,N)). [R1]
- The convex hull of Div(M) ∪ Div(N) is Div(lcm(M,N)). [R2]
- The union itself is convex ~~only when~~ **[v0.1.1, F6]** if and only if one atom divides the other. [R2 and R3: since v0.1.1 the pairs include divisible ones (6,12), (30,30030), (4,36), and the gate is lifted so (360, 30030) is tested]

**5.5 Coprime atoms multiply.** If gcd(M,N) = 1, then X(MN) = X(M) × X(N).
- The f-vectors convolve, and the hyperplane sets form a disjoint union.
- Every hyperplane of M crosses every hyperplane of N. [R5, C3; **v0.1.1, F10:** R5 now compares enumerated cubes, not the formula with itself]

**5.6 Fourier compatibility.** For d | gcd(M,N), the vertex character c_d is the same function whether it is read on ℤ/M, on ℤ/N or on ℤ/lcm. [R4]
- So the Ramanujan coordinates of §4 are coherent across the whole family. A vertex keeps its character when the atom grows.
- R4 checks this for n < 5000 only. That the expansion coefficients stay the same as the atom grows was confirmed by the independent check's script, not by R4.

## 6. Open items (not claims)

- **O1. The 30030 spine reading.** The memory record says that for an even prime count the antipodal anchors force 11 divisors of 30030 onto the viewer's spine. §3.3 gives the exact antipode, but the link from it to those 11 divisors, through the viewer's drawing map, is not derived here. This is the first known-answer test for the drawing register.
- **O2. Which Fourier structure the instrument draws.** §4 uses the Ramanujan/frequency-class layer. Two alternatives exist:
  - the Walsh characters of the Boolean cube in the squarefree case;
  - the graph-Laplacian eigenbasis of the box, a tensor product of path DCTs.

  These are different objects, and saphir chooses.
- **O3. Literature check.** The papers saved in `../openai_math_cat0_papers_20261011/` are obstruction results: groups with no geometric CAT(0) action, the Salvetti complex for Artin groups, and fillings. None is needed for §1–§5. A reviewer may judge whether any of them bears on §5.1.
- **O4. Instrument fit.** The viewer-redesign requirements v0.1 (bus #242) are under review. Fitting this note into an exact core, a panel and a dial ledger waits on those requirements and on saphir's word "build" (gate G7).

- **O5. Pin Leary 2013** (metric CAT(0) for infinite-dimensional cube complexes via the link condition) before the metric claim in §5.1 is cited. **[v0.1.1, from F1]**

## Corrigendum v0.1 → v0.1.1

| Finding | Severity | Disposition |
|---|---|---|
| F1 §5.1 "formulas of §2–§3 verbatim" false | MAJOR | Struck; reviewer's replacement adopted verbatim; reasons and O5 added |
| F2 §3.2 "convex" undefined, untested | MEDIUM | Reviewer's wording adopted verbatim; X(6) caveat added; new exhaustive check C7b |
| F3 registers line overstates coverage | MEDIUM | Reviewer's sentence adopted verbatim |
| F4 §3.3 "swaps H⁺ with H⁻" | LOW | Corrected, reviewer's wording |
| F5 §5.1 "finite atoms are its finite convex sub-boxes" | LOW | Reviewer's wording adopted |
| F6 §5.4 "only when" | LOW | "if and only if"; divisible pairs added; gate lifted |
| F7 §3.4 inversion hypothesis; C9 tautological | LOW | Hypothesis stated; C9 now tests the cube list, plus inversion |
| F8 §5.2 frequency map implicit | LOW | j ↦ j·N/M stated |
| F9 §2.3 count vs bijection | LOW | Justification added, and direct check C4b |
| F10 R5 self-comparison; "interval" used before defined | LOW | R5 enumerates cubes; forward reference added |
| F11 C12 needlessly numerical | INFO | Exact check C12 added in ℤ[x]/(Φ_d); C12n kept |

Not changed: R4's n < 5000 range (disclosed in §5.6), and C8/R6 checking edges only (judged acceptable by the reviewer).

## Files

- `NOTE.md` (this file)
- `check_v0_1_1.py` (exact checks; Python standard library only)
- `CHECK_OUTPUT.txt` (output of the run: 0 failures)
- `MANIFEST.sha256`
