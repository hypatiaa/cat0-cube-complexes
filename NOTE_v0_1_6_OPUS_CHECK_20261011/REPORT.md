# Independent check of NOTE v0.1.6 (O6 §7.6 and Astra #263 F1–F3)

**Provenance.** This file was written by the owner session from the verifier's returned text. The verifier was an independent Opus subagent at high thinking level, on a closed list of 5 files. Its findings are reproduced unchanged.

**Owner's confirmation.** The owner session independently confirmed the two headline counterexamples with the note's own exact map: in 216, 8 ≡ 12 and 18 ≡ 27; in 900900, 55 ≡ 14.

## VERDICT: FAIL (two counts)

1. The m = 2 injectivity "observation" in §7.6.6 and O7 is false: 216 = 2³·3³ is drawn non-injectively.
2. §7.6.5–§7.6.7 imply that every coincidence is a resonance pair or a zero-sum block. 900900 has a third kind; the note's own smallest group for it, [55, 14], is one.

Everything else in scope checks out: the telescoping identity, linearity and the viewer match, the coincidence criterion, m = 1, the resonance characterisation, and every number in the table. No fact the note asserts as proved is wrong.

## Integrity

- Every hash matches: NOTE 3f5510fc…, check 1ec85d2f…, output 21e40d4b…, MANIFEST bd7ad3ca…, viewer 3d65e14a….
- Re-running file 2 gives output byte-identical to CHECK_O6_OUTPUT.txt.

## Findings

- **G1, HIGH, §7.6.6 and O7.** m = 2 is not always injective.
  - In 216, 8 ≡ 12 and 18 ≡ 27. For a = b = n − 1 with n even, n ≥ 4, w_{0,1+n/2} = −(1/n)(ζ_n − 1) = w_{1,1}.
  - **Proved family:** p^a q^a is non-injective for every odd a ≥ 3.
  - *Correction:* "m = 2 is not always injective: in 2³·3³ the divisors 8 and 12 (resonance H(2,3) = H(3,1)) and 18 and 27 (H(2,1) = H(3,3)) coincide. More generally p^a q^a with a odd, a ≥ 3, is non-injective. With a ≠ b, or a = b even, no coincidence was found for a, b ≤ 14 (observation)."
  - *Correction to O7:* "a complete classification for all atoms, and which m = 2 exponent pairs (a, b) are injective".
- **G2, MEDIUM–HIGH, §7.6.5.** Mechanisms (i) and (ii) do not generate 900900.
  - w_{H(5,1)} − w_{H(2,1)} = −ζ₃ = w_{H(7,1)} − w_{H(11,1)}, so 55 ≡ 14.
  - Of the 64 losses, 24 come from single resonance swaps; 0 come from squarefree blocks; 60 coincident pairs lie outside the ℚ-span of the resonance vectors plus the squarefree height-zero kernel.
  - *Correction:* add "(iii) Mixed relations (observed in 900900): differences of non-squarefree edge vectors can be algebraic integers equal to differences of squarefree edges, e.g. w_{H(5,1)} − w_{H(2,1)} = −ζ₃ = w_{H(7,1)} − w_{H(11,1)}, so 55 and 14 coincide. 40 of 900900's 64 losses are not reached by resonance swaps or squarefree block swaps."
  - *Correction:* "is not claimed" → "is false (900900). A classification is open (O7)."
- **G3, MEDIUM, §7.6.7.** The labelling rule over-claims; it fails for 900900, and for 2⁵·3⁵ through two-edge segment swaps.
  - *Correction:* "…compute the hyperplane-coordinate difference δ and report it exactly. Name it a resonance swap or a squarefree zero-sum block swap when it is one; otherwise label it 'other kernel relation' and show δ."
- **G4, MEDIUM, §7.6.5 third bullet.** The length argument does not prove the claim. The conclusion holds for 60060 and 120120 (script-checked).
  - *Correction:* "…because each chain difference of the non-squarefree seat, (1/n_j)ζ_m^j(ζ_{n_j}^v − ζ_{n_j}^{v′}), is not an algebraic integer, while every squarefree combination lies in ℤ[ζ_L]. So with only one non-squarefree seat, that seat cannot take part in a coincidence. (With two or more, it can: 900900.)"
- **G5, LOW, §7.6.2.** The 8 = 2³ example shows the height condition, not the down-set condition.
  - *Correction:* use 36 = 2²·3², with kernel vector (1, −1, 1, −1). An optional rank ker(w, z) column: 0,0,0 | 0,0,1,1,0,1,1,1 | 1 | 2 | 2 | 3 | 1,1,2 | 0,0 | 3 | 4 | 4 | 6.
- **G6, LOW, notation.** Write w_{0,2} = w_{1,1} (H(2,2), H(3,1)) and w_{0,1} + w_{0,3} = 0.
- **G7, LOW, §7.6.4 parenthesis.** Lengths must agree, not values.
  - *Correction:* "(Equal vectors have equal length, and |w_{j,k}| = (2/n_j) sin(π/n_j) is strictly decreasing in n_j ≥ 2, since 2t·sin(πt) increases on (0, 1/2]; so n_j = n_{j′}.)"
- **G8, LOW, §7.6.4.** The anchor-gap condition is necessary but not sufficient.
  - *Correction:* "Necessarily the anchor gap … is a multiple of 1/n mod 1. For n ≥ 3 this is also sufficient for some k, k′ ∈ {1, …, n − 1}. For n = 2 resonance never occurs."
- **G9, INFO, §7.6.3.** Add "(Already the heights e are distinct.)"
- **G10, INFO, F3.** Only `divisorPosition` returning (0, 0, 0) is verified; whether the UI accepts N = 1 was not checked.
- **G11, INFO, F1.** Say "float transcriptions of the viewer's code".
- **G12, INFO, file 2 audit.**
  - L1, L2, L3, T1, T3, T4 and V1 test what they are cited for.
  - T2 is partial.
  - Printed but not asserted: the kernel ranks, the general resonance characterisation, w_1 + w_3 = 0, the 33/65 duads, the antipodal breaking, and the two-mechanism claim (which is false).
  - Lines 274–276 are stale comments, and `q, r = [], num` is dead code.

## O7 probe (verifier)

- **m = 2, p < q ≤ 13, a, b ≤ 5 (375 atoms):** 30 are non-injective, exactly the pairs (3,3) and (5,5).
- **Extended to a, b ≤ 14:** non-injective exactly at (a, a) for a = 3, 5, 7, 9, 11, 13, losing 2, 6, 12, 20, 30 and 42 points. None was found with a ≠ b or a even.
- **Proved:** a = b odd ≥ 3 is non-injective. **Observed only:** the rest.

## Confirmed correct

- §7.6.1, linearity and the viewer match, on all 24 atoms.
- §7.6.2, the criterion, on all pairs.
- §7.6.3 for a ≤ 30.
- §7.6.4, resonance, on 24 + 129 atoms. The 180 pairs are {4, 6} and {20, 30}.
- The table: every column matches.
- F2 (global mode).
- The §7.5 edits.
- The corrigendum rows, except that the O6 row inherits G1–G3.

## Verifier's files (this folder)

| File | sha256 (prefix) |
|---|---|
| verify_o6.py | e4e4f5ec… |
| VERIFY_O6_OUTPUT.txt | 91cea564… |
| followup.py | 4f2cca03… |
| FOLLOWUP_OUTPUT.txt | a77c5b22… |
| check_global_n1.py | c14d48e9… |
| CHECK_GLOBAL_N1_OUTPUT.txt | d79ee9d6… |
| RERUN_FILE2_OUTPUT.txt | 21e40d4b… |
