# Delta check of NOTE v0.1.7 against G1–G12

**Provenance.** This file was written by the owner session from the verifier's returned text. The verifier was a fresh independent Opus subagent at high thinking level, on a closed list of 7 files. Its findings are reproduced unchanged.

## VERDICT: PASS_WITH_FLAGS

- Eleven of the twelve findings are RESOLVED, and G12 is PARTIAL (INFO).
- There is no mathematical error in the v0.1.7 text or in the new asserts.
- There are seven new flags: H1 is LOW, and H2–H7 are INFO.

## Integrity

- MANIFEST 2a025a3c…, NOTE e4f14a90…, check ae0c663b… and output c7d61ddb… match.
- The v0.1.6 NOTE 3f5510fc… and script 1ec85d2f… match.
- File 5 (REPORT.md) is 5a4d59cb…, with no expected hash given.
- The v0.1.5 scripts in the folder and the folder MANIFEST 3176eee6… were outside the closed list and were not checked.
- Re-run of file 2: exit 0, 0 failures, output byte-identical (c7d61ddb…).
- **Diff of file 7 against file 2:** dead code and two stale comments removed; the docstring and header label changed (undisclosed, H7); 216 and 7776 added; the `store` and `krz` column added; all G-asserts added. Every v0.1.6 assert is byte-unchanged.

## Per-finding table

| Finding | Status | Reason (summary) |
|---|---|---|
| G1 | RESOLVED | The proof is correct, and so are the assert indices. The 216 classes are right. The sweep holds to a, b ≤ 14. Residuals: H1 and H3. |
| G2 | RESOLVED | The −ζ₃ identity is correct. 55 ~ 14 holds. The 24/40 split is correct. Residual: H2. |
| G3 | RESOLVED | The "other kernel relation" rule is in. δ for 7776 is confirmed, and 4 of its 6 losses come from single swaps. |
| G4 | RESOLVED | The argument is valid and the fixed-seat assert is faithful. Residual: H4. |
| G5 | RESOLVED | The 36 kernel vector is right, and the down-set argument is correct. |
| G6 | RESOLVED | |
| G7 | RESOLVED | The monotonicity argument is correct. The assert is a faithful iff test, with 356 executions. |
| G8 | RESOLVED | Residual: H5. |
| G9–G11 | RESOLVED | |
| G12 | PARTIAL (INFO) | T2 still asserts only 53/11 for 30030. |

## New findings

- **H1, LOW, §7.6.6, last bullet.** The sentence is now false, because 216 and 7776 are non-injective m = 2 rows, and "only because" asserts an unproved converse.
  - *Correction:* "The other m = 2 rows (12, 18, 24, 36, 48, 72, 108, 200) are injective. None of them has a = b odd ≥ 3. That a = b odd ≥ 3 is the only obstruction for m = 2 is an observation (§7.6.4), not a theorem."
- **H2, INFO, §7.6.5 (iii).** "Squarefree blocks reach none" and the combined 40 are not asserted by file 2. Both are true, because 7, 11, 13 at seats 3, 4, 5 carry no height-zero kernel vector.
  - *Correction:* append "(the squarefree part is script-checked by the v0.1.7 delta check, not by file 2)", or add an assert.
- **H3, INFO, §7.6.4.** Independence from the primes holds for every m, and the cited check compares loss counts only.
  - *Correction:* "For every m the positions depend only on the exponents (a_1, …, a_m) in prime order, not on the primes (the formula does not use p). [G1 compares loss counts for a = 3, 5 with primes 5, 7]"
- **H4, INFO, §7.6.5 G4.** State the reason, for v ≠ v′.
  - *Correction:* "it is a unit times (ζ_d − 1)/n_j with d | n_j, d > 1. Its norm from ℚ(ζ_d) is ±Φ_d(1)/n_j^{φ(d)}, where Φ_d(1) ∈ {1, p} and p ≤ d ≤ n_j. For n_j ≥ 3 this is not an integer: |norm| < 1 if φ(d) ≥ 2, and it is 2/n_j with n_j ≥ 4 if d = 2."
- **H5, INFO, corrigendum G8.** Sufficiency for n ≥ 3 is by proof, not asserted.
  - *Correction:* "n = 2 never: asserted (G8). Sufficiency for n ≥ 3 by proof: k − k′ ≡ c ≢ 0 (mod n) is solved by (c+1, 1) if c ≤ n−2, and by (1, 2) if c = n−1."
- **H6, INFO, status line.** The table cells, the resonant-pair list beyond 180, and the 216/7776 rank values remain printed only.
  - *Correction:* "asserts every claim the independent check listed as printed-only (G12); the table and resonant-pair list remain printed output."
- **H7, INFO, script header.** Disclose that the docstring and header label were updated.
- **Out of scope:** the Files list names CHECK_OUTPUT.txt twice.

## Script-checked versus read only

**Script-checked.** The verifier's `delta_independent.py` (b8d8d480…; output 709ec742…, 0 failures) covered:
- the full 26-atom table and both kernel ranks;
- the G1 family for n = 4…14;
- the m = 2 sweep to a, b ≤ 14;
- prime-independence of the positions;
- the −ζ₃ identity and 55 ~ 14;
- the 24/0/24 reach (40 not reached), and the checker's 60 pairs (60 of 84);
- the 7776 classes and δ;
- 900: 9;
- the G4 fixed seat on 4 atoms and the norm lemma (n < 60);
- the G5 vector, G8 sufficiency (n < 30) and the G7 count.

**Read or proved by hand only:** the G1 algebra, −ζ₃ = (1/3)(ζ₃−1)², the G7 monotonicity, the G5 down-set argument, and the match between the note text and the diff.

## Verifier's files in this folder

- delta_independent.py b8d8d480…
- DELTA_INDEPENDENT_OUTPUT.txt 709ec742…
- RERUN_FILE2_OUTPUT.txt c7d61ddb…
