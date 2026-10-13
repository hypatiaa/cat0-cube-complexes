# Delta check of NOTE v0.1.1 against findings F1–F11

**Provenance.** This file was written by the owner session from the delta verifier's returned text. The verifier was an independent Opus subagent at high thinking level, working on a closed file list of six files. The text below is the verifier's report with its findings unchanged.

## VERDICT: PASS_WITH_FLAGS

- All 11 findings are resolved, and there is no new mathematical or coding error.
- There are 5 new flags. D1–D4 are LOW and D5 is INFO; they are about wording, scope labels and unmarked changes.

## Integrity

All digests match:
- NOTE.md 57fb7ec5…
- check_v0_1_1.py 36b7ea82…
- CHECK_OUTPUT.txt 51dc2753…
- MANIFEST.sha256 aeb3bf60…31aa
- REPORT.md (v0.1 check) d1ce9054…232d
- v0.1 NOTE.md ef9397aa…79d1

## Per-finding table

| Finding | Disposition | Reason (summary) |
|---|---|---|
| F1 MAJOR §5.1 | RESOLVED | Struck, and the reviewer's text adopted verbatim. The examples are correct (checked in X(302400)), and so is the Sageev statement. Residues are D1 and D2. |
| F2 MEDIUM §3.2 | RESOLVED | Verbatim. C7b tests the classification on N ∈ {1, 12, 30, 36, 60} (D4). The X(6) caveat is true (script-checked). The equivalence with the metric sense rests on proof. |
| F3 MEDIUM registers | RESOLVED | Verbatim. The C7b scope label is in D4. |
| F4 LOW §3.3 | RESOLVED | The map H⁺(p,k) → H⁻(p,a_p−k+1), and the corresponding dual-edge map, are script-checked over 8 values of N. 0 bad. |
| F5 LOW §5.1 | RESOLVED | Verbatim; true by §5.3. |
| F6 LOW §5.4 | RESOLVED | The "if and only if" is correct. R2 and R3 run on all 7 pairs, including (360, 30030) with τ = 192. Wording is in D5. |
| F7 LOW §3.4 | RESOLVED | The hypothesis is stated. C9 is tested against the cube list. The inversion check catches 3 mutations. |
| F8 LOW §5.2 | RESOLVED | j ↦ j·N/M is script-checked on 4 pairs: injective, keeps order, keeps character values exactly, and has the right image. |
| F9 LOW §2.3 | RESOLVED | The argument is valid in general. C4b checks the bijection directly (214 executions), and a mutation is caught. |
| F10 LOW R5, §3.1 | RESOLVED | R5 convolves enumerated f-vectors; a perturbation is caught. The forward reference is present. |
| F11 INFO C12 | RESOLVED | Exact in ℤ[x]/(Φ_d), with 33,252 executions. It agrees with von Sterneck's formula on 3,991 cases. |

## New and changed code

- **pdivmod:** correct for monic divisors; a mutation is caught. A first, ineffective mutation is disclosed in the verifier's report.
- **cyclotomic:** verified for d = 1…210 (degree φ(d), monic, ∏_{e|d} Φ_e = x^d − 1, a root at ζ_d, and the −2 coefficient in Φ_105).
- **ramanujan_exact_from_roots:** a genuine exact test. Its "is it constant" guard is never exercised by the data, which is expected.
- **C7b:** the chain through C7 holds, and 2 mutations are caught.
- **R2/R3:** 2 mutations are caught.

## New findings

- **D1, LOW, §5.1.** Two sentences disagree about metric CAT(0).
  - *Correction:* keep the reviewer's sentence and append "(not yet cited; see O5)". Alternatively, change the bullet to "This combinatorial structure is all the construction uses; the metric CAT(0) sentence above is stated subject to O5."
- **D2, LOW, §1.1.** "Those carry over to the whole family (§4)" points to the wrong section, and it overclaims after F1.
  - *Correction:* "Those carry over to the whole family (§5.1), with the exceptions listed there."
- **D3, LOW, header and corrigendum.** These changes have no marker: (a) the §5.1 "locally infinite" sentence; (b) the R4 bullet in §5.6; (c) the C7 bullet split in §3.2; (d) "unreviewed" dropped from the status line.
  - *Correction:* mark (a)–(c), and add a corrigendum row for the script-audit notes.
- **D4, LOW, registers and §3.2.** The C7b scope reads as all N with τ(N) ≤ 12.
  - *Correction:* "[C7b: every vertex subset, for the test cases with τ(N) ≤ 12: N = 1, 12, 30, 36, 60]", here and in the registers line.
- **D5, INFO, §5.4 and corrigendum F6.** "The gate is lifted" is inaccurate; the gate was raised.
  - *Correction:* "the gate is raised to τ(lcm) ≤ 256, so all seven pairs, including (360, 30030), are tested".

## Script-checked versus read only

**Script-checked:**
- Re-run of check_v0_1_1.py: exit 0, output byte-identical (51dc2753…).
- An instrumented run with counts per label.
- 13 mutations.
- Independent checks of the cyclotomic polynomials, C12 against von Sterneck, the X(6) caveat, the §3.3 map, F9, F8, and finite proxies for §5.1.

**Read only:**
- The equivalence with the metric sense in §3.2.
- The Sageev statement for X(ℕ).
- The "if and only if" proof in §5.4.
- The Leary 2013 attribution (not pinned).
- Coefficient stability in §5.6.

## Verifier's files in this folder

- delta_probe.py (014947f7…)
- m3_probe.py (1967c845…)
- PROBE_OUTPUT.txt (2b644077…)
- rerun_output.txt (51dc2753…)
- probe_stderr.txt
