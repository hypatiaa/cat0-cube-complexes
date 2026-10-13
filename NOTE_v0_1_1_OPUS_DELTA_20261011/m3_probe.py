import io, contextlib
SRC = open(r"C:\Users\robin\s6_atom\cat0_cube_complexes\NOTE_divisor_atom_cube_complex_v0_1_1_20261011\check_v0_1_1.py", encoding="utf-8").read()
SRC = SRC.replace("CASES = [1, 12, 30, 36, 60, 360, 900, 6300, 30030]", "CASES = [1, 12]").replace("for N in [12, 30, 360, 900]:", "for N in [12, 30, 36]:").replace("for N in [12, 30, 360]:", "for N in [12]:")
muts = {
 "M3' pdivmod skips constant term": ("            a[s + i] -= c * x", "            a[s + i] -= c * x if i else 0"),
 "M3'' ramanujan_exact accepts non-constant (returns r[0])": ("return r[0] if all(x == 0 for x in r[1:]) else None", "return r[0]"),
}
for name, (o, n) in muts.items():
    assert SRC.count(o) == 1, name
    g = {"__name__": "x"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(SRC.replace(o, n), g)
        print(name, "fail-prefixes:", sorted({f.split()[0] for f in g["failures"]}))
    except AssertionError as e:
        print(name, "caught by AssertionError")
