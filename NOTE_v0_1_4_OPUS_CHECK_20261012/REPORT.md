# Independent check of NOTE v0.1.4 additions (O5 Leary pin, O2 record, O1 §7)

**Provenance.** This file was written by the owner session from the verifier's returned text, because subagent report writes are refused. The verifier was an independent Opus subagent at high thinking level, on a closed list of 7 files. Its findings are reproduced unchanged.

## VERDICT: PASS_WITH_FLAGS

- The Leary pin is correct: B.8, A.6, A.7 and B.11 say what the note says, and X(ℕ) meets B.8's hypotheses.
- All §7 mathematics reproduces exactly.
- O1's new "correction to the record" contains a false count (E1), which must be fixed. The other flags are wording, hypotheses and citations.

## Integrity

- NOTE.md 72e2c53e…, check_v0_1_4_drawing.py 20d0511e… and CHECK_DRAWING_OUTPUT.txt 1e77b9df… match MANIFEST 9013af6b….
- PDF 191d26ad…; viewer 3d65e14af4b0887b543e48d986ccc6367b0129afc150e0f9a254bd407b3ab106.
- leary_text.txt (dbf209d9…) was not pinned. The verifier re-extracted the PDF with pdftotext and it agrees.

## Findings

- **E1, MEDIUM, §6 O1.** "7 of those losses are off the spine" is FALSE. The loss is 5 on the spine (Ω=2: 2, Ω=3: 1, Ω=4: 2) and 6 off it, and 7 is the loss at Ω=3.
  - *Correction:* "11 is the total number of points lost to coincidence: 5 on the spine and 6 off it (the six Ω=3 pairs). 7 of the 11 losses occur at Ω=3."
- **E2, LOW, §7.2.** For m = 1, K_1 = 0, not ℤ·(1).
  - *Correction:* "For m = 1, K_1 = 0. For m prime, K_m = ℤ·(1,…,1), the multiples of Φ_m. …"
- **E3, LOW, §7.4.** The antipode reflection and the Walsh identity need m ≥ 2, and both fail at m = 1.
  - *Correction:* insert "For m ≥ 2,".
- **E4, LOW, §7.3.** "unions of cosets" should be "disjoint unions of cosets". {0,3} ∪ {0,2,4} is not zero-sum.
- **E5, LOW/MEDIUM, §7.4 and O2.** "sees only … frequency 1" over-claims, because the height carries frequency 0.
  - *Correction:* "for m ≥ 2, the drawing of a squarefree atom sees only the Walsh spectrum of degree ≤ 1. Of that it sees only the seat-circle frequencies 0 (height, z = (m − Σ_i W_i)/2) and 1 (plane, 2π_xy = Σ_i ζ_m^i W_i). Coincidences are exactly the pairs these two coefficients cannot separate." In O2: "lives entirely in the Walsh characters of degree ≤ 1".
- **E6, LOW, §7.5.** The claim about r_i and n_i is per prime.
  - *Correction:* "In a non-squarefree atom at least one prime has a_i ≥ 2, hence n_i ≥ 3 and r_i ≤ 1/3. Primes with a_i = 1 keep n_i = 2 and r_i = 1/2. The map is then no longer linear in the exponents."
- **E7, LOW, §7 Source.** The line numbers are wrong: the formula comment is at 1417–1428, the reversal modes at 1430–1444, and divisorPosition at 1445–1465. "Primes ascending" needs a cited line or must be marked unverified. Index i = 0…m−1, and i is also used as the imaginary unit.
- **E8, LOW, §5.1 simple connectivity.** The argument runs in the CW topology first, and A.7 then transfers it to the metric topology.
- **E9, LOW, §5.1 flag.** "A set" should be "A finite set". The spanning cube is (n/∏T, S).
- **E10, INFO.** For squarefree N the 'winding' mode gives the same drawing, and 'global' gives the conjugate, so §7.1–§7.4 hold in all three modes. O6 should name a mode.
- **E11, INFO.** B.8 needs neither completeness nor local finiteness; its proof goes through finite convex subcomplexes (B.4). B.11 gives a non-empty, contractible fixed set. The definition of a cubical complex is from Bridson–Haefliger I.7.40(3), not verified. The journal reference J. Topology 6 (2013) 251–284 is unchecked.
- **E12, INFO.**
  - Date: O2 is dated 2026-10-12 while the system date is 2026-10-11.
  - "Centre duads" should be "the three spine duads 14, 33, 65". k = 2 does not separate the triangles; k = 3 does.
  - The rank m − φ(m) needs a reason: ℤ^m → ℤ[ζ_m] is onto, and ℤ[ζ_m] is free of rank φ(m).
  - The O2 quote and the "eight copies" claim cannot be checked from the closed list.

## Audit of check_v0_1_4_drawing.py

- **Correct as cited:** V0, D1, D3/D4 (m ≥ 2), S1–S6.
- **D2 is nearly tautological.**
- **Not checked:** the rank m − φ(m), the six off-spine pairs (printed, never asserted), the coset characterisation, and the O1 sentence. That last gap is where E1 got in.

## Script-checked versus read only

**Script-checked.** The verifier's `opus_check_s7.py` (8a0ba85c…), with output in `opus_check_s7_output.txt` (aa982b52…), had 0 failures. It used two exact routes, Φ_m from the Möbius product and ℤ[ω]. It covered:
- K_m rank for m = 1…12;
- "coincidences iff composite" for m = 1…12;
- the counts for m = 4, 6, 8, 9, 10, 11, 12;
- the antipode and Walsh identities, both failing at m = 1;
- all the 30030 claims, including the 5/6/7 loss split and the disjoint-coset characterisation;
- k = 2 separating the duads;
- the reversal modes (numerically).

**Read only:** Leary's theorem texts and proofs; viewer lines 1395–1470; the cubical, simple-connectivity and flag arguments; the journal reference, the O2 quote and the "eight copies" claim.
