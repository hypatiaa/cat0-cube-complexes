# Independent check of NOTE v0.1 (divisor atom as a CAT(0) cube complex)

**Provenance.** This file was written by the owner session from the verifier's returned text, because the subagent harness refused the subagent's own write. The verifier was an independent Opus subagent working on a closed file list. Its text is reproduced below without changes to its findings. Its own files in this folder are `verify_opus.py` (90ef95df…), `VERIFY_OUTPUT.txt` (8c7a2be5…) and `MANIFEST.sha256` (ad2a92b5…), which covers those two files.

**Input:** NOTE v0.1 folder, MANIFEST.sha256 3fb52de4e0001850963df3858bab657948f0f617fde31056fb8bf6b189a3947d. All digests matched.

## VERDICT: PASS_WITH_FLAGS

- Every finite-atom claim in §1–§4 is true, and so are the relations in §5.2–§5.6.
- One sentence in §5.1 is false as stated (F1).
- The §3.2 convexity claim is true once "convex" is defined, but it is untested (F2).
- F1 must be corrected before the note is cited as a general statement about the whole family.

## Script-checked results (verifier's own script)

**Method.**
- Standard library only, with exact int and Fraction arithmetic and no floats.
- μ is computed as the Dirichlet inverse of 1.
- c_d(n) is computed exactly from its exponential-sum definition, by reducing Σx^{jn} modulo Φ_d. The result is compared with von Sterneck's formula and with the μ-formula.

**Run.** `python -I -X utf8 verify_opus.py` exits 0, with FAILURES: 0, in about 18 s.

**Negative control.** A mutated copy fails on exactly the checks it should. It had three changes: f₂(360) = 28, φ(e) in place of φ(N/e) in the coefficient, and one perturbed value of c₁₂.

**Results.**
- **f-vector table:** correct in all 6 rows. Enumerated cubes, the generating function ∏((a+1)+a·x), the note's formula and the table all agree. χ = 1 in every row, and every facet of every cube is a cube.
- **§2.1–2.4,** for N ∈ {1, 2, 4, 6, 8, 12, 18, 30, 36, 60, 72, 210, 360, 900, 6300, 30030}:
  - Each edge is dual to the predicted hyperplane.
  - Hyperplanes cross exactly when their primes differ, and same-prime half-spaces are strictly nested.
  - The Sageev correspondence is a real bijection with the principal orientations, and the rebuilt cubes reproduce the f-vector.
  - BFS distance equals the number of separating hyperplanes, which equals Ω(lcm/gcd).
- **§3.1:** for all triples, both median formulas agree with the coordinatewise median, and the intersection of the three BFS geodesic intervals is exactly that median.
- **§3.2 intervals:** the BFS interval equals {g | d | l} in every case.
- **§3.2 convexity:** every vertex subset was tested for N with τ ≤ 16 (N ∈ {1, …, 210}). The nonempty geodesically convex sets are exactly the sub-boxes, ∏C(a_p+2, 2) of them, and the empty set is also convex.
- **§3.3:** the antipode maps cubes to cubes. It sends H⁺(p,k) onto H⁻(p, a_p−k+1), and it has a fixed vertex exactly when N is a square.
- **§3.4:** the support and sign of μ match the cubes, and Möbius inversion holds.
- **§4.1–4.2:**
  - The class counts are φ(d).
  - The exact definition of c_d equals the closed formulas, and c_d depends only on gcd(n, d).
  - Orthogonality holds, with ‖c_d‖² = Nφ(d).
  - α(d) rebuilds f for 3 random rational test functions, and it equals ⟨f, c_d⟩/⟨c_d, c_d⟩.
  - Coverage: direct sums up to N = 900. For 6300 and 30030 the sums are grouped by gcd class, with class sizes verified by direct count.
- **§5:**
  - Meet, hull, and "union convex iff one atom divides the other" hold, tested in both directions on 10 pairs.
  - §5.2 holds as stated. Pullback j ↦ jN/M is injective, keeps order and character values, and its image is the frequencies of order dividing M.
  - §5.3: translates match on all cubes.
  - §5.5: the enumerated f-vector of X(MN) is the convolution of the enumerated factors.
  - §5.6: coefficients are unchanged when the atom grows.

