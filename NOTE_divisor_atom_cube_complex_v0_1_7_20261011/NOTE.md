# The divisor atom as a CAT(0) cube complex: note v0.1.7

Track `cat0-cube-complexes`, 2026-10-11. Owner: Opus [model: Claude Opus 5.5] (Skeleton), session `local_2851ecd3…`.
Status: **draft, spec scope.** v0.1.6 (O6, §7.6) **failed** its independent check: m = 2 is not always injective, and a third kind of coincidence exists. v0.1.7 corrects §7.6 at saphir's word ("go ahead"), in the checker's wording, and asserts every claim that v0.1.6 only printed. It is unreviewed. Nothing is built. **[v0.1.7]** This is a note, not an instrument core.

**v0.1.7 supersedes v0.1.6** (folder `../NOTE_divisor_atom_cube_complex_v0_1_6_20261011/`, MANIFEST bd7ad3ca…, kept unchanged as the record of what failed).
- The independent check of v0.1.6 (verdict FAIL): `../NOTE_v0_1_6_OPUS_CHECK_20261011/REPORT.md`, folder MANIFEST 3176eee6…. The owner confirmed both headline counterexamples with the note's own exact map.
- Changes are marked **[v0.1.7, Gn]**. v0.1.6 was never sent to Astra.
- `check_v0_1_7_o6.py` is check_v0_1_6_o6.py with dead code and stale comments removed, the 2³·3³ and 2⁵·3⁵ atoms added, a rank ker(w, z) column added, and new asserts G1–G12. Every v0.1.6 assert is kept unchanged. The v0.1.5 scripts are carried over byte-identical.

