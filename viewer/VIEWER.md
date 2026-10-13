# Atom viewer: frozen base

`helix_atlas_doily_witness_v27_patched_3_wl2.html`
sha256 `3d65e14af4b0887b543e48d986ccc6367b0129afc150e0f9a254bd407b3ab106` (7527 lines; v27-fix.1b)

This is the pinned viewer that §7 of the note transcribes and checks against:
- `factorize`: lines 1261–1271, primes in ascending order;
- `divisorPosition`: lines 1445–1465, reversal modes at 1430–1444.

It is a single self-contained HTML page. Open it in a browser.

**Rule for extending.** This file stays byte-identical as the frozen reference. Extensions go in new, versioned files next to it, with their own hashes. Any change in drawing behaviour is checked against the exact statements of §7, for example the 30030 spine and the 216 and 900900 coincidences.

The first planned extension, per O4, is labelling the coincident vertices this drawing already produces, using the note's rule. It waits on the viewer-redesign requirements being adopted, and on saphir's word "build".

An older build, 91a33a49…, dated 2026-09-04, differs only in the Ford-ring radius fix and some comments. Its drawing functions are byte-identical. It is not used here.