## Read and reasoned, not script-proved

- **§1–§4: TRUE,** including the §4.2 coefficient formula. The sum over n splits into gcd classes e of size φ(N/e), and c_d(n) = c_d(e) on each class.
- **§3.2 convexity: TRUE for nonempty sets in the metric sense.** The affine hull is axis-parallel, so the boundary lies in axis-parallel hyperplanes, so the set is a box with lattice corners. It is also TRUE for full subcomplexes on geodesically convex vertex sets. It is FALSE for a 1-skeleton-only reading: in X(6), the 4-cycle without its square.
- **§5.1, what holds for X(ℕ):**
  - Its 1-skeleton is a median graph.
  - Every finite configuration lies inside some convex X(n), so distance, median and intervals hold verbatim.
  - It is simply connected with flag links.
  - It is locally infinite, with cubes of every finite dimension but no infinite cube.
  - It is probably metrically CAT(0), by Leary 2013 (Gromov's link condition in any dimension). This is cited from memory and not pinned.
- **§5.2: TRUE,** by Pontryagin duality: the quotient ℤ/N → ℤ/M corresponds to the inclusion of character groups.

## Audit of check_v0_1.py

- **C7** never tests "the convex subcomplexes are exactly the sub-boxes".
- **C9** is near-tautological: it compares μ against its own definition.
- **C4** counts but never exhibits the bijection.
- **R3** only tests the non-convex direction.
- **R2 and R3** skip (360, 30030) because of the τ(lcm) ≤ 128 gate.
- **R5** compares the formula with itself.
- **R4** tests only n < 5000, and the claim in its comment is untested.
- **C8 and R6** check edges only (acceptable).
- **C11** is limited to N ≤ 360 (disclosed).

## Findings

- **F1, MAJOR, §5.1.** "with the formulas of §2–§3 holding verbatim" is false:
  - §2.3 needs the descending chain condition. {H⁺(p,1) ∀p} and {H⁺(2,k) ∀k} are consistent but correspond to no integer.
  - §3.2: infinite convex subcomplexes exist (multiples of g, H⁻(2,1), the ray {2^k}, X(ℕ) itself).
  - §3.3 has no global antipode, and the §1.2 counts are infinite.

  Suggested replacement: "Distance (§2.4), median (§3.1) and intervals (§3.2) hold verbatim. Sageev duality holds for orientations that choose only finitely many H⁺. The finite convex subcomplexes are exactly the I(g,l), each isomorphic to X(l/g). Infinite convex subcomplexes also exist. §3.3 has no global analogue. Metric CAT(0) follows from the link condition in arbitrary dimension [Leary 2013, to pin]."
- **F2, MEDIUM, §3.2.** Suggested text: "The nonempty convex subcomplexes, in the CAT(0) metric sense or equivalently the full subcomplexes on geodesically convex vertex sets, are exactly the sub-boxes {d : g | d | l} with g | l | N, ∏C(a_p+2, 2) of them." Add the X(6) 4-cycle as a caveat.
- **F3, MEDIUM, registers line.** Suggested text: "Script checks cover the stated test cases where cited; §5.1, §5.2 and the §3.2 convexity classification rest on proof only."
- **F4, LOW, §3.3.** "swaps H⁺ with H⁻" → "maps H(p,k) to H(p, a_p−k+1), sending H⁺(p,k) onto H⁻(p, a_p−k+1)".
- **F5, LOW, §5.1.** "The finite atoms are its finite convex sub-boxes" → "The atoms are the boxes I(1,N); each finite convex sub-box I(g,l) is a translate of X(l/g)."
- **F6, LOW, §5.4.** "only when" → "if and only if". Add a divisible pair to R3, and lift the R2/R3 gate.
- **F7, LOW, §3.4.** State the hypothesis g(n) = Σ_{d|n} f(d). Make C9 test against the cube list.
- **F8, LOW, §5.2.** State the frequency map j ↦ j·N/M explicitly.
- **F9, LOW, §2.3 / C4.** Justify count-implies-bijection, or check the bijection directly.
- **F10, LOW, §5.5 / R5.** Compare against enumerated cubes. Also, §3.1 uses "interval" before §3.2 defines it.
- **F11, INFO, C12.** Make C12 exact by reducing modulo Φ_d.
