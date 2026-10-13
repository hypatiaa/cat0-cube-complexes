# cat0-cube-complexes

The divisor-atom family described as a CAT(0) cube complex, with its exact Fourier layer and the exact relations between atoms. This is the working record of the Stack Bus track `cat0-cube-complexes`, together with the atom viewer we are extending.

**Scope (saphir, verbatim):** "a general cubical/Fourier description of the whole divisor-atom family, plus its exact inter-atom relations. The small examples test that general construction; they don't define its limits."

**Standing.** This is research notes at spec scope; nothing here is a released instrument.
- The current note is **v0.1.8**. It was reviewed by Astra (discipline seat) as PASS_WITH_FLAGS at bounded note/spec scope (Stack Bus #310).
- Four nonblocking flags from that review are pending for the next version.
- Builds are gated on saphir's word "build".

## What the note establishes

For N = ∏ p^{a_p}:

- **§1–§3, one atom.**
  - The divisors of N form a box of unit cubes, ∏[0, a_p]. It has dimension ω(N), Euler characteristic 1, and one Sageev hyperplane H(p,k) per prime power p^k | N.
  - Distance is Ω(lcm/gcd), and the median is gcd(lcm, lcm, lcm).
  - The convex subcomplexes are the sub-boxes, and Möbius is a cubical sign.
- **§4, the Fourier layer.** Each vertex d is a DFT frequency class of ℤ/N. The Ramanujan sums c_d form an exact orthogonal basis for functions of gcd(n, N); the coefficients are rational when the input is rational-valued.
- **§5, the whole family.** Each atom is a finite convex sub-box of one infinite cubical complex X(ℕ).
  - Divisibility is convex inclusion.
  - gcd gives the intersection, and lcm gives the smallest convex cubical subcomplex containing both atoms.
  - Coprime atoms multiply.
  - The Ramanujan coordinates are coherent across atoms under pullback.
  - X(ℕ) is CAT(0) by Leary's Theorem B.8, but it is not metrically complete (Leary's Theorem A.6).
- **§6, decisions.** O2 (saphir): Ramanujan is the primary layer, and **Walsh is a required overlay for squarefree N**, how the squarefree cube is seen. The overlay lives in the rendering layer, but it is never optional.
- **§7, drawing register** (the viewer below, mode `positive`).
  - The viewer's drawing is *linear in the Sageev hyperplane coordinates*.
  - Two divisors coincide exactly when they have equal height and their hyperplane difference lies in a kernel.
  - For squarefree N, coincidences occur if and only if the number of primes is composite. For 30030: 64 divisors, 53 points, 10 divisors on the spine.
  - For general atoms there is a resonance between equal exponents. For two primes, p^a q^a with odd a ≥ 3 is never injective (proved).
  - Mixed relations also occur (900900), so a full classification is open (O7).
  - Labelling rule: resonance swap, block swap, or "other kernel relation" with the exact difference shown.

## Layout

| Folder | What it is |
|---|---|
| `NOTE_divisor_atom_cube_complex_v0_1_*` | Every note version as written, each with its exact check scripts, their outputs and a `MANIFEST.sha256`. Earlier versions are never edited: corrections are marked in place in the successor, with a corrigendum table. |
| `NOTE_v0_1_OPUS_VERIFY_*`, `NOTE_v0_1_1_OPUS_DELTA_*`, `NOTE_v0_1_4_OPUS_CHECK_*`, `NOTE_v0_1_6_OPUS_CHECK_*`, `NOTE_v0_1_7_OPUS_DELTA_*` | Independent checks by fresh Opus agents on closed file lists, each with its own scripts. v0.1.6 **failed** its check; the report is kept as the record. |
| `EVIDENCE_line93_30030_profiles_20261012` | Cross-check of the Ω = 2 rings for 30030 and 30030², supplied to Idea Catalog PR #22 (stacked on #20). |
| `viewer/` | The atom viewer, frozen at its pinned version. This is the base we are extending; see `viewer/VIEWER.md`. |
| `references/REFERENCES.md` | Third-party sources, cited by URL and hash. The PDFs are not redistributed. |

## Running the checks

The scripts use the Python standard library only, with exact integer, `Fraction` and cyclotomic arithmetic. Floating-point values appear only as labelled numerical cross-checks. Run them from inside each note folder, for example:

```
cd NOTE_divisor_atom_cube_complex_v0_1_8_20261011
python -I check_v0_1_5.py
python -I check_v0_1_5_drawing.py
python -I check_v0_1_7_o6.py
```

Each script prints passed/run counts for every check ID, and `FAILURES: 0`. Verify the files with `sha256sum -c MANIFEST.sha256` in each folder.

## Registers

The registers are kept apart throughout:
- **Exact:** integers, rationals, ℤ[ζ_m] and ℚ(ζ_L).
- **Numerical:** floats, always labelled with a tolerance.
- **Drawing:** the viewer.

A numerical value is never the source of an exact one.

## Open items

- O3: whether the OpenAI CAT(0) papers bear on §5.1.
- O4: the instrument fit. After the requirements are adopted, the plan is a small exact library for the viewer integration: hyperplane coordinates and coincidence labels first.
- O7: a full classification of the drawing's coincidences.

## Credits

The mathematics and direction are saphir's (@saphirbijoux). Notes and checks are by Claude (Opus 5.5) sessions, and reviews by Astra and Sol (discipline seat). Independent checks were run by fresh Claude Opus agents.