**v0.1.6 superseded v0.1.5** (folder `../NOTE_divisor_atom_cube_complex_v0_1_5_20261012/`, MANIFEST e3d333e4…, kept unchanged).
- Astra's review of v0.1.5: bus #263, `stack_bus_autocheck/coordination/review-261-20261011/REVIEW.json` c8554610….
- Changes are marked **[v0.1.6, #263 Fn]** and **[v0.1.6, O6]**.
- The v0.1.5 scripts and outputs are carried over byte-identical. The new check for §7.6 is `check_v0_1_6_o6.py`, with output in `CHECK_O6_OUTPUT.txt`, which also prints per-check pass counts.

**v0.1.5 superseded v0.1.4** (folder `../NOTE_divisor_atom_cube_complex_v0_1_4_20261012/`, MANIFEST 9013af6b…, kept unchanged).
- Independent check of v0.1.4: `../NOTE_v0_1_4_OPUS_CHECK_20261012/REPORT.md`.
- Astra's delta review of v0.1.3: bus #260, `stack_bus_autocheck/coordination/review-259-20261011/REVIEW.json` a8018c54….
- Changes are marked **[v0.1.5, En]** for the check findings, **[v0.1.5, #260 F1]** and **[v0.1.5, O2 wording]**. The reviewers' wording is adopted verbatim where it was given.
- **Scripts.** `check_v0_1_5.py` is check_v0_1_3.py plus per-check pass counters. `check_v0_1_5_drawing.py` is check_v0_1_4_drawing.py plus the counters and new asserts E1, E2, E3, E4, E12. Both outputs now print, for every check ID, how many times it ran and passed, so a fresh run is visible (Astra #260). No earlier check logic was changed.
- **Date correction (E12).** v0.1.4 and this folder carry "20261012" in their names and in the O2 date, but the session date was 2026-10-11. The folder names are kept, so that existing references still resolve; the dates in the text are corrected.

**v0.1.4 superseded v0.1.3** (folder `../NOTE_divisor_atom_cube_complex_v0_1_3_20261011/`, MANIFEST dba2a6e5…, kept unchanged).
- Additions are marked **[v0.1.4, O1]**, **[v0.1.4, O2]** and **[v0.1.4, O5]**. No v0.1.3 statement is changed except where a marker shows.
- `check_v0_1_3.py` and its output are carried over byte-identical. The new checks for §7 are in `check_v0_1_4_drawing.py`, with output in `CHECK_DRAWING_OUTPUT.txt`.

**v0.1.3 superseded v0.1.2** (folder `../NOTE_divisor_atom_cube_complex_v0_1_2_20261011/`, MANIFEST 47d2e145…, kept unchanged).
- Astra's review: bus #255; `stack_bus_autocheck/coordination/review-252-20261011/REVIEW.json` 8b2eb7fa…, MANIFEST 8d852005….
- Changes are marked **[v0.1.3, C1]**, **[v0.1.3, C2]** and **[v0.1.3, P1/P2]** for the two nonblocking precision points. Astra's wording is adopted verbatim where it was given.
- The script is now `check_v0_1_3.py`. It is the v0.1.1 script unchanged, plus checks A1–A3; the earlier checks are byte-for-byte the same code.

**v0.1.2 superseded v0.1.1** (folder `../NOTE_divisor_atom_cube_complex_v0_1_1_20261011/`, MANIFEST aeb3bf60…, kept unchanged). An independent Opus delta check of v0.1.1 returned PASS_WITH_FLAGS: F1–F11 all RESOLVED, plus new flags D1–D5 (`../NOTE_v0_1_1_OPUS_DELTA_20261011/REPORT.md`). v0.1.2 changes wording only. Each change is marked **[v0.1.2, Dn]**, and the delta reviewer's wording is adopted verbatim. `check_v0_1_1.py` and its output are byte-identical to v0.1.1.

**v0.1.1 superseded v0.1** (folder `../NOTE_divisor_atom_cube_complex_v0_1_20261011/`, MANIFEST 3fb52de4…, which is kept unchanged).
- An independent Opus check of v0.1 returned PASS_WITH_FLAGS, with findings F1–F11 (`../NOTE_v0_1_OPUS_VERIFY_20261011/REPORT.md`, d1ce9054…).
- Every change below is marked **[v0.1.1, Fn]**, and the reviewer's suggested wording is adopted verbatim where it was given. The corrigendum table at the end lists each finding and its disposition.
- ~~v0.1.1 has not itself been re-checked by an independent reviewer.~~ It has been: see the delta check above. **[v0.1.2]**
- **[v0.1.2, D3]** Four v0.1.1 changes carried no marker. They are now marked **[v0.1.1, F1]**, **[v0.1.1, R4 audit note]** and **[v0.1.1, F2]**, and the status line change is marked D3d.

**Scope (saphir, verbatim).** "a general cubical/Fourier description of the whole divisor-atom family, plus its exact inter-atom relations. The small examples test that general construction; they don't define its limits."

**Registers.**
- **Exact:** every statement in §1–§5. ~~`check_v0_1_1.py`~~ **[v0.1.5, #260 F1]** `check_v0_1_5.py` (in this folder; its predecessor check_v0_1_1.py is in the v0.1.1 folder) checks them with integer or `Fraction` arithmetic, and the check IDs are given in brackets. Output is in `CHECK_OUTPUT.txt`. **[v0.1.1, F3]** Script checks cover the stated test cases where cited; §5.1, §5.2 and the §3.2 convexity classification rest on proof only. (Since v0.1.1, the §3.2 classification is also checked exhaustively [C7b: every vertex subset, for the test cases with τ(N) ≤ 12: N = 1, 12, 30, 36, 60]. **[v0.1.2, D4]**)
- **Numerical:** only C12n, with floating point and tolerance 10⁻⁹; the maximum observed error was 2.1·10⁻¹². **[v0.1.1, F11]** The same statement is now also checked exactly [C12], so it no longer depends on the numerical register.
- ~~**Drawing:** nothing yet.~~ **[v0.1.6, #263 F1]** **Drawing:** §7 is the drawing register. Its exact statements are checked in ℤ[ζ_m] or ℚ(ζ_L) [D1–D4, S1–S6, E1–E4, E12, L1–L3, T1–T4]. Its comparisons with ~~the viewer's own float code~~ **[v0.1.7, G11]** float transcriptions of the viewer's code are numerical cross-checks [V0, tolerance 10⁻¹², max 8.9·10⁻¹⁶; V1, tolerance 10⁻¹², max 1.3·10⁻¹⁵].
- **[v0.1.6, #263 F1]** The numerical register therefore holds C12n, V0 and V1. None of them is a source for an exact value.

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

*Honest remark.* As a metric space, the CAT(0) property is trivial here, because a box is convex in Euclidean space. The content is combinatorial: the hyperplanes, the median and the convex subcomplexes. Those carry over to the whole family ~~(§4)~~ **[v0.1.2, D2]** (§5.1), with the exceptions listed there, and they are what an instrument can read out exactly.

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
- **[v0.1.1, F2]** The interval identity is checked for all pairs with τ(N) ≤ 64. [C7]
- ~~The convex subcomplexes of X(N) are exactly the sub-boxes {d : g | d | l} with g | l | N.~~ **[v0.1.1, F2]** The nonempty convex subcomplexes, in the CAT(0) metric sense or equivalently the full subcomplexes on ~~geodesically convex~~ **[v0.1.3, P1]** combinatorially geodesically convex (closed under all graph intervals) vertex sets, are exactly the sub-boxes {d : g | d | l} with g | l | N, ∏C(a_p+2, 2) of them. [C7b: every vertex subset, for the test cases with τ(N) ≤ 12: N = 1, 12, 30, 36, 60] **[v0.1.2, D4]**
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
- [C11] The expansion is
  f(n) = Σ_{d|N} α(d) c_d(n), with α(d) = (1/(N φ(d))) Σ_{e|N} f(e) φ(N/e) c_d(e), writing f(e) for the value at gcd = e.
- ~~The expansion coefficients are exact rationals.~~ **[v0.1.3, C1]** Scalar field: the formula holds for f with values in ℚ, ℝ or ℂ. α is ℚ-linear in the values f(e), with rational weights. So α(d) is rational when f is rational-valued, and only then is the exact-rational claim made. Counterexample to the unqualified claim (Astra): the constant f = √2 gives α(1) = √2 and α(d) = 0 otherwise. [A1: a constant c gives α(1) = c and α(d) = 0 otherwise] Every function tested in C11 is rational-valued. Future serialization of rational α uses reduced numerator and positive-denominator decimal integer strings.

## 5. Inter-atom relations: the whole family

**5.1 The family is one complex.** X(N) is the convex sub-box I(1,N) of a single infinite cube complex X(ℕ).
- **Vertices:** all positive integers.
- **Edges:** n — np for every prime p.
- **Hyperplanes:** H(p,k) for all primes p and all k ≥ 1.

X(ℕ) is the restricted product of one ray per prime. **[v0.1.1, F1]** It is locally infinite, with cubes of every finite dimension but no infinite cube.

~~It is an infinite-dimensional, locally infinite CAT(0) cube complex in the combinatorial sense: median, hyperplanes and Sageev duality, with the formulas of §2–§3 holding verbatim. The finite atoms are its finite convex sub-boxes.~~

**[v0.1.1, F1]** Distance (§2.4), median (§3.1) and intervals (§3.2) hold verbatim. Sageev duality holds for orientations that choose only finitely many H⁺. The finite convex subcomplexes are exactly the I(g,l), each isomorphic to X(l/g). Infinite convex subcomplexes also exist. §3.3 has no global analogue. Metric CAT(0) follows from the link condition in arbitrary dimension ~~[Leary 2013, to pin] (not yet cited; see O5). **[v0.1.2, D1]**~~ **[v0.1.4, O5]** [Leary, *A metric Kan–Thurston theorem*, arXiv:1009.1540v3, Theorem B.8, p. 28]. See the pin below.
- *Why the old wording failed.* The choice {H⁺(2,k) for all k} is consistent but corresponds to no integer. The multiples of g, and the ray {2^k}, are infinite convex subcomplexes. There is no global antipode, and the §1.2 counts are infinite.
- *What does hold.* The 1-skeleton is a median graph, and every finite configuration lies inside some convex X(n). The complex is simply connected with flag links. ~~This combinatorial structure is all the construction uses; the metric CAT(0) statement waits on pinning Leary 2013.~~ **[v0.1.2, D1]** ~~This combinatorial structure is all the construction uses; the metric CAT(0) sentence above is stated subject to O5.~~ **[v0.1.4, O5]** The pin below discharges O5.

**[v0.1.4, O5] The pin.** The local copy is `../reference_leary_2013/leary_metric_kan_thurston_arXiv_1009.1540.pdf` (sha256 191d26ad…). The journal reference is from memory and not checked: J. Topology 6 (2013) 251–284. **[v0.1.5, E11]** The PDF itself says only "Submitted exclusively to the London Mathematical Society".
- **[v0.1.5, E11]** B.8 carries no completeness hypothesis and no local-finiteness hypothesis. Its general case is proved through finite combinatorially convex subcomplexes (Theorem B.4). Leary takes the definition of a cubical complex from Bridson–Haefliger I.7.40(3); that text was not read for this note.
- **Theorem B.8 (Gromov's criterion, proved in Leary's Appendix B with no dimension bound):** "A simply connected cubical complex is CAT(0) if and only if its vertex links are flag complexes."
- **The hypotheses hold for X(ℕ):**
  - *Cubical complex.* Each cube (d,S) is embedded, and two cubes meet in a common face or not at all, since the intersection of two sub-boxes is a sub-box. Leary works with cubical complexes, not the more general cube complexes; X(ℕ) is cubical.
  - *Simply connected.* ~~A loop is compact, so it lies in a finite subcomplex. … so this holds in either topology.~~ **[v0.1.5, E8]** In the CW topology a loop is compact, so it lies in a finite subcomplex, hence in some contractible box X(n), and is null-homotopic. Leary's Theorem A.7 (p. 25) makes the identity from the CW topology to the metric topology a homotopy equivalence, so X(ℕ) is simply connected in the metric topology too.
  - *Flag links.* The link of the vertex n has one vertex per edge at n: up-edges n—np for every prime p, and down-edges n—n/p for p | n. Two of these are joined exactly when they belong to a common square, that is, when their primes differ. ~~A set of pairwise-joined link vertices therefore has distinct primes, and so it spans a cube at n.~~ **[v0.1.5, E9]** A finite set of pairwise-joined link vertices has distinct primes, so it spans the cube (n/∏T, S) containing n, where S is its set of primes and T the primes of its down-edges. (The infinite set of all up-edges is pairwise joined but spans no simplex; flagness concerns finite sets.)
- **Conclusion:** X(ℕ), with its natural piecewise-Euclidean path metric, is CAT(0).
- **Caveat, new in v0.1.4: X(ℕ) is not metrically complete.** Leary's Theorem A.6 (p. 24) says the metric is complete if and only if there is no infinite ascending sequence of cells. X(ℕ) has one: the cubes at 1 spanned by {2}, {2,3}, {2,3,5}, …. So X(ℕ) is a CAT(0) space that is not complete. Results stated for complete CAT(0) spaces, such as fixed-point theorems, do not transfer without checking. Leary's Theorem B.11 handles finite group actions on arbitrary CAT(0) cubical complexes. **[v0.1.5, E11]** It applies to finite groups acting by automorphisms, complete or not, and gives a non-empty, contractible fixed set.
- Every finite atom X(N) is a finite box, so it is complete.

**[v0.1.1, F5]** The atoms are the boxes I(1,N); each finite convex sub-box I(g,l) is a translate of X(l/g). This is the general construction asked for in the scope. Every relation below is a statement about convex subcomplexes of X(ℕ), and the test cases only sample it.

**5.2 Divisibility = convex inclusion.** If M | N, then X(M) = I(1,M) ⊂ X(N) is a convex subcomplex.
- The hyperplanes of X(N) meeting it are the H(p,k) with k ≤ v_p(M).
- On the Fourier side, the characters of ℤ/N whose order divides M are exactly the characters of the quotient ℤ/M. So the inclusion of complexes is dual to the quotient map ℤ/N → ℤ/M. **[v0.1.1, F8]** Explicitly, a frequency j mod M corresponds to the frequency j·N/M mod N. This map is injective, keeps the order and the character values, and its image is the set of frequencies of order dividing M.
- Neither statement in §5.2 has its own script check; both rest on the proofs here. Convexity is §3.2 with g = 1 and l = M, and the duality is standard character theory of ℤ/N.

**5.3 Translates.** If eM | N, then d ↦ ed maps X(M) isomorphically onto the convex sub-box I(e, eM), as a full subcomplex. [R6]

**5.4 Meet and hull.** Inside X(lcm(M,N)):
- Div(M) ∩ Div(N) = Div(gcd(M,N)). [R1]
- The ~~convex hull~~ **[v0.1.3, P2]** smallest convex cubical subcomplex containing Div(M) ∪ Div(N) is Div(lcm(M,N)). [R2] This is not the Euclidean convex hull. For M = 2, N = 3 in X(6), the Euclidean hull of the three vertices is a triangle, while the cubical hull is the square. [A3]
- The union itself is convex ~~only when~~ **[v0.1.1, F6]** if and only if one atom divides the other. [R2 and R3: since v0.1.1 the pairs include divisible ones (6,12), (30,30030), (4,36); ~~the gate is lifted~~ **[v0.1.2, D5]** the gate is raised to τ(lcm) ≤ 256, so all seven pairs, including (360, 30030), are tested]

**5.5 Coprime atoms multiply.** If gcd(M,N) = 1, then X(MN) = X(M) × X(N).
- The f-vectors convolve, and the hyperplane sets form a disjoint union.
- Every hyperplane of M crosses every hyperplane of N. [R5, C3; **v0.1.1, F10:** R5 now compares enumerated cubes, not the formula with itself]

**5.6 Fourier compatibility.** For d | gcd(M,N), the vertex character c_d is the same function whether it is read on ℤ/M, on ℤ/N or on ℤ/lcm. [R4]
- So the Ramanujan coordinates of §4 are coherent across the whole family. A vertex keeps its character when the atom grows. **[v0.1.3, C2]** Read the common c_d as one periodic integer function of n, or as its pullback to ℤ/lcm.
- **[v0.1.1, R4 audit note]** R4 checks this for n < 5000 only. ~~That the expansion coefficients stay the same as the atom grows was confirmed by the independent check's script, not by R4.~~
- **[v0.1.3, C2]** Common basis functions do not make the coefficients invariant for unrelated data on different atoms. Counterexample (Astra): f_M(n) = gcd(n,M) gives (α1, α2) = (3/2, 1/2) for M = 2, and (α1, α2, α4) = (2, 1, 1/2) for M = 4. [A2b]
- **[v0.1.3, C2]** The actual statement: if M divides N and f_N(n) = f_M(n mod M), the old coefficients are retained, and the coefficients indexed by d not dividing M are zero. This follows from periodicity and the uniqueness of the expansion. It is the case the independent check tested, a fixed pullback function. [A2, 5 pairs]

## 6. Open items (not claims)

- ~~**O1. The 30030 spine reading.** … not derived here.~~ **[v0.1.4, O1]** Derived in §7. Correction to the record: 10 divisors lie on the spine, at 5 heights. ~~11 is the total number of points lost to coincidence, and 7 of those losses are off the spine.~~ **[v0.1.5, E1]** 11 is the total number of points lost to coincidence: 5 on the spine and 6 off it (the six Ω=3 pairs). 7 of the 11 losses occur at Ω=3. [E1, now asserted]
- **O2. Which Fourier structure the instrument draws.** §4 uses the Ramanujan/frequency-class layer. Two alternatives exist:
  - the Walsh characters of the Boolean cube in the squarefree case;
  - the graph-Laplacian eigenbasis of the box, a tensor product of path DCTs.

  ~~These are different objects, and saphir chooses.~~ **[v0.1.4, O2] Decided by saphir, ~~2026-10-12~~ 2026-10-11 [v0.1.5, E12]:** "o2 - go with your recommendation. I agree with Ramanujan for O2, but Walsh is necessary for squarefree N."
  - The Ramanujan/frequency-class layer (§4) is the primary Fourier layer.
  - ~~The Walsh layer is **required**, not optional, for squarefree N.~~ **[v0.1.5, O2 wording]** saphir, refining the decision: "walsh is an overlay, but not optional for squarefree N, it is how we see it." The Walsh layer is a **required overlay** for squarefree N. It is how the squarefree cube is seen, not an optional display feature, and it sits over the Ramanujan primary layer.
  - §7.4 ~~shows why~~ **[v0.1.5, E5]** gives the reason: the existing drawing of squarefree atoms already lives entirely in the Walsh characters of degree ≤ 1.
  - The Laplacian eigenbasis is not adopted.
- **O3. Literature check.** The papers saved in `../openai_math_cat0_papers_20261011/` are obstruction results: groups with no geometric CAT(0) action, the Salvetti complex for Artin groups, and fillings. None is needed for §1–§5. A reviewer may judge whether any of them bears on §5.1.
- ~~**O6. [v0.1.4, O1]** Coincidences in the drawing of non-squarefree atoms (general n_i, r_i). Not derived.~~ **[v0.1.6, O6]** Treated in §7.6: there is a general criterion, two mechanisms and a test table. Still open (O7): a complete classification for all atoms, and ~~whether m = 2 is always injective~~ **[v0.1.7, G1]** which m = 2 exponent pairs (a, b) are injective. Not all are: p^a q^a with a odd ≥ 3 never is (§7.6.4). **[v0.1.5, E10]** For non-squarefree atoms the three reversal modes give different drawings, so O6 is posed for mode `positive`.
- **O4. Instrument fit.** The viewer-redesign requirements v0.1 (bus #242) are under review. Fitting this note into an exact core, a panel and a dial ledger waits on those requirements and on saphir's word "build" (gate G7).

- ~~**O5. Pin Leary 2013** … before the metric claim in §5.1 is cited.~~ **[v0.1.4, O5]** Pinned in §5.1. It adds a caveat: X(ℕ) is CAT(0) but not metrically complete.

## 7. Drawing register: the 30030 known-answer test **[v0.1.4, O1]**

**Source.** This section uses the frozen viewer `helix_atlas_doily_witness_v27_patched_3_wl2.html` (sha256 3d65e14af4b0887b543e48d986ccc6367b0129afc150e0f9a254bd407b3ab106; all eight copies found on disk are identical). ~~lines 1412–1423~~ **[v0.1.5, E7]** The relevant lines are 1417–1428 (formula comment) and 1445–1465 (`divisorPosition`, the code), with reversal modes at 1430–1444, in reversal mode `positive`. Primes are ordered ascending because `factorize` (lines 1261–1271) appends them in trial-division order. The viewer was read only, and nothing in it is changed.
- Its shift-and-rotate position is pos(d) = Σ_i r_i(cos(2πe_i/n_i + φ_i) − cos φ_i, sin(2πe_i/n_i + φ_i) − sin φ_i), with n_i = a_i + 1, r_i = 1/n_i, φ_i = 2πi/m, primes ordered ascending, plus height z = Σ e_i. **[v0.1.5, E7]** Here the index runs over i = 0,…,m−1. In the complex form below, the index is written j, to keep it apart from the imaginary unit i.
- In complex form: pos(d) = Σ_j r_j e^{iφ_j}(ζ_{n_j}^{e_j} − 1).
- **[v0.1.5, E10]** For squarefree atoms the restriction to `positive` can be widened. Mode `winding` gives the same drawing, because ζ_2^{−1} = ζ_2. Mode `global` gives the complex conjugate. So §7.1–§7.4 hold in all three modes. **[v0.1.6, #263 F2]** For mode `global`, the formulas hold up to conjugation of the planar coordinates: there π(d) = (−Σ_{i∈S} ζ_m^{−i}, |S|), with ζ^{−i} in place of ζ^{i}. The counts, the coincidence classes and the Walsh degree support are unchanged.

**[v0.1.6, #263 F3]** Convention for N = 1: then m = 0 ~~and the viewer draws the single divisor 1 at the origin, at height 0 (`divisorPosition` returns (0,0,0) for an empty factorisation).~~ **[v0.1.7, G10]** and `divisorPosition` returns (0, 0, 0) for an empty factorisation; whether the UI accepts N = 1 was not checked. The seat-root formula and the coincidence criterion below are for m ≥ 1.

**7.1 Squarefree reduction.** For squarefree N with m ≥ 1 primes, a_i = 1, so n_i = 2 and r_i = 1/2. The divisor d with seat set S = {i : p_i | d} is drawn at
  π(d) = ( −Σ_{i∈S} ζ_m^i , |S| ),
which is exact in ℤ[ζ_m] × ℤ. This is a linear map on the cube coordinates x ∈ {0,1}^m of X(N).
- [V0, numerical] The float transcription of the viewer formula agrees with this exact map to 8.9·10⁻¹⁶, tolerance 10⁻¹², over m = 1…10.

**7.2 Coincidence criterion.** Two divisors are drawn at the same point if and only if their seat sets have equal size and the difference of their indicators lies in K_m = ker(ℤ^m → ℤ[ζ_m]). [D2: all pairs, m = 1…10, exact in ℤ[x]/(Φ_m)]
- K_m has rank m − φ(m). **[v0.1.5, E12]** This is because ℤ^m → ℤ[ζ_m] is onto and ℤ[ζ_m] is free of rank φ(m). [E12: m = 1…12, now asserted]
- **Coincidences occur if and only if m is composite.** [D1, m = 1…10]
  - ~~For m = 1 or m prime, K_m = ℤ·(1,…,1).~~ **[v0.1.5, E2]** For m = 1, K_1 = 0. For m prime, K_m = ℤ·(1,…,1), the multiples of Φ_m. The only kernel difference is between ∅ and the full set, and their heights differ. [E2]
  - For composite m, take a subgroup of ℤ/m of order t with 1 < t < m. Two of its cosets are distinct seat sets of the same size, each summing to 0, so they are drawn at the same point.
  - This agrees with the earlier proved record "collisions iff ω(N) composite".
- Counts of 2^m divisors → distinct points: m=4: 16→15, m=6: 64→53, m=8: 256→189, m=9: 512→490, m=10: 1024→647.

**7.3 N = 30030** (m = 6, seats 2, 3, 5, 7, 11, 13). [S1–S6, exact]
- There are 53 distinct points, so 11 points are lost to coincidence.
  - Per level Ω, divisors → points: 1→1, 6→6, 15→13, 20→13, 15→13, 6→6, 1→1.
- **Spine (xy = 0):** 10 divisors at 5 heights.
  - Ω=0: 1.
  - Ω=2: the antipodal duads 14, 33, 65.
  - Ω=3: the two 120° triangles 110 = 2·5·11 and 273 = 3·7·13.
  - Ω=4: the duad complements 462, 910, 2145.
  - Ω=6: 30030.

  These are exactly the zero-sum subsets of μ₆: ~~unions of cosets of the subgroups {0,3} and {0,2,4}~~ **[v0.1.5, E4]** the disjoint unions of cosets of {0,3} and {0,2,4}. A non-disjoint union such as {0,3} ∪ {0,2,4} is not zero-sum. [E4]
- **Off-spine coincidences:** six pairs at Ω=3 (42/195, 66/130, 70/165, 154/715, 182/429, 231/455).
- **Every coincidence is a block swap** [S6]: one zero-sum block (an antipodal duad or a triangle) is exchanged for another of the same size, and the rest of the seat set is kept. Multiplicity is at most 3.
- **Correction to the record:** the earlier statement that "11 divisors collapse onto the spine" conflated the 10 spine divisors with the 11 lost points.

**7.4 Cube reading.** In terms of §1–§3:
- The drawing sends the hyperplane H(p_i,1) of the Boolean cube to the edge direction −ζ_m^i, together with a unit step in height.
- **[v0.1.5, E3]** For m ≥ 2, the cube antipode d ↦ N/d (§3.3) becomes the point reflection through (0, m/2): xy ↦ −xy and z ↦ m − z. [D3]
- The spine is invariant under it.
- **Walsh link (O2):** **[v0.1.5, E3]** for m ≥ 2, 2·π_xy(d) = Σ_i ζ_m^i W_i(d), where W_i(d) = (−1)^{[p_i | d]} is the degree-1 Walsh character of the Boolean cube. [D4, exact, m = 2…10; both this and the antipode fail at m = 1, E3] ~~So the existing drawing … this data cannot separate.~~ **[v0.1.5, E5]** So, for m ≥ 2, the drawing of a squarefree atom sees only the Walsh spectrum of degree ≤ 1. Of that it sees only the seat-circle frequencies 0 (height, z = (m − Σ_i W_i)/2) and 1 (plane, 2π_xy = Σ_i ζ_m^i W_i). Coincidences are exactly the pairs these two coefficients cannot separate.
- Saphir's 2026-10-08 reading, recorded earlier, agrees: the k = 2 coefficient on the seats separates ~~the centre duads~~ **[v0.1.5, E12]** the three spine duads 14, 33, 65 (seat sums 2, 2ω, 2ω²). k = 2 does not separate the two triangles, whose k = 2 sums are both 0; k = 3 does, with sums 3 and −3 (checked by hand).

**7.5 Scope.** This section is about the drawing register only, and nothing here is a claim about the arithmetic.
- The drawing map is linear on the cube but not injective for composite m. **[v0.1.6, O6]** For non-squarefree atoms it is still linear in the hyperplane coordinates (§7.6), and it can fail to be injective even for prime m.
- Any instrument that draws X(N) this way must label coincident vertices rather than hide them (saphir: "draw degenerate cases, label them").
- ~~Non-squarefree atoms use r_i ≠ 1/2 and n_i ≥ 3.~~ **[v0.1.5, E6]** In a non-squarefree atom at least one prime has a_i ≥ 2, hence n_i ≥ 3 and r_i = 1/n_i ≤ 1/3. Primes with a_i = 1 keep n_i = 2 and r_i = 1/2. The map is then no longer linear in the exponents. ~~Their coincidence structure is not derived here (open item O6).~~ **[v0.1.6, O6]** It is linear in the Sageev hyperplane coordinates, and its coincidence structure is treated in §7.6.

**7.6 All atoms (O6), mode `positive`.** **[v0.1.6, O6]** Checks: ~~`check_v0_1_6_o6.py`~~ **[v0.1.7]** `check_v0_1_7_o6.py`. All are exact in ℚ(ζ_L), with L = lcm(m, n_1, …, n_m), except V1.

**7.6.1 The drawing is linear in the Sageev coordinates.** Write h_{j,k}(d) = [p_j^k | d] for 1 ≤ k ≤ a_j (§2.1).
- Telescoping gives ζ_n^e − 1 = Σ_{k=1}^{e} ζ_n^{k−1}(ζ_n − 1).
- So pos(d) = Σ_{j,k} h_{j,k}(d) · w_{j,k}, with w_{j,k} = (1/n_j) ζ_m^j ζ_{n_j}^{k−1}(ζ_{n_j} − 1), and z(d) = Σ_{j,k} h_{j,k}(d). [L1]
- Every edge dual to the hyperplane H(p_j,k) is drawn as the same vector w_{j,k} with a unit height step. [L2]
- So the viewer's drawing is a linear projection of the box X(N), taken in its hyperplane coordinates, to ℂ × ℤ. For squarefree N, w_{j,1} = −ζ_m^j recovers §7.1.
- This refines the v0.1.5 remark "no longer linear in the exponents": it is not linear in the exponents, but it is linear in the hyperplane coordinates.

**7.6.2 Coincidence criterion (all atoms).** Two divisors are drawn at the same point if and only if they have equal height and the difference of their hyperplane-coordinate vectors lies in the kernel of w: ℤ^{Ω(N)} → ℚ(ζ_L). [L3: all pairs, every test atom with τ ≤ 400]
- A nonzero kernel does not by itself produce a coincidence. The difference must come from two valid divisors, whose coordinates are down-sets in each prime's chain. ~~Example: 8 = 2³ has w_1 + w_3 = 0, a rank-1 kernel, yet its 4 divisors are drawn injectively.~~ **[v0.1.7, G5]** Example: 36 = 2²·3² has the height-zero kernel vector (1, −1, 1, −1) in (H(2,1), H(2,2), H(3,1), H(3,2)). Its signs alternate inside each chain, so no two divisors differ by it, and the 9 divisors are drawn injectively. (In 8 = 2³, w_{0,1} + w_{0,3} = 0, but this vector changes the height.) [G5]

**7.6.3 One prime is always injective.** For m = 1, pos(p^e) = (1/n)(ζ_n^e − 1), and these are distinct for 0 ≤ e ≤ a < n. [T1: 4, 8, 16] **[v0.1.7, G9]** (Already the heights e are distinct.)

**7.6.4 Prime m no longer guarantees injectivity.** This contrasts with §7.2.
- In 180 = 2²·3²·5 (m = 3), the divisors 4 and 6 are drawn at the same point. [T3, T4]
- The mechanism is *resonance*: H(2,2) and H(3,1) are drawn with the identical edge vector, ~~w_{2,2} = w_{3,1}~~ **[v0.1.7, G6]** w_{0,2} = w_{1,1} (that is, H(2,2) and H(3,1)) = (1/3)ζ_3(ζ_3 − 1). So the paths 1→2→4 and 1→2→6 end together.
- In general, w_{j,k} = w_{j',k'} for distinct primes exactly when n_j = n_{j'} = n (equal exponents) and j/m + (k−1)/n ≡ j'/m + (k'−1)/n (mod 1). ~~That is, the anchor gap (j' − j)/m must be a multiple of 1/n modulo 1. (The ratios r(ζ_n − 1) agree only if …)~~ **[v0.1.7, G8]** Necessarily the anchor gap (j' − j)/m is a multiple of 1/n mod 1. For n ≥ 3 this is also sufficient for some k, k′ ∈ {1, …, n − 1}. For n = 2 resonance never occurs. **[v0.1.7, G7]** (Equal vectors have equal length, and |w_{j,k}| = (2/n_j) sin(π/n_j) is strictly decreasing in n_j ≥ 2, since 2t·sin(πt) increases on (0, 1/2]; so n_j = n_{j′}.) [G7: the characterisation is asserted on every hyperplane pair of every test atom; G8: n = 2 never resonates]
- Resonant pairs found in the tests: 180: H(2,2)=H(3,1). 900: H(2,1)=H(5,2), H(2,2)=H(3,1), H(3,2)=H(5,1). 900900: H(2,2)=H(5,1). **[v0.1.7]** 216: H(2,1)=H(3,3), H(2,3)=H(3,1). 7776: H(2,1)=H(3,4), H(2,2)=H(3,5), H(2,4)=H(3,1), H(2,5)=H(3,2).
- **[v0.1.7, G1] Two primes are not always injective either.** For m = 2 the anchors are 1 and −1. If a = b = n − 1 with n even and n ≥ 4, then w_{0,1+n/2} = −(1/n)(ζ_n − 1) = w_{1,1}, so p^{1+n/2} and p^{n/2}·q coincide.
  - So p^a q^a is non-injective for every odd a ≥ 3 (proved). In 2³·3³ the divisors 8 and 12 (H(2,3) = H(3,1)) and 18 and 27 (H(2,1) = H(3,3)) coincide. [G1]
  - For m = 2 the positions depend only on (a, b), not on the primes. [G1, checked for a = 3, 5 with the primes 5, 7]
  - For a, b ≤ 10 the drawing is non-injective exactly when a = b is odd and ≥ 3, with losses 2, 6, 12, 20 at a = 3, 5, 7, 9. [G1 sweep, 100 exponent pairs] With a ≠ b, or a = b even, no coincidence was found for a, b ≤ 10 here, and for a, b ≤ 14 by the independent checker. That part is an observation, not a theorem.

**7.6.5 ~~Two~~ **[v0.1.7, G2]** Three mechanisms observed.**
- (i) Resonance, as above, which occurs only when some a_j ≥ 2.
- (ii) Zero-sum blocks, as in §7.3, among primes with a_j = 1. Examples: 60060 = 2²·30030 and 120120 = 2³·30030 keep the duads 33 and 65 coincident.
- A non-squarefree prime breaks the antipodal pairing of its own seat, ~~because its edge vectors have length r_j|ζ_{n_j} − 1| ≠ 1~~ **[v0.1.7, G4]** because each chain difference of the non-squarefree seat, (1/n_j)ζ_m^j(ζ_{n_j}^v − ζ_{n_j}^{v′}), is not an algebraic integer, while every squarefree combination lies in ℤ[ζ_L]. So with only one non-squarefree seat, that seat cannot take part in a coincidence. (With two or more, it can: 900900.) So 60060 loses only 6 points, against 11 for 30030. [G4: in 60060 and 120120 the non-squarefree seat is fixed inside every coincidence class, and the duads 33 and 65 coincide]
- **[v0.1.7, G2]** (iii) Mixed relations, observed in 900900: differences of non-squarefree edge vectors can be algebraic integers equal to differences of squarefree edges. For example, w_{H(5,1)} − w_{H(2,1)} = −ζ₃ = w_{H(7,1)} − w_{H(11,1)}, so 55 and 14 coincide. [G2]
  - 40 of 900900's 64 losses are not reached by single resonance swaps or squarefree block swaps: chains of single resonance swaps reach 24, and squarefree blocks reach none. [G2]
  - The independent checker also found 60 coincident pairs whose difference lies outside the ℚ-span of the resonance vectors plus the squarefree height-zero kernel. That is the checker's count and is not asserted here.
- **[v0.1.7, G3]** Even within resonance, single swaps are not enough. In 2⁵·3⁵ the classes {108, 243} and {32, 72} differ by two-edge segments, such as H(3,4) + H(3,5) − H(2,1) − H(2,2), and single swaps reach only 4 of its 6 losses. [G3]
- ~~Whether every coincidence is generated by (i) and (ii) is **not claimed**.~~ **[v0.1.7, G2]** That every coincidence is generated by (i) and (ii) is false (900900). A classification is open (O7).

**7.6.6 Test table** (exact; divisors → distinct points; "lost" = divisors − points):

| N | m | Ω | rank ker w | divisors | points | lost | max mult. |
|---|---|---|---|---|---|---|---|
| **[v0.1.7, G1]** 216 = 2³·3³ | 2 | 6 | 4 | 16 | 14 | 2 | 2 |
| **[v0.1.7, G3]** 7776 = 2⁵·3⁵ | 2 | 10 | 8 | 36 | 30 | 6 | 2 |
| 4, 8, 16 | 1 | 2–4 | 0, 1, 0 | 3, 4, 5 | same | 0 | 1 |
| 12, 18, 24, 36, 48, 72, 108, 200 | 2 | 3–5 | 1–2 | 6–12 | same | 0 | 1 |
| 60 = 2²·3·5 | 3 | 4 | 2 | 12 | 12 | 0 | 1 |
| 180 = 2²·3²·5 | 3 | 5 | 3 | 18 | 16 | 2 | 2 |
| 360 = 2³·3²·5 | 3 | 6 | 3 | 24 | 24 | 0 | 1 |
| 900 = 2²·3²·5² | 3 | 6 | 4 | 27 | 18 | 9 | 4 |
| 420, 1260, 6300 | 4 | 5–7 | 2–3 | 24, 36, 54 | same | 0 | 1 |
| 4620, 13860 | 5 | 6, 7 | 1 | 48, 72 | same | 0 | 1 |
| 30030 (squarefree, §7.3) | 6 | 6 | 4 | 64 | 53 | 11 | 3 |
| 60060 = 2²·3·5·7·11·13 | 6 | 7 | 5 | 96 | 90 | 6 | 2 |
| 120120 = 2³·3·5·7·11·13 | 6 | 8 | 5 | 128 | 120 | 8 | 2 |
| 900900 = 2²·3²·5²·7·11·13 | 6 | 9 | 7 | 216 | 152 | 64 | 4 |

- [V1, numerical] The exact map agrees with a float transcription of the viewer code to 1.3·10⁻¹⁵ (tolerance 10⁻¹²) over every divisor of every test atom.
- [T2] The 30030 row reproduces §7.3.
- **[v0.1.7, G12]** The script now also prints rank ker(w, z), which counts the kernel vectors that keep the height. Its column agrees with the independent checker's values on all 24 original atoms [G12]: 4, 8, 16: 0, 0, 0; 12, 18, 24, 36, 48, 72, 108, 200: 0, 0, 1, 1, 0, 1, 1, 1; 60: 1; 180: 2; 360: 2; 900: 3; 420, 1260, 6300: 1, 1, 2; 4620, 13860: 0, 0; 30030: 3; 60060: 4; 120120: 4; 900900: 6. For 216 it is 3, and for 7776 it is 7.
- These atoms test the criterion. They do not bound it. ~~and the m = 2 injectivity seen here is an observation, not a theorem (O7).~~ **[v0.1.7, G1]** The m = 2 rows above are injective only because none of them has a = b odd ≥ 3; see §7.6.4.

**7.6.7 For the instrument.** Since the drawing is linear in the hyperplane coordinates, a coincidence can be labelled exactly: ~~compute the hyperplane-coordinate difference and name it as a resonance pair or a zero-sum block.~~ **[v0.1.7, G3]** compute the hyperplane-coordinate difference δ and report it exactly. Name it a resonance swap or a squarefree zero-sum block swap when it is one; otherwise label it "other kernel relation" and show δ. This is the "draw degenerate cases, label them" rule applied to the drawing register, and it needs nothing outside §2. The other reversal modes are not treated for non-squarefree atoms; they give different drawings (E10).

## Corrigendum v0.1 → v0.1.1

| Finding | Severity | Disposition |
|---|---|---|
| F1 §5.1 "formulas of §2–§3 verbatim" false | MAJOR | Struck; reviewer's replacement adopted verbatim; reasons and O5 added |
| F2 §3.2 "convex" undefined, untested | MEDIUM | Reviewer's wording adopted verbatim; X(6) caveat added; new exhaustive check C7b |
| F3 registers line overstates coverage | MEDIUM | Reviewer's sentence adopted verbatim |
| F4 §3.3 "swaps H⁺ with H⁻" | LOW | Corrected, reviewer's wording |
| F5 §5.1 "finite atoms are its finite convex sub-boxes" | LOW | Reviewer's wording adopted |
| F6 §5.4 "only when" | LOW | "if and only if"; divisible pairs added; gate ~~lifted~~ raised to τ(lcm) ≤ 256 **[v0.1.2, D5]** |
| F7 §3.4 inversion hypothesis; C9 tautological | LOW | Hypothesis stated; C9 now tests the cube list, plus inversion |
| F8 §5.2 frequency map implicit | LOW | j ↦ j·N/M stated |
| F9 §2.3 count vs bijection | LOW | Justification added, and direct check C4b |
| F10 R5 self-comparison; "interval" used before defined | LOW | R5 enumerates cubes; forward reference added |
| F11 C12 needlessly numerical | INFO | Exact check C12 added in ℤ[x]/(Φ_d); C12n kept |
| Script-audit notes (C7/C9/C4/R3/R2–R3 gate/R5/R4) | — | Addressed as above; R4 range disclosed in §5.6 **[v0.1.2, D3]** |

Not changed: R4's n < 5000 range (disclosed in §5.6), and C8/R6 checking edges only (judged acceptable by the reviewer).

## Corrigendum v0.1.1 → v0.1.2

| Finding | Severity | Disposition |
|---|---|---|
| D1 §5.1 metric CAT(0) sentences disagree | LOW | "(not yet cited; see O5)" appended; bullet struck and replaced with reviewer's wording |
| D2 §1.1 "(§4)" wrong and overclaims | LOW | Reviewer's wording: "(§5.1), with the exceptions listed there" |
| D3 unmarked v0.1.1 changes | LOW | Marked; corrigendum row added; status line updated |
| D4 C7b scope label | LOW | Reviewer's wording, in §3.2 and in the registers line |
| D5 "gate lifted" | INFO | Reviewer's wording: "raised to τ(lcm) ≤ 256" |

## Corrigendum v0.1.2 → v0.1.3 (Astra review #255)

| Item | Kind | Disposition |
|---|---|---|
| C1 §4.2 α rational unqualified | blocking | Scalar field declared; exact-rational claim restricted to rational-valued f; √2 counterexample cited; serialization rule recorded; check A1 |
| C2 §5.6 coefficient invariance for unrelated data | blocking | Struck; pullback hypothesis stated verbatim; gcd(n,M) counterexample cited and reproduced (A2b); pullback statement checked (A2) |
| P1 §3.2 "geodesically convex" | nonblocking | "combinatorially geodesically convex (closed under all graph intervals)" |
| P2 §5.4 "convex hull" | nonblocking | "smallest convex cubical subcomplex"; X(6) triangle-vs-square example (A3) |
| Register note (#247 F1) | note | Consistent already: the only trigonometry is C12n, a labelled numerical cross-check, never a source for exact values |

## Corrigendum v0.1.3 → v0.1.4 (additions at saphir's word)

| Item | Disposition |
|---|---|
| O5 | Pinned to Leary arXiv:1009.1540v3, Thm B.8; hypotheses checked; new caveat: X(ℕ) is not metrically complete (Thm A.6) |
| O2 | saphir's decision recorded: Ramanujan primary, Walsh required for squarefree N |
| O1 | New §7: exact drawing map, coincidence criterion, the 30030 count, and the Walsh link; checks V0, D1–D4, S1–S6; the record's "11 on the spine" corrected to 10 |
| O6 | New open item: coincidences for non-squarefree atoms |

## Corrigendum v0.1.4 → v0.1.5

| Item | Severity | Disposition |
|---|---|---|
| E1 O1 "7 off the spine" false | MEDIUM | Corrected verbatim: 5 on, 6 off, 7 at Ω=3; now asserted |
| E2 K_1 | LOW | K_1 = 0 stated; asserted |
| E3 m ≥ 2 for antipode and Walsh | LOW | Hypothesis added; failure at m = 1 asserted |
| E4 "disjoint" unions of cosets | LOW | Added; characterisation and counterexample asserted |
| E5 Walsh over-claim | LOW/MEDIUM | Reviewer wording: degree ≤ 1, frequencies 0 and 1; O2 bullet updated |
| E6 per-prime n_i, r_i | LOW | Reviewer wording |
| E7 line citation, prime order, index i | LOW | Lines corrected; prime order cited to `factorize` 1261–1271 (read); index j in the complex form |
| E8 simple connectivity | LOW | Reviewer wording (CW first, then A.7) |
| E9 "finite set" in flag argument | LOW | Reviewer wording |
| E10 reversal modes | INFO | Widened for squarefree; O6 posed for `positive` |
| E11 B.8 hypotheses, B.11, B–H, journal | INFO | Added; B–H and journal marked unverified |
| E12 dates, "centre duads", k = 3, rank reason | INFO | Dates corrected in text; spine duads named; k = 3 noted; rank reason added and asserted |
| Astra #260 F1 registers line | nonblocking | Names check_v0_1_5.py and its predecessor |
| Astra #260 fresh-run evidence | note | Both scripts print per-check pass counts |
| saphir O2 wording | decision | "Walsh is a required overlay for squarefree N" recorded verbatim |

## Corrigendum v0.1.5 → v0.1.6

| Item | Kind | Disposition |
|---|---|---|
| #263 F1 registers lines | nonblocking | Drawing and numerical registers updated (V0, V1, §7) |
| #263 F2 global mode | nonblocking | "Up to conjugation of planar coordinates", with ζ^{−i} |
| #263 F3 N = 1 | nonblocking | m = 0 origin convention; the formulas are stated for m ≥ 1 |
| #263 note: block swap for 30030 only | note | Already scoped that way in §7.3; §7.6 adds that the 30030 mechanism is not the general one |
| O6 | saphir "go ahead" | New §7.6: linearity in hyperplane coordinates, kernel criterion, resonance and zero-sum mechanisms, m = 1 injectivity, test table; O7 opened |

## Corrigendum v0.1.6 → v0.1.7 (independent check of v0.1.6: FAIL)

| Finding | Severity | Disposition |
|---|---|---|
| G1 m = 2 injectivity "observation" false | HIGH | Struck; proved family p^a q^a (a odd ≥ 3) added with 216 example; sweep asserted (a, b ≤ 10); O7 reworded |
| G2 two mechanisms do not generate all | MEDIUM–HIGH | (iii) mixed relations added; "not claimed" → "false (900900)"; −ζ₃ identity, 55 ~ 14, and 24/64 asserted |
| G3 labelling rule over-claims | MEDIUM | "other kernel relation, show δ" added; 2⁵·3⁵ example asserted |
| G4 length argument wrong | MEDIUM | Algebraic-integer argument; fixed-seat property asserted for 60060 and 120120 |
| G5 8 = 2³ example | LOW | 36 example with its kernel vector; 8 kept as the height example; both asserted |
| G6 notation | LOW | Seat-indexed w_{0,2} = w_{1,1} |
| G7 lengths, not values | LOW | Monotonicity argument; characterisation asserted on all pairs |
| G8 anchor gap only necessary | LOW | n ≥ 3 sufficiency, n = 2 never; asserted |
| G9 heights already distinct | INFO | Added |
| G10 N = 1 UI claim | INFO | Limited to divisorPosition |
| G11 "viewer's own float code" | INFO | "float transcriptions" |
| G12 printed but not asserted; stale code | INFO | All printed claims now asserted; dead code and stale comments removed; rank ker(w, z) column |

## Files

- `NOTE.md` (this file)
- `check_v0_1_5.py` and `CHECK_OUTPUT.txt` (§1–§5; standard library; per-check counts; 0 failures)
- `check_v0_1_5_drawing.py` and `CHECK_DRAWING_OUTPUT.txt` (§7.1–§7.4; per-check counts; 0 failures)
- `check_v0_1_7_o6.py` and `CHECK_O6_OUTPUT.txt` (§7.6; per-check counts; 0 failures)
- `CHECK_OUTPUT.txt` (output of the run: 0 failures)
- `MANIFEST.sha256`
